/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./**/*.{html,js}", "!./node_modules/**/*"],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                display: ['Outfit', 'sans-serif'],
                'roboto-condensed': ['"Roboto Condensed"', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
