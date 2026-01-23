describe('데모 모드 건강습관 버튼 UI', () => {
  beforeEach(() => {
    cy.visit('/demo');
  });

  it('데모 모드에서 건강습관 버튼이 항상 보인다', () => {
    cy.contains('+10 물 마시기').should('be.visible');
    cy.contains('+50 운동하기').should('be.visible');
    cy.contains('+40 일찍 자기').should('be.visible');
  });

  it('각 버튼 클릭 시 알림이 뜬다', () => {
    cy.contains('+10 물 마시기').click();
    cy.contains('물 마시기').should('exist');
    cy.contains('+50 운동하기').click();
    cy.contains('운동하기').should('exist');
    cy.contains('+40 일찍 자기').click();
    cy.contains('일찍 자기').should('exist');
  });
});
