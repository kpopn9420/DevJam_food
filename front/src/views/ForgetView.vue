<template>
  <main class="items-center justify-center flex min-h-fit h-[calc(100svh-8rem)] m-8">
    <RegisterBackground
      class="w-full max-w-3xl"
      headline="忘記密碼？"
      subtitle1="請輸入註冊時的電子郵件帳號，"
      subtitle2="我們將會傳送一則郵件協助您重設密碼。"
    >
      <form class="w-full" @submit.prevent="submitForm">
        <BaseInputPlace
          v-model="email"
          label="電子郵件地址"
          placeholder="請輸入您的電子郵件"
          class="w-full mb-4"
        ></BaseInputPlace>
        <RegisterBlueButton button-text="傳送電子郵件" class="w-full" type="submit" @click="submitForm" />
      </form>
      <p v-if="errorMessage" class="text-red-500 mt-2">{{ errorMessage }}</p>
      <div class="w-full h-px bg-gray-300 my-6"></div>
      <BaseLink text="返回登入頁面" link="/login"></BaseLink>
    </RegisterBackground>
  </main>
</template>

<script setup>
  import { ref } from 'vue'
  import { useAuthStore } from '@/stores/authStore'
  import { useRouter } from 'vue-router'
  import RegisterBlueButton from '@/components/BaseButtonFilled.vue'
  import RegisterBackground from '@/components/FormBox.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseLink from '@/components/BaseLink.vue'
  import Auth from '@/api/auth'

  const router = useRouter()
  const authStore = useAuthStore()
  const email = ref('')
  const errorMessage = ref('')
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const submitForm = async () => {
    if (!validateEmail(email.value)) {
      errorMessage.value = '請輸入有效的電子郵件地址。'
      return
    }

    const response = await Auth.forgetPassword({ email: email.value })
    console.log(response)

    if (response.data.success && response.status === 200) {
      console.log('忘記密碼請求成功:', response.data)
      const url = new URL(response.data.message)
      // Extract token from the URL response
      const token = new URLSearchParams(url.search).get('token')
      console.log('Extracted Token:', token)
      authStore.setAccessToken(token)
      router.push(`/reset-password?token=${token}`)
      errorMessage.value = ''
    } else {
      errorMessage.value = response.message
    }
  }
</script>
