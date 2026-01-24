import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { petAPI, rankingAPI } from '../services/api';
import TopBar from '../components/TopBar';
import PetWorld from '../components/PetWorld';
import FoodTray from '../components/FoodTray';
import EvolutionModal from '../components/EvolutionModal';
import RankingModal from '../components/RankingModal';

function HomePage({ setAuth, isDemo }) {
  const [pet, setPet] = useState(null);
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showEvolution, setShowEvolution] = useState(false);
  const [evolutionInfo, setEvolutionInfo] = useState(null);
  const [showRanking, setShowRanking] = useState(false);
  const [feedingDisabled, setFeedingDisabled] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadPetData();
    loadFriends();
    
    // 5초마다 펫 정보 갱신
    const interval = setInterval(() => {
      loadPetData(true);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const loadPetData = async (silent = false) => {
    try {
      if (!silent) setLoading(true);
      const response = await petAPI.getPet();
      setPet(response.data.pet);
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        handleLogout();

// 커스텀 경험치로 운동(스트레칭)
const handleStretchCustom = async (exp) => {
  try {
    const response = await petAPI.stretch(exp);
    showNotification(`운동하기 +${exp} EXP!`, 'success');
    setPet(response.data.pet);
  } catch (error) {
    showNotification('운동 실패', 'error');
    console.error(error);
  }
};

// 커스텀 경험치로 일찍 자기
const handleSleepEarlyCustom = async (exp) => {
  try {
    const response = await petAPI.sleepEarly(exp);
    showNotification(`일찍 자기 +${exp} EXP!`, 'success');
    setPet(response.data.pet);
  } catch (err) {
    showNotification('오류가 발생했습니다', 'error');
  }
};

  const handleAddSteps = async () => {
    // 데모용: +100 걸음 추가
    const steps = 100;
    try {
      const response = await petAPI.addSteps(steps);
      setPet(response.data.pet);
      // 진화 체크
      if (response.data.evolved && response.data.evolution_info) {
        setEvolutionInfo(response.data.evolution_info);
        setShowEvolution(true);
      }
      // 성공 알림
      showNotification(`+${steps} 걸음! 🎉`, 'success');
    } catch (err) {
      showNotification(err.response?.data?.error || '걸음수 추가 실패', 'error');
    }
  };

  const handleFeedPet = async (foodType) => {
    if (feedingDisabled) return;
  };

  // 물 마시기 버튼 핸들러
  const handleDrinkWater = async () => {
    try {
      const response = await petAPI.drinkWater();
      showNotification(response.data.message, 'success');
      await loadPetData();
      if (response.data.evolution) {
        setEvolutionInfo(response.data.evolution);
        setShowEvolution(true);
      }
    } catch (err) {
      showNotification(err.response?.data?.error || '물 마시기 실패', 'error');
    }
  };

  // 스트레칭 버튼 핸들러
  const handleStretch = async () => {
    try {
      const response = await petAPI.stretch();
      showNotification(response.data.message, 'success');
      await loadPetData();
      if (response.data.evolution) {
        setEvolutionInfo(response.data.evolution);
        setShowEvolution(true);
      }
    } catch (err) {
      showNotification(err.response?.data?.error || '스트레칭 실패', 'error');
    }
  };

  // 일찍 자기 버튼 핸들러
  const handleSleepEarly = async () => {
    try {
      const response = await petAPI.sleepEarly();
      showNotification(response.data.message, 'success');
      await loadPetData();
      if (response.data.evolution) {
        setEvolutionInfo(response.data.evolution);
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

    setTimeout(() => {
      notification.style.animation = 'slideUp 0.3s ease-in';
      setTimeout(() => notification.remove(), 300);
    }, 2000);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-8xl mb-6 animate-bounce">🔥</div>
          <p className="text-2xl font-bold text-gray-700">불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-8xl mb-6">😢</div>
          <p className="text-2xl font-bold text-gray-700 mb-4">{error}</p>
          <button
            onClick={() => loadPetData()}
            className="px-6 py-3 bg-phoenix-red text-white font-bold rounded-xl hover:bg-phoenix-orange transition"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }


  // 커스텀 경험치로 물 마시기
  const handleDrinkWaterCustom = async (exp) => {
    try {
      // 40ml = 1exp, exp*40 만큼 ml로 환산
      const response = await petAPI.drinkWater(exp * 40);
      showNotification(`물 마시기 +${exp} EXP!`, 'success');
    } catch (error) {
      console.error(error);
      showNotification('물 마시기 실패', 'error');
    }
  };


  // 커스텀 경험치로 일찍 자기

  return (
    <div className="min-h-screen pb-32">
      {/* 상단 스탯 바 */}
      <TopBar 
        pet={pet} 
        onRankingClick={() => setShowRanking(true)}
      />

      {/* 로그아웃 버튼 */}
      <button
        onClick={handleLogout}
        className="fixed top-5 right-5 z-40 px-4 py-2 bg-white rounded-full shadow-lg text-sm font-bold text-gray-700 hover:bg-gray-100 transition"
      >
        로그아웃
      </button>

      {/* 메인 컨텐츠 */}
      <div className="container mx-auto px-4 pt-32">
        <PetWorld 
          pet={pet}
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
      }
    } catch (err) {
      showNotification(err.response?.data?.error || '일찍 자기 실패', 'error');
    }
  };

        {/* 펫 정보 카드 */}
        <div className="mt-8 bg-white rounded-3xl shadow-xl p-6 max-w-md mx-auto">
          <h3 className="text-2xl font-black text-gray-800 mb-4 text-center">
            {pet.name}의 정보
          </h3>
          
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">현재 단계</span>
              <span className="font-bold text-lg">{pet.stage_emoji} {pet.stage_name}</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-600">총 경험치</span>
              <span className="font-bold">{pet.total_exp?.toLocaleString() || 0} EXP</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-600">총 걸음수</span>
              <span className="font-bold">{pet.total_steps?.toLocaleString() || 0} 걸음</span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-600">태어난 지</span>
              <span className="font-bold">{pet.age_days || 0}일</span>
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


      {/* 먹이 트레이 + 건강습관 버튼 */}
      <div className="fixed bottom-8 left-1/2 transform -translate-x-1/2 z-50 flex flex-col items-center gap-4">
        <FoodTray 
          pet={pet}
          onFeed={handleFeedPet}
          disabled={feedingDisabled}
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
