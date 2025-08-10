from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import requests
from urllib.parse import urljoin

app = Flask(__name__)

def scrape_case(case_type, reg_no, year):
    if not all([case_type, reg_no, year]):
        raise ValueError("Missing one or more input parameters.")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://dhcmisc.nic.in/pcase/guiCaseWise.php")
    time.sleep(2)

    Select(driver.find_element(By.ID, "ctype")).select_by_visible_text(case_type)
    driver.find_element(By.ID, "regno").send_keys(reg_no)
    Select(driver.find_element(By.ID, "regyr")).select_by_visible_text(str(year))

    captcha_text = driver.find_element(By.ID, "cap").text.strip().split()[0]
    driver.find_element(By.NAME, "captcha_code").send_keys(captcha_text)

    driver.find_element(By.NAME, "Submit").click()
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    pdf_links = soup.find_all("a", href=True)
    pdf_urls = []
    for a_tag in pdf_links:
        href = a_tag['href']
        if href.lower().endswith('.pdf'):
            full_url = urljoin(driver.current_url, href)
            pdf_urls.append(full_url)

    downloads_folder = "downloads"
    os.makedirs(downloads_folder, exist_ok=True)

    for pdf_url in pdf_urls:
        filename = os.path.join(downloads_folder, pdf_url.split("/")[-1])
        try:
            resp = requests.get(pdf_url)
            resp.raise_for_status()
            with open(filename, "wb") as f:
                f.write(resp.content)
            print(f"Downloaded PDF: {filename}")
        except Exception as e:
            print(f"Failed to download PDF {pdf_url}: {e}")

    result_data = []
    tables = soup.find_all("table") or []
    for table in tables:
        rows = []
        trs = table.find_all("tr") or []
        for tr in trs:
            tds = tr.find_all(["td", "th"]) or []
            cells = [td.get_text(strip=True) for td in tds]
            if cells:
                rows.append(cells)
        if rows:
            result_data.append(rows)

    driver.quit()
    return result_data

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    error = None
    if request.method == "POST":
        case_type = request.form.get("case_type")
        reg_no = request.form.get("reg_no")
        year = request.form.get("year")

        try:
            data = scrape_case(case_type, reg_no, year)
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
