// routes/users.js
const express = require('express');
const router = express.Router();
const User = require('../models/userModel');
const bodyParser = require('body-parser');
const Job = require('../models/jobModel');
const userModel = require('../models/userModel');

// Middleware to check if user is authenticated
const isAuthenticated = async (req, res, next) => {

    const { email } = req.body;
    const user = await User.findOne({ email: email });
    if (user) {
      next();
    } else {
      // User is not authenticated, send unauthorized response
      res.status(401).json({ error: 'Unauthorized: email not verified' });
    }
};
// Add a new route to save user details
router.post('/userdetails/', async (req, res) => {
    try {
        const { name, email } = req.body;
        // Assuming you have a UserModel
        const user = new User({
            displayName: name,
            email: email
        });
        await user.save();
        res.status(201).json({ message: 'User details saved successfully' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Bookmark a job
router.post('/bookmarkjob/', isAuthenticated, async (req, res) => {
    try {
        const { email, title, company, experienceRequired, location, applyUrl } = req.body;
        
        // Check if the authenticated user exists in the database
        const user = await User.findOne({ email: email });
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        
        // Create a new job object to be saved
        const newJob = new Job({
            title: title ? title : 'N/A',
            company:  company ? company : 'N/A',
            experienceRequired: experienceRequired ? experienceRequired : 'N/A',
            location: location ? location : 'N/A',
            applyUrl: applyUrl ? applyUrl : 'N/A',
            applired: false,
            interviewing: false,
            negotiating: false, 
            accepted: false
        });

        // Save the job to the database and add it to the user's savedJobs array
        await newJob.save();
        user.savedJobs.push(newJob);
        await user.save();

        res.status(201).json({ message: 'Job bookmarked successfully', user: user });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to fetch all jobs of a user with applied: false, interviewing: false, negotiating: false, accepted: false
router.get('/bookmarkjobs/', isAuthenticated, async (req, res) => {
    try {
        const { email } = req.body;
        const user = await User.findOne({ email: email }).populate('savedJobs');
        const bookmarkedJobs = user.savedJobs.filter(job => !job.applied && !job.interviewing && !job.negotiating && !job.accepted);
        res.status(200).json({ bookmarkedJobs: bookmarkedJobs });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }   
});

// Route to fetch all jobs of a user with applied: true, interviewing: false, negotiating: false, accepted: false
router.get('/appliedjobs/', isAuthenticated, async (req, res) => {
    try {
        const { email } = req.body;
        const user = await User.findOne({ email: email }).populate('savedJobs');
        const appliedJobs = user.savedJobs.filter(job => job.applied && !job.interviewing && !job.negotiating && !job.accepted);
        res.json({ appliedJobs: appliedJobs });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to fetch all jobs of a user with applied: false, interviewing: true, negotiating: false, accepted: false
router.get('/interviewingjobs/', isAuthenticated, async (req, res) => {
    try {
        const { email } = req.body;
        const user = await User.findOne({ email: email }).populate('savedJobs');
        const interviewingJobs = user.savedJobs.filter(job => !job.applied && job.interviewing && !job.negotiating && !job.accepted);
        res.json({ interviewingJobs: interviewingJobs });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to fetch all jobs of a user with applied: false, interviewing: false, negotiating: true, accepted: false
router.get('/negotiatingjobs/', isAuthenticated, async (req, res) => {
    try {
        const { email } = req.body;
        const user = await User.findOne({ email: email }).populate('savedJobs');
        const negotiatingJobs = user.savedJobs.filter(job => !job.applied && !job.interviewing && job.negotiating && !job.accepted);
        res.json({ negotiatingJobs: negotiatingJobs });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to fetch all jobs of a user with applied: false, interviewing: false, negotiating: false, accepted: true
router.get('/acceptedjobs/', isAuthenticated, async (req, res) => {
    try {
        const { email } = req.body;
        const user = await User.findOne({ email: email }).populate('savedJobs');
        const acceptedJobs = user.savedJobs.filter(job => !job.applied && !job.interviewing && !job.negotiating && job.accepted);
        res.json({ acceptedJobs: acceptedJobs });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to update the status of a job for a particular user
router.patch('/updatejobstatus/:jobId', isAuthenticated, async (req, res) => {
    try {
        const { email, inx } = req.body;
        const { jobId } = req.params;

        // Find the user by email
        const user = await User.findOne({ email: email }).populate('savedJobs');
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        // Find the job by jobId
        const job = user.savedJobs.find(job => job._id.toString() === jobId);
        if (!job) {
            return res.status(404).json({ error: 'Job not found' });
        }

        // Update the status of the job based on the provided status
        switch (inx) {
            case '0': // Bookmark job
                job.applied = false;
                job.interviewing = false;
                job.negotiating = false;
                job.accepted = false;
                break;
            case '1': // Mark as applied
                job.applied = true;
                job.interviewing = false;
                job.negotiating = false;    
                job.accepted = false;
                break;
            case '2': // Mark as interviewing
                job.applied = false;
                job.interviewing = true;
                job.negotiating = false;
                job.accepted = false;
                break;
            case '3': // Mark as negotiating
                job.applied = false;
                job.interviewing = false;
                job.negotiating = true;
                job.accepted = false;
                break;
            case '4': // Mark as accepted
                job.applied = false;
                job.interviewing = false;
                job.negotiating = false;
                job.accepted = true;
                break;
            default:
                return res.status(400).json({ error: 'Invalid status' });
        }

        // Save the updated user
        await job.save();

        res.json({ message: 'Job status updated successfully', updatedJob: job });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to delete a job for a particular user by job ID
router.delete('/deletejob/:jobId', isAuthenticated, async (req, res) => {
    try {
        const { email } = req.body;
        const { jobId } = req.params;

        // Find the user by email
        const user = await User.findOne({ email: email }).populate('savedJobs');
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        // Find the index of the job by jobId
        const jobIndex = user.savedJobs.findIndex(job => job._id.toString() === jobId);
        if (jobIndex === -1) {
            return res.status(404).json({ error: 'Job not found' });
        }

        // Remove the job from the user's saved jobs
        user.savedJobs.splice(jobIndex, 1);

        // Save the updated user (without the deleted job)
        await user.save();

        res.json({ message: 'Job deleted successfully' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});


module.exports = router;
