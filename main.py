import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TORRES_DEL_PAINE_URL = "https://www.pasesparques.cl/es/torres-del-paine-300/parque-nacional-torres-del-paine-3412"

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1
        )

        page.goto(TORRES_DEL_PAINE_URL, wait_until="networkidle", timeout=60000)

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