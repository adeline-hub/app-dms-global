from playwright.sync_api import sync_playwright

def export_page_to_pdf(url: str) -> bytes:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(url, wait_until="networkidle")

        pdf_bytes = page.pdf(
            format="A3",
            print_background=True,
            margin={
                "top": "20mm",
                "bottom": "20mm",
                "left": "20mm",
                "right": "20mm",
            },
        )

        browser.close()
        return pdf_bytes