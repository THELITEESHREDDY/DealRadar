from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sqlmodel import Session, select

from app.database.models import Site, PriceHistory
from app.database.sessions import engine


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sqlmodel import Session, select
from urllib.parse import quote_plus
import time
import re
import logging

from app.database.models import Site, PriceHistory
from app.database.sessions import engine

logger = logging.getLogger(__name__)


def scrape_all_sites(product_name: str):
    # Encode product name
    query = quote_plus(product_name)

    # Fetch sites
    with Session(engine) as session:
        sites = session.exec(select(Site)).all()

    if not sites:
        logger.warning("No sites found")
        return

    # Setup driver
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        with Session(engine) as session:
            for site in sites:
                try:
                    full_url = f"{site}{query}"
                    logger.info(f"Scraping {site.name}: {full_url}")

                    driver.get(full_url)
                    time.sleep(2)

                    selectors = [
                        (By.CLASS_NAME, "Nx9bqj"),
                        (By.CLASS_NAME, "a-price-whole")
                    ]

                    found_price = "N/A"

                    for strategy, selector in selectors:
                        try:
                            element = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((strategy, selector))
                            )

                            found_price = element.text.strip() or element.get_attribute("innerText")

                            if found_price:
                                break

                        except Exception:
                            continue

                    # Clean price (optional)
                    clean_price = re.sub(r"[^\d]", "", found_price) if found_price != "N/A" else "N/A"

                    session.add(PriceHistory(
                        product_name=product_name,
                        site_name=site.name,
                        price=clean_price
                    ))

                except Exception as e:
                    logger.error(f"Error scraping {site.name}: {e}")
                    continue

            session.commit()

    finally:
        driver.quit()