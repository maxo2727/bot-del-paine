import os
import requests
from playwright.sync_api import expect, sync_playwright

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TORRES_DEL_PAINE_URL = "https://www.pasesparques.cl/es/torres-del-paine-300/parque-nacional-torres-del-paine-3412"

def advance_calendar_to_january_2027(page):
    current_month = page.locator("h2.react-datepicker__current-month:visible").first
    next_month = page.get_by_role("button", name="Next Month").first
    target_month = "enero 2027"

    current_month.wait_for(state="visible", timeout=10000)

    for _ in range(24):
        month_text = current_month.inner_text().strip().lower()
        if month_text == target_month:
            return

        next_month.click()
        expect(current_month).not_to_have_text(month_text, timeout=5000)

    raise RuntimeError(f"No se alcanzó {target_month}; mes actual: {current_month.inner_text()}")

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1
        )

        page.goto(TORRES_DEL_PAINE_URL, wait_until="networkidle", timeout=60000)
        advance_calendar_to_january_2027(page)

        page.screenshot(
            path="screenshot.jpeg",
            full_page=False
        )

        browser.close()

def send_to_telegram():

    with open("screenshot.jpeg", "rb") as photo:
        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "caption": "Hola, probando"
            },
            files={"photo": photo},
            timeout=60
    )
        
    print(response.text)
    response.raise_for_status()

if __name__ == "__main__":
    take_screenshot()
    send_to_telegram()
    print("Foto enviada")
