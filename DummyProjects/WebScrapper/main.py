

import nest_asyncio
nest_asyncio.apply()
from playwright.sync_api import sync_playwright
pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://vidyansh.tech")
print(page.title())
# let's write the script to find the contect form and fill it and submit it
page.fill('input[name="name"]', "Test Name")
page.fill('input[name="email"]', "test@example.com")
page.fill('textarea[name="message"]', "This is a test message.")
page.click('button[type="submit"]')

# from fastapi import FastAPI
# import asyncio
# from playwright.async_api import async_playwright
# app = FastAPI()
# playwright = None
# browser = None
# @app.on_event("startup")
# async def startup_event():
#     global playwright, browser
#     playwright = await async_playwright().start()
#     browser = await playwright.chromium.launch(headless=False)
# @app.on_event("shutdown")
# async def shutdown_event():
#     global playwright, browser
#     await browser.close()
#     await playwright.stop()