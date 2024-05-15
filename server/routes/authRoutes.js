// routes/auth.js
const express = require('express');
const router = express.Router();
const firebase = require('firebase-admin');
const User = require('../models/userModel');

// Initialize Firebase Admin SDK
const serviceAccount = require('../jobsavvyai-firebase.json');
firebase.initializeApp({
    credential: firebase.credential.cert(serviceAccount)
});

// Google Authentication
router.post('/google', async (req, res) => {
    const { tokenId } = req.body;
    try {
      const decodedToken = await firebase.auth().verifyIdToken(tokenId);
      const { uid, name, email, picture } = decodedToken;
      let user = await User.findOne({ googleId: uid });
  
      if (!user) {
        // If user does not exist, create a new user in the database
        user = await User.create({
          googleId: uid,
          displayName: name,
          email,
          photo: picture
        });
      }
  
      // Set user session (you may customize session data)
      req.session.user = {
        _id: user._id,
        googleId: uid,
        displayName: name,
        email,
        photo: picture
      };
  
      res.json(user);
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });
  

module.exports = router;
