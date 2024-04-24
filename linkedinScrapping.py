# Install selenium using command " pip install selenium "
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

def scrape_linkedin():

    # Set Firefox options for headless browsing
    firefox_options = Options()
    firefox_options.headless = True

    driver = webdriver.Firefox(options=firefox_options)
    wait = WebDriverWait(driver, 20)

    scraped_jobs = []

    # Update the URL of the LinkedIn job listing page
    url = f"https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=Bangalore%2C%20India"

    driver.get(url)

    count = 10  # Update the Number of Vacancy count you want to scrape.

    index, new_index, i = '1', 1, 0  # This is the index variable of the elements from which data will be scraped

    csv_file = open('LinkedIn_scrape.csv', 'a', encoding="utf-8", newline='')
    csv_writer = csv.writer(csv_file)
    # Writing the Heading of CSV file.
    csv_writer.writerow(['Position Name', 'Company Name', 'Location', 'Apply URL'])

    while i < count:

        for j in range(20):
            # Here we're replacing the Old index count of Xpath with New Index count.
            temp_index = str(new_index)
            position_xpath = f'(.//li[@data-occludable-job-id])[{temp_index}]//a[contains(@class, "job-card-list__title")]'
            company_xpath = f'(.//li[@data-occludable-job-id])[{temp_index}]//span[contains(@class, "job-card-container__company-name")]'
            location_xpath = f'(.//li[@data-occludable-job-id])[{temp_index}]//li[contains(@class, "job-card-container__metadata-item")]'
            apply_url_xpath = f'(.//li[@data-occludable-job-id])[{temp_index}]//a[contains(@class, "job-card-container__link")]'

            position = ""
            company = ""
            location = ""
            apply_url = ""

            try:
                # Capturing the Position Name from webpage and storing that into position variable.
                position = wait.until(EC.presence_of_element_located((By.XPATH, position_xpath))).text
                print(position)
            except:
                position = "NULL"
            try:
                company = wait.until(EC.presence_of_element_located((By.XPATH, company_xpath))).text
                print(company)
            except:
                company = "NULL"
            try:
                location = wait.until(EC.presence_of_element_located((By.XPATH, location_xpath))).text
                print(location)
            except:
                location = "NULL"
            try:
                apply_url = wait.until(EC.presence_of_element_located((By.XPATH, apply_url_xpath))).get_attribute('href')
                print(apply_url)
            except:
                apply_url = "NULL"

            new_index += 1
            i += 1

            job_data = {
                'Position Name': position,
                'Company Name': company,
                'Location': location,
                'Apply URL': apply_url
            }

            # Append job data to list
            scraped_jobs.append(job_data)

            print("--------------------------- "+str(i)+" ----------------------------------")
            # Writing all the Scrapped data into CSV file.
            csv_writer.writerow([position, company, location, apply_url])
            if i >= count:
                break
        if i >= count:
            break

    csv_file.close()
    driver.quit()

    print(scraped_jobs)
    return scraped_jobs
