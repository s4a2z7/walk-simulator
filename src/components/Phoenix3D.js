import React, { useRef, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, Cylinder, Cone } from '@react-three/drei';

// 3D 불사조 메인 컴포넌트
const Phoenix = ({ stage = 1, isAnimating = false }) => {
  const groupRef = useRef();
  const wingLeftRef = useRef();
  const wingRightRef = useRef();
  const headRef = useRef();

  useFrame(({ clock }) => {
    if (!groupRef.current) return;

    const time = clock.getElapsedTime();

    // 떠다니는 애니메이션
    if (!isAnimating) {
      groupRef.current.position.y = Math.sin(time * 1.5) * 0.3;
      groupRef.current.rotation.z = Math.cos(time * 1.5) * 0.1;
    } else {
      // 점프 애니메이션
      const jumpY = Math.abs(Math.sin(time * 8)) * 0.8;
      groupRef.current.position.y = jumpY;
    }

    // 날개 움직임 (4단계 이상)
    if (wingLeftRef.current && stage >= 4) {
      wingLeftRef.current.rotation.z = Math.sin(time * 4) * 0.5;
      wingLeftRef.current.position.y = Math.cos(time * 4) * 0.1;
    }

    if (wingRightRef.current && stage >= 4) {
      wingRightRef.current.rotation.z = -Math.sin(time * 4) * 0.5;
      wingRightRef.current.position.y = Math.cos(time * 4) * 0.1;
    }

    // 머리 회전
    if (headRef.current) {
      headRef.current.rotation.y = Math.sin(time * 2) * 0.2;
    }
  });

  // 단계별 색상
  const getBodyColor = () => {
    if (stage === 1) return '#808080'; // 회색 (알)
    if (stage === 2) return '#FFD700'; // 노란색 (병아리)
    if (stage === 3) return '#FF8C00'; // 주황색 (새)
    if (stage === 4) return '#FF4500'; // 빨간색 (불사조)
    if (stage === 5) return '#FFD700'; // 금색 (황금 불사조)
  };

  const getEmissive = () => {
    if (stage === 5) return '#FFD700'; // 황금 발광
    if (stage === 4) return '#FF6347'; // 불꽃 발광
    return '#000000';
  };

  return (
    <group ref={groupRef}>
      {/* 몸체 */}
      <Sphere args={[0.6, 32, 32]} position={[0, 0, 0]}>
        <meshStandardMaterial
          color={getBodyColor()}
          emissive={getEmissive()}
          emissiveIntensity={stage >= 4 ? 0.5 : 0}
          roughness={stage === 5 ? 0.2 : 0.7}
          metalness={stage === 5 ? 0.8 : 0}
        />
      </Sphere>

      {/* 머리 */}
      <Sphere args={[0.4, 32, 32]} position={[0, 0.7, 0.3]} ref={headRef}>
        <meshStandardMaterial
          color={getBodyColor()}
          emissive={getEmissive()}
          emissiveIntensity={stage >= 4 ? 0.5 : 0}
        />
      </Sphere>

      {/* 눈 */}
      <Sphere args={[0.1, 32, 32]} position={[-0.12, 0.85, 0.6]}>
        <meshStandardMaterial color="#000000" />
      </Sphere>
      <Sphere args={[0.1, 32, 32]} position={[0.12, 0.85, 0.6]}>
        <meshStandardMaterial color="#000000" />
      </Sphere>

      {/* 부리 */}
      <Cone args={[0.15, 0.4, 16]} position={[0, 0.6, 0.7]} rotation={[Math.PI / 2, 0, 0]}>
        <meshStandardMaterial color="#FFA500" />
      </Cone>

      {/* 다리 */}
      <Cylinder args={[0.08, 0.08, 0.4, 16]} position={[-0.2, -0.65, 0]}>
        <meshStandardMaterial color="#8B4513" />
      </Cylinder>
      <Cylinder args={[0.08, 0.08, 0.4, 16]} position={[0.2, -0.65, 0]}>
        <meshStandardMaterial color="#8B4513" />
      </Cylinder>

      {/* 꼬리 */}
      <Sphere args={[0.25, 32, 32]} position={[0, 0.2, -0.8]}>
        <meshStandardMaterial
          color={getBodyColor()}
          emissive={getEmissive()}
          emissiveIntensity={stage >= 4 ? 0.5 : 0}
        />
      </Sphere>

      {/* 날개 (4단계 이상) */}
      {stage >= 4 && (
        <>
          {/* 왼쪽 날개 */}
          <group ref={wingLeftRef} position={[-0.7, 0.2, 0]}>
            <Sphere args={[0.2, 32, 32]} position={[-0.3, 0, 0]}>
              <meshStandardMaterial
                color="#FF4500"
                emissive="#FF6347"
                emissiveIntensity={0.6}
              />
            </Sphere>
            <Sphere args={[0.15, 32, 32]} position={[-0.65, 0.15, 0.1]}>
              <meshStandardMaterial
                color="#FF4500"
                emissive="#FF6347"
                emissiveIntensity={0.6}
              />
            </Sphere>
          </group>

          {/* 오른쪽 날개 */}
          <group ref={wingRightRef} position={[0.7, 0.2, 0]}>
            <Sphere args={[0.2, 32, 32]} position={[0.3, 0, 0]}>
              <meshStandardMaterial
                color="#FF4500"
                emissive="#FF6347"
                emissiveIntensity={0.6}
              />
            </Sphere>
            <Sphere args={[0.15, 32, 32]} position={[0.65, 0.15, 0.1]}>
              <meshStandardMaterial
                color="#FF4500"
                emissive="#FF6347"
                emissiveIntensity={0.6}
              />
            </Sphere>
          </group>
        </>
      )}

      {/* 황금 왕관 (5단계) */}
      {stage === 5 && (
        <group position={[0, 1.4, 0.3]}>
          <Cylinder args={[0.5, 0.5, 0.1, 32]}>
            <meshStandardMaterial
              color="#FFD700"
              emissive="#FFD700"
              emissiveIntensity={1}
              metalness={1}
              roughness={0}
            />
          </Cylinder>
          <Cone args={[0.15, 0.3, 16]} position={[-0.3, 0.15, 0]}>
            <meshStandardMaterial
              color="#FFD700"
              emissive="#FFD700"
              emissiveIntensity={1}
            />
          </Cone>
          <Cone args={[0.15, 0.3, 16]} position={[0.3, 0.15, 0]}>
            <meshStandardMaterial
              color="#FFD700"
              emissive="#FFD700"
              emissiveIntensity={1}
            />
          </Cone>
        </group>
      )}
    </group>
  );
};

// 3D 캔버스 래퍼
const Phoenix3D = ({ stage = 1, isAnimating = false }) => {
  return (
    <div style={{ width: '400px', height: '400px' }}>
      <Suspense fallback={<div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>로딩 중...</div>}>
        <Canvas
          camera={{ position: [0, 0, 3], fov: 50 }}
          style={{ width: '100%', height: '100%' }}
          dpr={[1, 2]}
        >
          <ambientLight intensity={0.6} />
          <pointLight position={[10, 10, 10]} intensity={1} />
          <pointLight position={[-10, -10, 10]} intensity={0.5} />
          
          {/* 5단계 황금 빛 */}
          {stage === 5 && (
            <>
              <pointLight position={[5, 5, 5]} intensity={1} color="#FFD700" />
              <pointLight position={[-5, -5, 5]} intensity={0.8} color="#FFD700" />
            </>
          )}

          {/* 4단계 불꽃 빛 */}
          {stage === 4 && (
            <pointLight position={[5, 0, 5]} intensity={0.8} color="#FF6347" />
          )}

          <Phoenix stage={stage} isAnimating={isAnimating} />

          {/* 배경 */}
          <color attach="background" args={['#e0f7ff']} />
        </Canvas>
      </Suspense>
    </div>
  );
};

export default Phoenix3D;
