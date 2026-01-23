import React, { useState } from 'react';

const STAGE_INFO = {
  1: { emoji: '🥚', color: '#E0E0E0', message: '따뜻한 알이에요 😊' },
  2: { emoji: '🐤', color: '#FFD54F', message: '삐약삐약! 귀여워요 🐤' },
  3: { emoji: '🐦', color: '#FFB74D', message: '날개가 자라나요! 🔥', hasFlames: true },
  4: { emoji: '🔥', color: '#FF6B6B', message: '불꽃이 타올라요! 🔥🔥', hasFlames: true },
  5: { emoji: '✨', color: '#FFD700', message: '전설이 되었어요! 👑✨', isGolden: true }
};

function PetCharacter({ pet, size = 'large', onClick, showEffects = true }) {
  const [animation, setAnimation] = useState('idle');
  const stageInfo = STAGE_INFO[pet.current_stage] || STAGE_INFO[1];
  
  const sizeClasses = {
    small: 'w-16 h-16 text-4xl',
    medium: 'w-24 h-24 text-6xl',
    large: 'w-48 h-48 text-8xl'
  };

  const handleClick = () => {
    setAnimation('happy');
    setTimeout(() => setAnimation('idle'), 600);
    if (onClick) onClick();
  };

  const getAnimationClass = () => {
    if (animation === 'happy') return 'animate-[petJump_0.6s_ease-in-out]';
    return 'animate-[petFloat_3s_ease-in-out_infinite]';
  };

  // 배고픔에 따른 메시지
  const getMessage = () => {
    if (pet.hunger_level < 30) {
      return '배고파요... 🥺';
    } else if (pet.happiness_level < 50) {
      return '심심해요... 😢';
    }
    return stageInfo.message;
  };

  return (
    <div 
      className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 ${onClick ? 'cursor-pointer' : ''}`}
      onClick={handleClick}
    >
      <div className={`relative ${sizeClasses[size]} flex items-center justify-center ${getAnimationClass()}`}>
        {/* 이름표 */}
        {size === 'large' && (
          <div className="absolute -top-10 left-1/2 transform -translate-x-1/2 bg-white px-4 py-1 rounded-full text-sm font-black shadow-lg whitespace-nowrap">
            {pet.name || '불사조'}
          </div>
        )}

        {/* 불꽃 효과 */}
        {showEffects && stageInfo.hasFlames && (
          <div className="absolute w-full h-full">
            <div className="absolute text-3xl animate-[flameRise_1.5s_ease-out_infinite]"
                 style={{ bottom: '20%', left: '25%', animationDelay: '0s' }}>
              🔥
            </div>
            <div className="absolute text-3xl animate-[flameRise_1.5s_ease-out_infinite]"
                 style={{ bottom: '15%', right: '25%', animationDelay: '0.7s' }}>
              🔥
            </div>
          </div>
        )}

        {/* 황금 반짝임 효과 */}
        {showEffects && stageInfo.isGolden && (
          <div className="absolute w-full h-full">
            <div className="absolute text-4xl animate-[sparkleOrbit_3s_linear_infinite]" style={{ animationDelay: '0s' }}>
              ✨
            </div>
            <div className="absolute text-4xl animate-[sparkleOrbit_3s_linear_infinite]" style={{ animationDelay: '1s' }}>
              💫
            </div>
            <div className="absolute text-4xl animate-[sparkleOrbit_3s_linear_infinite]" style={{ animationDelay: '2s' }}>
              ⭐
            </div>
          </div>
        )}

        {/* 펫 이모지 */}
        <div 
          className={stageInfo.isGolden ? 'animate-[goldenGlow_2s_ease-in-out_infinite]' : ''}
          style={{ 
            fontSize: 'inherit',
            filter: 'drop-shadow(0 10px 30px rgba(0,0,0,0.3))'
          }}
        >
          {stageInfo.emoji}
        </div>

        {/* 그림자 */}
        {size === 'large' && (
          <div 
            className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 w-24 h-4 rounded-full"
            style={{ background: 'radial-gradient(ellipse, rgba(0,0,0,0.3), transparent)' }}
          />
        )}

        {/* 메시지 */}
        {size === 'large' && (
          <div className="absolute -bottom-16 left-1/2 transform -translate-x-1/2 bg-yellow-100 border-2 border-yellow-300 px-4 py-2 rounded-2xl text-sm font-bold text-yellow-800 whitespace-nowrap max-w-xs">
            {getMessage()}
          </div>
        )}
      </div>

      {/* 애니메이션 스타일 */}
      <style jsx>{`
        @keyframes petFloat {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
        
        @keyframes petJump {
          0%, 100% { transform: translateY(0) scale(1); }
          50% { transform: translateY(-40px) scale(1.15); }
        }
        
        @keyframes flameRise {
          0% { transform: translateY(0) scale(1); opacity: 1; }
          100% { transform: translateY(-50px) scale(0.5); opacity: 0; }
        }
        
        @keyframes sparkleOrbit {
          0% { transform: rotate(0deg) translateX(80px) rotate(0deg); opacity: 0; }
          20%, 80% { opacity: 1; }
          100% { transform: rotate(360deg) translateX(80px) rotate(-360deg); opacity: 0; }
        }
        
        @keyframes goldenGlow {
          0%, 100% { filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.6)); }
          50% { filter: drop-shadow(0 0 60px rgba(255, 215, 0, 1)); }
        }
      `}</style>
    </div>
  );
}

export default PetCharacter;
