import streamlit as st
import requests
import secrets as secrets

import google.generativeai as genai

from naukriScrapping import scrape_naukri
from indeedScraping import scrape_indeed
from glassdoorScraping import scrape_glassdoor
from monsterScraping import scrape_monster


from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")

genai.configure(api_key=api_key)

# Function to call Gemini API with initial prompt
def call_gemini_api(search_query):

    # Set up the model
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    initialPrompt = "Extract these 4 keywords from given prompt Job Title, Experience, Location, Work Mode. For Example if the prompt is Flutter Developer Internships in gurugram in office, then i want response as Job Title: Flutter Developer Internship Experience: Any, Location: Gurugram, Work Mode: in office.Use NA if anything is missing. here is the prompt: "
    convo.send_message(initialPrompt + search_query)
    # print(convo.last.text)

    return convo.last.text


# Streamlit app
def main():
    st.title('JobSavvy')
    st.subheader('Enhanced Job searching and Tracking using AI')

    search_query = st.text_input('Enter your search query')

    if st.button('Search'):
        gemini_response = call_gemini_api(search_query)
        print(gemini_response)
        job_info = parse_gemini_response(gemini_response)
        print(job_info)

        scraped_naukri_jobs = scrape_naukri(job_info)

        i = 1
        # Display the list of scraped jobs using Streamlit components
        if scraped_naukri_jobs:
            st.write('### Jobs according to your perference:')
            for job in scraped_naukri_jobs:
                st.write(f'**Job {i}:** {job["Heading"]} @ naukri.com') # Heading
                st.write(f'**Company:** {job["Sub Heading"]}') # Sub Heading
                st.write(f'**Experience Needed:** {job["Experience Needed"]}') # Experience Needed
                st.write(f'**Salary:** {job["Salary"]}') # Salary
                st.write(f'**Vacancy Link:** [{job["Link"]}]') # Vacancy Link
                st.write('---')
                i += 1
        else:
            st.write('No jobs found.')
            
        # scraped_indeed_jobs = scrape_indeed(job_info)
        # scraped_glassdoor_jobs = scrape_glassdoor(job_info)
        scraped_monster_jobs = scrape_monster(job_info)


        # if scraped_glassdoor_jobs:
        #     st.write('### Naukri.com Jobs according to your perference:')
        #     i = 1
        #     for job in scraped_glassdoor_jobs:
        #         st.write(f'**Job {i}:** {job["Heading"]}') # Heading
        #         st.write(f'**Company:** {job["Sub Heading"]}') # Sub Heading
        #         st.write(f'**Experience Needed:** {job["Experience Needed"]}') # Experience Needed
        #         st.write(f'**Salary:** {job["Salary"]}') # Salary
        #         st.write(f'**Vacancy Link:** [{job["Link"]}]') # Vacancy Link
        #         st.write('---')
        #         i += 1
        # else:
        #     st.write('No jobs found.')   
            
        # if scraped_indeed_jobs:
        #     st.write('### Naukri.com Jobs according to your perference:')
        #     i = 1
        #     for job in scraped_indeed_jobs:
        #         st.write(f'**Job {i}:** {job["Heading"]}') # Heading
        #         st.write(f'**Company:** {job["Sub Heading"]}') # Sub Heading
        #         st.write(f'**Experience Needed:** {job["Experience Needed"]}') # Experience Needed
        #         st.write(f'**Salary:** {job["Salary"]}') # Salary
        #         st.write(f'**Vacancy Link:** [{job["Link"]}]') # Vacancy Link
        #         st.write('---')
        #         i += 1
        # else:
        #     st.write('No jobs found.')        

        if scraped_monster_jobs:
            # st.write('### Naukri.com Jobs according to your perference:')
            for job in scraped_monster_jobs:
                st.write(f'**Job {i}:** {job["Heading"]} @ monster.com') # Heading
                st.write(f'**Company:** {job["Sub Heading"]}') # Sub Heading
                st.write(f'**Experience Needed:** {job["Experience Needed"]}') # Experience Needed
                st.write(f'**Location:** {job["Location"]}') # Salary
                st.write(f'**Vacancy Link:** [{job["Link"]}]') # Vacancy Link
                st.write('---')
                i += 1
        else:
            st.write('No jobs found.')  

        # st.write('### Job Information:')
        # st.write(f'**Job Title:** {job_info["Job Title"]}')
        # st.write(f'**Experience:** {job_info["Experience"]}')
        # st.write(f'**Location:** {job_info["Location"]}')
        # st.write(f'**Work Mode:** {job_info["Work Mode"]}')

        # Print clean dictionary of Gemini response in terminal

def parse_gemini_response(input_string):
    
    
    # Split the input string by newline character to get individual lines
    lines = input_string.split('\n')

    # Initialize variables to store values
    job_title = None
    experience = None
    location = None
    work_mode = None

    # Iterate through each line and extract key-value pairs
    for line in lines:
        key, value = line.split(': ')
        if value == "NA":
            value = "Any"
        if key == "Job Title":
            job_title = value
        elif key == "Experience":
            experience = value
        elif key == "Location":
            location = value
        elif key == "Work Mode":
            work_mode = value

    # Create the dictionary
    return {
        'Job Title': job_title,
        'Experience': experience,
        'Location': location,
        'Work Mode': work_mode
    }

if __name__ == '__main__':
    main()
