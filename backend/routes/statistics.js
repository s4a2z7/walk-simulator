const express = require('express');
const router = express.Router();
const statisticsController = require('../controllers/statisticsController');
const authenticateToken = require('../middleware/auth');

// All statistics routes require authentication
router.use(authenticateToken);

// Statistics endpoints
router.get('/today', statisticsController.getTodayStats);
router.get('/history', statisticsController.getHistory);
router.get('/evolutions', statisticsController.getEvolutionHistory);
router.get('/feedings', statisticsController.getFeedingHistory);

module.exports = router;
