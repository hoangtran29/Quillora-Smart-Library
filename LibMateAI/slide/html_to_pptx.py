"""Convert slide/01.html..10.html to Quillora_Slides.pptx.

Strategy for best visual quality + most preserved components:
  1. Render each HTML with headless Chrome (Selenium) at 2x => pixel-perfect PNG.
  2. Place the PNG as a full-slide picture (pristine background).
  3. Extract every [data-object-type="textbox"] element with bounding box
     AND computed style, then place a matching text box on top of the image
     so every text block stays as an editable PPTX component at the correct
     position (invisible 1pt white text — the picture carries the visuals).
  4. Also dump full text into speaker notes.
"""
import base64
import glob
import io
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn


SLIDE_W_PX = 1280
SLIDE_H_PX = 720
DEVICE_SCALE = 2  # retina screenshot

PPT_W_IN = 13.333
PPT_H_IN = 7.5
EMU_PER_IN = 914400

slide_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(slide_dir, "Quillora_Slides.pptx")
slide_files = sorted(glob.glob(os.path.join(slide_dir, "[0-9][0-9].html")))
print(f"Found {len(slide_files)} slide(s)")


def px_to_emu_x(px: float) -> int:
    return int(px / SLIDE_W_PX * PPT_W_IN * EMU_PER_IN)


def px_to_emu_y(px: float) -> int:
    return int(px / SLIDE_H_PX * PPT_H_IN * EMU_PER_IN)


def css_align_to_pp(align: str):
    m = {
        "center": PP_ALIGN.CENTER,
        "right": PP_ALIGN.RIGHT,
        "justify": PP_ALIGN.JUSTIFY,
        "left": PP_ALIGN.LEFT,
        "start": PP_ALIGN.LEFT,
        "end": PP_ALIGN.RIGHT,
    }
    return m.get((align or "").lower(), PP_ALIGN.LEFT)


def disable_autosize(text_frame):
    bodyPr = text_frame._txBody.find(qn("a:bodyPr"))
    if bodyPr is None:
        return
    for tag in ("a:normAutofit", "a:spAutoFit"):
        existing = bodyPr.find(qn(tag))
        if existing is not None:
            bodyPr.remove(existing)


EXTRACT_JS = r"""
// Find every "text leaf" element — an element whose children are all inline
// (span/i/b/strong/em/u/br/a/small/mark/sub/sup), so its text is one visual block.
const INLINE = new Set(['SPAN','I','B','STRONG','EM','U','BR','A','SMALL','MARK','SUB','SUP','CODE','TIME','LABEL']);
const SKIP   = new Set(['SCRIPT','STYLE','NOSCRIPT','META','LINK']);
const out = [];

function isVisible(el, cs) {
  if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return false;
  const r = el.getBoundingClientRect();
  if (r.width < 2 || r.height < 2) return false;
  return true;
}

function walk(el) {
  if (!el || el.nodeType !== 1) return;
  if (SKIP.has(el.tagName)) return;

  const cs = window.getComputedStyle(el);
  if (!isVisible(el, cs)) return;

  const childEls = Array.from(el.children);
  const hasBlockChild = childEls.some(c => !INLINE.has(c.tagName));

  if (!hasBlockChild) {
    const text = (el.innerText || '').replace(/\u00A0/g, ' ').replace(/[ \t]+\n/g, '\n').trim();
    if (text) {
      const r = el.getBoundingClientRect();
      out.push({
        text,
        x: r.x, y: r.y, w: r.width, h: r.height,
        fontSize: parseFloat(cs.fontSize) || 18,
        fontWeight: cs.fontWeight || '400',
        fontFamily: cs.fontFamily || 'Inter',
        color: cs.color || 'rgb(26,26,26)',
        textAlign: cs.textAlign || 'left'
      });
    }
    return;
  }
  for (const c of childEls) walk(c);
}

walk(document.querySelector('.slide-container') || document.body);
return out;
"""


prs = Presentation()
prs.slide_width = Inches(PPT_W_IN)
prs.slide_height = Inches(PPT_H_IN)
blank_layout = prs.slide_layouts[6]


opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")
opts.add_argument("--hide-scrollbars")
opts.add_argument(f"--window-size={SLIDE_W_PX},{SLIDE_H_PX}")
opts.add_argument(f"--force-device-scale-factor={DEVICE_SCALE}")

driver = webdriver.Chrome(options=opts)
driver.set_window_size(SLIDE_W_PX, SLIDE_H_PX)

try:
    for idx, html_file in enumerate(slide_files, 1):
        url = "file:///" + html_file.replace("\\", "/")
        print(f"[{idx}/{len(slide_files)}] {os.path.basename(html_file)}")
        driver.get(url)
        time.sleep(2)  # wait for Font Awesome + Google Fonts

        # Remove scrollbars / overflow just in case
        driver.execute_script(
            "document.body.style.overflow='hidden';"
            "document.documentElement.style.overflow='hidden';"
        )

        # Take a screenshot of the .slide-container at 2x scale using CDP clip
        # Use Page.captureScreenshot with clip for the container rect at deviceScaleFactor
        rect = driver.execute_script(
            "const r=document.querySelector('.slide-container').getBoundingClientRect();"
            "return {x:r.x, y:r.y, w:r.width, h:r.height};"
        )
        shot = driver.execute_cdp_cmd(
            "Page.captureScreenshot",
            {
                "format": "png",
                "captureBeyondViewport": True,
                "clip": {
                    "x": rect["x"],
                    "y": rect["y"],
                    "width": rect["w"],
                    "height": rect["h"],
                    "scale": DEVICE_SCALE,
                },
                "fromSurface": True,
            },
        )
        img_bytes = base64.b64decode(shot["data"])

        # Extract text boxes via JS
        text_boxes = driver.execute_script(EXTRACT_JS)

        slide = prs.slides.add_slide(blank_layout)

        slide.shapes.add_picture(
            io.BytesIO(img_bytes),
            0, 0,
            width=Inches(PPT_W_IN),
            height=Inches(PPT_H_IN),
        )

        for tb in text_boxes:
            x = px_to_emu_x(tb["x"])
            y = px_to_emu_y(tb["y"])
            cx = max(px_to_emu_x(tb["w"]), Emu(Pt(1)))
            cy = max(px_to_emu_y(tb["h"]), Emu(Pt(1)))

            shape = slide.shapes.add_textbox(x, y, cx, cy)
            shape.fill.background()  # transparent fill

            tf = shape.text_frame
            tf.word_wrap = True
            tf.margin_left = 0
            tf.margin_right = 0
            tf.margin_top = 0
            tf.margin_bottom = 0
            disable_autosize(tf)

            try:
                weight = int(tb.get("fontWeight") or 400)
            except (TypeError, ValueError):
                weight = 400

            for i, line in enumerate(tb["text"].split("\n")):
                para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                para.alignment = css_align_to_pp(tb.get("textAlign"))
                run = para.add_run()
                run.text = line
                run.font.size = Pt(1)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                run.font.bold = weight >= 600
                run.font.name = "Inter"

        notes_tf = slide.notes_slide.notes_text_frame
        notes_tf.text = "\n\n".join(tb["text"] for tb in text_boxes)

        print(f"    -> {len(text_boxes)} text component(s) preserved")

finally:
    driver.quit()

prs.save(out_path)
size_kb = os.path.getsize(out_path) / 1024
print(f"\nSaved: {out_path} ({size_kb:.1f} KB)")
