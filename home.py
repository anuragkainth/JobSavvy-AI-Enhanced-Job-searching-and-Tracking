import streamlit as st
import requests
import webbrowser
import secrets as secrets
import google.generativeai as genai
from naukriScrapping import scrape_naukri
from monsterScraping import scrape_monster
from hirist_scrape import scrape_hirist
import pyrebase
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from bokeh.models.widgets import Div
import os
import sys

# Configuration Key

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

def bookmark_job(title, company, experience, location, link, email):
    data = {
        'email': email,
        'title': title,
        'company': company,
        'experienceRequired': experience,
        'location': location,
        'applyUrl': link
    }
    print(email)
    print(title)
    print(company)
    print(experience)
    print(location)
    print(link)
    response = requests.post('http://localhost:4000/api/user/bookmarkjob/', json=data)
    if response.status_code == 201:
        st.success("Job bookmarked successfully!")
    else:
        try:
            error_data = response.json()
            st.error(f"Failed to bookmark job. Error: {error_data['error']}")
        except:
            st.error("Failed to bookmark job. Please try again.")


script = """
<script>
    function bookmarkJob(title, company, experience, location, link, email) {
    
        var data = {
            email: email,
            title: title,
            company: company,
            experienceRequired: experience,
            location: location,
            applyUrl: link
        };

        fetch('http://localhost:4000/api/bookmarkjob/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Display success message
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
</script>
"""
alert_script = """
<script>
function showAlert(message) {
  alert(message);
}
</script>
"""
st.markdown(script, unsafe_allow_html=True)
st.markdown(alert_script, unsafe_allow_html=True)
def trigger_alert(message):
    st.markdown(f'<script>showAlert("{message}")</script>', unsafe_allow_html=True)

def main():
    
    #Initialize Firebase
    firebaseConfig = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
    }
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()

    # Initialize user_name variable to None
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = None

    # Load local CSS file
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    local_css("styles.css")

    # App layout
    col1, col2 = st.columns([0.7, 2.9])
    col1.image("images/jobsavvy-logo-2-removebg-preview.png", width=125)
    col2.title('JobSavvy.AI 🔥')
    st.subheader('Enhanced Job searching and Tracking using AI 🔥')

    # Navigation bar
    st.sidebar.subheader("Hey, " + (st.session_state['user_name'] if st.session_state['user_name'] else "User") + " 👋")
    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up'])

    # Obtain user input for email and password
    email = st.sidebar.text_input('Please enter your email address')
    password = st.sidebar.text_input('Please enter your password', type='password')

    # Sign up
    if choice == 'Sign up':
        handle = st.sidebar.text_input('Please input your full name', value='')
        submit = st.sidebar.button('Create my account')

        if submit:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success('Your account is created successfully!')
                st.balloons()
                # Sign in
                    
                db.child(user['localId']).child("Handle").set(handle)
                db.child(user['localId']).child("ID").set(user['localId'])
                # Set user_name after successful signup
                st.session_state['user_name'] = handle
                # st.title('Welcome ' + handle)
                st.sidebar.write("Welcome! You are sucessfully signed up!")
                st.sidebar.write(handle)
                # st.info('Login via login drop down selection')
                # Make a POST request to save user details in backend
                api_url = "http://localhost:4000/api/user/userdetails/"
                data = {"name": handle, "email": email}
                response = requests.post(api_url, json=data)
                if response.status_code == 201:
                    st.sidebar.write("User details saved successfully!")
                    trigger_alert("You have signed up successfully!")
                else:
                    st.sidebar.error("Failed to save user details")
                    trigger_alert("Error: Unable to Signup. Please try again later.")
                    
            except Exception as e:
                st.sidebar.error("Failed to create account")
                print(e)

    # Login
    if choice == 'Login':
        login = st.sidebar.button('Login')
        if login:
            # print('hi')
            # bookmark_job("job['Heading']", "job['Sub Heading']", "job['Experience Needed']", '', "job['Link']", "anurag@anurag.com")
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                # Retrieve user's handle from the database
                user_handle = db.child(user['localId']).child("Handle").get()
                if user_handle != None:
                    user_handle = user_handle.val()
                    # print(user_handle)
                    st.session_state['user_name'] = user_handle
                    st.sidebar.success('Welcome! You are sucessfully logged in!')
                    trigger_alert("You have signed up successfully!")
                    # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    # bio = st.radio('Jump to', ['Home', 'Workplace Feeds', 'Settings'])
                    # st.sidebar.write("Welcome! You are sucessfully logged in as:")
                    st.sidebar.write("Email: " + email)
                else:
                    st.sidebar.error("User not found in the database")
                    trigger_alert("Error: User not found in the database. Please try again later.")
            except Exception as e:
                st.sidebar.error("Invalid email or password")
                trigger_alert("Invalid email or password. Please try again later.")
                print(e)

    # Show dashboard and sign out option only if user is logged in
    if st.session_state['user_name']:
        if st.sidebar.button("Dashboard"):
            os.system(f"streamlit run dashboard_main.py {email}")

        if st.sidebar.button("Sign Out"):
            # Clear user_name to signify sign out
            st.session_state['user_name'] = None
            st.success("Logged out successfully!")  
            st.rerun()

    search_query = st.text_input('Enter your search query')

    filter_options = ['Naukri.com', 'foundit.in (Monster.com)', 'Hirist.tech']
    selected_filters = st.multiselect('Select Top Websites to Explore:', filter_options)
    
    
    if st.button('Search', key='goodsearch'):
        if st.session_state['user_name'] == None:
            st.error("Failed to fetch jobs. Please Login to your account.")
        else:    
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
                        heading = job['Heading']
                        sub_heading = job['Sub Heading']
                        experience_needed = job['Experience Needed']
                        link = job['Link']
                        print(email)
                        print(heading)
                        if  st.button(f"Bookmark Job {i} ⭐", on_click=lambda: bookmark_job(job['Heading'], job['Sub Heading'], job['Experience Needed'], "", job['Link'], email)):
                            bookmark_job(heading, sub_heading, experience_needed, '', link, email)
                        st.markdown(
                            f"""
                            <div style="padding: 10px; border: 1px solid #ccc; border-radius: 10px; margin-bottom: 10px;">
                                <h3>Job {i}: {job["Heading"]} @ naukri.com</h3>
                                <p><strong>Company:</strong> {job["Sub Heading"]}</p>
                                <p><strong>Experience Needed:</strong> {job["Experience Needed"]}</p>
                                <p><strong>Salary:</strong> {job["Salary"]}</p>
                                <p><a href="{job['Link']}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #fb4c4c; color: #fff; text-decoration: none; border: none; border-radius: 5px; cursor: pointer;">Apply</a></p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                            # st.success("Job bookmarked successfully!")
                        i += 1
                else:
                    st.write('No jobs found.')
            if 'foundit.in (Monster.com)' in selected_filters:            
                scraped_monster_jobs = scrape_monster(job_info)
                if scraped_monster_jobs:
                    # st.write('### Naukri.com Jobs according to your perference:')
                    for job in scraped_monster_jobs:
                        heading = job['Heading']
                        sub_heading = job['Sub Heading']
                        experience_needed = job['Experience Needed']
                        location = job['Location']
                        link = job['Link']
                        if  st.button(f"Bookmark Job {i} ⭐", on_click=lambda: bookmark_job(job['Heading'], job['Sub Heading'], job['Experience Needed'], job['Location'], job['Link'], email)):
                            bookmark_job(heading, sub_heading, experience_needed, '', link, email)
                        st.markdown(
                        f"""
                        <div style="padding: 10px; border: 1px solid #ccc; border-radius: 10px; margin-bottom: 10px;">
                            <h3>Job {i}: {job["Heading"]} @ monster.com</h3>
                            <p><strong>Company:</strong> {job["Sub Heading"]}</p>
                            <p><strong>Experience Needed:</strong> {job["Experience Needed"]}</p>
                            <p><strong>Location:</strong> {job["Location"]}</p>
                            <p><a href="{job['Link']}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #fb4c4c; color: #fff; text-decoration: none; border: none; border-radius: 5px; cursor: pointer;">Apply</a></p>
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
                        heading = job['Job Title']
                        sub_heading = job['Company Name']
                        experience_needed = job['Experience Required']
                        location = job['Location']
                        link = job['Apply URL']
                        if  st.button(f"Bookmark Job {i} ⭐", on_click=lambda: bookmark_job(job['Job Title'], job['Company Name'], job['Experience Required'], job['Location'], job['Apply URL'], email)):
                            bookmark_job(heading, sub_heading, experience_needed, '', link, email)
                        st.markdown(
                        f"""
                        <div style="padding: 10px; border: 1px solid #ccc; border-radius: 10px; margin-bottom: 10px;">
                            <h3>Job {i}: {job["Job Title"]} @ hirist.tech</h3>
                            <p><strong>Company:</strong> {job["Company Name"]}</p>
                            <p><strong>Location:</strong> {job["Location"]}</p>
                            <p><strong>Experience:</strong> {job["Experience Required"]}</p>
                            <p><strong>Posting Date:</strong> {job["Job Posting Date"]}</p>
                            <p><a href="{job['Apply URL']}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #fb4c4c; color: #fff; text-decoration: none; border: none; border-radius: 5px; cursor: pointer;">Apply</a></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                        i += 1
                else:
                    st.write('No jobs found.') 

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
