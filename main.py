from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, csv

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

def scroll_full_page():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_experience():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//section[.//span[text()[contains(.,"Experience")]]]'))
        )
        exp_section = driver.find_element(By.XPATH, '//section[.//span[text()[contains(.,"Experience")]]]')
        first_exp = exp_section.find_element(By.XPATH, './/li[1]')

        # Job Title
        try:
            job_title = first_exp.find_element(By.XPATH, './/div[contains(@class, "display-flex")]/div/span[1]').text.strip()
        except:
            try:
                job_title = first_exp.find_element(By.XPATH, './/span[@aria-hidden="true"]').text.strip()
            except:
                job_title = "N/A"

        # Company Name
        try:
            raw_company = first_exp.find_element(By.XPATH, './/span[contains(text(), "·")]/preceding-sibling::span[1]').text.strip()
            company_name = raw_company.split("·")[0].strip()
        except:
            company_name = "N/A"

        return job_title, company_name

    except Exception as e:
        print(f"❌ Error extracting experience: {e}")
        return "N/A", "N/A"

# Step 1: Manual login
driver.get("https://www.linkedin.com/login")
input("🔐 Log in manually and navigate to the search page, then press Enter here...")

# Step 2: Go to LinkedIn search results
search_url = "https://www.linkedin.com/search/results/people/?keywords=cardiologist%2C%20oncologist&location=India&origin=GLOBAL_SEARCH_HEADER&sid=_Dj"
driver.get(search_url)
time.sleep(5)

# Step 3: Prepare CSV
csv_file = open('Doctors_linkedin.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['Name', 'Profile Link', 'Current Job Title', 'Company Name', 'Location'])

page = 1
visited_profiles = set()

while True:
    print(f"\n📄 Scraping search results on page {page}...")

    # Scroll to load all profile cards
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight / 3);")
        time.sleep(2)

    # Get profile links
    profile_links = []
    cards = driver.find_elements(By.XPATH, '//a[contains(@href, "/in/")]')
    for link_elem in cards:
        url = link_elem.get_attribute("href").split("?")[0]
        if url not in visited_profiles:
            profile_links.append(url)
            visited_profiles.add(url)

    print(f"🔗 Found {len(profile_links)} new profiles.")

    for profile_url in profile_links:
        try:
            driver.get(profile_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1')))
            scroll_full_page()

            # Name
            try:
                name = driver.find_element(By.XPATH, '//h1').text.strip()
            except:
                name = "N/A"

            # Location
            try:
                location = driver.find_element(By.XPATH, '//span[contains(@class, "text-body-small inline")]').text.strip()
            except:
                location = "N/A"

            # Experience info
            job_title, company_name = extract_experience()

            # Save to CSV
            print(f"✅ {name} | {job_title} | {company_name} | {location}")
            writer.writerow([name, profile_url, job_title, company_name, location])
            time.sleep(2)

        except Exception as e:
            print(f"⚠️ Failed to scrape {profile_url} → {e}")

    # Manual pagination
    next_step = input("\n➡️ Click 'Next' on LinkedIn, then press Enter to continue (or type 'q' to quit): ").strip().lower()
    if next_step == 'q':
        break
    page += 1

# Cleanup
csv_file.close()
driver.quit()
print("\n✅ Scraping complete! Data saved to 'Doctors_linkedin.csv'.")
