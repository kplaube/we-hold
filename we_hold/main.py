import datetime
import os
import time
import urllib.parse
from typing import List, Optional

import requests
from dotenv import load_dotenv
from splinter import Browser

WEBSITES = [
    (
        "https://www.elgiganten.dk/product/gaming/konsoller/xbox-konsoller/218667/xbox-series-x-1-tb-sort",  # noqa
        ".product-price-text",
        "Ikke tilgængelig",
    ),
    (
        "https://www.xbox.com/en-gb/configure/8WJ714N3RBTL?ranMID=24542&ranEAID=kXQk6*ivFEQ&ranSiteID=kXQk6.ivFEQ-1calhptjboV60i5_9LNqOg&epi=kXQk6.ivFEQ-1calhptjboV60i5_9LNqOg&irgwc=1&OCID=AID2000142_aff_7593_1243925&tduid=%28ir__auezd9kuk0kfqkb9kk0sohz3ze2xs9d9kecxn9gf00%29%287593%29%281243925%29%28kXQk6.ivFEQ-1calhptjboV60i5_9LNqOg%29%28%29&irclickid=_auezd9kuk0kfqkb9kk0sohz3ze2xs9d9kecxn9gf00",  # noqa
        "button[aria-label='Checkout bundle']",
        "Out of stock",
    ),
    (
        "https://www.power.dk/gaming-og-underholdning/konsol/konsol/xbox-series-x-konsol/p-1119853/",
        ".buy-area .buy-area__webshop .btn-mega",
        "Ikke på lager online",
    ),
    (
        "https://www.amazon.de/-/en/RRT-00009/dp/B08H93ZRLL/ref=pd_ybh_a_1?_encoding=UTF8&psc=1&refRID=6TQZHKJC7M7MSP434G0P",  # noqa
        ".a-color-price",
        "Currently unavailable.",
    ),
    (
        "https://www.amazon.fr/Xbox-X-plus-puissante/dp/B08H93ZRLL/ref=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=37KXKCGU9D0GO&dchild=1&keywords=xbox+series+x&qid=1607954316&sprefix=xbox+se%2Caps%2C193&sr=8-1",  # noqa
        ".a-color-price",
        "Actuellement indisponible.",
    ),
    (
        "https://www.elgiganten.se/product/gaming/spelkonsol/xbox-konsol/218667/xbox-series-x-1-tb-svart",  # noqa
        ".product-price-text",
        "Ej köpbar",
    ),
    (
        "https://www.amazon.es/Microsoft-RRT-00009-Xbox-Series-X/dp/B08H93ZRLL/ref=sr_1_1?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=xbox+series+x&qid=1607954345&sr=8-1",  # noqa
        ".a-color-price",
        "No disponible.",
    ),
    (
        "https://www.elkjop.no/product/gaming/spillkonsoll/xbox-konsoller/218667/xbox-series-x-1-tb-sort",  # noqa
        ".product-price-text",
        "Ikke tilgjengelig",
    ),
    ("https://www.box.co.uk/RRT-00007-Xbox-Series-X-Console_3201195.html",
     ".p-buy", "Request Stock Alert"),
]


def in_stock_xbox_finder(browser: Browser) -> List[str]:
    urls = []

    for website in WEBSITES:
        url, css_selector, out_of_stock_price_text = website

        try:
            browser.visit(url)
            price_text = browser.find_by_css(css_selector).text
        except Exception as e:
            price_text = f"FAILED with {e}"
            log_check_event(url, price_text)
            continue

        log_check_event(url, price_text)
        if price_text.lower() != out_of_stock_price_text.lower():
            urls.append(url)

    return urls


def log_check_event(url: str, price_text: str) -> None:
    parsed_url = urllib.parse.urlparse(url)
    print(
        f"{datetime.datetime.now()} checking {parsed_url.netloc} -> {price_text}"
    )


def send_found_email(xbox_url: str) -> Optional[requests.models.Response]:
    url = os.environ.get('MAILGUN_URL')
    api_key = os.environ.get('MAILGUN_API_KEY')
    if (url or api_key) is None:
        error_message = "ERROR No mailgun info"
        print(error_message)
        return None

    recipients = os.environ.get('EMAILS', '').split(',')
    domain = os.environ.get('MAILGUN_DOMAIN')

    from_email = "We hold xbox monitor <weholdmonitor@sandbox.mgsend.net>"
    return requests.post(url,
                         auth=("api", api_key),
                         data={
                             "from": from_email,
                             "to": recipients,
                             "subject": "Available xbox found",
                             "text": f"FOUND IT!! RUN FORREST: {xbox_url}"
                         })


if __name__ == "__main__":
    load_dotenv()
    loop = os.environ.get('LOOP')
    send_found_email("STARTING SERVICE TESTING EMAIL")

    headless = os.environ.get('HEADLESS')
    while True:
        with Browser("chrome", headless=headless == "True",
                     incognito=True) as browser:
            urls = in_stock_xbox_finder(browser)

        for url in urls:
            print(f"RUN FORREST: {url}")
            send_found_email(url)

        if not urls:
            print("Hoooold!")

        if loop:
            print("...for one minute!")
            time.sleep(60)  # 1 minute
        else:
            break
