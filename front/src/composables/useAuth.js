// src/composables/useAuth.js
import { ref } from 'vue'
import Auth from '@/api/auth'  // 你現有的api呼叫物件
import { useAuthStore } from '@/stores/authStore'

export function useAuth() {
  const error = ref(null)
  const loading = ref(false)
  const authStore = useAuthStore()

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const response = await Auth.signIn({ email, password })
      if (response.status === 200 && response.data.success) {
        authStore.login(response.data)
      } else {
        error.value = '登入失敗'
      }
    } catch (e) {
      error.value = e.message || '伺服器錯誤'
    } finally {
      loading.value = false
    }
  }

  return { login, error, loading }
}
// This composable provides a simple interface for logging in users.
// It uses the Auth API to perform the login operation and manages loading and error states.