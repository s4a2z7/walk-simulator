import React, { useState, useEffect } from 'react';
import { allergyAPI } from '../services/api';

const AllergyCheckPage = () => {
  const [selectedAllergies, setSelectedAllergies] = useState([]);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [ocrText, setOcrText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('setup'); // setup, analysis, history
  const [checkHistory, setCheckHistory] = useState([]);

  const allergyOptions = [
    '계란', '우유', '땅콩', '새우', '게', '밀', '메밀', '대두', '견과류', '아황산염',
    '호두', '아몬드', '캐슈넛', '피스타치오', '조개', '굴', '오징어', '복숭아', '키위'
  ];

  // 사용자 알러지 정보 로드
  useEffect(() => {
    loadUserAllergies();
  }, []);

  const loadUserAllergies = async () => {
    try {
      const response = await allergyAPI.getAllergies();
      setSelectedAllergies(response.data.allergies || []);
    } catch (error) {
      console.error('Failed to load allergies:', error);
    }
  };

  const loadCheckHistory = async () => {
    try {
      const response = await allergyAPI.getCheckHistory(20);
      setCheckHistory(response.data.history || []);
    } catch (error) {
      console.error('Failed to load check history:', error);
    }
  };

  const handleAllergyToggle = (allergy) => {
    setSelectedAllergies(prev => {
      if (prev.includes(allergy)) {
        return prev.filter(a => a !== allergy);
      } else {
        return [...prev, allergy];
      }
    });
  };

  const saveAllergies = async () => {
    try {
      setError('');
      await allergyAPI.setAllergies(selectedAllergies);
      alert('알러지 정보가 저장되었습니다!');
    } catch (error) {
      setError(error.response?.data?.error || '알러지 정보 저장 실패');
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUploadedImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyze = async () => {
    if (!uploadedImage) {
      setError('이미지를 선택해주세요.');
      return;
    }

    if (!ocrText.trim()) {
      setError('제품 정보(텍스트)를 입력해주세요.');
      return;
    }

    if (selectedAllergies.length === 0) {
      setError('먼저 알러지 정보를 등록해주세요.');
      return;
    }

    try {
      setError('');
      setIsAnalyzing(true);
      const imageBase64 = uploadedImage.replace(/^data:image\/\w+;base64,/, '');
      
      const response = await allergyAPI.checkAllergy(imageBase64, ocrText);
      setAnalysisResult(response.data.analysis);
      setUploadedImage(null);
      setOcrText('');
    } catch (error) {
      setError(error.response?.data?.error || '알러지 검사 실패');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getVerdictColor = (verdict) => {
    switch (verdict) {
      case '위험': return 'text-red-600 bg-red-50 border-red-200';
      case '주의': return 'text-amber-600 bg-amber-50 border-amber-200';
      case '안전': return 'text-green-600 bg-green-50 border-green-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getVerdictEmoji = (verdict) => {
    switch (verdict) {
      case '위험': return '🚨';
      case '주의': return '⚠️';
      case '안전': return '✅';
      default: return '❓';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-sky-100 to-sky-200 py-8">
      <div className="max-w-2xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-sky-900 mb-2">🏥 알러지 측정 검사소</h1>
          <p className="text-sky-700">개인화된 식품 안전 검사 서비스</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => { setActiveTab('setup'); loadUserAllergies(); }}
            className={`flex-1 py-2 px-4 rounded-lg font-medium transition ${
              activeTab === 'setup'
                ? 'bg-blue-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            🔍 알러지 등록
          </button>
          <button
            onClick={() => setActiveTab('analysis')}
            className={`flex-1 py-2 px-4 rounded-lg font-medium transition ${
              activeTab === 'analysis'
                ? 'bg-blue-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            📸 검사하기
          </button>
          <button
            onClick={() => { setActiveTab('history'); loadCheckHistory(); }}
            className={`flex-1 py-2 px-4 rounded-lg font-medium transition ${
              activeTab === 'history'
                ? 'bg-blue-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            📋 검사 기록
          </button>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Setup Tab */}
          {activeTab === 'setup' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6">본인의 알러지를 선택하세요</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-8">
                {allergyOptions.map(allergy => (
                  <button
                    key={allergy}
                    onClick={() => handleAllergyToggle(allergy)}
                    className={`p-3 rounded-lg font-medium transition border-2 ${
                      selectedAllergies.includes(allergy)
                        ? 'bg-blue-500 text-white border-blue-500'
                        : 'bg-gray-100 text-gray-700 border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    {allergy}
                  </button>
                ))}
              </div>

              <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-900 font-medium">
                  선택된 알러지: {selectedAllergies.length > 0 ? selectedAllergies.join(', ') : '없음'}
                </p>
              </div>

              <button
                onClick={saveAllergies}
                disabled={selectedAllergies.length === 0}
                className="w-full py-3 px-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-bold rounded-lg hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                💾 알러지 정보 저장
              </button>
            </div>
          )}

          {/* Analysis Tab */}
          {activeTab === 'analysis' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6">식품 알러지 검사</h2>

              {selectedAllergies.length === 0 && (
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg mb-6">
                  <p className="text-yellow-900">⚠️ 먼저 알러지 정보를 등록해주세요.</p>
                </div>
              )}

              {/* Image Upload */}
              <div className="mb-6">
                <label className="block text-lg font-semibold text-gray-800 mb-2">
                  📸 식품 영양정보 이미지
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition cursor-pointer">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                    id="image-upload"
                  />
                  <label htmlFor="image-upload" className="cursor-pointer block">
                    {uploadedImage ? (
                      <div>
                        <img 
                          src={uploadedImage} 
                          alt="uploaded" 
                          className="w-32 h-32 object-cover mx-auto mb-2 rounded"
                        />
                        <p className="text-blue-600 font-medium">이미지가 선택되었습니다.</p>
                        <p className="text-sm text-gray-500">다른 이미지를 선택하려면 클릭하세요.</p>
                      </div>
                    ) : (
                      <div>
                        <p className="text-4xl mb-2">📷</p>
                        <p className="text-gray-700 font-medium">이미지를 클릭하여 업로드</p>
                        <p className="text-sm text-gray-500">JPG, PNG 형식 지원</p>
                      </div>
                    )}
                  </label>
                </div>
              </div>

              {/* OCR Text Input */}
              <div className="mb-6">
                <label className="block text-lg font-semibold text-gray-800 mb-2">
                  📝 제품 정보 (원재료명, 주의사항 등)
                </label>
                <textarea
                  value={ocrText}
                  onChange={(e) => setOcrText(e.target.value)}
                  placeholder="제품의 원재료명, 주의사항, 혼입 가능성 등의 텍스트를 입력하세요.&#10;&#10;예: 원재료명: 밀, 계란, 우유, 호두, 아몬드&#10;주의: 견과류를 사용한 시설에서 제조됨"
                  className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none text-gray-700 placeholder-gray-400"
                  rows={6}
                />
              </div>

              {/* Selected Allergies Display */}
              <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-900 font-medium">
                  🔍 검사 대상 알러지: {selectedAllergies.join(', ')}
                </p>
              </div>

              {/* Analyze Button */}
              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing || !uploadedImage || !ocrText.trim() || selectedAllergies.length === 0}
                className="w-full py-3 px-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white font-bold rounded-lg hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {isAnalyzing ? '🤔 AI 분석 중...' : '🔬 알러지 위험 분석'}
              </button>

              {/* Analysis Result */}
              {analysisResult && (
                <div className="mt-8">
                  <h3 className="text-2xl font-bold text-gray-800 mb-4">분석 결과</h3>
                  
                  {/* Verdict */}
                  <div className={`p-6 rounded-lg border-2 mb-6 ${getVerdictColor(analysisResult.verdict)}`}>
                    <p className="text-4xl font-bold mb-2">
                      {getVerdictEmoji(analysisResult.verdict)} {analysisResult.verdict}
                    </p>
                    <p className="text-lg font-semibold">{analysisResult.coreMessage}</p>
                  </div>

                  {/* Detailed Analysis */}
                  <div className="bg-gray-50 rounded-lg p-6">
                    <h4 className="text-lg font-semibold text-gray-800 mb-4">📊 상세 분석</h4>
                    
                    <div className="mb-4">
                      <p className="font-semibold text-gray-700 mb-2">검출된 성분:</p>
                      {analysisResult.detailedAnalysis.detectedIngredients?.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                          {analysisResult.detailedAnalysis.detectedIngredients.map((ingredient, idx) => (
                            <span key={idx} className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium">
                              {ingredient}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <p className="text-gray-600">검출된 알러지 성분 없음</p>
                      )}
                    </div>

                    <div>
                      <p className="font-semibold text-gray-700 mb-2">판단 근거:</p>
                      <p className="text-gray-700 leading-relaxed">
                        {analysisResult.detailedAnalysis.judgmentReason}
                      </p>
                    </div>
                  </div>

                  {/* Checked At */}
                  <div className="mt-4 text-right">
                    <p className="text-sm text-gray-500">
                      검사일시: {new Date(analysisResult.checkedAt).toLocaleString('ko-KR')}
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* History Tab */}
          {activeTab === 'history' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6">검사 기록</h2>

              {checkHistory.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-4xl mb-4">📋</p>
                  <p className="text-gray-600">아직 검사 기록이 없습니다.</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {checkHistory.map((record) => (
                    <div key={record.id} className={`p-4 rounded-lg border-2 ${getVerdictColor(record.verdict)}`}>
                      <div className="flex justify-between items-start mb-2">
                        <p className="text-lg font-bold">
                          {getVerdictEmoji(record.verdict)} {record.verdict}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(record.checked_at).toLocaleString('ko-KR')}
                        </p>
                      </div>
                      <p className="font-medium mb-2">{record.core_message}</p>
                      {record.detected_ingredients?.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {record.detected_ingredients.map((ingredient, idx) => (
                            <span key={idx} className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-medium">
                              {ingredient}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AllergyCheckPage;
