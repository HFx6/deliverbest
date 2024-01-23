from playwright.sync_api import sync_playwright
import json
from pathlib import Path


def run(playwright):
    browser = playwright.chromium.launch(
        headless=True
    )  # Set headless=False to run browser visibly
    context = browser.new_context(
        geolocation={"longitude": 174.77706, "latitude": -41.31010},
        permissions=["geolocation"],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    )
    page = context.new_page()
    page.wait_for_load_state("networkidle")
    page.goto("https://www.doordash.com/en-NZ/store/the-old-quarter-wellington-23585633/")
    page.wait_for_load_state("domcontentloaded")
    name = ""
    category = []
    page.wait_for_selector(".sc-f9492ecc-10:nth-child(1)")

    # page.wait_for_selector(".sc-f9492ecc-10", state="detached")
    # cats = page.query_selector_all(".sc-f9492ecc-10")

    # _name = page.query_selector('[data-testid="HeroPrimaryImage"]')
    # if json_data is not None:
    #     _page_json = json_data.text_content()
    #     page_json = json.loads(_page_json)
    #     print(page_json["name"])
    # name = _name.get_attribute("alt")
    # # print(cats)
    # for c in cats:
    #     text = c.text_content()
    #     print(text)
    #     category.append(text)
    # print(name, category)

    json_data = page.query_selector("script[type='application/ld+json']")
    if json_data is not None:
        _page_json = json_data.text_content()
        page_json = json.loads(_page_json)
        name = page_json["name"]
        print(name)

        for item in page_json["hasMenu"]["hasMenuSection"][0]:
            category.append(item["name"])
        print(category)
    else:
        #     json_data = page.query_selector("#__NEXT_DATA__")
        # if json_data is not None:
        #     _page_json = json_data.text_content()
        #     page_json = json.loads(_page_json)
        #     name = any(
        #         key.startswith("Business")
        #         for key in page_json["props"]["pageProps"]["ssrPageProps"][
        #             "initialApolloState"
        #         ]
        #     )
        #     print(name)
        #     cats = any(
        #         key.startswith("storepageFeed")
        #         for key in page_json["props"]["pageProps"]["ssrPageProps"][
        #             "initialApolloState"
        #         ]["ROOT_QUERY"]
        #     )
        #     for item in cats["itemLists"]:
        #         print(item)
        #         category.append(item["name"])
        #     print(category)
        # else:
        #     print("No JSON data found.")
        print("No JSON data found.")
    return [name, category]


def search(playwright):
    browser = playwright.chromium.launch(
        headless=True
    )  # Set headless=False to run browser visibly
    context = browser.new_context(
        geolocation={"longitude": 174.77706, "latitude": -41.31010},
        permissions=["geolocation"],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    )

    page = context.new_page()
    # context.add_cookies(json.loads(Path("cookies.json").read_text()))
    page.wait_for_load_state("domcontentloaded")
    # Navigate to the url from the curl command
    page.goto(
        "https://www.doordash.com/en-NZ/search/store/The%20Old%20Quarter/?event_type=search"
    )
    page.get_by_test_id("InfoPicker").locator("div").nth(1).click()
    page.get_by_placeholder("Address").click()
    page.get_by_placeholder("Address").fill("245 adelaide road, new town, wellington")
    page.get_by_role("option", name="245 Adelaide Road, Newtown,").click()
    page.get_by_role("button", name="Save").click()
    result = page.query_selector('a[data-anchor-id="StoreCard"]')
    print(result.get_attribute("href"))
    
    # page.pause()
    browser.close()


with sync_playwright() as p:
    run(p)
    search(p)
