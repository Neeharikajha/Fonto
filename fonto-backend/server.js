const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// MongoDB connection
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("Connected to MongoDB"))
  .catch(err => console.log(err));

// Basic API routes
app.get('/fonts', (req, res) => {
  // Your logic to fetch fonts from MongoDB
});

app.post('/describe', (req, res) => {
  // Your NLP model logic for font description
});

app.listen(process.env.PORT || 5000, () => {
  console.log('Server is running...');
});
