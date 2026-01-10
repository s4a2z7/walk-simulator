import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import AllergyCheckPage from './pages/AllergyCheckPage';
import DemoPage from './pages/DemoPage';
import DemoAllergyPage from './pages/DemoAllergyPage';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/allergy"
          element={
            <ProtectedRoute>
              <AllergyCheckPage />
            </ProtectedRoute>
          }
        />
        <Route path="/demo" element={<DemoPage />} />
        <Route path="/demo-allergy" element={<DemoAllergyPage />} />
        <Route path="/" element={<Navigate to="/demo" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
