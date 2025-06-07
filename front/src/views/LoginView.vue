<template>
  <BaseBanner
    :is-open="notificationData.open.value"
    :type="notificationData.type.value"
    :headline="notificationData.headline.value"
    :content="notificationData.content.value"
    @close="notificationData.open.value = false"
  />
  <div class="items-center justify-center flex min-h-fit h-[calc(100svh-8rem)] m-8">
    <FormBox
      class="m-0 max-md:w-full max-lg:w-10/12 lg:block lg:w-2/3 xl:w-1/2 md:m-8 h-fit transition-all duration-100"
      headline="歡迎回來"
      subtitle1="請登入以繼續使用"
    >
      <form class="w-full" @submit.prevent="handleLogin">
        <BaseInputPlace
          v-model="email"
          label="電子郵件地址"
          placeholder="輸入您的電子郵件"
          class="w-full mb-4"
        ></BaseInputPlace>
        <PasswordInput
          v-model="password"
          label="密碼"
          type="password"
          placeholder="輸入您的密碼"
          class="w-full"
        ></PasswordInput>
        <div class="flex items-center justify-between my-4 w-full">
          <InputCheck class="flex items-center my-4">
            <label>記住我</label>
          </InputCheck>
          <BaseLink text="忘記密碼？" link="/forget-password"></BaseLink>
        </div>
        <LoginBlueButton button-text="登入" type="submit" width="w-full" @click="handleLogin" />
      </form>
      <div class="w-full h-px bg-gray-300 my-6"></div>
      <div class="text-center">
        <BaseLink text="還沒有帳號嗎？註冊" link="/register"></BaseLink>
      </div>
    </FormBox>

    <img src="/src/assets/login-placeholder.png" class="hidden overflow-hidden lg:block lg:w-1/3 top-1/2" />
  </div>
</template>

<script setup>
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
</script>
