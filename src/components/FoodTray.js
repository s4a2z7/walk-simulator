import React from 'react';

const FOODS = [
  { type: 'berry', emoji: '🍓', name: '불꽃 베리', cost: 0, costLabel: '무료' },
  { type: 'meat', emoji: '🍖', name: '신성한 고기', cost: 100, costLabel: '100걸음' },
  { type: 'golden_fruit', emoji: '🍑', name: '황금 과일', cost: 500, costLabel: '500걸음' }
];

const FoodTray = ({ onFeedClick, canAfford = { berry: true, meat: true, golden_fruit: true }, isLoading = false }) => {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 flex justify-center pb-5 px-4">
      <div className="bg-white rounded-3xl shadow-2xl px-8 py-6 flex items-center gap-8">
        {FOODS.map((food) => (
          <button
            key={food.type}
            onClick={() => onFeedClick(food.type)}
            disabled={isLoading || !canAfford[food.type]}
            className={`flex flex-col items-center gap-2 p-4 rounded-3xl transition-all duration-200 ${
              canAfford[food.type]
                ? 'bg-gradient-to-b from-amber-100 to-amber-200 hover:shadow-lg hover:scale-105 active:scale-95'
                : 'bg-gray-200 opacity-50 cursor-not-allowed'
            }`}
          >
            <span className="text-5xl">{food.emoji}</span>
            <span className="text-xs font-bold text-gray-700 text-center">{food.name}</span>
            <span className="text-xs text-gray-600">{food.costLabel}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default FoodTray;
