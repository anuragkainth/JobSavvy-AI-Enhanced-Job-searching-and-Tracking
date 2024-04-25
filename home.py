import streamlit as st
import requests
import secrets as secrets

import google.generativeai as genai

from naukriScrapping import scrape_naukri
from indeedScraping import scrape_indeed
from glassdoorScraping import scrape_glassdoor
from monsterScraping import scrape_monster
from linkedinScrapping import scrape_linkedin
from hirist_scrape import scrape_hirist
from internshala_scrapping import scrape_internshala
from instahyre_scrape import scrape_instahyre

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

    initialPrompt = "Extract these 4 keywords from given prompt Job Title, Experience, Location, Work Mode. For Example if the prompt is Flutter Developer Internships in gurugram with 2 years of experience, then i want response as Job Title: Flutter Developer Internship, Experience: 2, Location: Gurugram, Work Mode: NA, all are sepereated in new line. Use NA if anything is missing. here is the prompt: "
    convo.send_message(initialPrompt + search_query)
    # print(convo.last.text)

    return convo.last.text

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# Streamlit app
def main():

    # Call the CSS function to load the local CSS file
    local_css("styles.css")

    col1, col2 = st.columns([0.7, 2.9])
    
    col1.image("C:/Users/hp/Desktop/project/jobsavvy-logo-2-removebg-preview.png", width=125 )
    col2.title('JobSavvy.AI 🔥')
    st.subheader('Enhanced Job searching and Tracking using AI 🔥')

    # Navigation bar
    
    st.sidebar.image("C:/Users/hp/Desktop/project/6130408.png", width=140)
    st.sidebar.subheader("Hey, Mr. User User 👋")
    st.sidebar.button("Sign Up")
    st.sidebar.button("Sign In")

    page = st.sidebar.selectbox("Menu", ["Select Option", "Dashboard", "Sign Out"])

    #connecting to dashboard2
    if page == "Dashboard":
        if st.sidebar.button('Dashboard'):
            os.system("streamlit run dashboard2.py")

    search_query = st.text_input('Enter your search query')

    filter_options = ['Naukri.com', 'foundit.in (Monster.com)', 'LinkedIn.com', 'Glassdoor.com', 'Indeed.com', 'Hirist.tech', 'Instahyre.com']
    selected_filters = st.multiselect('Select Top Websites to Explore:', filter_options)

    # # Display selected filters
    # if selected_filters:
    #     st.write('Select Top Websites to Explore:')
    #     for filter_name in selected_filters:
    #         st.write(f'{filter_name}')


    if st.button('Search'):
        gemini_response = call_gemini_api(search_query)
        print(gemini_response)
        job_info = gemini_text_to_map(gemini_response)
        print(job_info)

        i = 1

        # Display the list of scraped jobs using Streamlit components
        if 'Naukri.com' in selected_filters:

            scraped_naukri_jobs = scrape_naukri(job_info)
            if scraped_naukri_jobs:
                st.write('### Jobs according to your perference:')
                for job in scraped_naukri_jobs:
                    st.markdown(
                        f"""
                        <div style="padding: 10px; border: 1px solid #ccc; border-radius: 10px; margin-bottom: 10px;">
                            <h3>Job {i}: {job["Heading"]} @ naukri.com</h3>
                            <p><strong>Company:</strong> {job["Sub Heading"]}</p>
                            <p><strong>Experience Needed:</strong> {job["Experience Needed"]}</p>
                            <p><strong>Salary:</strong> {job["Salary"]}</p>
                            <p><strong>Vacancy Link:</strong> <a href="{job["Link"]}">{job["Link"]}</a></p>
                            <hr>
                            ⭐️ "Add to bookmarks"
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    i += 1
            else:
                st.write('No jobs found.')


        if 'foundit.in (Monster.com)' in selected_filters:            
            scraped_monster_jobs = scrape_monster(job_info)

            if scraped_monster_jobs:
                # st.write('### Naukri.com Jobs according to your perference:')
                for job in scraped_monster_jobs:
                    st.markdown(
                    f"""
                    <div style="padding: 10px; border: 1px solid #ccc; border-radius: 10px; margin-bottom: 10px;">
                        <h3>Job {i}: {job["Heading"]} @ monster.com</h3>
                        <p><strong>Company:</strong> {job["Sub Heading"]}</p>
                        <p><strong>Experience Needed:</strong> {job["Experience Needed"]}</p>
                        <p><strong>Location:</strong> {job["Location"]}</p>
                        <p><strong>Vacancy Link:</strong> <a href="{job["Link"]}">{job["Link"]}</a></p>
                        <hr>
                        ⭐️ "Add to bookmarks"
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    i += 1
            else:
                st.write('No jobs found.')  
        

        if 'Hirist.tech' in selected_filters:
            scraped_hirist_jobs = scrape_hirist(job_info)

            if scraped_hirist_jobs:
                # st.write('### Naukri.com Jobs according to your perference:')
                for job in scraped_hirist_jobs:
                    st.markdown(
                    f"""
                    <div style="padding: 10px; border: 1px solid #ccc; border-radius: 10px; margin-bottom: 10px;">
                        <h3>Job {i}: {job["Job Title"]} @ hirist.tech</h3>
                        <p><strong>Company:</strong> {job["Company Name"]}</p>
                        <p><strong>Location:</strong> {job["Location"]}</p>
                        <p><strong>Experience:</strong> {job["Experience Required"]}</p>
                        <p><strong>Posting Date:</strong> {job["Job Posting Date"]}</p>
                        <p><strong>Vacancy Link:</strong> <a href="{job["Apply URL"]}">{job["Apply URL"]}</a></p>
                        <hr>
                        ⭐️ "Add to bookmarks"
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    i += 1
            else:
                st.write('No jobs found.') 


        # scraped_instahyre_jobs = scrape_instahyre(job_info)

        # # Display the list of scraped jobs using Streamlit components
        # if scraped_instahyre_jobs:
        #     st.write('### Jobs according to your perference:')
        #     for job in scraped_instahyre_jobs:
        #         st.write(f'**Job {i}:** {job["Job Title"]} @ instahyre.com') # Heading
        #         st.write(f'**Experience Needed:** {job["Experience Required"]}') # Experience Needed
        #         st.write(f'**Location:** {job["Location"]}') # Location
        #         st.write(f'**Company Founded:** {job["Company Founded"]}') # Job Type
        #         st.write(f'**No. of Employees:** {job["No. of Employees"]}') # Job Type
        #         st.write(f'**job Description:** {job["Job Description"]}') # Salary
        #         st.write(f'**Vacancy Link:** [{job["Apply URL"]}]') # Vacancy Link
        #         st.write('---')
        #         i += 1
        # else:
        #     st.write('No jobs found.')

        # scraped_internshala_jobs = scrape_internshala(job_info)
        # # Display the list of scraped jobs using Streamlit components
        # if scraped_internshala_jobs:
        #     st.write('### Jobs according to your perference:')
        #     for job in scraped_internshala_jobs:
        #         st.write(f'**Job {i}:** {job["Job Title"]} @ internshala.com') # Heading
        #         st.write(f'**Company:** {job["Company Name"]}') # Sub Heading
        #         st.write(f'**Experience Needed:** {job["Experience Required"]}') # Experience Needed
        #         st.write(f'**Salary:** {job["Salary"]}') # Salary
        #         st.write(f'**Location:** {job["Location"]}') # Experience Needed
        #         st.write(f'**Start Date:** {job["Start Date"]}') # Salary
        #         st.write(f'**Vacancy Link:** [{job["Apply URL"]}]') # Vacancy Link
        #         st.write('---')
        #         i += 1
        # else:
        #     st.write('No jobs found.')


        # scraped_linkedin_jobs = scrape_linkedin(job_info)

        # if scraped_linkedin_jobs:
        #     # st.write('### Naukri.com Jobs according to your perference:')
        #     for job in scraped_linkedin_jobs:
        #         st.write(f'**Job {i``}:** {job["Position Name"]} @ linkedIn.com') # Heading
        #         st.write(f'**Company:** {job["Company Name"]}') # Sub Heading
        #         st.write(f'**Location:** {job["Location"]}') # Salary
        #         st.write(f'**Vacancy Link:** [{job["Apply URL"]}]') # Vacancy Link
        #         st.write('---')
        #         i += 1
        # else:
        #     st.write('No jobs found.') 
        
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

def gemini_text_to_map(text):
    # Splitting the text by newline characters
    lines = text.strip().split('\n')

    # Initializing an empty dictionary to store key-value pairs
    job_info = {}
    print(lines)

    # Iterating through each line to extract key-value pairs
    for line in lines:
        # Splitting each line by the first occurrence of the colon to separate key and value
        key, value = line.split(':', 1)

        # Stripping the whitespace and converting keys to lowercase for consistency
        key = key.strip().lower()
        value = value.strip()

        # If value is 'NA', replace it with 'Any'
        if value == 'NA':
            value = 'any'

        # Adding key-value pairs to the dictionary
        job_info[key] = value

    return job_info



if __name__ == '__main__':
    main()
