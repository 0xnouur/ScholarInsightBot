from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator
import os
import time

os.environ["TOKENIZERS_PARALLELISM"] = "false"

author_name = input("📌 Enter the author's name: ").strip()

options = Options()
# options.add_argument('--headless')  # Uncomment to run in headless mode
service = Service('/opt/homebrew/bin/geckodriver')  # Adjust if needed

driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 10)

try:
    search_url = f"https://scholar.google.com/scholar?hl=en&q={author_name.replace(' ', '+')}"
    driver.get(search_url)
    
    # Try to locate the author profile link using two fallback selectors
    try:
        author_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4.gs_rt2 a")))
    except:
        try:
            author_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_ai_name a")))
        except:
            print("\n⚠️ Author profile not found or page structure may have changed.")
            input("Press Enter to close...")
            driver.quit()
            exit()
    
    print(f"\n👤 Navigating to author profile: {author_link.get_attribute('href')}")
    author_link.click()
    time.sleep(2)

    first_paper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gsc_a_at")))
    paper_title = first_paper.text.strip()
    paper_link = first_paper.get_attribute('href')

    print(f"\n📌 Most cited paper title:\n{paper_title}")
    print(f"🔗 Paper link:\n{paper_link}")
    
    driver.get(paper_link)
    time.sleep(2)

    try:
        abstract = driver.find_element(By.CLASS_NAME, "gsh_small").text.strip()
        print(f"\n📝 Paper Abstract (English):\n{abstract}")
        
        if abstract.endswith("..."):
            print("\n⚠️ The abstract might be incomplete. You can check the full version on the publisher's website.")
        
        translated = GoogleTranslator(source='auto', target='tr').translate(abstract)
        print(f"\n🇹🇷 Translated Abstract (Turkish):\n{translated}")
    except:
        print("\n⚠️ No abstract found. Google Scholar may not display it for this paper.")
    
    input("\n🟢 Firefox is still open. Press Enter to close...")
    
except Exception as e:
    print(f"\n🔴 An error occurred: {e}")
    input("Press Enter to close...")
    
finally:
    driver.quit()
