/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['../templates/*.html', '../main/templates/main/**/*.html', '../chat/templates/chat/**/*.html', '../static/js/**/*.js'],
  theme: {
    extend: {},
  },
  plugins: [],
  variants: {
    extend: {
        display: ["group-hover"],
    },
  },
}
