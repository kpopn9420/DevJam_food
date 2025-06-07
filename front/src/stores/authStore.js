// stores/auth.js
import { defineStore } from 'pinia'
import router from '@/router'
import Auth from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
    userId: '123',
  }),
  actions: {
    login(response) {
      this.isAuthenticated = true
      this.accessToken = response.data.accessToken
      this.refreshToken = response.data.refreshToken
      this.userId = response.data.userId
      sessionStorage.setItem('userId', this.userId)
      sessionStorage.setItem('refreshToken', this.refreshToken)
      console.log('Login:', response)
      console.log('Refresh Token:', sessionStorage.getItem('refreshToken'))
      return response
    },
    async logout() {
      const response = await Auth.signOut({ refreshToken: sessionStorage.getItem('refreshToken') })
      if (response.status === 204) {
        console.log(response)
        this.isAuthenticated = false
        this.accessToken = null
        this.refreshToken = null
        sessionStorage.removeItem('refreshToken')
        router.push({ name: 'login' })
        return 204
      } else {
        console.log(response)
      }
    },
    loadAuthState() {
      const refreshToken = sessionStorage.getItem('refreshToken')
      if (refreshToken) {
        this.isAuthenticated = true
        this.refreshToken = refreshToken
      } else {
        this.isAuthenticated = false
      }
    },
    setAccessToken(token) {
      this.accessToken = token
    },
  },
  getters: {
    getAccessToken: (state) => state.token,
  },
})
