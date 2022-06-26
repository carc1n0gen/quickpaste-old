module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/templates/**/*.jinja"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}