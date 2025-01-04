from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

def scrape_website(website):
    print("Connecting to Scraping Browser...")
    options = Options()
    service = Service(SBR_WEBDRIVER)  # Use Service to specify ChromeDriver path

    # Initialize the Chrome WebDriver with Service
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(website)
        print("Waiting for captcha (if any) to solve manually...")
        
        # Wait here if manual captcha solving is required
        input("Press Enter after solving captcha to continue...")

        print("Navigated! Scraping page content...")
        html = driver.page_source
    return html


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Clean and format text content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
