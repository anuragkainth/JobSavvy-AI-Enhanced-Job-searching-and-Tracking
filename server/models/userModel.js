// models/User.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    googleId: {
        type: String,
        required: false
    },
    displayName: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true
    },
    photo: {
        type: String,
        required: false
    },
    savedJobs: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Job',
        required: false
    }]
});

module.exports = mongoose.model('User', userSchema);
