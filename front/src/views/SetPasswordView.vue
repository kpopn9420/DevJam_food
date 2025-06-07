<template>
  <main class="items-center justify-center flex min-h-fit h-[calc(100svh-8rem)] m-8">
    <FormBox
      headline="歡迎！"
      subtitle1="為確保帳戶安全性及您的權益，"
      subtitle2="請設定您的密碼並且同意網站的使用條款及隱私權說明。"
      class="w-full max-w-3xl"
    >
      <PasswordInput
        v-model="newPassword"
        required
        class="w-full"
        label="新密碼"
        :remind="remindMessage"
        :condition="remindCondition"
      ></PasswordInput>
      <PasswordInput
        v-model="confirmPassword"
        required
        class="w-full"
        :passwords-match="passwordsMatch"
        remind="密碼不一致"
        :condition="passwordsMatch ? 'hidden' : 'text-red-500'"
        label="確認新密碼"
      />
      <CheckBox v-model="isTosAgreed" class="mb-4">
        我已同意
        <BaseLink text="使用條款及隱私權說明" @click="openTos()"></BaseLink>
      </CheckBox>
      <RegisterBlueButton button-text="創建帳號" class="w-full" @click="submitForm" />
      <div class="w-full h-px bg-gray-300 my-6"></div>
      <BaseLink text="不同意使用條款及登出" link="/login"></BaseLink>
    </FormBox>
  </main>
  <PageDialog :is-open="isTosOpen" dialog-title="使用條款及隱私權說明">
    <p class="text-gray-700 mb-4">這是使用條款及隱私權說明的內容。</p>
    <RegisterBlueButton button-text="同意" class="mb-3" @click="agreeTos" />
    <div class="w-full h-px bg-gray-300"></div>
    <BaseLink class="text-center" text="不同意" @click="closeTos" />
  </PageDialog>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import RegisterBlueButton from '@/components/BaseButtonFilled.vue'
  import FormBox from '@/components/FormBox.vue'
  import BaseLink from '@/components/BaseLink.vue'
  import CheckBox from '@/components/InputCheck.vue'
  import PasswordInput from '@/components/PasswordInput.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import Auth from '@/api/auth'
  import { useRouter } from 'vue-router'
  import { hashPassword } from '@/utils/hashUtil'
  import { useAuthStore } from '@/stores/authStore'

  const router = useRouter()
  const authStore = useAuthStore()
  const newPassword = ref('')
  const confirmPassword = ref('')
  const passwordsMatch = ref(true)
  const remindMessage = ref('新密碼需為八位以上，包含英文數字及特殊字元')
  const remindCondition = ref('text-gray-500')

  const passwordStrengthRegex =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/

  watch([newPassword, confirmPassword], () => {
    passwordsMatch.value = newPassword.value === confirmPassword.value
  })

  watch(newPassword, (newValue) => {
    if (!passwordStrengthRegex.test(newValue)) {
      remindCondition.value = 'text-red-500'
    } else {
      remindCondition.value = 'text-gray-500'
    }
  })

  const isTosAgreed = ref(false)
  const isTosOpen = ref(false)

  const openTos = () => {
    isTosOpen.value = true
  }

  const closeTos = () => {
    isTosOpen.value = false
  }

  const agreeTos = () => {
    isTosAgreed.value = true
    closeTos()
  }

  const submitForm = async () => {
    if (!passwordsMatch.value) {
      alert('密碼與確認密碼不一致，請重新檢查')
      return
    }

    if (!newPassword.value || !confirmPassword.value) {
      alert('請輸入新密碼及確認新密碼')
      return
    }

    if (!isTosAgreed.value) {
      alert('請同意使用條款及隱私權說明')
      return
    }
    const encryptedPassword = await hashPassword(newPassword.value)
    console.log('正在提交密碼設置請求...', encryptedPassword)
    const response = await Auth.setPassword({ password: encryptedPassword })
    console.log(response)
    if (response.status === 201 && response.data.success) {
      authStore.login(response)
      console.log(response)
      router.push('/')
      alert('密碼設置成功！')
    } else {
      alert(`錯誤`)
    }
  }
</script>
