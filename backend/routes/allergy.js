const express = require('express');
const router = express.Router();
const allergyController = require('../controllers/allergyController');
const { authenticateToken } = require('../middleware/auth');

// 모든 알러지 라우트는 인증 필요
router.use(authenticateToken);

// 사용자 알러지 정보 설정
router.post('/allergies', allergyController.setUserAllergies);

// 사용자 알러지 정보 조회
router.get('/allergies', allergyController.getUserAllergies);

// 식품 이미지 알러지 검사
router.post('/check', allergyController.checkAllergy);

// 알러지 검사 기록 조회
router.get('/history', allergyController.getAllergyCheckHistory);

module.exports = router;
