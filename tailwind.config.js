module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        grass: { DEFAULT: '#7ED321', dark: '#5FB304' },
        sky: '#B3E5FC',
        phoenix: {
          gray: '#E0E0E0',
          yellow: '#FFD54F',
          orange: '#FFB74D',
          red: '#FF6B6B',
          gold: '#FFD700'
        }
      },
      animation: {
        'float': 'petFloat 3s ease-in-out infinite',
        'jump': 'petJump 0.6s ease-out',
        'cloud': 'cloudFloat 20s linear infinite',
        'flame': 'flameRise 1s ease-out forwards',
        'sparkle': 'sparkleOrbit 2s ease-in-out infinite',
        'glow': 'goldenGlow 2s ease-in-out infinite'
      },
      keyframes: {
        cloudFloat: {
          '0%': { transform: 'translateX(-10%)' },
          '100%': { transform: 'translateX(120vw)' }
        },
        petFloat: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        petJump: {
          '0%, 100%': { transform: 'translateY(0) scale(1)' },
          '50%': { transform: 'translateY(-30px) scale(1.1)' }
        },
        flameRise: {
          '0%': { transform: 'translateY(0) scale(1)', opacity: '1' },
          '100%': { transform: 'translateY(-50px) scale(0.5)', opacity: '0' }
        },
        sparkleOrbit: {
          '0%': { transform: 'rotate(0deg) translateX(80px)', opacity: '0' },
          '20%, 80%': { opacity: '1' },
          '100%': { transform: 'rotate(360deg) translateX(80px)', opacity: '0' }
        },
        goldenGlow: {
          '0%, 100%': { boxShadow: '0 0 30px rgba(255, 215, 0, 0.6)' },
          '50%': { boxShadow: '0 0 60px rgba(255, 215, 0, 1)' }
        }
      }
    }
  },
  plugins: []
}
