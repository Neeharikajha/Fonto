const express = require('express');
const router = express.Router();
const fontsController = require('../controllers/fontsController');

router.get('/fonts', fontsController.getFonts);
router.post('/describe', fontsController.describeFont);

module.exports = router;
