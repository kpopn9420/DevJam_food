import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import Auth from '@/api/auth'

// Create an axios instance
export const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptors to add the Authorization header if needed
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()

    if (config.requiresAuth !== false) {
      const accessToken = authStore.accessToken
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`
        console.log('Authorization Header Set:', config.headers.Authorization)
      }
    }

    console.log('Axios Request:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data,
    })

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptors to update access tokens using the refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Check if the error is due to forbidden access and retry is not already attempted
    if (error.response && error.response.status === 403 && !originalRequest._retry) {
      originalRequest._retry = true // Prevent multiple retries for the same request

      try {
        console.log('Refresh token', sessionStorage.getItem('refreshToken'))
        const response = await Auth.refresh({
          refreshToken: sessionStorage.getItem('refreshToken'),
        })

        if (response.status === 200) {
          const authStore = useAuthStore()

          // Update the access token in the store
          authStore.setAccessToken(response.data.accessToken)

          // Set the Authorization header for the original request
          originalRequest.headers.Authorization = `Bearer ${response.data.accessToken}`

          // Retry the original request with the new token
          return api(originalRequest)
        }
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError)
        return Promise.reject(refreshError)
      }
    }

    // Reject the error if it doesn't qualify for retrying
    return Promise.reject(error)
  }
)

export default api
