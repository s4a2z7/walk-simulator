import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const DemoAllergyPage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('register');
  const [selectedAllergies, setSelectedAllergies] = useState([]);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [ocrText, setOcrText] = useState('');
  const [checkResult, setCheckResult] = useState(null);
  const [isChecking, setIsChecking] = useState(false);
  const [history, setHistory] = useState([]);

  const allergyList = [
    '우유', '계란', '생선', '갑각류', '조개류', '땅콩',
    '견과류', '밀', '콩', '참깨', '메타황산염', '겨자',
    '셀러리', '루핀', '몰루스크', '기타'
  ];

  const handleAllergyToggle = (allergy) => {
    setSelectedAllergies(prev =>
      prev.includes(allergy)
        ? prev.filter(a => a !== allergy)
        : [...prev, allergy]
    );
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setUploadedImage(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCheckAllergy = async () => {
    if (!uploadedImage && !ocrText) {
      alert('이미지를 업로드하거나 텍스트를 입력해주세요.');
      return;
    }

    setIsChecking(true);

    // 데모 응답 시뮬레이션
    setTimeout(() => {
      const mockResult = {
        verdict: '⚠️',
        coreMessage: '주의가 필요합니다.',
        detectedIngredients: ['달걀', '우유', '밀'],
        reason: '업로드된 제품에 알레르기 유발 성분이 포함되어 있을 수 있습니다.'
      };

      setCheckResult(mockResult);
      setHistory(prev => [
        {
          id: Date.now(),
          image: uploadedImage,
          text: ocrText,
          ...mockResult,
          timestamp: new Date().toLocaleString('ko-KR')
        },
        ...prev
      ]);

      setIsChecking(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-sky to-grass p-4">
      {/* 헤더 */}
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate('/demo')}
          className="bg-white text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          ← 돌아가기
        </button>
        <h1 className="text-3xl font-bold text-white">🏥 알러지 검사소</h1>
      </div>

      {/* 탭 */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab('register')}
          className={`px-6 py-3 rounded-lg font-bold transition-all ${
            activeTab === 'register'
              ? 'bg-purple-500 text-white'
              : 'bg-white text-gray-800 hover:bg-gray-100'
          }`}
        >
          🔍 알러지 등록
        </button>
        <button
          onClick={() => setActiveTab('check')}
          className={`px-6 py-3 rounded-lg font-bold transition-all ${
            activeTab === 'check'
              ? 'bg-purple-500 text-white'
              : 'bg-white text-gray-800 hover:bg-gray-100'
          }`}
        >
          📸 검사하기
        </button>
        <button
          onClick={() => setActiveTab('history')}
          className={`px-6 py-3 rounded-lg font-bold transition-all ${
            activeTab === 'history'
              ? 'bg-purple-500 text-white'
              : 'bg-white text-gray-800 hover:bg-gray-100'
          }`}
        >
          📋 검사 기록
        </button>
      </div>

      {/* 탭 콘텐츠 */}
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
        {/* 알러지 등록 탭 */}
        {activeTab === 'register' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">내 알러지 정보 등록</h2>
            <div className="grid grid-cols-2 gap-4">
              {allergyList.map(allergy => (
                <label
                  key={allergy}
                  className="flex items-center gap-3 p-3 border-2 rounded-lg cursor-pointer hover:bg-purple-50 transition-colors"
                >
                  <input
                    type="checkbox"
                    checked={selectedAllergies.includes(allergy)}
                    onChange={() => handleAllergyToggle(allergy)}
                    className="w-5 h-5 cursor-pointer"
                  />
                  <span className="text-gray-800">{allergy}</span>
                </label>
              ))}
            </div>
            <button
              onClick={() => {
                if (selectedAllergies.length > 0) {
                  alert(`✅ ${selectedAllergies.join(', ')}이(가) 등록되었습니다!`);
                } else {
                  alert('등록할 알러지를 선택해주세요.');
                }
              }}
              className="w-full mt-6 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-3 rounded-lg hover:shadow-lg transition-all"
            >
              저장하기
            </button>
          </div>
        )}

        {/* 검사하기 탭 */}
        {activeTab === 'check' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">음식 안전성 검사</h2>

            {/* 이미지 업로드 */}
            <div className="mb-6">
              <label className="block text-gray-800 font-bold mb-3">이미지 업로드</label>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="w-full p-3 border-2 border-dashed border-purple-300 rounded-lg"
              />
              {uploadedImage && (
                <img
                  src={uploadedImage}
                  alt="uploaded"
                  className="mt-4 max-h-32 rounded-lg"
                />
              )}
            </div>

            {/* OCR 텍스트 */}
            <div className="mb-6">
              <label className="block text-gray-800 font-bold mb-3">성분 정보 (OCR 또는 직접 입력)</label>
              <textarea
                value={ocrText}
                onChange={(e) => setOcrText(e.target.value)}
                placeholder="음식 포장지의 성분을 입력하세요..."
                className="w-full p-3 border-2 border-gray-300 rounded-lg h-24 focus:outline-none focus:border-purple-500"
              />
            </div>

            {/* 검사 결과 */}
            {checkResult && (
              <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                <div className="text-4xl mb-3">{checkResult.verdict}</div>
                <p className="text-lg font-bold text-gray-800 mb-2">{checkResult.coreMessage}</p>
                {checkResult.detectedIngredients.length > 0 && (
                  <p className="text-gray-700 mb-2">
                    <strong>감지된 성분:</strong> {checkResult.detectedIngredients.join(', ')}
                  </p>
                )}
                <p className="text-gray-700">
                  <strong>판정 사유:</strong> {checkResult.reason}
                </p>
              </div>
            )}

            <button
              onClick={handleCheckAllergy}
              disabled={isChecking}
              className="w-full bg-gradient-to-r from-orange-400 to-orange-500 text-white font-bold py-3 rounded-lg hover:shadow-lg transition-all disabled:opacity-50"
            >
              {isChecking ? '검사 중...' : '🔍 검사하기'}
            </button>
          </div>
        )}

        {/* 검사 기록 탭 */}
        {activeTab === 'history' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">검사 기록</h2>
            {history.length === 0 ? (
              <p className="text-gray-500 text-center py-8">아직 검사 기록이 없습니다.</p>
            ) : (
              <div className="space-y-4">
                {history.map(record => (
                  <div key={record.id} className="p-4 border-2 border-gray-200 rounded-lg">
                    <div className="flex justify-between items-start mb-3">
                      <div className="text-4xl">{record.verdict}</div>
                      <span className="text-xs text-gray-500">{record.timestamp}</span>
                    </div>
                    <p className="font-bold text-gray-800 mb-2">{record.coreMessage}</p>
                    {record.image && (
                      <img
                        src={record.image}
                        alt="history"
                        className="max-h-24 rounded mb-2"
                      />
                    )}
                    {record.detectedIngredients.length > 0 && (
                      <p className="text-sm text-gray-700 mb-1">
                        성분: {record.detectedIngredients.join(', ')}
                      </p>
                    )}
                    <p className="text-sm text-gray-600">{record.reason}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default DemoAllergyPage;
