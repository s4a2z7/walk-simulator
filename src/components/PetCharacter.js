import React from 'react';

const PetCharacter = ({ stage = 1, stage_name = '신비한 알', stage_emoji = '🥚', name = 'Phoenix', isAnimating = false }) => {
  
  const handlePetClick = () => {
    // Will be handled by parent component
  };

  const hasFlames = stage >= 3;
  const hasWings = stage >= 4;
  const hasGoldenAura = stage === 5;

  // 단계별 텍스트 설명 (3D 대체)
  const stage3DDescription = {
    1: '🥚 신비한 알',
    2: '🐤 노란 병아리',
    3: '🐦 주황색 새',
    4: '🔥 불꽃 불사조',
    5: '✨ 황금 불사조'
  };

  return (
    <div className="flex flex-col items-center gap-4">
      {/* 그림자 */}
      <div className="w-48 h-12 bg-black/20 rounded-full blur-md"></div>

      {/* 펫 컨테이너 - 향상된 2D 버전 */}
      <div
        className={`relative w-80 h-80 flex items-center justify-center rounded-2xl bg-gradient-to-b from-sky-100 to-sky-50 shadow-lg ${isAnimating ? 'animate-jump' : 'animate-float'}`}
        onClick={handlePetClick}
      >
        {/* 배경 요소들 */}
        <div className="absolute top-10 left-10 text-6xl opacity-50 animate-pulse">☁️</div>
        <div className="absolute top-20 right-10 text-5xl opacity-60 animate-float">☁️</div>

        {/* 황금 오라 (5단계) */}
        {hasGoldenAura && (
          <div className="absolute inset-0 rounded-2xl bg-yellow-200 opacity-20 blur-xl animate-pulse"></div>
        )}

        {/* 불꽃 효과 (3단계+) */}
        {hasFlames && (
          <>
            <div className="absolute text-4xl animate-flame" style={{ left: '15%', top: '25%', animationDelay: '0s' }}>
              🔥
            </div>
            <div className="absolute text-4xl animate-flame" style={{ right: '15%', top: '30%', animationDelay: '0.2s' }}>
              🔥
            </div>
            <div className="absolute text-3xl animate-flame" style={{ left: '20%', bottom: '30%', animationDelay: '0.4s' }}>
              🔥
            </div>
            <div className="absolute text-3xl animate-flame" style={{ right: '20%', bottom: '35%', animationDelay: '0.6s' }}>
              🔥
            </div>
          </>
        )}

        {/* 날개 (4단계+) */}
        {hasWings && (
          <>
            <div className="absolute text-5xl animate-bounce" style={{ left: '-20px', top: '50%', transform: 'translateY(-50%)', animationDelay: '0s' }}>
              🪶
            </div>
            <div className="absolute text-5xl animate-bounce" style={{ right: '-20px', top: '50%', transform: 'translateY(-50%)', animationDelay: '0.1s' }}>
              🪶
            </div>
          </>
        )}

        {/* 메인 캐릭터 - 큰 이모지 */}
        <div className="text-9xl hover:scale-110 transition-transform duration-200 cursor-pointer drop-shadow-lg">
          {stage_emoji}
        </div>

        {/* 왕관 (5단계) */}
        {hasGoldenAura && (
          <div className="absolute top-5 text-6xl animate-bounce" style={{ animationDelay: '0.2s' }}>
            👑
          </div>
        )}
      </div>

      {/* 단계 설명 */}
      <div className="text-center font-semibold text-lg text-gray-700">
        {stage3DDescription[stage]}
      </div>

      {/* 이름과 메시지 */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-800">{name}</h2>
        <p className="text-gray-600 text-sm">{stage_name}</p>
        <p className="text-lg mt-2">행복해요! 💫</p>
      </div>

      {/* 친구 펫들 */}
      <div className="flex gap-8 mt-8 justify-center">
        <div className="text-center">
          <div className="text-5xl">🐕</div>
          <p className="text-xs text-gray-600 mt-1">친구 1</p>
        </div>
        <div className="text-center">
          <div className="text-5xl">🐱</div>
          <p className="text-xs text-gray-600 mt-1">친구 2</p>
        </div>
        <div className="text-center">
          <div className="text-5xl">🦊</div>
          <p className="text-xs text-gray-600 mt-1">친구 3</p>
        </div>
      </div>
    </div>
  );
};

export default PetCharacter;
