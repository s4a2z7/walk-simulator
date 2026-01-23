import React, { useState } from 'react';

const DemoPage = () => {
  const [gameStarted, setGameStarted] = useState(false);

  return (
    <div style={{ width: '100%', height: '100vh', overflow: 'hidden' }}>
      {!gameStarted ? (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'linear-gradient(135deg, #7ED321, #5FB304)',
            zIndex: 1000,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontFamily: 'Arial, sans-serif'
          }}
        >
          <h1 style={{ fontSize: '4rem', marginBottom: '20px' }}>🔥 PHOENIX FARM</h1>
          <p style={{ fontSize: '20px', marginBottom: '30px' }}>
            알을 모아 레벨업하는 불사조 농장 데모
          </p>
          <button
            onClick={() => setGameStarted(true)}
            style={{
              padding: '20px 60px',
              fontSize: '24px',
              fontWeight: '900',
              color: '#5FB304',
              background: 'white',
              border: 'none',
              borderRadius: '50px',
              cursor: 'pointer',
              boxShadow: '0 8px 0 #4a8a03',
              transition: 'all 0.1s'
            }}
            onMouseDown={(e) => (e.target.style.transform = 'translateY(4px)')}
            onMouseUp={(e) => (e.target.style.transform = 'translateY(0)')}
          >
            게임 시작!
          </button>
        </div>
      ) : (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'linear-gradient(to bottom, #87CEEB 0%, #87CEEB 30%, #E0F6FF 60%, #90EE90 100%)',
          zIndex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontFamily: 'Arial, sans-serif'
        }}>
          <div style={{
            textAlign: 'center',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            padding: '40px',
            borderRadius: '20px'
          }}>
            <h2>🎮 3D 게임 로딩 중...</h2>
            <p>W/A/S/D로 조종하세요!</p>
            <div style={{ marginTop: '20px', fontSize: '60px' }}>
              🔥
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DemoPage;
