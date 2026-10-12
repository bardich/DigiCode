/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './static/js/site.js',
    './apps/**/*.py',
  ],
  safelist: ['bg-blue-500/20', 'bg-cyan-500/20', 'bg-emerald-500/20', 'bg-indigo-500/20', 'bg-orange-500/20', 'bg-pink-500/20', 'bg-purple-500/20', 'bg-red-500/20', 'from-blue-500', 'from-cyan-500', 'from-emerald-500', 'from-indigo-500', 'from-orange-500', 'from-pink-500', 'from-purple-500', 'from-red-500', 'to-amber-400', 'to-blue-400', 'to-cyan-400', 'to-pink-400', 'to-purple-400', 'to-rose-400', 'to-teal-400'],
  theme: {
    extend: {
      colors: {
        primary: '#0F172A',
        accent: '#2563EB',
        highlight: '#F59E0B',
        background: '#F8FAFC',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        arabic: ['Fustat', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out forwards',
        'slide-in-right': 'slideInRight 0.6s ease-out forwards',
        'slide-in-left': 'slideInLeft 0.6s ease-out forwards',
      },
      boxShadow: {
        'soft': '0 4px 20px rgba(15, 23, 42, 0.08)',
        'medium': '0 10px 40px rgba(15, 23, 42, 0.12)',
        'large': '0 20px 60px rgba(15, 23, 42, 0.18)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
