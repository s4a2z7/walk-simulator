const { pool } = require('../config/database');
const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// 사용자 알러지 정보 등록/업데이트
exports.setUserAllergies = async (req, res) => {
  try {
    const { userId } = req.user;
    const { allergies } = req.body;

    if (!Array.isArray(allergies)) {
      return res.status(400).json({ error: '알러지는 배열이어야 합니다.' });
    }

    // 기존 알러지 정보 삭제
    await pool.query('DELETE FROM user_allergies WHERE user_id = $1', [userId]);

    // 새로운 알러지 정보 삽입
    if (allergies.length > 0) {
      const values = allergies.map((allergy) => [userId, allergy.trim()]);
      const query = 'INSERT INTO user_allergies (user_id, allergy_name) VALUES ($1, $2)';
      
      for (const value of values) {
        await pool.query(query, value);
      }
    }

    res.json({ 
      success: true, 
      message: '알러지 정보가 저장되었습니다.',
      allergies: allergies
    });
  } catch (error) {
    console.error('setUserAllergies error:', error);
    res.status(500).json({ error: '알러지 정보 저장 실패' });
  }
};

// 사용자 알러지 정보 조회
exports.getUserAllergies = async (req, res) => {
  try {
    const { userId } = req.user;

    const result = await pool.query(
      'SELECT allergy_name FROM user_allergies WHERE user_id = $1 ORDER BY created_at',
      [userId]
    );

    const allergies = result.rows.map(row => row.allergy_name);

    res.json({
      success: true,
      allergies: allergies
    });
  } catch (error) {
    console.error('getUserAllergies error:', error);
    res.status(500).json({ error: '알러지 정보 조회 실패' });
  }
};

// 알러지 검사 - 이미지 분석
exports.checkAllergy = async (req, res) => {
  try {
    const { userId } = req.user;
    const { imageBase64, ocrText } = req.body;

    if (!imageBase64 || !ocrText) {
      return res.status(400).json({ error: '이미지와 OCR 텍스트가 필요합니다.' });
    }

    // 사용자 알러지 정보 조회
    const allergyResult = await pool.query(
      'SELECT allergy_name FROM user_allergies WHERE user_id = $1',
      [userId]
    );

    const allergies = allergyResult.rows.map(row => row.allergy_name);

    if (allergies.length === 0) {
      return res.status(400).json({ error: '먼저 알러지 정보를 등록해주세요.' });
    }

    // OpenAI Vision API를 사용한 분석
    const prompt = buildAllergyPrompt(allergies);

    const response = await openai.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: prompt + '\n\n===== 제품 정보 =====\n' + ocrText
            },
            {
              type: 'image',
              source: {
                type: 'base64',
                media_type: 'image/jpeg',
                data: imageBase64.replace(/^data:image\/\w+;base64,/, '')
              }
            }
          ]
        }
      ]
    });

    const analysisText = response.content[0].text;

    // 분석 결과 파싱
    const verdict = extractVerdict(analysisText);
    const coreMessage = extractCoreMessage(analysisText);
    const detectedIngredients = extractIngredients(analysisText);
    const judgmentReason = extractReason(analysisText);

    // 검사 기록 저장
    const recordResult = await pool.query(
      `INSERT INTO allergy_check_records 
       (user_id, image_url, ocr_text, verdict, core_message, detected_ingredients, judgment_reason) 
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       RETURNING id, verdict, core_message, detected_ingredients, judgment_reason, checked_at`,
      [userId, null, ocrText, verdict, coreMessage, detectedIngredients, judgmentReason]
    );

    const record = recordResult.rows[0];

    res.json({
      success: true,
      analysis: {
        verdict: record.verdict,
        coreMessage: record.core_message,
        detailedAnalysis: {
          detectedIngredients: record.detected_ingredients,
          judgmentReason: record.judgment_reason
        },
        checkedAt: record.checked_at,
        rawAnalysis: analysisText
      }
    });
  } catch (error) {
    console.error('checkAllergy error:', error);
    res.status(500).json({ error: '알러지 검사 실패: ' + error.message });
  }
};

// 알러지 검사 기록 조회
exports.getAllergyCheckHistory = async (req, res) => {
  try {
    const { userId } = req.user;
    const { limit = 10 } = req.query;

    const result = await pool.query(
      `SELECT id, verdict, core_message, detected_ingredients, judgment_reason, checked_at
       FROM allergy_check_records 
       WHERE user_id = $1 
       ORDER BY checked_at DESC 
       LIMIT $2`,
      [userId, limit]
    );

    res.json({
      success: true,
      history: result.rows
    });
  } catch (error) {
    console.error('getAllergyCheckHistory error:', error);
    res.status(500).json({ error: '검사 기록 조회 실패' });
  }
};

// Helper function: 프롬프트 생성
function buildAllergyPrompt(allergies) {
  return `당신은 CareLog라는 개인화 식품 알러지 안전 AI입니다.

사용자의 알러지:
${allergies.join(', ')}

아래의 식품 정보를 분석하고 다음 형식으로만 응답하세요:

[판단 결과]: 🚨 위험 / ⚠️ 주의 / ✅ 안전
[핵심 메시지]: (한 문장으로 판단 결과를 설명)
[상세 분석]:
- 검출된 성분: (발견된 알러지 성분)
- 판단 근거: (판단의 이유)

분석할 때 다음을 확인하세요:
1. 원재료명에서 사용자 알러지 성분 직접 노출 여부
2. 해당 성분을 포함한 복합 재료 (예: 땅콩 → 땅콩기름, 피넛, 땅콩함유)
3. 혼입 가능성 문구 (예: "메밀, 밀, 땅콩 등을 사용한 제품과 같은 시설에서 제조")
4. 일반적으로 위험해 보이는 요소가 있으면 '주의' 권고
5. OCR 텍스트가 뭉개져서 확인 불가능한 성분이 있으면 "식별 불가능한 성분이 있어 주의가 필요합니다" 안내`;
}

// Helper function: 판단 결과 추출
function extractVerdict(text) {
  if (text.includes('🚨 위험')) return '위험';
  if (text.includes('⚠️ 주의')) return '주의';
  if (text.includes('✅ 안전')) return '안전';
  return '판단불가';
}

// Helper function: 핵심 메시지 추출
function extractCoreMessage(text) {
  const match = text.match(/\[핵심 메시지\]:\s*(.+?)(?:\n|$)/);
  return match ? match[1].trim() : '';
}

// Helper function: 성분 추출
function extractIngredients(text) {
  const match = text.match(/검출된 성분:\s*(.+?)(?:\n|$)/);
  if (match) {
    const ingredients = match[1].trim();
    return ingredients.split(/,|\//).map(ing => ing.trim()).filter(ing => ing);
  }
  return [];
}

// Helper function: 판단 근거 추출
function extractReason(text) {
  const match = text.match(/판단 근거:\s*(.+?)(?:\n\[|$)/);
  return match ? match[1].trim() : '';
}
