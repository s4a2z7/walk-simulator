const express = require('express');
const router = express.Router();
const rankingController = require('../controllers/rankingController');
const { authenticateToken } = require('../middleware/auth');

// All ranking routes require authentication
router.use(authenticateToken);

// Rankings and leaderboards
router.get('/', rankingController.getRanking);
router.get('/leaderboard', rankingController.getLeaderboard);

// Friends management
router.get('/friends', rankingController.getFriends);
router.post('/friends', rankingController.addFriend);
router.delete('/friends/:friendshipId', rankingController.removeFriend);

module.exports = router;
