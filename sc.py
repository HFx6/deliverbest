import pathlib

import modal

stub = modal.Stub("example-screenshot")
image = modal.Image.debian_slim().run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "pip install playwright==1.30.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)
@stub.function(image=image)
async def screenshot(url):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.screenshot(path="screenshot.png")
        await browser.close()
        data = open("screenshot.png", "rb").read()
        print("Screenshot of size %d bytes" % len(data))
        return data

@stub.local_entrypoint()
def main(url: str = "https://modal.com"):
    filename = pathlib.Path("/screenshot.png")
    data = screenshot.remote(url)
    filename.parent.mkdir(exist_ok=True)
    with open(filename, "wb") as f:
        f.write(data)
    print(f"wrote {len(data)} bytes to {filename}")

