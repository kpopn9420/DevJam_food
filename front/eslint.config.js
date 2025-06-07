import js from '@eslint/js'
import eslintPluginVue from 'eslint-plugin-vue'
import eslintConfigPrettier from 'eslint-config-prettier'

export default [
  js.configs.recommended,
  ...eslintPluginVue.configs['flat/recommended'],
  {
    files: ['src/**/*.{js,vue}'],
    ignores: ['.gitignore', '.eslintrc.config.js', 'tailwind.config.js', 'postcss.config.js'], // or manually specify patterns to ignore if necessary
    languageOptions: {
      globals: {
        webkitSpeechRecognition: 'readonly',
      },
    },
    rules: {
      // Your ESLint rules go here
    },
  },
  eslintConfigPrettier,
]
