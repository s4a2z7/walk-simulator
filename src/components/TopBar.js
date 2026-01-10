import React from 'react';

const TopBar = ({ todaySteps = 8500, level = 5, progress = 65, hunger = 85, onRankingClick }) => {
  return (
    <div className="fixed top-0 left-0 right-0 z-40 flex justify-center pt-5 px-4">
      <div className="bg-white rounded-full shadow-xl px-8 py-4 flex items-center gap-4 max-w-2xl">
        
        {/* 걸음수 */}
        <div className="flex items-center gap-2 px-4 py-2 bg-sky/10 rounded-full">
          <span className="text-2xl">👣</span>
          <span className="font-bold text-gray-800">{todaySteps.toLocaleString()}</span>
        </div>

        {/* 경험치 바 */}
        <div className="flex items-center gap-3 px-4 py-2 bg-gradient-to-r from-red-100 to-orange-100 rounded-full">
          <span className="text-2xl">🔥</span>
          <div className="flex flex-col gap-1">
            <div className="w-32 h-3 bg-gray-300 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-orange-400 to-red-500 transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="text-xs font-bold text-gray-700">Lv. {level}</span>
          </div>
        </div>

        {/* 배고픔 */}
        <div className="flex items-center gap-2 px-4 py-2 bg-amber-100 rounded-full">
          <span className="text-2xl">🍖</span>
          <span className="font-bold text-gray-800">{hunger}%</span>
        </div>

        {/* 랭킹 버튼 */}
        <button
          onClick={onRankingClick}
          className="text-3xl hover:scale-110 transition-transform duration-200 bg-gradient-to-b from-yellow-300 to-yellow-400 rounded-full p-3 shadow-lg hover:shadow-2xl"
        >
          🏆
        </button>
      </div>
    </div>
  );
};

export default TopBar;
