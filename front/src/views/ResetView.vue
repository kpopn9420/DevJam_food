<template>
  <main class="items-center justify-center flex min-h-fit h-[calc(100svh-8rem)] m-8">
    <RegisterBackground
      class="w-full max-w-3xl -mt-10"
      headline="重設密碼"
      subtitle1="請輸入新密碼"
      subtitle2=""
    >
      <form class="w-full" @submit.prevent="submitForm">
        <PasswordInput
          v-model="originalpassword"
          required
          class="w-full"
          label="新密碼"
          :remind="remindMessage"
          :condition="remindCondition"
        ></PasswordInput>
        <PasswordInput
          v-model="newPassword"
          required
          class="w-full"
          :passwords-match="passwordsMatch"
          remind="密碼不一致"
          :condition="passwordsMatch ? 'hidden' : 'text-red-500'"
          label="確認新密碼"
        ></PasswordInput>
        <RegisterBlueButton
          type="submit"
          class="group-invalid:pointer-events-none group-invalid:opacity-30"
          button-text="更改密碼"
          @click="submitForm"
        />
      </form>
      <div class="w-full h-px bg-gray-300 my-6"></div>
      <BaseLink text="已經有帳號了嗎？登入" link="/login"></BaseLink>
    </RegisterBackground>
  </main>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import RegisterBlueButton from '@/components/BaseButtonFilled.vue'
  import RegisterBackground from '@/components/FormBox.vue'
  import BaseLink from '@/components/BaseLink.vue'
  import PasswordInput from '@/components/PasswordInput.vue'
  import Auth from '@/api/auth'
  import { useAuthStore } from '@/stores/authStore'
  import { hashPassword } from '@/utils/hashUtil'

  const router = useRouter()
  const authStore = useAuthStore()
  const originalpassword = ref('')
  const newPassword = ref('')

  const passwordsMatch = ref(true)
  const remindMessage = ref('新密碼需為八位以上，包含英文數字及特殊字元')
  const remindCondition = ref('text-gray-500')

  const passwordStrengthRegex =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/

  watch([originalpassword, newPassword], () => {
    passwordsMatch.value = originalpassword.value === newPassword.value
  })

  watch(originalpassword, (newValue) => {
    if (!passwordStrengthRegex.test(newValue)) {
      remindCondition.value = 'text-red-500'
    } else {
      remindCondition.value = 'text-gray-500'
    }
  })

  const submitForm = async () => {
    if (!originalpassword.value || !newPassword.value) {
      alert('請輸入新密碼及確認新密碼')
      return
    }

    if (!passwordsMatch.value) {
      alert('密碼與確認密碼不一致，請重新檢查')
      return
    }

    if (remindCondition.value !== 'text-gray-500') {
      alert('密碼強度不符合要求，請重新輸入')
      return
    }

    const encryptedNewPassword = await hashPassword(originalpassword.value)

    try {
      const response = await Auth.setPassword({
        password: encryptedNewPassword,
      })

      if (response.status === 201 && response.data.success) {
        alert('密碼更改成功！')
        authStore.login(response)
        router.push('/')
      } else {
        alert(`錯誤: ${response.data?.message || '密碼更改失敗，請稍後再試'}`)
      }
    } catch (error) {
      alert(`發生錯誤: ${error.response?.data?.message || '未知錯誤'}`)
    }
  }
</script>
