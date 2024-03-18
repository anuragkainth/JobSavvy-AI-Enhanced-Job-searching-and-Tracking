# Install selenium using command " pip install selenium "
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

def scrape_monster(job_info):

    # Set Firefox options for headless browsing
    firefox_options = Options()
    firefox_options.headless = True

    driver = webdriver.Firefox(options=firefox_options)
    wait = WebDriverWait(driver, 20)

    scraped_jobs = []

    # Update the URL of the job listing page

     # Extract job title and location from job_info dictionary
    job_title = job_info['Job Title'].replace(" ", "+")
    job_location = job_info['Location'].replace(" ", "+")

    # Construct the URL for job listings
    url = f"https://www.foundit.in/srp/results?query=%22{job_title}%22&locations={job_location}"

    # driver.get(f"https://www.foundit.in/srp/results?sort=1&limit=15&query=%22{job_info['Job Title']}%22&locations={job_info['Location']}&experienceRanges=0~{job_info['Experience']}")
    driver.get(url)
    # https://www.foundit.in/srp/results?query=%22Flutter+Developer%22&locations=Bengaluru+%2F+Bangalore&searchId=7d9b1d74-12c2-4644-aded-6a6060e4fa36

    count = 10  # Update the Number of Vacancy count you want to scrape.

    index, new_index, i = '0', 1, 0  # This is the index variable of the elements from which data will be scraped
    # Xpaths of the various element from which data will be scraped.
# XPaths for the job listings
    # XPaths for the job listings

    # heading_xpath = '//div[contains(@class, "srpResultCardContainer")]/div[contains(@class, "cardHead")]/div[contains(@class, "headerContent")]/div[contains(@class, "infoSection")]/div[@class="jobTitle"]'
    # link_xpath = '//div[contains(@class, "srpResultCardContainer")]/div[contains(@class, "cardHead")]/div[contains(@class, "headerContent")]/div[contains(@class, "infoSection")]/div[@class="jobTitle"]/a/@href'
    # subheading_xpath = '//div[contains(@class, "srpResultCardContainer")]/div[contains(@class, "cardHead")]/div[contains(@class, "headerContent")]/div[contains(@class, "infoSection")]/div[@class="companyName"]/p'
    # experience_xpath = '//div[contains(@class, "srpResultCardContainer")]/div[contains(@class, "cardBody")]/div[contains(@class, "bodyRow")][3]/div[@class="details"]'
    # salary_xpath = '//div[contains(@class, "srpResultCardContainer")]/div[contains(@class, "cardBody")]/div[contains(@class, "bodyRow")][4]/div[@class="details"]'


    # Job title XPath (using `jobTitle` class for clarity):
    heading_xpath = "(.//div[contains(@class, 'cardContainer')])[" + str(index) + "]//div[contains(@class, 'jobTitle')]"

    link_xpath = "(.//div[contains(@class, 'cardContainer')])[" + str(index) + "]//div[contains(@class, 'jobTitle')]"

    # Company name XPath:
    subheading_xpath = "(.//div[contains(@class, 'cardContainer')])[" + str(index) + "]//div[contains(@class, 'companyName')]//p"

    # Location XPath:
    location_xpath = "(.//div[contains(@class, 'cardContainer')])[" + str(index) + "]//div[contains(@class, 'bodyRow')][2]//div[contains(@class, 'details')]"

    # Experience XPath:
    experience_xpath = "(.//div[contains(@class, 'cardContainer')])[" + str(index) + "]//div[contains(@class, 'bodyRow')][3]//div[contains(@class, 'details')]"

    # Skills XPath (assuming all skills are within a single `skillDetails` element):
    # salary_xpath = "(.//div[contains(@class, 'cardContainer')])[" + str(index) + "]//div[contains(@class, 'bodyRow')][*]//div[contains(@class, 'skillDetails')]//div[contains(@class, 'skillTitle')]"

    # Apply button XPath (using `cardApplyLabel` class for direct targeting):
    # link_xpath = ""


    csv_file = open('Monster_scrape.csv', 'a', encoding="utf-8", newline='')
    csv_writer = csv.writer(csv_file)
    # Writing the Heading of CSV file.
    csv_writer.writerow(['Heading', 'Sub Heading', 'Vacancy Link', 'Experience Needed', 'Salary'])

    while i < count:

        for j in range(20):
            # Here we're replacing the Old index count of Xpath with New Index count.
            temp_index = str(new_index).zfill(2)  # Zfill(2) is used to put zeros to the left of any digit till 2 decimal places.
            heading_xpath = heading_xpath.replace(index, temp_index)
            location_xpath = location_xpath.replace(index, temp_index)
            link_xpath = link_xpath.replace(index, temp_index)
            subheading_xpath = subheading_xpath.replace(index, temp_index)
            experience_xpath = experience_xpath.replace(index, temp_index)
            # salary_xpath = salary_xpath.replace(index, temp_index)
            index = str(new_index).zfill(2)

            heading = ""
            location = ""
            subheading = ""
            experience = ""
            link = ""

            try:
                # Capturing the Heading from webpage and storing that into Heading variable.
                heading = wait.until(EC.presence_of_element_located((By.XPATH, heading_xpath))).text
                print(heading)
            except:
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
                location = wait.until(EC.presence_of_element_located((By.XPATH, location_xpath))).text
                print(location)
            except:
                salary = "NULL"
            new_index += 1
            i += 1

            job_data = {
            'Heading': heading,
            'Link': url,
            'Sub Heading': subheading,
            'Experience Needed': experience,
            'Location': location
            }

            # Append job data to list
            scraped_jobs.append(job_data)

            print("--------------------------- "+str(i)+" ----------------------------------")
            # Writing all the Scrapped data into CSV file.
            csv_writer.writerow([heading, subheading, link, experience, location])
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