import React from 'react';

const PetCharacter = ({ stage = 1, stage_name = '신비한 알', stage_emoji = '🥚', name = 'Phoenix', isAnimating = false }) => {
  
  const handlePetClick = () => {
    // Will be handled by parent component
  };

  const hasFlames = stage >= 3;
  const hasWings = stage >= 4;
  const hasGoldenAura = stage === 5;

  return (
    <div className="flex flex-col items-center gap-4">
      {/* 그림자 */}
      <div className="w-48 h-12 bg-black/20 rounded-full blur-md"></div>

      {/* 펫 컨테이너 */}
      <div
        className={`relative ${isAnimating ? 'animate-jump' : 'animate-float'}`}
        onClick={handlePetClick}
      >
        {/* 황금 오라 (5단계) */}
        {hasGoldenAura && (
          <div className="absolute inset-0 animate-glow rounded-full w-64 h-64 -z-10 left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"></div>
        )}

        {/* 불꽃 파티클 (3단계+) */}
        {hasFlames && (
          <>
            <div className="absolute text-2xl animate-flame" style={{ left: '20%', top: '30%', animationDelay: '0s' }}>
              🔥
            </div>
            <div className="absolute text-2xl animate-flame" style={{ right: '20%', top: '25%', animationDelay: '0.3s' }}>
              🔥
            </div>
            <div className="absolute text-2xl animate-flame" style={{ left: '15%', top: '50%', animationDelay: '0.6s' }}>
              🔥
            </div>
          </>
        )}

        {/* 날개 (4단계+) */}
        {hasWings && (
          <>
            <div className="absolute text-3xl animate-pulse" style={{ left: '-30px', top: '50%', transform: 'translateY(-50%)' }}>
              🪶
            </div>
            <div className="absolute text-3xl animate-pulse" style={{ right: '-30px', top: '50%', transform: 'translateY(-50%)' }}>
              🪶
            </div>
          </>
        )}

        {/* 메인 캐릭터 */}
        <div className="text-9xl text-center cursor-pointer hover:scale-110 transition-transform duration-200">
          {stage_emoji}
        </div>
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
