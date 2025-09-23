import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
const pinia = createPinia()
const app = createApp(App)
app.use(router) // add this
app.use(pinia)
app.mount('#app')

