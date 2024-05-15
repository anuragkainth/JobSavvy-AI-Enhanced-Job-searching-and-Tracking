// models/Job.js
const mongoose = require('mongoose');

const jobSchema = new mongoose.Schema({
    title: {
        type: String,
        required: false
    },
    company: {
        type: String,
        required: false
    },
    location: {
        type: String,
        required: false
    },
    experienceRequired: {
        type: String,
        required: false
    },
    postingDate: {
        type: Date,
        default: Date.now
    },
    applyUrl: {
        type: String,
        required: false
    },
    applied: {
        type: Boolean,
        default: false
    },
    interviewing: {
        type: Boolean,
        default: false
    },
    negotiating: {
        type: Boolean,
        default: false
    },
    accepted: {
        type: Boolean,
        default: false
    }
});

module.exports = mongoose.model('Job', jobSchema);
