/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        grass: {
          DEFAULT: '#7ED321',
          dark: '#5FB304',
          light: '#9FE855',
        },
        water: {
          DEFAULT: '#4FC3F7',
          light: '#81D4FA',
        },
        sky: '#B3E5FC',
        phoenix: {
          gray: '#E0E0E0',
          yellow: '#FFD54F',
          orange: '#FFB74D',
          red: '#FF6B6B',
          gold: '#FFD700',
        }
      },
      animation: {
        'float': 'float 3s ease-in-out infinite',
        'bounce-slow': 'bounce 2s ease-in-out infinite',
        'spin-slow': 'spin 8s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        }
      }
    },
  },
  plugins: [],
}
