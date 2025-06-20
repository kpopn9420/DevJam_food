import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { setupCalendar } from 'v-calendar'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(setupCalendar, {})
app.use(createPinia())
app.use(router)

app.mount('#app')
