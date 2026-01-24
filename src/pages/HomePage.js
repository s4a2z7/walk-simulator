import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { petAPI } from '../services/api';
import PetWorld from '../components/PetWorld';
import FoodTray from '../components/FoodTray';
import EvolutionModal from '../components/EvolutionModal';
import RankingModal from '../components/RankingModal';

function HomePage({ setAuth, isDemo }) {
  // 안전한 기본값: mockPet
  const mockPet = {
    name: '불사조',
    current_stage: 1,
    stage_emoji: '🥚',
    stage_name: '알',
    total_exp: 0,
    total_steps: 0,
    age_days: 0,
    hunger_level: 100,
    happiness_level: 100,
  };
  const [pet, setPet] = useState(null);
  const [friends, setFriends] = useState([]); // getFriends 제거, 빈 배열 유지
  const [error, setError] = useState('');
  const [showEvolution, setShowEvolution] = useState(false);
  const [evolutionInfo, setEvolutionInfo] = useState(null);
  const [showRanking, setShowRanking] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    loadPetData();
    // getFriends 제거
    // 5초마다 펫 정보 갱신
    const interval = setInterval(() => {
      loadPetData(true);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadPetData = async (silent = false) => {
    try {

      const petData = await petAPI.getPet();
      setPet(petData.data.pet);
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        handleLogout();
      } else {
        setError('펫 정보를 불러오는 데 실패했습니다.');
      }
    } finally {

    }
  };



  // 커스텀 경험치로 운동(스트레칭)
  const handleStretchCustom = async (exp) => {
    try {
      const stretchData = await petAPI.stretch(exp);
      showNotification(`운동하기 +${exp} EXP!`, 'success');
      setPet(stretchData.data.pet);
    } catch (error) {
      showNotification('운동 실패', 'error');
      console.error(error);
    }
  };

  const handleAddSteps = async () => {
    // 데모용: +100 걸음 추가
    const steps = 100;
    try {
      const addStepsData = await petAPI.addSteps(steps);
      setPet(addStepsData.data.pet);
      // 진화 체크
      if (addStepsData.data.evolved && addStepsData.data.evolution_info) {
        setEvolutionInfo(addStepsData.data.evolution_info);
        setShowEvolution(true);
      }
      // 성공 알림
      showNotification(`+${steps} 걸음! 🎉`, 'success');
    } catch (err) {
      showNotification(err.response?.data?.error || '걸음수 추가 실패', 'error');
    }
  };

  const handleFeedPet = async (foodType) => {

  };

  // 물 마시기 버튼 핸들러
  // handleDrinkWater 제거 (미사용)

  // 스트레칭 버튼 핸들러
  // handleStretch 제거 (미사용)

  // 일찍 자기 버튼 핸들러
  // handleSleepEarly 제거 (미사용)

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setAuth(false);
    navigate('/login');
  };

  const showNotification = (message, type = 'info') => {
    // 간단한 알림 (실제로는 toast 라이브러리 사용 권장)
    const notification = document.createElement('div');
    notification.className = `fixed top-24 left-1/2 transform -translate-x-1/2 z-[9999] px-6 py-3 rounded-2xl font-bold text-white shadow-2xl animate-[slideDown_0.3s_ease-out] ${
      type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    // useEffect 제거됨: React Hook은 함수 컴포넌트 또는 커스텀 Hook에서만 사용 가능
  }

  // 커스텀 경험치로 물 마시기
  const handleDrinkWaterCustom = async (exp) => {
    try {
      // 40ml = 1exp, exp*40 만큼 ml로 환산
      await petAPI.drinkWater(exp * 40);
      showNotification(`물 마시기 +${exp} EXP!`, 'success');
    } catch (error) {
      console.error(error);
      showNotification('물 마시기 실패', 'error');
    }
  };

  // 커스텀 경험치로 일찍 자기
  const handleSleepEarlyCustom = async (exp) => {
    try {
      const sleepEarlyData = await petAPI.sleepEarly(exp);
      showNotification(sleepEarlyData.data.message, 'success');
      await loadPetData();
      if (sleepEarlyData.data.evolution) {
        setEvolutionInfo(sleepEarlyData.data.evolution);
        setShowEvolution(true);
      }
    } catch (err) {
      showNotification(
        err?.response?.data?.error ||
        err?.response?.data?.message ||
        err?.message ||
        '일찍 자기 실패',
        'error'
      );
    }
  };

      if (!pet) {
        return (
          <div className="min-h-screen flex items-center justify-center">
            <div className="text-center">
              <div className="text-8xl mb-6 animate-bounce">🐾</div>
              <p className="text-2xl font-bold text-gray-700">펫 정보를 불러오는 중...</p>
            </div>
          </div>
        );
      }
      return (
        <div className="min-h-screen pb-32">
        pet={pet} 

      <button
        onClick={handleLogout}
        className="fixed top-5 right-5 z-40 px-4 py-2 bg-white rounded-full shadow-lg text-sm font-bold text-gray-700 hover:bg-gray-100 transition"
      >
        로그아웃
      </button>

      {/* 메인 컨텐츠 */}
      <div className="container mx-auto px-4 pt-32">
        <PetWorld 
          pet={pet || mockPet}
          friends={friends}
          onPetClick={handleAddSteps}
        />

        {/* 테스트/습관 버튼 */}
        <div className="text-center mt-8 flex flex-col gap-4">
          <button
            onClick={handleAddSteps}
            className="px-8 py-4 bg-gradient-to-r from-phoenix-red to-phoenix-gold text-white text-xl font-black rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition flex items-center justify-center gap-2"
          >
            <span role="img" aria-label="shoes">👟</span> +100 걸음
          </button>
          <button
            onClick={() => handleDrinkWaterCustom(10)}
            className="px-8 py-4 bg-gradient-to-r from-blue-400 to-blue-600 text-white text-xl font-black rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition flex items-center justify-center gap-2"
          >
            <span role="img" aria-label="water">💧</span> +10 물 마시기
          </button>
          <button
            onClick={() => handleStretchCustom(50)}
            className="px-8 py-4 bg-gradient-to-r from-green-400 to-green-600 text-white text-xl font-black rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition flex items-center justify-center gap-2"
          >
            <span role="img" aria-label="exercise">🏃‍♂️</span> +50 운동하기
          </button>
          <button
            onClick={() => handleSleepEarlyCustom(40)}
            className="px-8 py-4 bg-gradient-to-r from-purple-400 to-purple-600 text-white text-xl font-black rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition flex items-center justify-center gap-2"
          >
            <span role="img" aria-label="sleep">🌙</span> +40 일찍 자기
          </button>
          <p className="text-sm text-gray-600 mt-2">
            * 실제 앱에서는 걸음수 센서, 물 마시기, 운동, 일찍 자기 등 다양한 건강습관이 연동됩니다
          </p>
          {/* 펫 정보 카드 */}
          <div className="mt-8 bg-white rounded-3xl shadow-xl p-6 max-w-md mx-auto">
            <h3 className="text-2xl font-black text-gray-800 mb-4 text-center">
              {(pet || mockPet).name}의 정보
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">현재 단계</span>
                <span className="font-bold text-lg">{(pet || mockPet).stage_emoji} {(pet || mockPet).stage_name}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">총 경험치</span>
                <span className="font-bold">{(pet || mockPet).total_exp?.toLocaleString() || 0} EXP</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">총 걸음수</span>
                <span className="font-bold">{(pet || mockPet).total_steps?.toLocaleString() || 0} 걸음</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">태어난 지</span>
                <span className="font-bold">{(pet || mockPet).age_days || 0}일</span>
              </div>
              {pet.current_stage < 5 && (
                <div className="pt-3 border-t">
                  <div className="text-sm text-gray-600 mb-2">다음 진화까지</div>
                  <div className="font-bold text-phoenix-red">
                    {((pet.exp_to_next_stage - pet.current_exp) * 10).toLocaleString()} 걸음 남음
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>


      {/* 먹이 트레이 + 건강습관 버튼 */}
      <div className="fixed bottom-8 left-1/2 transform -translate-x-1/2 z-50 flex flex-col items-center gap-4">
        <FoodTray 
          pet={pet}
          onFeed={handleFeedPet}
          disabled={false}
        />
        {/* 데모 모드 건강습관 버튼: /demo 경로 또는 isDemo prop이 true일 때만 노출 */}
        {(isDemo || window.location.pathname === '/demo') && (
          <div className="flex gap-3 mt-2">
            <button
              onClick={() => handleDrinkWaterCustom(10)}
              className="px-5 py-3 bg-gradient-to-r from-blue-400 to-blue-600 text-white text-lg font-black rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition flex items-center gap-2"
            >
              💧 +10 물 마시기
            </button>
            <button
              onClick={() => handleStretchCustom(50)}
              className="px-5 py-3 bg-gradient-to-r from-green-400 to-green-600 text-white text-lg font-black rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition flex items-center gap-2"
            >
              🏃‍♂️ +50 운동하기
            </button>
            <button
              onClick={() => handleSleepEarlyCustom(40)}
              className="px-5 py-3 bg-gradient-to-r from-purple-400 to-purple-600 text-white text-lg font-black rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition flex items-center gap-2"
            >
              🌙 +40 일찍 자기
            </button>
          </div>
        )}
      </div>

      {/* 진화 모달 */}
      {showEvolution && (
        <EvolutionModal 
          evolutionInfo={evolutionInfo}
          onClose={() => {
            setShowEvolution(false);
            setEvolutionInfo(null);
          }}
        />
      )}

      {/* 랭킹 모달 */}
      {showRanking && (
        <RankingModal 
          onClose={() => setShowRanking(false)}
          currentUserId={pet.user_id}
        />
      )}

      {/* 애니메이션 스타일 */}
      <style jsx>{`
        @keyframes slideDown {
          from { transform: translate(-50%, -100%); opacity: 0; }
          to { transform: translate(-50%, 0); opacity: 1; }
        }
        
        @keyframes slideUp {
          from { transform: translate(-50%, 0); opacity: 1; }
          to { transform: translate(-50%, -100%); opacity: 0; }
        }
      `}</style>
    </div>
  );
}

export default HomePage;
