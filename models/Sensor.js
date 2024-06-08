
const mongoose = require('mongoose');

const SensorSchema = new mongoose.Schema({
    name: { type: String, required: true },
    ssid: { type: String, required: true },
    password: { type: String, required: true },
});

module.exports = mongoose.model('Sensor', SensorSchema);
