from playwright.sync_api import sync_playwright
import json
from pathlib import Path


def run(playwright):
    browser = playwright.chromium.launch(
        headless=True
    )  # Set headless=False to run browser visibly
    context = browser.new_context()
    page = context.new_page()
    page.wait_for_load_state("networkidle")
    page.goto(
        "https://www.ubereats.com/nz/store/the-old-quarter/zGJ_JoVYSXi_syIhQmk6IQ?diningMode=DELIVERY&ps=1"
    )
    # Enter value into form and submit
    form_selector = "#location-typeahead-location-manager-input"
    input_value = "245 adelaide road, new town, wellington"
    page.fill(form_selector, input_value)
    page.press(form_selector, "Enter")  # Submit form

    # name = page.get_by_test_id("store-title-summary")
    # print(name.text_content())
    # # Loop through each item and get the text content
    # selector = "nav > div"
    # elements = page.query_selector_all(selector)
    # for element in elements[1:]:
    #     print(element.text_content())
    page.wait_for_load_state("domcontentloaded")
    name = ""
    category = []
    page.wait_for_selector("nav[role='navigation']")

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

        for item in page_json["hasMenu"]["hasMenuSection"]:
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
        headless=False
    )  # Set headless=False to run browser visibly
    context = browser.new_context()

    page = context.new_page()
    # context.add_cookies(json.loads(Path("cookies.json").read_text()))
    page.wait_for_load_state("domcontentloaded")
    # Navigate to the url from the curl command
    page.goto(
        "https://www.ubereats.com/nz/search?diningMode=DELIVERY&q=The%20Old%20Quarter&sc=SEARCH_BAR&vertical=ALL"
    )
    form_selector = "#location-typeahead-home-input"
    input_value = "245 adelaide road, new town, wellington"
    page.query_selector(form_selector).fill(input_value)
    page.query_selector(form_selector).press("Enter")  # Submit form
    addy = page.locator("#location-typeahead-home-item-0")
    addy.wait_for()
    addy.click()
    page.wait_for_load_state("domcontentloaded")
    # cookies = context.cookies()
    # Path("cookies.json").write_text(json.dumps(cookies))
    # Do something with the page, such as extracting the results
    results = page.get_by_role("link", name="Mama Brown")
    print(results.get_attribute("href"))
    # Close the browser
    page.pause()
    # browser.close()


with sync_playwright() as p:
    run(p)
    search(p)
