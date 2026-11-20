import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: { DEFAULT: '#CC5500', dark: '#A84600', deep: '#4A1F00', soft: '#FCEEE3', line: '#F2CBAE' },
        ink: { DEFAULT: '#121212', 2: '#3d3d3d', 3: '#6b6b6b', 4: '#9a9a9a' },
        line: { DEFAULT: '#e8e8e6', strong: '#d6d6d3' },
        surface: { DEFAULT: '#f6f6f4', 2: '#efefec' },
        night: { DEFAULT: '#0a0a0a', 2: '#151515', 3: '#222222' },
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
