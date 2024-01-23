import re
import urllib.request
import modal

stub = modal.Stub(name="link-scraper")
playwright_image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "pip install playwright==1.30.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)


@stub.function(image=playwright_image)
async def get_links(cur_url: str):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(cur_url)
        # Enter value into form and submit
        form_selector = "#location-typeahead-location-manager-input"
        input_value = "245 adelaide road, new town, wellington"
        await page.fill(form_selector, input_value)
        await page.press(form_selector, "Enter")  # Submit form

        name = page.get_by_test_id("store-title-summary")
        nametext = await name.text_content()
        print(nametext)
        # Loop through each item and get the text content
        selector = "nav > div"
        elements = await page.query_selector_all(selector)
        texts = []
        for item in elements[1:]:
            text = await item.text_content()
            texts.append(text)
        await browser.close()

    print("Texts", texts)
    return [nametext, texts]


@stub.local_entrypoint()
def main(url):
    links = get_links.remote(url)
    print(links)
