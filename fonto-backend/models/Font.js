const mongoose = require('mongoose');

const fontSchema = new mongoose.Schema({
  name: String,
  category: String,
  description: String,
  style: String,
});

const Font = mongoose.model('Font', fontSchema);

module.exports = Font;
