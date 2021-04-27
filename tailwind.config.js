
const colors = require('tailwindcss/colors')

module.exports = {
  purge: {
    enabled: true,
    content: [
        './**/*.html',
        './**/*.js',
        './**/*.css',
    ],
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        orange: colors.orange,
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
