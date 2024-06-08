
const express = require('express');
const router = express.Router();
const User = require('../models/User');
const path = require('path');

// Serve the authentication page
router.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public/auth.html'));
});

// Sign-In Route
router.post('/signin', async (req, res) => {
    const { username, password } = req.body;

    try {
        let user = await User.findOne({ username });

        if (user) {
            return res.status(400).json({ message: 'User already exists' });
        }

        user = new User({ username, password });
        await user.save();
        res.status(200).json({ message: 'User created successfully', user });
    } catch (err) {
        res.status(500).json({ message: 'Server error', error: err.message });
    }
});

// Login Route
router.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        let user = await User.findOne({ username });

        if (!user || user.password !== password) {
            return res.status(400).json({ message: 'Invalid username or password' });
        }

        // Redirect to main.html upon successful login
        res.redirect('/sensor-setup.html');
    } catch (err) {
        res.status(500).json({ message: 'Server error', error: err.message });
    }
});

module.exports = router;
