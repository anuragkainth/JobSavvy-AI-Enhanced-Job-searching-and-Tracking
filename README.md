# JobSavvy: AI-Enhanced Job Searching and Tracking

JobSavvy is a Streamlit-based web application that uses AI to enhance job search and tracking. It combines job scraping from popular job portals, Firebase for user authentication, and MongoDB for job management.

## Features
- AI-powered job searching using Google API.
- Job scraping from Naukri, Hirist, and Foundit using Selenium.
- User dashboard for job tracking and management (e.g., bookmarked, applied, interviewing, negotiating, accepted) via MongoDB.
- Firebase integration for user authentication.

## Prerequisites
To run this application, you will need:
- Basic understanding of Python (including Streamlit) and JavaScript (including Node.js).
- Familiarity with Docker for containerization.
- A pre-fetched Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
- A pre-configured Firebase app on the [Firebase Console](https://console.firebase.google.com/).
- A MongoDB database set up on MongoDB Cloud using [MongoDB Atlas](https://www.mongodb.com/docs/atlas/getting-started/).

## Environment Variables
Create a `.env` file in root directory and include the following variables:

```bash
# Google API Key
API_KEY="your-google-api-key-here"

# MongoDB
MONGO_URI="your-mongodb-uri-here"

# Firebase Config
FIREBASE_API_KEY="your-firebase-api-key-here"
FIREBASE_AUTH_DOMAIN="your-firebase-auth-domain-here"
FIREBASE_DATABASE_URL="your-firebase-database-url-here"
FIREBASE_PROJECT_ID="your-firebase-project-id-here"
FIREBASE_STORAGE_BUCKET="your-firebase-storage-bucket-here"
FIREBASE_MESSAGING_SENDER_ID="your-firebase-messaging-sender-id-here"
FIREBASE_APP_ID="your-firebase-app-id-here"
FIREBASE_MEASUREMENT_ID="your-firebase-measurement-id-here"
```

## Firebase JSON Setup
1. Go to your [Firebase Console](https://console.firebase.google.com/).
2. Select your project.
3. Navigate to **Project Settings**.
4. Under the **Service Accounts** tab, click **Generate New Private Key**.
5. Save the JSON file and place it in the `server` directory.

## Running the App Locally

### Backend
1. Navigate to the backend directory.
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Add the MongoDB URI to the `.env` file and place the Firebase JSON file in the `server` directory.
4. Start the backend server:
   ```
   npm run dev
   ```
### Frontend
1. Navigate to the frontend directory.
2. Install Python dependencies:
   ```python
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```python
   streamlit run home.py
   ```

### Docker
To run the app using Docker, follow the steps below. Docker allows you to containerize your application for easier deployment and scaling in professional environments.

1. Build the Docker image:
   ```bash
   docker build -t job-savvy-app .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 8501:8501 job-savvy-app
   ```
