import React from 'react';

function TopBar({ pet, onRankingClick }) {
  if (!pet) return null;

  const expProgress = pet.exp_to_next_stage > 0 
    ? Math.min(100, (pet.current_exp / pet.exp_to_next_stage) * 100)
    : 100;

  const getHungerColor = () => {
    if (pet.hunger_level >= 70) return 'text-green-600';
    if (pet.hunger_level >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="fixed top-5 left-1/2 transform -translate-x-1/2 z-50 flex flex-wrap gap-3 justify-center px-4">
      {/* 걸음수 */}
      <div className="bg-white rounded-full px-5 py-3 shadow-lg flex items-center gap-3">
        <span className="text-2xl">👣</span>
        <span className="font-black text-lg text-gray-800">
          {pet.today_steps?.toLocaleString() || 0}
        </span>
      </div>

      {/* 경험치 */}
      <div className="bg-white rounded-full px-5 py-3 shadow-lg flex items-center gap-3 min-w-[200px]">
        <span className="text-2xl">🔥</span>
        <div className="flex-1">
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-phoenix-red to-phoenix-gold transition-all duration-500"
              style={{ width: `${expProgress}%` }}
            />
          </div>
        </div>
        <span className="font-black text-sm text-phoenix-red">
          Lv.{pet.current_stage}
        </span>
      </div>

      {/* 배고픔 */}
      <div className="bg-white rounded-full px-5 py-3 shadow-lg flex items-center gap-3">
        <span className="text-2xl">🍖</span>
        <span className={`font-black text-lg ${getHungerColor()}`}>
          {pet.hunger_level}%
        </span>
      </div>

      {/* 행복도 */}
      <div className="bg-white rounded-full px-5 py-3 shadow-lg flex items-center gap-3">
        <span className="text-2xl">{pet.happiness_level >= 70 ? '😊' : pet.happiness_level >= 40 ? '😐' : '😢'}</span>
        <span className="font-black text-lg text-gray-800">
          {pet.happiness_level}%
        </span>
      </div>

      {/* 랭킹 버튼 */}
      <button
        onClick={onRankingClick}
        className="w-14 h-14 bg-white rounded-full shadow-lg flex items-center justify-center text-2xl hover:scale-110 transform transition-transform"
      >
        🏆
      </button>
    </div>
  );
}

export default TopBar;
