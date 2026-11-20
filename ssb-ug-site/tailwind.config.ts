import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: { DEFAULT: '#068852', dark: '#00703c', deep: '#014d2a', soft: '#e9f6ef', line: '#bfe3cf' },
        ink: { DEFAULT: '#121212', 2: '#3d3d3d', 3: '#6b6b6b', 4: '#9a9a9a' },
        line: { DEFAULT: '#e8e8e6', strong: '#d6d6d3' },
        surface: { DEFAULT: '#f6f6f4', 2: '#efefec' },
        night: { DEFAULT: '#0e0f0e', 2: '#171917', 3: '#222522' },
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans Variable"', '"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
      },
      maxWidth: { page: '1240px' },
      letterSpacing: { tightish: '-0.015em', tighter2: '-0.025em' },
      keyframes: {
        marquee: { from: { transform: 'translateX(0)' }, to: { transform: 'translateX(-50%)' } },
      },
      animation: { marquee: 'marquee 40s linear infinite' },
    },
  },
  plugins: [],
};
export default config;
