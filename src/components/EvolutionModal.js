import React, { useEffect } from 'react';

function EvolutionModal({ evolutionInfo, onClose }) {
  useEffect(() => {
    if (evolutionInfo) {
      const duration = evolutionInfo.to_stage === 5 ? 5000 : 3000;
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [evolutionInfo, onClose]);

  if (!evolutionInfo) return null;

  const isGolden = evolutionInfo.to_stage === 5;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center animate-[evolutionBurst_0.6s_ease-out]"
         style={{
           background: isGolden 
             ? 'linear-gradient(135deg, #FFD700, #FFA500, #FF6B6B)'
             : 'linear-gradient(135deg, #FF6B6B, #FFD700)'
         }}>
      
      {/* 배경 광선 */}
      <div className="absolute w-full h-full overflow-hidden">
        {[...Array(isGolden ? 16 : 12)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-full left-1/2 top-1/2 origin-center animate-[rayExpand_2s_ease-out_infinite]"
            style={{
              background: 'linear-gradient(to bottom, transparent, white, transparent)',
              transform: `rotate(${i * (360 / (isGolden ? 16 : 12))}deg)`,
              animationDelay: `${i * 0.1}s`,
              opacity: 0.3
            }}
          />
        ))}
      </div>

      {/* 진화 내용 */}
      <div className="relative text-center text-white z-10">
        {/* 이전 캐릭터 */}
        <div className="mb-8 animate-[fadeOut_0.8s_ease-out_forwards]">
          <div className="text-8xl mb-4">{evolutionInfo.from_emoji}</div>
          <div className="text-2xl font-black text-shadow">
            {evolutionInfo.from_name}
          </div>
        </div>

        {/* 화살표 */}
        <div className="text-6xl mb-8 animate-pulse">
          ✨ → ✨
        </div>

        {/* 새 캐릭터 */}
        <div className="mb-8 animate-[evolveAppear_1s_ease-out_0.5s_both]">
          <div className="text-9xl mb-4 animate-[spin_2s_ease-in-out]">
            {evolutionInfo.to_emoji}
          </div>
          <div className="text-3xl font-black text-shadow">
            {evolutionInfo.to_name}
          </div>
        </div>

        {/* 축하 메시지 */}
        <div className="animate-[bounceIn_1s_ease-out_1s_both]">
          <h1 className="text-5xl font-black mb-4" style={{ textShadow: '4px 4px 8px rgba(0,0,0,0.3)' }}>
            {isGolden ? '👑 전설 달성! 👑' : '🎉 진화 성공! 🎉'}
          </h1>
          <p className="text-2xl font-bold">
            {evolutionInfo.celebration_message}
          </p>
        </div>

        {/* 왕관 하강 (황금 불사조) */}
        {isGolden && (
          <div className="absolute -top-20 left-1/2 transform -translate-x-1/2 text-8xl animate-[crownDescend_2s_ease-out_1.5s_both]">
            👑
          </div>
        )}
      </div>

      {/* 폭죽 효과 */}
      <div className="absolute w-full h-full pointer-events-none">
        {[...Array(isGolden ? 30 : 20)].map((_, i) => (
          <div
            key={i}
            className="absolute left-1/2 top-1/2 text-4xl animate-[fireworkBurst_1.5s_ease-out_forwards]"
            style={{
              animationDelay: `${1 + i * 0.05}s`,
              transform: `rotate(${i * (360 / (isGolden ? 30 : 20))}deg)`
            }}
          >
            {isGolden ? '✨' : '🔥'}
          </div>
        ))}
      </div>

      {/* 애니메이션 스타일 */}
      <style jsx>{`
        @keyframes evolutionBurst {
          0% { opacity: 0; transform: scale(0); }
          100% { opacity: 1; transform: scale(1); }
        }
        
        @keyframes rayExpand {
          0%, 100% { opacity: 0.2; }
          50% { opacity: 0.6; }
        }
        
        @keyframes fadeOut {
          0% { opacity: 1; transform: scale(1); }
          100% { opacity: 0; transform: scale(0.8); }
        }
        
        @keyframes evolveAppear {
          0% { 
            opacity: 0; 
            transform: scale(0) rotate(-180deg); 
          }
          60% { 
            transform: scale(1.3) rotate(10deg); 
          }
          100% { 
            opacity: 1; 
            transform: scale(1) rotate(0deg); 
          }
        }
        
        @keyframes bounceIn {
          0% { 
            opacity: 0; 
            transform: translateY(50px); 
          }
          60% { 
            transform: translateY(-10px); 
          }
          100% { 
            opacity: 1; 
            transform: translateY(0); 
          }
        }
        
        @keyframes crownDescend {
          0% { 
            opacity: 0; 
            transform: translate(-50%, -200px) rotate(0deg); 
          }
          100% { 
            opacity: 1; 
            transform: translate(-50%, 0) rotate(360deg); 
          }
        }
        
        @keyframes fireworkBurst {
          0% { 
            opacity: 0; 
            transform: rotate(var(--angle, 0deg)) translateY(0) scale(0); 
          }
          50% { 
            opacity: 1; 
          }
          100% { 
            opacity: 0; 
            transform: rotate(var(--angle, 0deg)) translateY(-300px) scale(1); 
          }
        }
        
        .text-shadow {
          text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
        }
      `}</style>
    </div>
  );
}

export default EvolutionModal;
