import React from 'react';

const AllergyClinicHouse = ({ onClick, position = 'right' }) => {
  return (
    <div
      onClick={(e) => {
        e.stopPropagation();
        onClick();
      }}
      className={`absolute cursor-pointer transition-transform hover:scale-110 ${
        position === 'right' ? 'right-20' : 'left-20'
      }`}
      style={{ bottom: '80px' }}
    >
      {/* 건물 */}
      <div className="relative w-24 h-32">
        {/* 지붕 */}
        <div className="absolute top-0 left-0 right-0 h-8 bg-red-600 clip-path-triangle" style={{
          clipPath: 'polygon(0 100%, 50% 0, 100% 100%)'
        }}>
        </div>

        {/* 십자가 */}
        <div className="absolute top-1 left-1/2 transform -translate-x-1/2 text-2xl animate-pulse">
          ⊕
        </div>

        {/* 벽 */}
        <div className="absolute top-8 left-0 right-0 bottom-0 bg-white border-4 border-gray-400 rounded-lg">
          {/* 문 */}
          <div className="absolute left-1/4 bottom-0 w-8 h-16 bg-blue-900 rounded-t-lg flex items-end justify-center pb-1 border-2 border-yellow-600">
            🔑
          </div>

          {/* 창문 1 */}
          <div className="absolute top-4 left-2 w-6 h-6 bg-blue-300 border-2 border-gray-600 rounded flex items-center justify-center text-sm">
            🔍
          </div>

          {/* 창문 2 */}
          <div className="absolute top-4 right-2 w-6 h-6 bg-blue-300 border-2 border-gray-600 rounded flex items-center justify-center text-sm">
            ⚕️
          </div>

          {/* 간판 */}
          <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-yellow-300 px-4 py-1 rounded-full font-bold text-xs text-red-700 border-2 border-red-700 whitespace-nowrap">
            🏥 검사소
          </div>
        </div>
      </div>

      {/* 설명 텍스트 */}
      <p className="text-xs font-bold text-center mt-2 text-gray-800">알러지 검사</p>
    </div>
  );
};

export default AllergyClinicHouse;
