import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import PetWorld from '../components/PetWorld';
import PetCharacter from '../components/PetCharacter';
import TopBar from '../components/TopBar';
import FoodTray from '../components/FoodTray';
import RankingModal from '../components/RankingModal';
import EvolutionModal from '../components/EvolutionModal';
import BGMController from '../components/BGMController';
import { petAPI, rankingAPI } from '../services/api';

const HomePage = () => {
  const navigate = useNavigate();
  const [pet, setPet] = useState(null);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isAnimating, setIsAnimating] = useState(false);

  const [showRankingModal, setShowRankingModal] = useState(false);
  const [showEvolutionModal, setShowEvolutionModal] = useState(false);

  // 펫 정보 로드
  const loadPet = async () => {
    try {
      const response = await petAPI.getPet();
      const petData = response.data.pet;
      setPet({
        id: petData.id,
        name: petData.name,
        stage: petData.current_stage,
        stage_name: petData.stage_name,
        stage_emoji: petData.stage_emoji,
        level: Math.floor(petData.total_exp / 1000) + 1,
        experience: petData.current_exp,
        steps: petData.today_steps,
        hunger: petData.hunger_level,
        happiness: petData.happiness_level,
        total_steps: petData.total_steps,
        total_exp: petData.total_exp,
      });
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        navigate('/login');
      } else {
        setError(err.response?.data?.error || '펫 정보를 로드할 수 없습니다.');
      }
    }
  };

  // 랭킹 로드
  const loadRanking = async () => {
    try {
      const response = await rankingAPI.getRanking(10);
      const rankings = response.data.rankings || [];
      setRankings(rankings.map((rank) => ({
        id: rank.user_id,
        display_name: rank.display_name,
        level: Math.floor(rank.total_exp / 1000) + 1,
        steps: rank.total_steps,
        stage: rank.pet_stage,
      })));
    } catch (err) {
      console.error('랭킹 로드 실패:', err);
    }
  };

  // 초기 로드 및 자동 새로고침
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    loadPet();
    loadRanking();
    setLoading(false);

    const interval = setInterval(() => {
      loadPet();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // 먹이 주기
  const handleFeedClick = async (foodType) => {
    if (!pet) return;

    try {
      const response = await petAPI.feedPet(foodType);
      const petData = response.data.pet;

      setPet(prev => ({
        ...prev,
        hunger: petData.hunger_level,
        happiness: petData.happiness_level,
        steps: petData.today_steps,
      }));
    } catch (err) {
      setError(err.response?.data?.error || '먹이를 줄 수 없습니다.');
      console.error('먹이 주기 실패:', err);
    }
  };

  // 걸음수 추가 (클릭 애니메이션)
  const handlePetClick = async () => {
    if (!pet) return;

    setIsAnimating(true);
    setTimeout(() => setIsAnimating(false), 600);

    try {
      const response = await petAPI.addSteps(10);
      const petData = response.data.pet;
      const evolved = response.data.evolved;

      setPet(prev => ({
        ...prev,
        stage: petData.current_stage,
        stage_name: petData.stage_name,
        level: Math.floor(petData.total_exp / 1000) + 1,
        experience: petData.current_exp,
        steps: petData.today_steps,
        hunger: petData.hunger_level,
        total_steps: petData.total_steps,
        total_exp: petData.total_exp,
      }));

      if (evolved) {
        setShowEvolutionModal(true);
      }
    } catch (err) {
      console.error('걸음수 추가 실패:', err);
    }
  };

  // 로그아웃
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-sky to-grass flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🔥</div>
          <p className="text-2xl font-bold text-gray-800">로딩 중...</p>
        </div>
      </div>
    );
  }

  if (!pet) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-sky to-grass flex items-center justify-center">
        <div className="text-center">
          <p className="text-2xl font-bold text-gray-800 mb-4">펫을 불러올 수 없습니다.</p>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-8 py-3 rounded-xl font-bold"
          >
            로그아웃
          </button>
        </div>
      </div>
    );
  }

  const canAfford = {
    berry: true,
    meat: pet.steps >= 100,
    golden_fruit: pet.steps >= 500
  };

  return (
    <div>
      <PetWorld onPetClick={handlePetClick} onAllergyClinicClick={() => navigate('/allergy')}>
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
        onRankingClick={() => {
          loadRanking();
          setShowRankingModal(true);
        }}
      />

      <FoodTray
        onFeedClick={handleFeedClick}
        canAfford={canAfford}
        isLoading={loading}
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

      {/* 로그아웃 버튼 */}
      <button
        onClick={handleLogout}
        className="fixed top-24 right-6 bg-red-500 text-white px-4 py-2 rounded-xl font-bold hover:bg-red-600 transition-colors z-30"
      >
        로그아웃
      </button>

      {/* 알러지 검사소 버튼 */}
      <button
        onClick={() => navigate('/allergy')}
        className="fixed top-24 right-44 bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-2 rounded-xl font-bold hover:shadow-lg transition-shadow z-30 flex items-center gap-2"
      >
        🏥 알러지 검사소
      </button>

      {/* 에러 메시지 */}
      {error && (
        <div className="fixed bottom-32 left-4 right-4 bg-red-100 border-2 border-red-400 text-red-700 px-4 py-3 rounded-xl">
          {error}
        </div>
      )}
    </div>
  );
};

export default HomePage;
