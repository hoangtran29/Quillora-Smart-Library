"""Build Quillora Demo DOCX — full-width screenshots, stacked vertically."""
import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

SLIDE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SLIDE_DIR, "screenshots")
OUT = os.path.join(SLIDE_DIR, "Quillora_Demo.docx")

RED = RGBColor(190, 17, 40)
BLACK = RGBColor(30, 30, 30)
GRAY = RGBColor(110, 110, 110)
WHITE = RGBColor(255, 255, 255)

IMG_W = Inches(6.2)  # full content width


def add_red_bar(doc):
    """Thin red bar as a table row."""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.cell(0, 0)
    cell.text = ""
    shading = cell._element.get_or_add_tcPr()
    bg = shading.makeelement(qn('w:shd'), {
        qn('w:fill'): 'BE1128', qn('w:val'): 'clear'
    })
    shading.append(bg)
    # Make row tiny
    row = t.rows[0]
    row.height = Cm(0.15)


def add_badge(doc, text):
    p = doc.add_paragraph()
    p.space_before = Pt(6)
    p.space_after = Pt(2)
    run = p.add_run(f"  {text}  ")
    run.font.size = Pt(8)
    run.font.bold = True
    run.font.color.rgb = RED
    # Highlight background
    run.font.highlight_color = 6  # Yellow-ish (closest to pink available)


def add_heading(doc, text):
    p = doc.add_paragraph()
    p.space_before = Pt(4)
    p.space_after = Pt(4)
    run = p.add_run(text)
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = BLACK


def add_intro(doc, text):
    p = doc.add_paragraph()
    p.space_before = Pt(0)
    p.space_after = Pt(6)
    run = p.add_run(text)
    run.font.size = Pt(9.5)
    run.font.color.rgb = GRAY


def add_label(doc, text):
    p = doc.add_paragraph()
    p.space_before = Pt(8)
    p.space_after = Pt(2)
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.color.rgb = RED


def add_screenshot(doc, filename):
    path = os.path.join(IMG_DIR, filename)
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.space_before = Pt(2)
        p.space_after = Pt(4)
        run = p.add_run()
        run.add_picture(path, width=IMG_W)
    else:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f"[ {filename} ]")
        run.font.size = Pt(9)
        run.font.italic = True
        run.font.color.rgb = GRAY


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.space_before = Pt(1)
        p.space_after = Pt(1)
        run = p.add_run(item)
        run.font.size = Pt(9)
        run.font.color.rgb = BLACK


def add_note(doc, text):
    """Italic note paragraph."""
    p = doc.add_paragraph()
    p.space_before = Pt(4)
    p.space_after = Pt(4)
    run = p.add_run(text)
    run.font.size = Pt(8.5)
    run.font.italic = True
    run.font.color.rgb = GRAY


def add_page_break(doc):
    doc.add_page_break()


def build():
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = Cm(1.5)
        section.bottom_margin = Cm(1.5)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)

    # ══════ 1. BIA ══════
    add_red_bar(doc)

    p = doc.add_paragraph()
    p.space_before = Pt(20)
    run = p.add_run("NGAY HOI DOC SACH PTIT 2026")
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.color.rgb = RED

    p = doc.add_paragraph()
    run = p.add_run("Hoc vien Cong nghe Buu chinh Vien thong")
    run.font.size = Pt(10)
    run.font.color.rgb = GRAY

    p = doc.add_paragraph()
    p.space_before = Pt(20)
    run = p.add_run("Quillora")
    run.font.size = Pt(36)
    run.font.bold = True
    run.font.color.rgb = BLACK
    run2 = p.add_run(".")
    run2.font.size = Pt(36)
    run2.font.bold = True
    run2.font.color.rgb = RED

    p = doc.add_paragraph()
    run = p.add_run("Nen tang doc sach thong minh ung dung AI cho sinh vien PTIT")
    run.font.size = Pt(14)
    run.font.color.rgb = BLACK

    p = doc.add_paragraph()
    p.space_after = Pt(10)
    run = p.add_run('"Tu ngoi but den binh minh tri thuc"')
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = RED

    add_label(doc, "Anh chup trang chu Quillora")
    add_screenshot(doc, "trangchu.png")
    add_note(doc, "Giao dien trang chu voi hero section, ke sach giao trinh PTIT, nut CTA vao thu vien. Responsive, ho tro dark mode.")

    # ══════ 2. THU VIEN ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "THU VIEN SACH")
    add_heading(doc, "Ke sach giao trinh PTIT")
    add_intro(doc, "Hien thi tat ca giao trinh duoi dang grid card. Moi card co: bia sach (Google Books), tom tat AI, danh muc, muc do kho, nut yeu thich. Click vao bat ky sach nao de mo reader.")
    add_label(doc, "Giao dien thu vien")
    add_screenshot(doc, "thuvien.png")
    add_bullets(doc, [
        "10 giao trinh PTIT san co: Mang may tinh, He dieu hanh, CTDL, Java, CNPM, Do hoa, ATTT, Kho DL, Toan roi rac, AI.",
        "Bia sach that tu Google Books API.",
        "Tom tat AI tu dong cho moi cuon sach khi upload.",
        "Danh dau yeu thich - luu vao trang ca nhan.",
        "Upload them PDF moi: keo tha -> trich xuat -> embedding -> san sang chat trong vai giay.",
    ])

    # ══════ 3. DANG NHAP ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "XAC THUC")
    add_heading(doc, "Dang nhap & Dang ky")
    add_intro(doc, "Hai phuong thuc: email/password hoac Microsoft OAuth qua Auth0. Sinh vien PTIT dang nhap 1-click bang email @stu.ptit.edu.vn.")
    add_label(doc, "Modal dang nhap")
    add_screenshot(doc, "dangnhap.png")
    add_label(doc, "Modal dang ky")
    add_screenshot(doc, "dangki.png")

    # ══════ 4. DOC SACH ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "DOC SACH PDF")
    add_heading(doc, "PDF Reader tren trinh duyet")
    add_intro(doc, "Doc giao trinh truc tiep tren web voi PDF.js - zoom, cuon trang, lazy loading. Khong can tai ve hay cai phan mem.")
    add_label(doc, "Giao dien doc sach")
    add_screenshot(doc, "docsach.png")
    add_bullets(doc, [
        "PDF.js (Mozilla): render PDF client-side, lazy load tung trang khi scroll.",
        "Zoom: 43% -> 214%. Download PDF goc voi ten file tieng Viet co dau.",
        "Tab navigation: Doc sach / Hoi dap / Tom tat / Quiz / Flashcard / Minh hoa / Nghe sach.",
    ])

    # ══════ 5. HOI DAP ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "HOI DAP AI")
    add_heading(doc, "Chat truc tiep voi sach")
    add_intro(doc, 'Dat cau hoi bang tieng Viet tu nhien. Quillora tim dung doan lien quan trong sach (RAG), sinh cau tra loi kem trich dan [Chuong - tr.X]. Ho tro lich su hoi thoai lien mach.')
    add_label(doc, "Cau hoi dau tien")
    add_screenshot(doc, "hoidap.png")
    add_label(doc, "Hoi tiep (chat history)")
    add_screenshot(doc, "hoidap2.png")

    # ══════ 6. HOI DAP (tiep) + TOM TAT ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "HOI DAP & TOM TAT")
    add_heading(doc, "Format Markdown & Tom tat sach")
    add_label(doc, "Cau tra loi format dep (bold, list, trich dan)")
    add_screenshot(doc, "hoidap3.png")
    add_label(doc, "Tom tat noi dung sach bang AI (~200 tu)")
    add_screenshot(doc, "tomtat.png")
    add_note(doc, "RAG truy hoi cac doan quan trong nhat, Gemini 2.5 Flash sinh tom tat ngan gon, de hieu.")

    # ══════ 7. QUIZ ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "QUIZ TU DONG")
    add_heading(doc, "On tap bang trac nghiem AI")
    add_intro(doc, "Sinh 3-20 cau hoi trac nghiem theo chu de tuy chon tu noi dung sach goc. Cham diem tuc thi, giai thich dap an chi tiet. Lam quiz giup nho gap 5x so voi doc lai (Roediger, 2006).")
    add_label(doc, "Tao quiz theo chu de")
    add_screenshot(doc, "sinhquiz.png")
    add_label(doc, "Ket qua cham diem")
    add_screenshot(doc, "sinhquiz2.png")

    # ══════ 8. FLASHCARD ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "FLASHCARD")
    add_heading(doc, "Flashcard on tap nhanh")
    add_intro(doc, "Tao 3-20 the thuat ngu - dinh nghia tu noi dung sach. Click lat the. On tap trong 24h dau tang 80% ghi nho (Murre & Dros, 2015).")
    add_label(doc, "Mat truoc (thuat ngu)")
    add_screenshot(doc, "flashcard.png")
    add_label(doc, "Mat sau (lat the)")
    add_screenshot(doc, "flashcard2.png")

    # ══════ 9. MINH HOA ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "MINH HOA DOAN VAN")
    add_heading(doc, "AI ve tranh tu doan van")
    add_intro(doc, "Chon doan van yeu thich -> AI chuyen thanh prompt tieng Anh -> Gemini Image Generation ve tranh phong cach watercolor / children's book illustration.")
    add_label(doc, "Nhap doan van & gen anh")
    add_screenshot(doc, "minhhoaanh.png")
    add_label(doc, "Ket qua minh hoa AI")
    add_screenshot(doc, "minhhoa2.png")

    # ══════ 10. TUONG TRANH ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "TUONG TRANH")
    add_heading(doc, "Gallery minh hoa ca nhan")
    add_intro(doc, "Moi user co tuong tranh rieng - luu lai tat ca anh AI da gen. Dang nhap khac -> tuong tranh khac.")
    add_label(doc, "Tuong tranh /wall")
    add_screenshot(doc, "tuongtranh.png")
    add_note(doc, "Ca nhan hoa: anh chi hien thi cho user da tao. Gan user_id tu JWT token vao moi visualization.")

    # ══════ 11. CHATBOT ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "CHATBOT THU VIEN")
    add_heading(doc, "Tro ly noi - hoi dap da sach")
    add_intro(doc, "FAB goc phai duoi, luon hien o moi trang. Tim kiem ngu nghia xuyen suot toan bo thu vien, trich dan tu nhieu sach.")
    add_label(doc, "Chatbot noi")
    add_screenshot(doc, "chatbot.png")
    add_bullets(doc, [
        "Cross-book RAG: hoi 1 cau -> tim trong TAT CA sach cung luc.",
        "Goi y cau hoi mau, lich su hoi thoai lien mach.",
        "Breathing glow animation thu hut nguoi dung.",
    ])

    # ══════ 12. UPLOAD + TRANG CA NHAN ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "UPLOAD & TRANG CA NHAN")
    add_heading(doc, "Tai tai lieu & Dashboard hoc tap")
    add_label(doc, "Upload PDF - san sang chat vai giay")
    add_screenshot(doc, "upload.png")
    add_label(doc, "Trang ca nhan - thong ke & lich su")
    add_screenshot(doc, "trangcanhan.png")

    # ══════ 13. GIOI THIEU ══════
    add_page_break(doc)
    add_red_bar(doc)
    add_badge(doc, "GIOI THIEU")
    add_heading(doc, "Trang About - 4 tinh nang noi bat")
    add_intro(doc, "Trang /about trinh bay 4 tinh nang cot loi voi mo ta cuon hut, so lieu khoa hoc.")
    add_label(doc, "Giao dien trang gioi thieu")
    add_screenshot(doc, "tranggioithieu.png")
    add_bullets(doc, [
        "Hoi la co, trich dan luon trang sach - RAG giam 94% cau tra loi sai.",
        "On thi 10 phut thay 10 tieng - Quiz nho gap 5x, Flashcard +80% ghi nho.",
        "Noi chuyen voi sach bang giong noi that - gia su ca nhan realtime.",
        "Doc den dau, ve tranh den do - hinh anh giup nho sau hon 65%.",
    ])

    doc.save(OUT)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    build()
