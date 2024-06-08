
const express = require('express');
const router = express.Router();
const path = require('path');
const Sensor = require('../models/Sensor'); // Assuming you have a Sensor model

// Serve the sensor values page
router.get('/sensor-values.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../public/sensor-values.html'));
});

// Serve the sensor setup page
router.get('/sensor-setup.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../public/sensor-setup.html'));
});

// Handle sensor setup form submission
router.post('/setup-sensor', async (req, res) => {
    const { sensorName, sensorSSID, sensorPassword } = req.body;

    try {
        let sensor = new Sensor({ name: sensorName, ssid: sensorSSID, password: sensorPassword });
        await sensor.save();
        res.redirect('/sensor-values.html');
    } catch (err) {
        res.status(500).json({ message: 'Server error', error: err.message });
    }
});

module.exports = router;
