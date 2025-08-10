# 🏛 Delhi High Court Case Scraper with PDF Download

A Flask-based web application that allows users to search for Delhi High Court case details by **Case Type**, **Case Number**, and **Year**.  
The app scrapes the official Delhi High Court case status portal, displays results in a clean UI, and downloads any related PDF documents.

---

## 📌 Features

- Search cases by:
  - **Case Type**
  - **Case Number**
  - **Year**
- Beautiful web UI with responsive design
- Scrapes case information from [Delhi High Court Case Status](https://dhcmisc.nic.in/pcase/guiCaseWise.php)
- Automatically downloads PDF files if available
- Saves downloaded files in a local `downloads/` folder
- Uses Selenium for browser automation

---

## 🛠 Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS (Bootstrap/Tailwind if included)  
- **Web Scraping:** Selenium, BeautifulSoup4, Requests  
- **Browser Automation:** Google Chrome (headless mode) with ChromeDriver  

---

## 📦 Requirements

- Python **3.8+**
- **Google Chrome** browser installed
- **ChromeDriver** matching your Chrome version ([Download here](https://sites.google.com/chromium.org/driver/))
- Python dependencies:
pip install flask selenium beautifulsoup4 requests

 How to Run
1 Clone the repository
2 pip install flask selenium beautifulsoup4 requests
3 python app.py


Approach Used

1. User Input via UI

   * The application provides a simple web form where the user enters **Case Type**, **Case Number**, and **Year**.

2. Automated Browsing with Selenium

   * A headless Chrome browser (via Selenium) navigates to the Delhi High Court case search page.
   * Selenium programmatically fills in the form fields and triggers the search.

3. Scraping Results with BeautifulSoup

   * The returned HTML is parsed using BeautifulSoup.
   * Relevant case details are extracted from the results table or section.

4. PDF Detection & Download

   * The scraper checks the results page for PDF file links.

5. Displaying Results

   * Extracted case details are cleaned (removing empty lines or extra spaces).
   * The data is sent back to the frontend for display in a user-friendly format.

6. Error Handling

   Handles cases where:

     * No matching case is found.
     * PDF is not available.
     * HTML structure changes cause missing elements (`NoneType` errors).
   * Prevents the application from crashing by adding checks before accessing elements.
