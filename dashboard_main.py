import streamlit as st
import requests
import asyncio
import aiohttp
import sys

# Access the email argument
if len(sys.argv) > 1:
    email = sys.argv[1]
else:
    email = None

# Function to fetch jobs data for a specific section
async def fetch_bookmarked_jobs(email):
    endpoint = "http://localhost:4000/api/user/bookmarkjobs/"
    return await fetch_jobs(email, endpoint)

async def fetch_applied_jobs(email):
    endpoint = "http://localhost:4000/api/user/appliedjobs/"
    return await fetch_jobs(email, endpoint)

async def fetch_interviewing_jobs(email):
    endpoint = "http://localhost:4000/api/user/interviewingjobs/"
    return await fetch_jobs(email, endpoint)

async def fetch_negotiating_jobs(email):
    endpoint = "http://localhost:4000/api/user/negotiatingjobs/"
    return await fetch_jobs(email, endpoint)

async def fetch_accepted_jobs(email):
    endpoint = "http://localhost:4000/api/user/acceptedjobs/"
    return await fetch_jobs(email, endpoint)

async def fetch_jobs(email, endpoint):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, json={"email": email}) as response:
                if response.status == 200:
                    data = await response.json()
                    # Extract the appropriate key based on endpoint
                    if "bookmarkedJobs" in data:
                        return data["bookmarkedJobs"]
                    elif "appliedJobs" in data:
                        return data["appliedJobs"]
                    elif "interviewingJobs" in data:
                        return data["interviewingJobs"]
                    elif "negotiatingJobs" in data:
                        return data["negotiatingJobs"]
                    elif "acceptedJobs" in data:
                        return data["acceptedJobs"]
                    else:
                        return []
                else:
                    st.error("Error fetching jobs data")
                    return []
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []


# Set up the main layout
st.set_page_config(page_title="dashboard2", layout="wide")

# Main content area with Dashboard statistics
st.subheader("Dashboard")
col1, col3, col2, col4 = st.columns(4)

# Function to display metric with image
def display_metric_with_image(column, title, value, image_path):
    with column:
        st.metric(label=title, value=value)
        st.image(image_path, width=100)

# Display metrics with images
display_metric_with_image(col1, "📌 Bookmarked", "", "./images/9135326.png")
display_metric_with_image(col3, "📋 Applications", "", "./images/6130033.png")
display_metric_with_image(col2, "✨ Shortlisted", "", "./images/6130061.png")
display_metric_with_image(col4, "💵 Accepted", "", "./images/7090895.png")

# Layout for My Jobs on the right side of the screen
st.sidebar.markdown("---")

# List different job positions
st.subheader("My Jobs")

# Function to display job cards
def display_job_card(job):
    st.markdown(
        f"""
        <div style="padding: 10px; border: 1px solid #ccc; border-radius: 10px; margin-bottom: 10px;">
            <h3>{job['title']}</h3>
            <p><strong>Company:</strong> {job['company']}</p>
            <p><strong>Location:</strong> {job['location']}</p>
            <p><strong>Experience Required:</strong> {job['experienceRequired']}</p>
            <p><strong>Posting Date:</strong> {job['postingDate']}</p>
            <p><a href="{job['applyUrl']}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #fb4c4c; color: #fff; text-decoration: none; border: none; border-radius: 5px; cursor: pointer;">Apply</a></p>
            <p><select id="status_select_{job['title']}">
                <option value="">Change Section</option>
                <option value="0">Bookmarked</option>
                <option value="1">Applied</option>
                <option value="2">Interviewing</option>
                <option value="3">Negotiating</option>
                <option value="4">Accepted</option>
            </select></p>
            <button onclick="applyChanges('{job['title']}')">Apply Changes</button>
        </div>
        """,
        unsafe_allow_html=True
    )

# Fetch and display job cards on the right side of the screen
async def display_jobs():
    for section, fetch_function in {
        "BOOKMARKED": fetch_bookmarked_jobs,
        "APPLIED": fetch_applied_jobs,
        "INTERVIEWING": fetch_interviewing_jobs,
        "NEGOTIATING": fetch_negotiating_jobs,
        "ACCEPTED": fetch_accepted_jobs
    }.items():
        if st.sidebar.button(section):
            jobs = await fetch_function(email)  # Run async function synchronously
            if jobs:
                for job in jobs:
                    display_job_card(job)
            else:
                st.error("No jobs present")

# Function to trigger API to update job status
async def apply_changes(email, job_id, index):
    try:
        endpoint = f"http://localhost:4000/api/updatejobstatus/{job_id}"
        payload = {"email": email, "inx": index}
        async with aiohttp.ClientSession() as session:
            async with session.patch(endpoint, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    st.error("Error updating job status")
                    return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Trigger the API to update job status when Apply Changes button is clicked
def apply_changes_trigger(job_title):
    # Get the selected index
    index = st.selectbox(f"Select new status for {job_title}", ["Bookmark", "Applied", "Interviewing", "Negotiating", "Accepted"])
    if index:
        index_map = {"Bookmark": 0, "Applied": 1, "Interviewing": 2, "Negotiating": 3, "Accepted": 4}
        index_value = index_map[index]
        # Trigger API to update job status
        asyncio.create_task(apply_changes(email, job_title, index_value))

# Run the app
async def main():
    await display_jobs()

if __name__ == "__main__":
    asyncio.run(main())
