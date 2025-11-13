# ...existing code...
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import re
import time

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://job-boards.greenhouse.io/anthropic/")
page.wait_for_load_state("domcontentloaded")
print(page.title())

# I want to check the software engineering and other words in the page same like a page search
search_terms = ["software engineering", "engineering", "developer", "development", "programmer", "software", "engineer"]
search_terms = [t.lower() for t in search_terms]

# 1) Snapshot links BEFORE any navigation to avoid stale handles
snapshot = []
for el in page.query_selector_all("a"):
    try:
        text = (el.inner_text() or "").strip()
    except Exception:
        text = (el.text_content() or "").strip()
    href = el.get_attribute("href") or ""
    snapshot.append((text, href))

# 2) Iterate snapshot and navigate using page.goto (no ElementHandle reuse)
for text, href in snapshot:
    low = text.lower()
    if any(term in low for term in search_terms):
        print(f"FOUND TERM in link: text='{text}' href='{href}'")
        if href:
            target = href if href.startswith("http") else urljoin(page.url, href)
            page.goto(target, wait_until="domcontentloaded")
            job_title = page.query_selector("h1")
            if job_title:
                print(f"  JOB TITLE: {job_title.inner_text().strip()}")
            # Look for an 'apply' link on the job details page or button and navigate to it
            # <button type="button" class="btn btn--rounded" aria-label="Apply">Apply</button>
            apply = page.get_by_role("button", name=re.compile("apply", re.I))
            if apply.count() > 0:
                apply.first.click()
                page.wait_for_load_state("domcontentloaded")
                print("  Navigated to Apply page.")

            else:
                print("NO Apply link found on this page.")


# 3) Click a 'contact' link if present (re-query on current page)
contact = page.get_by_role("link", name=re.compile("contact", re.I))
if contact.count() > 0:
    contact.first.click()
    page.wait_for_load_state("domcontentloaded")

html_content = page.content()
print(html_content)

# I want to close the browser after 20 seconds
time.sleep(20)
browser.close()
pw.stop()