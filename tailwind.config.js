/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          DEFAULT: '#FFFDF7',
          light: '#FFFDF7',
          dark: '#FFF8F0',
        },
        slate: {
          700: '#334155',
          800: '#1E293B',
          900: '#0F172A',
          500: '#64748B',
          400: '#94A3B8',
        },
        gold: {
          light: '#E8D5A3',
          DEFAULT: '#C8A951',
          dark: '#B8963E',
          medium: '#D4B968',
        },
      },
      fontFamily: {
        playfair: ['Playfair Display', 'Georgia', 'serif'],
        inter: ['Inter', 'system-ui', 'sans-serif'],
      },
      maxWidth: {
        '8xl': '88rem',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
    },
  },
  plugins: [],
};
