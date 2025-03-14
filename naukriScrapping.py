# Install selenium using command " pip install selenium "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

def scrape_naukri(job_info):

     # Set Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"  # Path to Chromium binary
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
    chrome_options.add_argument("--window-size=1920x1080")  # Set a default window size

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 30)

    scraped_jobs = []

    # Update the URL of Naukri Page! ( Make Sure that the page link which you're putting must be a job listing page and it must have Next page buttons. )
    driver.get(f"https://www.naukri.com/{job_info['job title']}-jobs-in-{job_info['location']}&experience={job_info['experience']}")

    count = 10  # Update the Number of Vacancy count you want to scrape.

    index, new_index, i = '0', 1, 0  # This the the index variable of the elements from which data will be Scraped
    # Xpaths of the various element from which data will be scraped.

    heading_xpath = f'(//div[contains(@class, "cust-job-tuple") and contains(@class, "sjw__tuple")])[{index}]/div[contains(@class, "row1")]/h2/a'
    link_xpath = f'(//div[contains(@class, "cust-job-tuple") and contains(@class, "sjw__tuple")])[{index}]/div[contains(@class, "row1")]/h2/a'
    subheading_xpath = f'(//div[contains(@class, "cust-job-tuple") and contains(@class, "sjw__tuple")])[{index}]/div[contains(@class, "row2")]/span[contains(@class, "comp-dtls-wrap")]/a'
    experience_xpath = f'(//div[contains(@class, "cust-job-tuple") and contains(@class, "sjw__tuple")])[{index}]/div[contains(@class, "row3")]/div[contains(@class, "job-details")]/span[contains(@class, "exp-wrap")]/span//span[@class="expwdth"]'
    salary_xpath = f'(//div[contains(@class, "cust-job-tuple") and contains(@class, "sjw__tuple")])[{index}]/div[contains(@class, "row3")]/div[contains(@class, "job-details")]/span[contains(@class, "sal-wrap")]/span//span[@title]'

    csv_file = open('Naukri_scrape.csv', 'a', encoding="utf-8", newline='')
    csv_writer = csv.writer(csv_file)
    # Writing the Heading of CSV file.
    csv_writer.writerow(['Heading', 'Sub Heading', 'Vacancy Link', 'Experience Needed', 'Salary'])

    while i < count:

        for j in range(20):
            # Here we're replacing the Old index count of Xpath with New Index count.
            temp_index = str(new_index).zfill(2)  # Zfill(2) is used to put zeros to the left of any digit till 2 decimal places.
            heading_xpath = heading_xpath.replace(index, temp_index)
            link_xpath = link_xpath.replace(index, temp_index)
            subheading_xpath = subheading_xpath.replace(index, temp_index)
            experience_xpath = experience_xpath.replace(index, temp_index)
            salary_xpath = salary_xpath.replace(index, temp_index)
            index = str(new_index).zfill(2)

            heading = ""
            link = ""
            subheading = ""
            experience = ""
            salary = ""

            try:
                # Capturing the Heading from webpage and storing that into Heading variable.
                heading = wait.until(EC.presence_of_element_located((By.XPATH, heading_xpath))).text
                print(heading)
            except Exception as e:
                print(f"Error occurred while fetching heading: {e}")
                heading = "NULL"
            try:
                link = wait.until(EC.presence_of_element_located((By.XPATH, link_xpath))).get_attribute('href')
                print(link)
            except:
                link = "NULL"
            try:
                subheading = wait.until(EC.presence_of_element_located((By.XPATH, subheading_xpath))).text
                print(subheading)
            except:
                subheading = "NULL"
            try:
                experience = wait.until(EC.presence_of_element_located((By.XPATH, experience_xpath))).text
                print(experience)
            except:
                experience = "NULL"
            try:
                salary = wait.until(EC.presence_of_element_located((By.XPATH, salary_xpath))).text
                print(salary)
            except:
                salary = "Not Disclosed"
            new_index += 1
            i += 1

            job_data = {
            'Heading': heading,
            'Link': link,
            'Sub Heading': subheading,
            'Vacancy Link': link,
            'Experience Needed': experience,
            'Salary': salary
            }

            # Append job data to list
            scraped_jobs.append(job_data)

            print("--------------------------- "+str(i)+" ----------------------------------")
            # Writing all the Scrapped data into CSV file.
            csv_writer.writerow([heading, subheading, link, experience, salary])
            if i >= count:
                break
        if i >= count:
            break
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text() = "Next"]'))).click()
        new_index = 1
    csv_file.close()
    driver.quit()

    print(scraped_jobs)
    return scraped_jobs