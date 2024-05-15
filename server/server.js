
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });
const PORT = process.env.PORT || 4000;
const cors = require("cors");

const crypto = require('crypto');
// Generate a random secret key
const secret = crypto.randomBytes(32).toString('hex');

const express = require('express');
const authRouter = require('./routes/authRoutes');
const userRouter = require('./routes/userRoutes')
const mongoose = require("mongoose");

const app = express();
app.use(express.json());

// const userRoutes = require('./user_routes');
// app.use('/api', userRoutes);


const session = require('express-session');
// Set up session middleware
app.use(session({
  secret: secret,
  resave: false,
  saveUninitialized: true
}));

// Mount authentication routes
app.use(cors());
app.use(express.json());
app.use((req, res, next) => {
  console.log(req.path, req.method);
  next();
});
app.use("/api/auth", authRouter);
app.use("/api/user", userRouter);

// Use authenticated user in your routes
// app.get('/home', (req, res) => {
//   if (req.session.user) {
//     res.send(`Welcome, ${req.session.user.displayName}`);
//   } else {
//     res.send('Please sign in');
//   }
// });

// Other routes and middleware...

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    // listen for requests
    app.listen(PORT, () => {
      console.log("connected to DB & listen for port: ", PORT);
    });
  })
  .catch((error) => {
    console.log(error);
  });
