from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def scrape_indeed(job_info):
    # Set Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    scraped_jobs = []

    url = f"https://in.indeed.com/jobs?q={job_info['Job Title']}&l={job_info['Location']}"
    driver.get(url)

    count = 10  # Number of vacancies to scrape

    # Writing the data to a CSV file
    with open('Indeed_scrape.csv', 'w', encoding="utf-8", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Heading', 'Sub Heading', 'Vacancy Link', 'Experience Needed', 'Salary'])

        for i in range(count):
            try:
                job_title_element = wait.until(EC.presence_of_element_located((By.XPATH, f'(//h2[@class="title"])[{i+1}]')))
                job_title = job_title_element.text.strip()
                job_link = job_title_element.find_element(By.XPATH, "./a").get_attribute("href")
            except:
                job_title = "NULL"
                job_link = "NULL"
                
            try:
                company_element = wait.until(EC.presence_of_element_located((By.XPATH, f'(//span[@class="company"])[{i+1}]')))
                company_name = company_element.text.strip()
            except:
                company_name = "NULL"
                
            try:
                job_info_element = wait.until(EC.presence_of_element_located((By.XPATH, f'(//div[@class="summary"])[{i+1}]')))
                job_info = job_info_element.text.strip()
            except:
                job_info = "NULL"

            try:
                more_info_element = wait.until(EC.presence_of_element_located((By.XPATH, f'(//div[@class="jobsearch-SerpJobCard-footer"])[{i+1}]/a')))
                more_info_link = more_info_element.get_attribute("href")
            except:
                more_info_link = "NULL"
                
            try:
                salary_element = wait.until(EC.presence_of_element_located((By.XPATH, f'(//span[@class="salaryText"])[{i+1}]')))
                salary = salary_element.text.strip()
            except:
                salary = "Not Disclosed"

            job_data = {
                'Heading': job_title,
                'Sub Heading': company_name,
                'Vacancy Link': job_link,
                'Experience Needed': job_info,
                'Salary': salary,
            }

            scraped_jobs.append(job_data)
            csv_writer.writerow([job_title, company_name, job_link, job_info, salary])

    driver.quit()
    return scraped_jobs