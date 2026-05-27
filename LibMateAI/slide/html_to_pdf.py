import os
import base64
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

slide_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(slide_dir, "Genspark.pdf")

slide_files = sorted(glob.glob(os.path.join(slide_dir, "[0-9][0-9].html")))
print(f"Found {len(slide_files)} slides:")
for f in slide_files:
    print(f"  {os.path.basename(f)}")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1280,720")

driver = webdriver.Chrome(options=options)

try:
    from pypdf import PdfWriter, PdfReader
    merger = PdfWriter()
    temp_pdfs = []

    for i, slide_file in enumerate(slide_files):
        file_url = "file:///" + slide_file.replace("\\", "/")
        print(f"\nRendering slide {i+1}/{len(slide_files)}: {os.path.basename(slide_file)}")

        driver.get(file_url)
        time.sleep(2)

        # Inject CSS to ensure slide fits the page when printing
        driver.execute_script("""
            const style = document.createElement('style');
            style.textContent = `
                @page {
                    size: 13.33in 7.5in;
                    margin: 0;
                }
                body {
                    margin: 0 !important;
                    padding: 0 !important;
                    overflow: hidden !important;
                }
                .slide-container {
                    width: 100vw !important;
                    height: 100vh !important;
                    page-break-after: avoid;
                }
            `;
            document.head.appendChild(style);
        """)

        # Paper: 13.33 x 7.5 inches = landscape 16:9
        # landscape=False because we set the width > height ourselves
        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
            "landscape": False,
            "printBackground": True,
            "preferCSSPageSize": True,
            "paperWidth": 13.33,
            "paperHeight": 7.5,
            "marginTop": 0,
            "marginBottom": 0,
            "marginLeft": 0,
            "marginRight": 0,
            "scale": 1,
        })

        temp_pdf = os.path.join(slide_dir, f"_temp_slide_{i+1:02d}.pdf")
        with open(temp_pdf, "wb") as f:
            f.write(base64.b64decode(pdf_data["data"]))
        temp_pdfs.append(temp_pdf)
        print(f"  Done ({os.path.getsize(temp_pdf) / 1024:.1f} KB)")

    print(f"\nMerging {len(temp_pdfs)} slides...")
    for pdf in temp_pdfs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            merger.add_page(page)
    with open(pdf_path, "wb") as f:
        merger.write(f)

    for pdf in temp_pdfs:
        os.remove(pdf)

    size = os.path.getsize(pdf_path)
    print(f"\nPDF saved: {pdf_path} ({size / 1024:.1f} KB)")

finally:
    driver.quit()
