# 🕵️‍♂️ LinkedIn Doctors Scraper with Selenium + Proxy Rotation

This Python script automates scraping of **LinkedIn profiles** (e.g., Cardiologists, Oncologists in India) with support for:

- Proxy rotation
- Headless browser mode
- Manual login for authentication

Extracted data includes:

- Name
- Profile URL
- Current Job Title
- Company Name
- Location

Saved into a CSV file: `Doctors_linkedin.csv`. or anyother file 

---

## 🚀 Features

- ✅ Manual LinkedIn login for authentication
- 🔁 Proxy rotation to avoid blocks
- 🧭 Scrolls and navigates search results automatically
- 📄 Visits each profile and scrapes key details
- 📤 Stores data in a CSV file

---

## 📦 Setup

# 1. Install dependencies
pip install -r requirements.txt
pip install selenium 
pip install requests

#🔐 Manual Login Instructions
Due to LinkedIn's strict policies:

The script will open a Chrome browser.

Log in manually to LinkedIn (use a real account).

Once logged in and on the search results page, press Enter in the terminal to proceed.

#🌐 Proxy Rotation (Optional)
To use rotating proxies:

Prepare a list of HTTP/S proxies (free or paid).

Load them in your script.

For each request/session, change the proxy.

Example code snippet:

python
Copy
Edit
options.add_argument(f'--proxy-server=http://{proxy}')
Note: Free proxies often break or get blocked. Use premium rotating proxies for better reliability.

#🧠 How It Works
Load LinkedIn search results for doctors in India.

Scroll to load full results.

Collect unique profile links.

Visit each profile and extract:

Name

Job Title

Company Name

Location

Save the results to Doctors_linkedin.csv.
