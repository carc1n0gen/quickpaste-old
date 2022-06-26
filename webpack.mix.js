let mix = require('laravel-mix');

mix.scripts([
    'app/assets/js/toast.js',
], 'app/static/bundle.js');

mix.postCss("app/assets/css/main.css", "app/static/css", [
    require("tailwindcss"),
]);

mix.copyDirectory('app/assets/img', 'app/static/img');
