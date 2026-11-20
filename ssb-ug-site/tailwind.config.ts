import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: { DEFAULT: '#0C9D60', dark: '#17B877', deep: '#8FE3B5', soft: '#0D2A1C', line: '#1D5A3C' },
        ink: { DEFAULT: '#f5f5f3', 2: '#d4d4d1', 3: '#a3a3a0', 4: '#7a7a77' },
        paper: '#0a0a0a',
        line: { DEFAULT: '#262626', strong: '#3a3a3a' },
        surface: { DEFAULT: '#141414', 2: '#1e1e1e' },
        night: { DEFAULT: '#000000', 2: '#111111', 3: '#1c1c1c' },
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
