import React, { useEffect } from 'react';

const EvolutionModal = ({ show = false, stage = 1, petName = 'Phoenix', onComplete }) => {
  useEffect(() => {
    if (show) {
      const timer = stage === 5 ? setTimeout(onComplete, 7000) : setTimeout(onComplete, 3000);
      return () => clearTimeout(timer);
    }
  }, [show, stage, onComplete]);

  if (!show) return null;

  const isLegendary = stage === 5;

  // 파티클 생성 함수
  const generateParticles = () => {
    const count = stage === 5 ? 50 : 20;
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 0.5,
      duration: 1 + Math.random() * 0.5
    }));
  };

  const particles = generateParticles();

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* 배경 오버레이 */}
      <div
        className={`absolute inset-0 ${
          isLegendary
            ? 'bg-gradient-to-b from-yellow-300 via-yellow-200 to-orange-300'
            : 'bg-gradient-to-b from-orange-300 via-red-300 to-orange-300'
        } opacity-90`}
      />

      {/* 파티클 효과 */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {particles.map((particle) => (
          <div
            key={particle.id}
            className="absolute animate-flame"
            style={{
              left: `${particle.left}%`,
              top: isLegendary ? '-10px' : '50%',
              animationDelay: `${particle.delay}s`
            }}
          >
            {isLegendary ? '✨' : '🔥'}
          </div>
        ))}
      </div>

      {/* 콘텐츠 */}
      <div className="relative z-10 text-center">
        {/* 왕관 (5단계) */}
        {isLegendary && (
          <div className="text-7xl mb-4 animate-bounce">👑</div>
        )}

        {/* 메시지 */}
        <h1 className="text-5xl font-bold text-white mb-6">
          {isLegendary ? '👑 전설 달성! 👑' : '🎉 진화 성공! 🎉'}
        </h1>

        {/* 캐릭터 진화 표시 */}
        <div className="flex items-center justify-center gap-8 mb-8">
          <div className="text-6xl opacity-75">→</div>
          <div className={`text-8xl ${isLegendary ? 'animate-glow' : ''}`}>
            {isLegendary ? '✨' : ['🥚', '🐤', '🐦', '🔥', '✨'][stage - 1]}
          </div>
        </div>

        <p className="text-2xl text-white font-bold">
          {petName}가 진화했습니다!
        </p>

        {isLegendary && (
          <p className="text-lg text-yellow-100 mt-4">
            황금 불사조로 진화했어요!
          </p>
        )}
      </div>
    </div>
  );
};

export default EvolutionModal;
