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
        <BaseButtonFilled button-text="傳送電子郵件" width="w-full" type="submit" @click="submitForm" />
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
  import { ref } from 'vue'
  import { useAuthStore } from '@/stores/authStore'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import Formbox from '@/components/FormBox.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseLink from '@/components/BaseLink.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import Auth from '@/api/auth'
  import router from '@/router'

  const authStore = useAuthStore()

  const email = ref('')
  const isDialogOpen = ref(false)

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
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
    const result = await signup(email.value)

    if (result.success) {
      console.log('操作成功:', result.message)
      isDialogOpen.value = true
    } else {
      console.log('操作失敗:', result.message)
      alert(`錯誤: ${result.message}`)
    }
  }

  const closeDialog = () => {
    isDialogOpen.value = false
  }
</script>
