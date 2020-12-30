from splinter import Browser
from typing import Optional

WEBSITES = [
    (
        "https://www.elgiganten.dk/product/gaming/konsoller/xbox-konsoller/218667/xbox-series-x-1-tb-sort",  # noqa
        ".product-price-text",
        "Ikke tilgængelig",
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
     ".p-buy", "Request Stock Alert")
]


def in_stock_xbox_finder(browser: Browser) -> Optional[str]:
    for website in WEBSITES:
        url, css_selector, out_of_stock_price_text = website

        browser.visit(url)
        price_text = browser.find_by_css(css_selector).text

        if price_text != out_of_stock_price_text:
            return url

    return None


if __name__ == "__main__":
    with Browser("chrome") as browser:
        url = in_stock_xbox_finder(browser)

    if url:
        print(f"RUN FORREST: {url}")
    else:
        print("Hoooold!")
