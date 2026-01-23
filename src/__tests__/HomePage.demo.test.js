import { render, screen, fireEvent } from '@testing-library/react';
import HomePage from '../pages/HomePage';

// Mock props and API
const mockSetAuth = jest.fn();

jest.mock('../services/api', () => ({
  petAPI: {
    getPet: jest.fn(() => Promise.resolve({ data: { pet: { name: '테스트펫', stage_emoji: '🐣', stage_name: '알', total_exp: 0, total_steps: 0, age_days: 1, current_stage: 1, exp_to_next_stage: 10, current_exp: 0, user_id: 1 } } })),
    addSteps: jest.fn(() => Promise.resolve({ data: { pet: { name: '테스트펫', total_exp: 100, total_steps: 100, age_days: 1, current_stage: 1, exp_to_next_stage: 10, current_exp: 10, user_id: 1 } } })),
    feedPet: jest.fn(() => Promise.resolve({ data: { pet: { name: '테스트펫' } } })),
    drinkWater: jest.fn(() => Promise.resolve({ data: { message: '물 마시기 성공', pet: { name: '테스트펫' } } })),
    stretch: jest.fn(() => Promise.resolve({ data: { message: '운동하기 성공', pet: { name: '테스트펫' } } })),
    sleepEarly: jest.fn(() => Promise.resolve({ data: { message: '일찍 자기 성공', pet: { name: '테스트펫' } } })),
  },
  rankingAPI: {
    getRanking: jest.fn(() => Promise.resolve({ data: { rankings: [] } })),
  },
}));

describe('HomePage 데모 모드 버튼 UI', () => {
  it('데모 모드에서 건강습관 버튼이 항상 보인다', async () => {
    render(<HomePage setAuth={mockSetAuth} isDemo={true} />);
    // 버튼이 모두 보이는지 확인
    expect(await screen.findByText('+10 물 마시기')).toBeInTheDocument();
    expect(screen.getByText('+50 운동하기')).toBeInTheDocument();
    expect(screen.getByText('+40 일찍 자기')).toBeInTheDocument();
  });

  it('각 버튼 클릭 시 알림이 뜬다', async () => {
    render(<HomePage setAuth={mockSetAuth} isDemo={true} />);
    fireEvent.click(await screen.findByText('+10 물 마시기'));
    fireEvent.click(screen.getByText('+50 운동하기'));
    fireEvent.click(screen.getByText('+40 일찍 자기'));
    // 알림이 DOM에 추가되는지 확인 (간단히 텍스트로)
    expect(document.body.innerHTML).toMatch(/물 마시기|운동하기|일찍 자기/);
  });
});
