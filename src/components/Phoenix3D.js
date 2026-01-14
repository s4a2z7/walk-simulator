import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

const Phoenix3D = ({ stage = 1, isAnimating = false }) => {
  const containerRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const phoenixRef = useRef(null);
  const animationIdRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene 설정
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xe0f7ff);
    sceneRef.current = scene;

    // Camera 설정
    const camera = new THREE.PerspectiveCamera(
      50,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 0, 3);
    cameraRef.current = camera;

    // Renderer 설정
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // 조명
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0xffffff, 1);
    pointLight1.position.set(10, 10, 10);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0xffffff, 0.5);
    pointLight2.position.set(-10, -10, 10);
    scene.add(pointLight2);

    // 단계별 조명 추가
    if (stage === 5) {
      const goldLight1 = new THREE.PointLight(0xFFD700, 1);
      goldLight1.position.set(5, 5, 5);
      scene.add(goldLight1);

      const goldLight2 = new THREE.PointLight(0xFFD700, 0.8);
      goldLight2.position.set(-5, -5, 5);
      scene.add(goldLight2);
    } else if (stage === 4) {
      const fireLight = new THREE.PointLight(0xFF6347, 0.8);
      fireLight.position.set(5, 0, 5);
      scene.add(fireLight);
    }

    // 불사조 생성
    const phoenix = new THREE.Group();
    phoenixRef.current = phoenix;

    // 색상 정의
    const getBodyColor = () => {
      if (stage === 1) return 0x808080; // 회색 (알)
      if (stage === 2) return 0xFFD700; // 노란색 (병아리)
      if (stage === 3) return 0xFF8C00; // 주황색 (새)
      if (stage === 4) return 0xFF4500; // 빨간색 (불사조)
      if (stage === 5) return 0xFFD700; // 금색 (황금 불사조)
      return 0xFF8C00;
    };

    const getEmissive = () => {
      if (stage === 5) return 0xFFD700;
      if (stage === 4) return 0xFF6347;
      return 0x000000;
    };

    const bodyColor = getBodyColor();
    const emissiveColor = getEmissive();

    // 몸체
    const bodyGeometry = new THREE.SphereGeometry(0.6, 32, 32);
    const bodyMaterial = new THREE.MeshStandardMaterial({
      color: bodyColor,
      emissive: emissiveColor,
      emissiveIntensity: stage >= 4 ? 0.5 : 0,
      roughness: stage === 5 ? 0.2 : 0.7,
      metalness: stage === 5 ? 0.8 : 0,
    });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.position.set(0, 0, 0);
    phoenix.add(body);

    // 머리
    const headGeometry = new THREE.SphereGeometry(0.4, 32, 32);
    const headMaterial = new THREE.MeshStandardMaterial({
      color: bodyColor,
      emissive: emissiveColor,
      emissiveIntensity: stage >= 4 ? 0.5 : 0,
    });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.set(0, 0.7, 0.3);
    phoenix.add(head);

    // 눈
    const eyeGeometry = new THREE.SphereGeometry(0.1, 32, 32);
    const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.12, 0.85, 0.6);
    phoenix.add(leftEye);

    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.12, 0.85, 0.6);
    phoenix.add(rightEye);

    // 부리
    const beakGeometry = new THREE.ConeGeometry(0.15, 0.4, 16);
    const beakMaterial = new THREE.MeshStandardMaterial({ color: 0xFFA500 });
    const beak = new THREE.Mesh(beakGeometry, beakMaterial);
    beak.position.set(0, 0.6, 0.7);
    beak.rotation.x = Math.PI / 2;
    phoenix.add(beak);

    // 다리
    const legGeometry = new THREE.CylinderGeometry(0.08, 0.08, 0.4, 16);
    const legMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
    const leftLeg = new THREE.Mesh(legGeometry, legMaterial);
    leftLeg.position.set(-0.2, -0.65, 0);
    phoenix.add(leftLeg);

    const rightLeg = new THREE.Mesh(legGeometry, legMaterial);
    rightLeg.position.set(0.2, -0.65, 0);
    phoenix.add(rightLeg);

    // 꼬리
    const tailGeometry = new THREE.SphereGeometry(0.25, 32, 32);
    const tailMaterial = new THREE.MeshStandardMaterial({
      color: bodyColor,
      emissive: emissiveColor,
      emissiveIntensity: stage >= 4 ? 0.5 : 0,
    });
    const tail = new THREE.Mesh(tailGeometry, tailMaterial);
    tail.position.set(0, 0.2, -0.8);
    phoenix.add(tail);

    // 날개 (4단계 이상)
    if (stage >= 4) {
      const wingGeometry = new THREE.SphereGeometry(0.2, 32, 32);
      const wingMaterial = new THREE.MeshStandardMaterial({
        color: 0xFF4500,
        emissive: 0xFF6347,
        emissiveIntensity: 0.6,
      });

      const leftWing = new THREE.Mesh(wingGeometry, wingMaterial);
      leftWing.position.set(-0.7, 0.2, 0);
      leftWing.name = 'leftWing';
      phoenix.add(leftWing);

      const rightWing = new THREE.Mesh(wingGeometry, wingMaterial);
      rightWing.position.set(0.7, 0.2, 0);
      rightWing.name = 'rightWing';
      phoenix.add(rightWing);
    }

    // 왕관 (5단계)
    if (stage === 5) {
      const crownGeometry = new THREE.CylinderGeometry(0.5, 0.5, 0.1, 32);
      const crownMaterial = new THREE.MeshStandardMaterial({
        color: 0xFFD700,
        emissive: 0xFFD700,
        emissiveIntensity: 1,
        metalness: 1,
        roughness: 0,
      });
      const crown = new THREE.Mesh(crownGeometry, crownMaterial);
      crown.position.set(0, 1.4, 0.3);
      phoenix.add(crown);

      // 왕관 장식
      const gemGeometry = new THREE.ConeGeometry(0.15, 0.3, 16);
      const gemMaterial = new THREE.MeshStandardMaterial({
        color: 0xFFD700,
        emissive: 0xFFD700,
        emissiveIntensity: 1,
      });

      const leftGem = new THREE.Mesh(gemGeometry, gemMaterial);
      leftGem.position.set(-0.3, 1.55, 0.3);
      phoenix.add(leftGem);

      const rightGem = new THREE.Mesh(gemGeometry, gemMaterial);
      rightGem.position.set(0.3, 1.55, 0.3);
      phoenix.add(rightGem);
    }

    scene.add(phoenix);

    // 애니메이션 루프
    const clock = new THREE.Clock();

    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate);
      const time = clock.getElapsedTime();

      // 떠다니는 애니메이션
      if (!isAnimating) {
        phoenix.position.y = Math.sin(time * 1.5) * 0.3;
        phoenix.rotation.z = Math.cos(time * 1.5) * 0.1;
      } else {
        // 점프 애니메이션
        const jumpY = Math.abs(Math.sin(time * 8)) * 0.8;
        phoenix.position.y = jumpY;
      }

      // 머리 회전
      const head = phoenix.children[1];
      if (head) {
        head.rotation.y = Math.sin(time * 2) * 0.2;
      }

      // 날개 움직임 (4단계 이상)
      if (stage >= 4) {
        const leftWing = phoenix.children.find(child => child.name === 'leftWing');
        const rightWing = phoenix.children.find(child => child.name === 'rightWing');

        if (leftWing) {
          leftWing.rotation.z = Math.sin(time * 4) * 0.5;
          leftWing.position.y = 0.2 + Math.cos(time * 4) * 0.1;
        }

        if (rightWing) {
          rightWing.rotation.z = -Math.sin(time * 4) * 0.5;
          rightWing.position.y = 0.2 + Math.cos(time * 4) * 0.1;
        }
      }

      renderer.render(scene, camera);
    };

    animate();

    // 윈도우 리사이즈 처리
    const handleResize = () => {
      if (!containerRef.current) return;
      const width = containerRef.current.clientWidth;
      const height = containerRef.current.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };

    window.addEventListener('resize', handleResize);

    // 정리
    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }
      if (containerRef.current && renderer.domElement.parentNode === containerRef.current) {
        containerRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [stage, isAnimating]);

  return <div ref={containerRef} style={{ width: '100%', height: '100%', minHeight: '400px' }} />;
};

export default Phoenix3D;
