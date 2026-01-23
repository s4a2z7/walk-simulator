import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DemoPage from './pages/DemoPage';

function App() {
  const [loading, setLoading] = useState(false);

  // 데모 모드: 앱 시작 시 데모 토큰 자동 주입
  useEffect(() => {
    // 실제 백엔드에서 허용하는 데모 토큰이 있다면 그 값을 넣으세요.
    // 여기서는 "demo-token"이라는 임의 값 사용
    if (!localStorage.getItem('token')) {
      localStorage.setItem('token', 'demo-token');
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/demo" element={<HomePage isDemo={true} />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
