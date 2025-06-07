<template>
  <main class="items-center justify-center flex min-h-fit h-[calc(100svh-8rem)] m-8">
    <Formbox
      class="w-full max-w-3xl"
      headline="創建帳號"
      subtitle1="請輸入學校機構的電子郵件帳號，"
      subtitle2="我們將會傳送一則郵件協助創建帳號。"
    >
      <form class="w-full" @submit.prevent="submitForm">
        <BaseInputPlace
          v-model="email"
          label="電子郵件地址"
          placeholder="請輸入您的電子郵件"
          class="w-full mb-4"
        ></BaseInputPlace>
        <PasswordInput
          v-model="password"
          label="密碼"
          type="password"
          placeholder="輸入您的密碼"
          class="w-full"
        ></PasswordInput>
        <div class="flex gap-4 w-full">
          <BaseButtonFilled
            button-text="註冊"
            class="flex-1 min-w-0"
            type="submit"
            @click="submitForm"
          />
          <BaseButtonFilled
            button-text="使用Google註冊"
            bg-color="bg-gray-400"
            hover-color="hover:bg-gray-500"
            class="flex-1 min-w-0"
            @click="googleLogin"
          />
        </div>
      </form>
      <div class="w-full h-px bg-gray-300 my-6"></div>
      <BaseLink text="已經有帳號了嗎？登入" link="/login"></BaseLink>
    </Formbox>

    <PageDialog
      :is-open="isDialogOpen"
      dialog-title="請檢查你的信箱"
      :email="email"
      hidden
      @close="isDialogOpen = false"
    >
      <div class="text-center px-8">
        <p class="text-gray-500">我們已傳送登入連結至 {{ email }}</p>
        <p class="mb-4 text-gray-500">請點擊該連結以繼續完成註冊手續。</p>
        <BaseButtonFilled
          button-text="重新傳送連結"
          width="w-full"
          :countdown-time="5"
          :is-counting="true"
          @click="submitForm"
        />
        <div class="w-full h-px bg-gray-300 my-4"></div>
        <BaseLink text="帳號錯誤？重新輸入電子郵件" link="/register" @click="closeDialog"></BaseLink>
      </div>
    </PageDialog>
  </main>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { useAuthStore } from '@/stores/authStore'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import Formbox from '@/components/FormBox.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseLink from '@/components/BaseLink.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import PasswordInput from '@/components/PasswordInput.vue'
  import BaseButtonOutlined from '@/components/BaseButtonOutlined.vue'
  import Auth from '@/api/auth'
  import router from '@/router'
  import { initializeApp } from 'firebase/app'
  import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth'

  const authStore = useAuthStore()

  const email = ref('')
  const password = ref('')
  const isDialogOpen = ref(false)

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const firebaseConfig = {
    apiKey: "AIzaSyCN25Bd28KyvxpJt3P-YPkSTsLnupKbfQU",
    authDomain: "gdg-foodshare.firebaseapp.com",
    projectId: "gdg-foodshare",
    storageBucket: "gdg-foodshare.firebasestorage.app",
    messagingSenderId: "202811512487",
    appId: "1:202811512487:web:75d7b523db4daf36a6ad82",
    measurementId: "G-2FDN861HWZ"
  }

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

      // ✅ 驗證成功才跳轉（例如去首頁）
      if (data.success) {
        router.push('/')  // 這裡可以換成你要導向的頁面
      }
    } catch (err) {
      console.error(err)
      result.value = '❌ 登入失敗：' + err.message
    }
  }

  const signup = async () => {
    const response = await Auth.signUp(
      {
        email: email.value,
      },
      {
        requiresAuth: false,
      }
    )
    if (response.status === 200 && response.data.success) {
      console.log('註冊請求成功:', response.data)
      const url = new URL(response.data.message)
      // Extract token from the URL response
      const token = new URLSearchParams(url.search).get('token')
      console.log('Extracted Token:', token)
      authStore.setAccessToken(token)
      router.push(`/set-password?token=${token}`)
      return { success: true, message: response.data.message }
    } else if (response.status === 409 && !response.data.success) {
      return { success: false, message: response.data.message }
    } else {
      return { success: false, message: response.data.message }
    }
  }

  const submitForm = async () => {
    if (!email.value) {
      console.log('請輸入電子郵件地址')
      alert('請輸入電子郵件地址')
      return
    }

    if (!validateEmail(email.value)) {
      console.log('請輸入有效的 Email 地址')
      alert('請輸入有效的 Email 地址')
      return
    }

    console.log('正在處理註冊請求...')

    // ✅ 模擬成功結果（不調用 API）
    const result = { success: true, message: '模擬註冊成功' }

    if (result.success) {
      console.log('操作成功:', result.message)
      isDialogOpen.value = true
      router.push('/')
    } else {
      console.log('操作失敗:', result.message)
      alert(`錯誤: ${result.message}`)
    }
  }

  const closeDialog = () => {
    isDialogOpen.value = false
  }
</script>
