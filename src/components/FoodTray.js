import React from 'react';

const FOODS = [
  { 
    type: 'berry', 
    emoji: '🍓', 
    name: '불꽃 베리', 
    cost: 0,
    hunger: 15,
    happiness: 5,
    description: '무료'
  },
  { 
    type: 'meat', 
    emoji: '🍖', 
    name: '신성한 고기', 
    cost: 100,
    hunger: 40,
    happiness: 15,
    description: '100 걸음'
  },
  { 
    type: 'golden_fruit', 
    emoji: '🍑', 
    name: '황금 과일', 
    cost: 500,
    hunger: 100,
    happiness: 30,
    description: '500 걸음'
  }
];

function FoodTray({ pet, onFeed, disabled }) {
  const canAfford = (cost) => {
    return pet && pet.today_steps >= cost;
  };

  return (
    <div className="fixed bottom-8 left-1/2 transform -translate-x-1/2 z-50 flex gap-4">
      {FOODS.map((food) => {
        const affordable = canAfford(food.cost);
        
        return (
          <button
            key={food.type}
            onClick={() => onFeed(food.type)}
            disabled={disabled || !affordable}
            className="group relative w-20 h-20 bg-white rounded-full shadow-xl flex flex-col items-center justify-center gap-1 transition-all duration-300 hover:scale-110 hover:shadow-2xl disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:scale-100"
            title={`${food.name} - ${food.description}\n배고픔 +${food.hunger}, 행복 +${food.happiness}`}
          >
            <div className="text-4xl">{food.emoji}</div>
            <div className="text-xs font-black text-gray-600">
              {food.cost === 0 ? '무료' : food.cost}
            </div>

            {/* 툴팁 */}
            <div className="absolute bottom-full mb-2 hidden group-hover:block bg-gray-800 text-white px-3 py-2 rounded-lg text-xs whitespace-nowrap">
              <div className="font-bold">{food.name}</div>
              <div>🍖 +{food.hunger} | 😊 +{food.happiness}</div>
              {!affordable && food.cost > 0 && (
                <div className="text-red-300 mt-1">걸음수 부족!</div>
              )}
            </div>
          </button>
        );
      })}
    </div>
  );
}

export default FoodTray;
