import React from 'react';

const RankingModal = ({ show = false, rankings = [], onClose }) => {
  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full max-h-96 overflow-y-auto">
        {/* 헤더 */}
        <div className="bg-gradient-to-r from-orange-400 to-red-500 text-white p-6 rounded-t-3xl">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">🏆 랭킹</h2>
            <button
              onClick={onClose}
              className="text-2xl hover:scale-110 transition-transform"
            >
              ✕
            </button>
          </div>
        </div>

        {/* 랭킹 리스트 */}
        <div className="p-6 space-y-3">
          {rankings.length === 0 ? (
            <p className="text-center text-gray-500 py-8">랭킹 정보를 로드할 수 없습니다.</p>
          ) : (
            rankings.map((rank, index) => (
              <div
                key={rank.id}
                className={`flex items-center gap-4 p-4 rounded-2xl ${
                  index === 0
                    ? 'bg-gradient-to-r from-yellow-200 to-amber-200 border-2 border-yellow-400'
                    : index === 1
                    ? 'bg-gradient-to-r from-gray-200 to-gray-100 border-2 border-gray-400'
                    : index === 2
                    ? 'bg-gradient-to-r from-orange-200 to-amber-100 border-2 border-orange-400'
                    : 'bg-gray-100 border-2 border-gray-300'
                }`}
              >
                {/* 순위 */}
                <div className="text-2xl font-bold w-8 text-center">
                  {index === 0 && '🥇'}
                  {index === 1 && '🥈'}
                  {index === 2 && '🥉'}
                  {index > 2 && `${index + 1}`}
                </div>

                {/* 정보 */}
                <div className="flex-1">
                  <div className="font-bold text-gray-800">{rank.display_name}</div>
                  <div className="text-sm text-gray-600">Lv. {rank.level}</div>
                </div>

                {/* 걸음수 */}
                <div className="text-right">
                  <div className="font-bold text-gray-800">👣 {rank.steps.toLocaleString()}</div>
                  <div className="text-xs text-gray-600">{rank.stage}단계</div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* 닫기 버튼 */}
        <div className="p-4 border-t border-gray-200">
          <button
            onClick={onClose}
            className="w-full bg-gradient-to-r from-orange-400 to-red-500 text-white font-bold py-3 rounded-xl hover:shadow-lg transition-all"
          >
            닫기
          </button>
        </div>
      </div>
    </div>
  );
};

export default RankingModal;
