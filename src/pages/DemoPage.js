import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import PetWorld from '../components/PetWorld';
import PetCharacter from '../components/PetCharacter';
import TopBar from '../components/TopBar';
import FoodTray from '../components/FoodTray';
import RankingModal from '../components/RankingModal';
import EvolutionModal from '../components/EvolutionModal';
import BGMController from '../components/BGMController';
import { petAPI } from '../services/api';

const DemoPage = () => {
  const navigate = useNavigate();
  
  // 데모 펫 데이터
  const [pet, setPet] = useState({
    id: 'demo-pet-001',
    name: '불사조',
    stage: 1,
    stage_name: '신비한 알',
    stage_emoji: '🥚',
    level: 1,
    experience: 0,
    steps: 0,
    hunger: 100,
    happiness: 100,
    total_steps: 0,
    total_exp: 0,
  });

  const [rankings] = useState([
    { id: '1', display_name: '불사조 마스터', level: 5, steps: 50000, stage: 5 },
    { id: '2', display_name: '펫 사랑꾼', level: 4, steps: 35000, stage: 4 },
    { id: '3', display_name: '게임 초보', level: 3, steps: 20000, stage: 3 },
    { id: '4', display_name: '열심히 플레이', level: 2, steps: 10000, stage: 2 },
    { id: '5', display_name: '데모 사용자', level: 1, steps: 500, stage: 1 },
  ]);

  const [isAnimating, setIsAnimating] = useState(false);
  const [showRankingModal, setShowRankingModal] = useState(false);
  const [showEvolutionModal, setShowEvolutionModal] = useState(false);
  const [useBackend, setUseBackend] = useState(false);
  const [loading, setLoading] = useState(true);

  // 백엔드 연결 시도 (마운트 시)
  useEffect(() => {
    const initializeDemo = async () => {
      try {
        // 데모용 토큰 (없으면 로컬 모드)
        const demoToken = localStorage.getItem('token');
        
        if (demoToken) {
          // 토큰이 있으면 실제 펫 데이터 로드
          const response = await petAPI.getPet();
          if (response.data.pet) {
            setPet(prev => ({
              ...prev,
              ...response.data.pet,
              level: Math.floor(response.data.pet.total_exp / 100) + 1,
            }));
            setUseBackend(true);
          }
        }
      } catch (error) {
        console.log('백엔드 연결 실패 - 로컬 모드로 실행:', error);
        setUseBackend(false);
      } finally {
        setLoading(false);
      }
    };

    initializeDemo();
  }, []);

  // 진화 체크
  const checkEvolution = (newExp) => {
    let newStage = pet.stage;
    let newStageName = pet.stage_name;
    let newStageEmoji = pet.stage_emoji;
    let evolved = false;

    const stageThresholds = {
      1: { exp: 0, name: '신비한 알', emoji: '🥚' },
      2: { exp: 100, name: '병아리', emoji: '🐤' },
      3: { exp: 200, name: '어린 새', emoji: '🐦' },
      4: { exp: 300, name: '불꽃 새', emoji: '🔥' },
      5: { exp: 400, name: '황금 불사조', emoji: '✨' },
    };

    Object.entries(stageThresholds).forEach(([stage, { exp, name, emoji }]) => {
      if (newExp >= exp && parseInt(stage) > newStage) {
        newStage = parseInt(stage);
        newStageName = name;
        newStageEmoji = emoji;
        evolved = true;
      }
    });

    return { newStage, newStageName, newStageEmoji, evolved };
  };

  // 걸음수 추가 (클릭)
  const handlePetClick = async () => {
    setIsAnimating(true);
    setTimeout(() => setIsAnimating(false), 600);

    if (useBackend) {
      // 백엔드 사용
      try {
        const response = await petAPI.addSteps(10);
        const petData = response.data.pet;
        const evolved = response.data.evolved;

        setPet(prev => ({
          ...prev,
          stage: petData.current_stage,
          stage_name: petData.stage_name,
          stage_emoji: petData.stage_emoji,
          level: Math.floor(petData.total_exp / 100) + 1,
          experience: petData.total_exp % 100,
          steps: petData.today_steps,
          hunger: petData.hunger_level,
          total_steps: petData.total_steps,
          total_exp: petData.total_exp,
        }));

        if (evolved) {
          setShowEvolutionModal(true);
        }
      } catch (error) {
        console.error('API 호출 실패:', error);
      }
    } else {
      // 로컬 모드
      const newSteps = pet.steps + 10;
      const newTotalSteps = pet.total_steps + 10;
      const newExp = Math.floor(newTotalSteps / 10);
      const newExperience = newExp % 1000;

      const { newStage, newStageName, newStageEmoji, evolved } = checkEvolution(newExp);

      setPet(prev => ({
        ...prev,
        steps: newSteps,
        total_steps: newTotalSteps,
        total_exp: newExp,
        experience: newExperience,
        level: Math.floor(newExp / 100) + 1,
        stage: newStage,
        stage_name: newStageName,
        stage_emoji: newStageEmoji,
        hunger: Math.max(0, prev.hunger - 2),
      }));

      if (evolved) {
        setShowEvolutionModal(true);
      }
    }
  };

  // 100 걸음 추가 (버튼)
  const handleAdd100Steps = async () => {
    console.log('🐾 +100 걸음 버튼 클릭됨. useBackend:', useBackend);
    
    if (useBackend) {
      // 백엔드 사용 - 100 걸음 (10씩 10번)
      try {
        let response;
        for (let i = 0; i < 10; i++) {
          response = await petAPI.addSteps(10);
        }
        
        if (response.data.pet) {
          const petData = response.data.pet;
          console.log('✅ 백엔드 응답:', petData);
          setPet(prev => ({
            ...prev,
            stage: petData.current_stage,
            stage_name: petData.stage_name,
            stage_emoji: petData.stage_emoji,
            level: Math.max(1, Math.floor(petData.total_exp / 1000)),
            experience: petData.total_exp % 1000,
            steps: petData.today_steps,
            hunger: Math.max(0, petData.hunger_level - 2),
            total_steps: petData.total_steps,
            total_exp: petData.total_exp,
          }));
        }
      } catch (error) {
        console.error('❌ API 호출 실패:', error);
      }
    } else {
      // 로컬 모드
      console.log('💾 로컬 모드 사용');
      const newSteps = pet.steps + 100;
      const newTotalSteps = pet.total_steps + 100;
      const newExp = Math.floor(newTotalSteps / 10);
      const newExperience = newExp % 1000;

      const { newStage, newStageName, newStageEmoji, evolved } = checkEvolution(newExp);

      setPet(prev => ({
        ...prev,
        steps: newSteps,
        total_steps: newTotalSteps,
        total_exp: newExp,
        experience: newExperience,
        level: Math.floor(newExp / 100) + 1,
        stage: newStage,
        stage_name: newStageName,
        stage_emoji: newStageEmoji,
        hunger: Math.max(0, prev.hunger - 5),
      }));

      if (evolved) {
        setShowEvolutionModal(true);
      }
    }
  };

  // 먹이 주기
  const handleFeedClick = (foodType) => {
    const foodData = {
      berry: { hunger: 20, happiness: 5, cost: 0 },
      meat: { hunger: 40, happiness: 15, cost: 100 },
      golden_fruit: { hunger: 80, happiness: 50, cost: 500 },
    };

    const food = foodData[foodType] || foodData.berry;

    setPet(prev => ({
      ...prev,
      hunger: Math.min(100, prev.hunger + food.hunger),
      happiness: Math.min(100, prev.happiness + food.happiness),
      steps: Math.max(0, prev.steps - food.cost),
    }));
  };

  // 로그아웃 (로그인 페이지로)
  const handleLogout = () => {
    navigate('/login');
  };

  // eslint-disable-next-line no-unused-vars
  const handleBackToDemo = () => {
    window.location.reload();
  };

  const canAfford = {
    berry: true,
    meat: pet.steps >= 100,
    golden_fruit: pet.steps >= 500,
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-sky to-grass flex items-center justify-center">
        <div className="text-center">
          <p className="text-2xl font-bold text-gray-800">로딩 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <PetWorld onPetClick={handlePetClick}>
        <PetCharacter
          stage={pet.stage || 1}
          stage_name={pet.stage_name || '신비한 알'}
          stage_emoji={pet.stage_emoji || '🥚'}
          name={pet.name}
          isAnimating={isAnimating}
        />
      </PetWorld>

      <TopBar
        todaySteps={pet.steps || 0}
        level={pet.level || 1}
        progress={(pet.experience || 0) % 100}
        hunger={pet.hunger || 50}
        onRankingClick={() => setShowRankingModal(true)}
      />

      <FoodTray
        onFeedClick={handleFeedClick}
        canAfford={canAfford}
        isLoading={false}
      />

      <RankingModal
        show={showRankingModal}
        rankings={rankings}
        onClose={() => setShowRankingModal(false)}
      />

      <EvolutionModal
        show={showEvolutionModal}
        stage={pet.stage}
        petName={pet.name}
        onComplete={() => setShowEvolutionModal(false)}
      />

      {/* BGM 컨트롤러 */}
      <BGMController />

      {/* 데모 정보 배너 */}
      <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-full shadow-lg font-bold text-sm z-50">
        ✨ 데모 버전 (로그인 불필요) ✨
      </div>

      {/* 로그인 페이지로 이동 버튼 */}
      <button
        onClick={handleLogout}
        className="fixed top-24 right-6 bg-blue-500 text-white px-4 py-2 rounded-xl font-bold hover:bg-blue-600 transition-colors z-30"
      >
        🔐 계정 로그인
      </button>

      {/* 데모 정보 - 우상단으로 이동 */}
      <div className="fixed top-44 right-6 bg-white bg-opacity-95 rounded-xl shadow-lg p-4 max-w-xs z-30 text-sm">
        <h3 className="font-bold text-gray-800 mb-3">📋 데모 버전 가이드</h3>
        <ul className="text-gray-700 space-y-2">
          <li>✨ <strong>펫 클릭</strong>: 걸음수 +10 증가</li>
          <li>🍖 <strong>먹이 주기</strong>: 배고픔 회복</li>
          <li>📊 <strong>랭킹</strong>: 전체 플레이어 순위</li>
          <li>⭐ <strong>진화</strong>: 경험치로 5단계 진화</li>
          <li>🔐 <strong>로그인</strong>: 계정으로 게임 시작</li>
        </ul>
      </div>

      {/* 펫 정보 대시보드 */}
      <div className="fixed bottom-20 left-6 bg-white bg-opacity-95 rounded-xl shadow-lg p-4 max-w-xs z-40">
        <h3 className="font-bold text-gray-800 mb-3">🐾 펫 정보</h3>
        <div className="text-sm text-gray-700 space-y-2">
          <p>이름: <span className="font-bold">{pet.name}</span></p>
          <p>단계: <span className="font-bold">{pet.stage_emoji} {pet.stage_name}</span></p>
          <p>레벨: <span className="font-bold">Lv.{pet.level}</span></p>
          <p>총 걸음: <span className="font-bold">{pet.total_steps.toLocaleString()}</span></p>
          <p>경험치: <span className="font-bold">{pet.total_exp}</span></p>
          <p className="text-xs text-purple-600 mt-3">
            {useBackend ? '✅ 백엔드 연결됨 (데이터 저장)' : '💾 로컬 모드 (임시)'}
          </p>
        </div>

        {/* +100 걸음 버튼 */}
        <button
          onClick={handleAdd100Steps}
          type="button"
          className="w-full mt-4 bg-gradient-to-r from-orange-400 to-orange-500 text-white font-bold py-2 px-3 rounded-lg hover:shadow-lg hover:from-orange-500 hover:to-orange-600 transition-all text-sm cursor-pointer z-50"
        >
          👟 +100 걸음
        </button>
      </div>
    </div>
  );
};

export default DemoPage;
