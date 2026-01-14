const express = require('express');
const router = express.Router();
const petController = require('../controllers/petController');
const { authenticateToken } = require('../middleware/auth');

// All pet routes require authentication
router.use(authenticateToken);

// Pet management
router.get('/', petController.getPet);
router.post('/steps', petController.addSteps);
router.post('/feed', petController.feedPet);
router.patch('/name', petController.updatePetName);
router.get('/status', petController.getPetStatus);

module.exports = router;
