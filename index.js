// index.js

const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const logger = require("morgan");
const mongoose = require("mongoose");
const path = require("path"); // Import path module

const app = express();

const port = 3031;
//const ipAddress = '192.168.1.4'
const ipAddress = '192.168.0.26'
const config = require("./config");

const postsRouter = require("./routes/posts");
const authRouter = require('./routes/auth'); // Import the login router
const sensorRouter = require('./routes/sensor'); // Import the sensor router


app.use(logger("dev"));

const dbUrl = config.dbUrl;

var options = {
  connectTimeoutMS: 30000,
};

mongoose.connect(dbUrl, options);

app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Use the auth router for login and sign-in
app.use('/', authRouter);


app.use("/posts", postsRouter);

// Use the sensor router for sensor-related routes
app.use('/', sensorRouter);

app.listen(port, ipAddress, function () {
  console.log('Running on ' + ipAddress + ':' + port);
});
module.exports = app;