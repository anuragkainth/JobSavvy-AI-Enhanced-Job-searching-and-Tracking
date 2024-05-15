# Install selenium using command " pip install selenium "
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

def scrape_hirist(job_info):

    # Set Firefox options for headless browsing
    firefox_options = Options()
    firefox_options.add_argument('--ignore-certificate-errors')
    firefox_options.add_argument('--ignore-ssl-errors')
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--disable-gpu")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 20)

    scraped_jobs = []

    job_title = job_info['job title'].replace(" ", "&")
    job_location = job_info['location'].replace(" ", "&")
    job_experience = job_info['experience'].replace(" ", "&")

    # Update the URL of the Hirist job listing page
    # url = "https://hirist.com/search/software-developer-jobs-in-delhi"
    url = f"https://www.hirist.tech/search/{job_title}.html?locIds=36&exp={job_experience}&ref=homepage"

    driver.get(url)

    job_cards_count = len(driver.find_elements(By.XPATH, "//div[@class='job-card row  job-card-with-checkbox']"))

    index, new_index, i = '1', 1, 0  # This is the index variable of the elements from which data will be scraped

    csv_file = open('Hirist_scrape.csv', 'a', encoding="utf-8", newline='')
    csv_writer = csv.writer(csv_file)
    # Writing the Heading of CSV file.
    csv_writer.writerow(['Company Name', 'Job Title', 'Experience Required', 'Location', 'Job Posting Date', 'Apply URL'])

    card_count = job_cards_count if job_cards_count <= 5 else 5
    while i <= card_count:

        for j in range(job_cards_count):
            # Here we're replacing the Old index count of Xpath with New Index count.
            temp_index = str(new_index)
            company_xpath = f'(.//div[contains(@class, "job-description")])[{temp_index}]//span[@id="company-job"]//span[@class="dark_grey align-title"]'
            job_title_xpath = f'(.//div[contains(@class, "job-description")])[{temp_index}]//div[@class="job-title"]//a'
            experience_xpath = f'(.//div[contains(@class, "job-description")])[{temp_index}]//div[@class="job-fields"]//span[@class="dark_grey col-year"]'
            location_xpath = f'(.//div[contains(@class, "job-description")])[{temp_index}]//div[@class="job-fields"]//span[@class="show-tooltip dark_grey"]'
            posting_date_xpath = f'(.//div[contains(@class, "job-description")])[{temp_index}]//span[@class="original dark_grey"]'
            # apply_url_xpath = f"(.//div[contains(@class, 'job-description')])[{temp_index}]//a[contains(@class, 'job-title')]/@href"

            company = ""
            job_title = ""
            experience = ""
            location = ""
            posting_date = ""
            apply_url = url

            try:
                company = wait.until(EC.presence_of_element_located((By.XPATH, company_xpath))).text
                print(company)
            except:
                company = "NULL"
            try:
                job_title = wait.until(EC.presence_of_element_located((By.XPATH, job_title_xpath))).text
                print(job_title)
            except:
                job_title = job_title
            # try:                   
            #     apply_url = wait.until(EC.presence_of_element_located((By.XPATH, apply_url_xpath))).get_attribute('href')
            #     print(apply_url)
            # except:
            #     apply_url = url
            try:
                experience = wait.until(EC.presence_of_element_located((By.XPATH, experience_xpath))).text
                print(experience)
            except:
                experience = job_experience
            try:
                location = wait.until(EC.presence_of_element_located((By.XPATH, location_xpath))).text
                print(location)
            except:
                location = job_location
            try:
                posting_date = wait.until(EC.presence_of_element_located((By.XPATH, posting_date_xpath))).text
                print(posting_date)
            except:
                posting_date = "NULL"

            new_index += 1
            i += 1

            job_data = {
                'Company Name': company,
                'Job Title': job_title,
                'Experience Required': experience,
                'Location': location,
                'Job Posting Date': posting_date,
                'Apply URL': apply_url
            }

            # Append job data to list
            scraped_jobs.append(job_data)

            print("--------------------------- "+str(i)+" ----------------------------------")
            # Writing all the Scrapped data into CSV file.
            csv_writer.writerow([company, job_title, experience, location, posting_date, apply_url])
            if i >= job_cards_count:
                break
        if i >= job_cards_count:
            break

    csv_file.close()
    driver.quit()

    print(scraped_jobs)
    return scraped_jobs