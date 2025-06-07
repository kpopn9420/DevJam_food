<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-2">登入</h2>
    <input v-model="email" placeholder="輸入 Email" /><br />
    <input v-model="password" type="password" placeholder="輸入密碼" /><br />

    <button @click="loginWithEmail" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">用帳號密碼登入</button>
    <button @click="googleLogin" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
      🔐 使用 Google 登入
    </button>
    <pre class="mt-4 whitespace-pre-wrap bg-gray-100 p-4 rounded">{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth'
import Auth from '@/api/auth'

const email = ref('')
const password = ref('')

// ✅ Firebase 設定
const firebaseConfig = {
  apiKey: "AIzaSyCN25Bd28KyvxpJt3P-YPkSTsLnupKbfQU",
  authDomain: "gdg-foodshare.firebaseapp.com",
  projectId: "gdg-foodshare",
  storageBucket: "gdg-foodshare.firebasestorage.app",
  messagingSenderId: "202811512487",
  appId: "1:202811512487:web:75d7b523db4daf36a6ad82",
  measurementId: "G-2FDN861HWZ"
}

// ✅ 初始化 Firebase
const result = ref('')
let auth

onMounted(() => {
  const app = initializeApp(firebaseConfig)
  auth = getAuth(app)
})

async function googleLogin() {
  const provider = new GoogleAuthProvider()
  try {
    const signInResult = await signInWithPopup(auth, provider)
    const token = await signInResult.user.getIdToken()
    console.log('ID Token:', token)
    result.value = `✅ 成功登入\n\nID Token:\n${token}`

    // ✅ 傳 token 到後端測試驗證
    const response = await fetch('http://127.0.0.1:5000/secure', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
    const data = await response.json()
    result.value += `\n\n🎯 後端回應：\n${JSON.stringify(data, null, 2)}`
  } catch (err) {
    console.error(err)
    result.value = '❌ 登入失敗：' + err.message
  }
}
const loginWithEmail = async () => {
  try {
    const response = await Auth.signIn({
      email: email.value,
      passwd: password.value,
    })

    if (response.status === 200) {
      result.value = '✅ 傳統登入成功，User ID：' + response.data.user_id
      window.location.href = '/'
    } else {
      result.value = '❌ 登入失敗，帳號或密碼錯誤'
    }
  } catch (err) {
    result.value = '❌ 登入錯誤：' + err.message
  }
}
</script>

<style scoped>
pre {
  font-family: monospace;
}
</style>


<!-- <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'
  import { hashPassword } from '@/utils/hashUtil'
  import InputCheck from '@/components/InputCheck.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import FormBox from '@/components/FormBox.vue'
  import BaseLink from '@/components/BaseLink.vue'
  import LoginBlueButton from '@/components/BaseButtonFilled.vue'
  import BaseBanner from '@/components/BaseBanner.vue'
  import PasswordInput from '@/components/PasswordInput.vue'
  import Auth from '@/api/auth'

  const authStore = useAuthStore()
  const router = useRouter()
  const email = ref('')
  const password = ref('')

  const notificationData = {
    open: ref(false),
    type: ref('error'),
    headline: ref('登入失敗'),
    content: ref('請檢查您的輸入帳號或密碼是否正確。'),
  }

  const handleLogin = async () => {
    if (email.value === '' || password.value === '') {
      notificationData.open.value = true
      notificationData.type.value = 'error'
      notificationData.headline.value = '登入失敗'
      notificationData.content.value = '電子郵件和密碼不可為空。'
      return
    }
    try {
      const response = await Auth.signIn({
        email: email.value,
        password: await hashPassword(password.value),
      })

      if (response.status === 200 && response.data.success) {
        console.log('登入成功', response)
        notificationData.open.value = true
        notificationData.type.value = 'success'
        notificationData.headline.value = '登入成功'
        notificationData.content.value = '您已成功登入。'
        authStore.login(response)
        router.push('/')
      } else {
        console.error('登入失敗')
        notificationData.open.value = true
        notificationData.type.value = 'error'
        notificationData.headline.value = '登入失敗'
        notificationData.content.value = '請檢查您的帳號或密碼是否正確。'
      }
    } catch (error) {
      console.error('登入失敗:', error)
      notificationData.open.value = true
      notificationData.type.value = 'error'
      notificationData.headline.value = '登入失敗'
      notificationData.content.value = '伺服器發生錯誤，請稍後再試。'
    }
  }
</script> -->
