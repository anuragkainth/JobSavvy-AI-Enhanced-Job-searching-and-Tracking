from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

def scrape_internshala(job_info):
    # Set Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.headless = True

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    scraped_jobs = []

    job_title = job_info['Job Title'].replace(" ", "-")
    job_location = job_info['Location'].replace(" ", "-")
    job_experience = job_info['Experience'].replace(" ", "-")

    # Update the URL of the job listing page
    url = f"https://internshala.com/jobs/{job_title}-jobs-in-{job_location}/"

    driver.get(url)

    job_cards_count = len(driver.find_elements(By.CLASS_NAME, "container-fluid.individual_internship"))

    index, new_index, i = '1', 1, 0

    csv_file = open('JobWebsite_scrape.csv', 'a', encoding="utf-8", newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Company Name', 'Job Title', 'Experience Required', 'Location', 'Start Date', 'Salary', 'Apply URL'])

    while i < job_cards_count:

        for j in range(job_cards_count):
            temp_index = str(new_index)
            # job_title_xpath = f'(.//h3[contains(@class, "heading_4_5 profile")])[{temp_index}]'
            # company_xpath = f'(.//div[contains(@class, "heading_6 company_name")])[{temp_index}]//p'
            # location_xpath = f'(.//p[contains(@id, "location_names")])[{temp_index}]//span//a'
            # start_date_xpath = f'(.//div[contains(@class, "item_body")])[{temp_index}]'
            # salary_xpath = f'(.//div[contains(@class, "item_body salary")])[{temp_index}]//span[@class="mobile"]'
            # experience_xpath = f'(.//div[contains(@class, "item_body mobile-text")])[{temp_index}]'
            # apply_url_xpath = f'(.//a[contains(@class, "button_easy_apply_t")])[{temp_index}]'

            job_title_xpath = f'(.//h3[contains(@class, "heading_4_5 profile")])[{temp_index}]'
            company_xpath = f'(.//div[contains(@class, "heading_6 company_name")])[{temp_index}]//p'
            location_xpath = f'(.//p[contains(@id, "location_names")])[{temp_index}]//a'
            start_date_xpath = f'(.//div[contains(@class, "item_heading") and contains(text(), "Start date")])[{temp_index}]/following-sibling::div[@class="item_body"]//span'
            salary_xpath = f'(.//div[contains(@class, "item_heading") and contains(text(), "CTC")])[{temp_index}]/following-sibling::div[@class="item_body salary"]//span'
            experience_xpath = f'(.//div[contains(@class, "item_heading") and contains(text(), "Experience")])[{temp_index}]/following-sibling::div[contains(@class, "item_body")]'
            apply_url_xpath = f'(.//div[contains(@class, "button_container_card")])[{temp_index}]//a[contains(@class, "button_easy_apply_t")]/@href'


            company = ""
            job_title = ""
            experience = ""
            location = ""
            start_date = ""
            salary = ""
            apply_url = url

            try:
                company = wait.until(EC.presence_of_element_located((By.XPATH, company_xpath))).text.strip()
                print(company)
            except:
                company = "NULL"
            try:
                job_title = wait.until(EC.presence_of_element_located((By.XPATH, job_title_xpath))).text.strip()
                print(job_title)
            except:
                job_title = "NULL" 
            try:
                experience = wait.until(EC.presence_of_element_located((By.XPATH, experience_xpath))).text.strip()
                print(experience)
            except:
                experience = "NULL"
            try:
                location = wait.until(EC.presence_of_element_located((By.XPATH, location_xpath))).text.strip()
                print(location)
            except:
                location = "NULL"
            try:
                start_date = wait.until(EC.presence_of_element_located((By.XPATH, start_date_xpath))).text.strip()
                print(start_date)
            except:
                start_date = "NULL"
            try:
                salary = wait.until(EC.presence_of_element_located((By.XPATH, salary_xpath))).text.strip()
                print(salary)
            except:
                salary = "NULL"
            try:
                apply_url_element = wait.until(EC.element_to_be_clickable((By.XPATH, apply_url_xpath)))
                apply_url = apply_url_element.get_attribute('href')

                print(apply_url)
            except:
                apply_url = url

            new_index += 1
            i += 1

            job_data = {
                'Company Name': company,
                'Job Title': job_title,
                'Experience Required': experience,
                'Location': location,
                'Start Date': start_date,
                'Salary': salary,
                'Apply URL': apply_url
            }

            scraped_jobs.append(job_data)

            print("--------------------------- "+str(i)+" ----------------------------------")

            csv_writer.writerow([company, job_title, experience, location, start_date, salary, apply_url])
            if i >= job_cards_count:
                break
        if i >= job_cards_count:
            break

    csv_file.close()
    driver.quit()

    return scraped_jobs