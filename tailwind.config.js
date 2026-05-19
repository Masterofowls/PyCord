/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './pycord/**/*.py',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        discord: {
          bg:       '#313338',
          sidebar:  '#2B2D31',
          rail:     '#1E1F22',
          accent:   '#5865F2',
          muted:    '#949BA4',
          text:     '#F2F3F5',
          channel:  '#404249',
          input:    '#383A40',
          mention:  '#FAA61A',
        },
      },
      fontFamily: {
        sans: ['gg sans', 'Inter', 'ui-sans-serif', 'system-ui'],
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        pycord: {
          'primary':        '#5865F2',
          'secondary':      '#4752C4',
          'accent':         '#EB459E',
          'neutral':        '#2B2D31',
          'base-100':       '#313338',
          'base-200':       '#2B2D31',
          'base-300':       '#1E1F22',
          'base-content':   '#F2F3F5',
          'info':           '#00A8FC',
          'success':        '#23A55A',
          'warning':        '#F0B232',
          'error':          '#F23F43',
        },
      },
      'dark',
    ],
    darkTheme: 'pycord',
  },
}
