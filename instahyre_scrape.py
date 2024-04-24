# Install selenium using command " pip install selenium "
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

def scrape_instahyre(job_info):

    # Set Firefox options for headless browsing
    firefox_options = Options()
    firefox_options.headless = True

    driver = webdriver.Firefox(options=firefox_options)
    wait = WebDriverWait(driver, 20)

    scraped_jobs = []

    job_title = job_info['Job Title'].replace(" ", "+")
    job_location = job_info['Location'].replace(" ", "+")
    job_experience = job_info['Experience'].replace(" ", "+")

    # Update the URL of the Instahyre job listing page
    url = f"https://www.instahyre.com/search-jobs?company_size=0&isLandingPage=true&job_type=1&location={job_location}&search=true&skills={job_title}&years={job_experience}"

    driver.get(url)

    # Find the number of job cards
    job_cards_count = len(driver.find_elements(By.XPATH, "//div[@class='employer-block ng-scope']"))

    csv_file = open('Instahyre_scrape.csv', 'a', encoding="utf-8", newline='')
    csv_writer = csv.writer(csv_file)
    # Writing the Heading of CSV file.
    csv_writer.writerow(['Job Title', 'Location', 'Company Founded', 'No. of Employees', 'Job Description', 'Apply URL'])

    # Iterating through each job card
    for i in range(job_cards_count):
        # Here we're replacing the Old index count of Xpath with the new index count.
        temp_index = str(i + 1)

        job_name_xpath = f'(.//div[@class="employer-job-name"]//div[@class="company-name"])[{temp_index}]'
        job_location_xpath = f'(.//div[@class="employer-locations"]/span[@class="ng-binding"])[{temp_index}]'
        company_founded_xpath = f'(.//span[@class="ng-binding" and contains(text(), "Founded in")])[{temp_index}]'
        num_employees_xpath = f'(.//span[@class="ng-binding" and contains(text(), "employees")])[{temp_index}]'
        company_description_xpath = f'(.//div[@class="employer-notes ng-binding ng-scope"])[{temp_index}]'
        apply_url_xpath = f'(.//a[@id="employer-profile-opportunity"]/@href)[{temp_index}]'

        try:
            job_title = wait.until(EC.presence_of_element_located((By.XPATH, job_name_xpath))).text
            print(job_title)
        except:
            job_title = "NULL"
        try:
            location = wait.until(EC.presence_of_element_located((By.XPATH, job_location_xpath))).text
            print(location)
        except:
            location = "NULL" 
        try:                   
            apply_url = wait.until(EC.presence_of_element_located((By.XPATH, apply_url_xpath))).get_attribute('href')
            print(apply_url)
        except:
            apply_url = url
        try:
            company_founded = wait.until(EC.presence_of_element_located((By.XPATH, company_founded_xpath))).text
            print(company_founded)
        except:
            company_founded = "NULL"
        try:
            no_of_employees = wait.until(EC.presence_of_element_located((By.XPATH, num_employees_xpath))).text
            print(no_of_employees)
        except:
            no_of_employees = "NULL"
        try:
            job_desc = wait.until(EC.presence_of_element_located((By.XPATH, company_description_xpath))).text
            print(job_desc)
        except:
            job_desc = "NULL"

        job_data = {
            'Job Title': job_title,
            'Experience Required': job_experience,
            'Location': location,
            'Company Founded': company_founded,
            'No. of Employees': no_of_employees,
            'Job Description': job_desc,
            'Apply URL': apply_url
        }

        # Append job data to list
        scraped_jobs.append(job_data)

        print("--------------------------- "+str(i + 1)+" ----------------------------------")
        # Writing all the Scrapped data into CSV file.
        csv_writer.writerow([job_title, location, company_founded, no_of_employees, job_desc, apply_url])

    csv_file.close()
    driver.quit()

    print(scraped_jobs)
    return scraped_jobs