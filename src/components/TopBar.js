// 안전 숫자 변환 유틸
const safeNum = (v, fallback = 0) =>
  typeof v === "number"
    ? v
    : typeof v === "string" && !isNaN(Number(v))
      ? Number(v)
      : fallback;
import React from 'react';

function TopBar({ pet, onRankingClick }) {
  if (!pet) return null;

  const expProgress = safeNum(pet.exp_to_next_stage) > 0 
    ? Math.min(100, (safeNum(pet.current_exp) / safeNum(pet.exp_to_next_stage)) * 100)
    : 100;

  const getHungerColor = () => {
    const hunger = safeNum(pet.hunger_level);
    if (hunger >= 70) return 'text-green-600';
    if (hunger >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="fixed top-5 left-1/2 transform -translate-x-1/2 z-50 flex flex-wrap gap-3 justify-center px-4">
      {/* 걸음수 */}
      <div className="bg-white rounded-full px-5 py-3 shadow-lg flex items-center gap-3">
        <span className="text-2xl">👣</span>
        <span className="font-black text-lg text-gray-800">
          {safeNum(pet.today_steps).toLocaleString()}
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
          Lv.{safeNum(pet.current_stage)}
        </span>
      </div>

      {/* 배고픔 */}
      <div className="bg-white rounded-full px-5 py-3 shadow-lg flex items-center gap-3">
        <span className="text-2xl">🍖</span>
        <span className={`font-black text-lg ${getHungerColor()}`}>
          {safeNum(pet.hunger_level)}%
        </span>
      </div>

      {/* 행복도 */}
      <div className="bg-white rounded-full px-5 py-3 shadow-lg flex items-center gap-3">
        <span className="text-2xl">{safeNum(pet.happiness_level) >= 70 ? '😊' : safeNum(pet.happiness_level) >= 40 ? '😐' : '😢'}</span>
        <span className="font-black text-lg text-gray-800">
          {safeNum(pet.happiness_level)}%
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
