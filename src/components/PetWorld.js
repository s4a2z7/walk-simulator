import React from 'react';

const Cloud = ({ delay = 0 }) => (
  <div
    className="absolute text-4xl animate-cloud"
    style={{ animationDelay: `${delay}s`, top: '10%' }}
  >
    ☁️
  </div>
);

const Tree = ({ position = 'left' }) => (
  <div
    className={`absolute text-6xl opacity-75 ${
      position === 'left' ? 'left-10' : 'right-10'
    }`}
    style={{ top: '30%' }}
  >
    🌳
  </div>
);

const PetWorld = ({ children, onPetClick }) => {
  const handlePetAreaClick = (e) => {
    onPetClick(e);
  };

  return (
    <div
      className="relative w-full h-screen bg-gradient-to-b from-sky via-sky to-grass overflow-hidden"
      onClick={handlePetAreaClick}
    >
      {/* 구름들 */}
      <Cloud delay={0} />
      <Cloud delay={5} />
      <Cloud delay={10} />

      {/* 나무들 */}
      <Tree position="left" />
      <Tree position="right" />

      {/* 메인 콘텐츠 */}
      <div className="absolute inset-0 flex items-center justify-center pt-20 pb-32">
        {children}
      </div>

      {/* 그라데이션 바닥 */}
      <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-grass-dark to-transparent"></div>
    </div>
  );
};

export default PetWorld;
