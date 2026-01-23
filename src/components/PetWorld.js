import React from 'react';
import PetCharacter from './PetCharacter';

function PetWorld({ pet, friends, onPetClick }) {
  return (
    <div className="relative w-full max-w-4xl h-[500px] mx-auto rounded-3xl overflow-hidden shadow-2xl">
      {/* 구름 */}
      <div className="absolute w-full h-full pointer-events-none">
        <div className="absolute text-6xl opacity-70 animate-[cloudFloat_20s_linear_infinite]" 
             style={{ top: '10%', left: '-10%', animationDelay: '0s' }}>
          ☁️
        </div>
        <div className="absolute text-6xl opacity-70 animate-[cloudFloat_20s_linear_infinite]" 
             style={{ top: '15%', left: '-15%', animationDelay: '7s' }}>
          ☁️
        </div>
        <div className="absolute text-6xl opacity-70 animate-[cloudFloat_20s_linear_infinite]" 
             style={{ top: '8%', left: '-20%', animationDelay: '14s' }}>
          ☁️
        </div>
      </div>

      {/* 나무 */}
      <div className="absolute text-7xl animate-[treeWave_3s_ease-in-out_infinite]"
           style={{ left: '10%', bottom: '15%', filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))' }}>
        🌳
      </div>
      <div className="absolute text-7xl animate-[treeWave_3s_ease-in-out_infinite]"
           style={{ right: '12%', bottom: '18%', filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))' }}>
        🌳
      </div>

      {/* 꽃들 */}
      <div className="absolute text-4xl" style={{ left: '20%', bottom: '10%' }}>🌸</div>
      <div className="absolute text-4xl" style={{ right: '25%', bottom: '12%' }}>🌼</div>
      <div className="absolute text-4xl" style={{ left: '65%', bottom: '8%' }}>🌺</div>

      {/* 메인 펫 */}
      {pet && (
        <PetCharacter 
          pet={pet}
          size="large"
          onClick={onPetClick}
          showEffects={true}
        />
      )}

      {/* 친구 펫들 */}
      <div className="absolute bottom-8 left-0 right-0 flex justify-center gap-8 pointer-events-none">
        {friends && friends.slice(0, 3).map((friend, index) => (
          <div 
            key={friend.user_id || index}
            className="flex flex-col items-center animate-bounce-slow pointer-events-auto cursor-pointer hover:scale-110 transition-transform"
            style={{ animationDelay: `${index * 0.2}s` }}
          >
            <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center text-4xl shadow-lg">
              {friend.pet_emoji || '🐦'}
            </div>
            <div className="mt-2 text-xs font-black text-white bg-black bg-opacity-50 px-3 py-1 rounded-full">
              {friend.display_name || friend.username}
            </div>
          </div>
        ))}
      </div>

      {/* CSS 애니메이션 스타일 */}
      <style jsx>{`
        @keyframes cloudFloat {
          0% { transform: translateX(0); }
          100% { transform: translateX(120vw); }
        }
        
        @keyframes treeWave {
          0%, 100% { transform: rotate(-2deg); }
          50% { transform: rotate(2deg); }
        }
      `}</style>
    </div>
  );
}

export default PetWorld;
