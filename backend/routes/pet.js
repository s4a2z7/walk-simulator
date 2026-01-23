// 건강습관: 스트레칭, 일찍 자기
router.post('/stretch', petController.stretch);
router.post('/sleep-early', petController.sleepEarly);
const express = require('express');
const router = express.Router();
const petController = require('../controllers/petController');
const authenticateToken = require('../middleware/auth');

// All pet routes require authentication
router.use(authenticateToken);

// Pet management
router.get('/', petController.getPet);
router.post('/steps', petController.addSteps);
router.post('/feed', petController.feedPet);

// 건강습관: 물 마시기
router.post('/drink-water', petController.drinkWater);

router.patch('/name', petController.updatePetName);
router.get('/status', petController.getPetStatus);

module.exports = router;
