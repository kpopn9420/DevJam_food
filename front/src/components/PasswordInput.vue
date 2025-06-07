<template>
  <div class="mb-4 flex flex-col">
    <label class="block mb-2 text-gray-700">{{ label }}</label>
    <div class="relative w-full items-center">
      <input
        id="passwordInput"
        v-model="inputValue"
        :type="isPasswordVisible ? 'text' : 'password'"
        :placeholder="placeholder"
        :class="[
          'py-3 ps-4 pe-10 block w-full border-gray-200 border text-sm focus:outline-none',
          !passwordsMatch
            ? 'focus:ring-red-500 focus:ring-2 ring-2 ring-red-300 caret-red-500'
            : 'focus:ring-blue-500 focus:ring-2 caret-blue-500',
          sizeClasses[size],
        ]"
        :pattern="passwordPattern"
      />
      <button
        type="button"
        class="absolute inset-y-0 end-0 flex items-center z-20 px-3 cursor-pointer text-gray-400 rounded-e-md focus:outline-none focus:text-blue-600"
        @click="togglePasswordVisibility"
      >
        <EyeIcon v-if="isPasswordVisible" class="h-5 w-5" />
        <EyeSlashIcon v-else class="h-5 w-5" />
      </button>
    </div>
    <span
      :class="['text-sm mt-1 peer-[&:not(:placeholder-shown):not(:focus):invalid]:text-red-500', condition]"
    >
      {{ remind }}
    </span>
  </div>
</template>

<script setup>
  import { ref, watch, defineProps, defineEmits } from 'vue'
  import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'

  const props = defineProps({
    label: {
      type: String,
      required: true,
    },
    remind: {
      type: String,
      default: '',
    },
    modelValue: {
      type: String,
      default: '',
    },
    id: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: '請輸入密碼',
    },
    passwordsMatch: {
      type: Boolean,
      default: true,
    },
    condition: {
      type: String,
      default: 'text-gray-500',
    },
    size: {
      type: String,
      default: 'base',
      validator: (value) => ['sm', 'md', 'base', 'lg'].includes(value),
    },
  })

  const sizeClasses = {
    base: 'rounded-lg',
    lg: 'h-12 rounded-md',
    md: 'h-10 rounded-lg',
    sm: 'h-8 rounded-full',
  }

  const emit = defineEmits(['update:modelValue'])

  const inputValue = ref(props.modelValue)
  const isPasswordVisible = ref(false)
  const passwordPattern = '^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*.]).{8,}$'

  watch(inputValue, (newValue) => {
    emit('update:modelValue', newValue)
  })

  watch(
    () => props.modelValue,
    (newValue) => {
      inputValue.value = newValue
    }
  )

  const togglePasswordVisibility = () => {
    isPasswordVisible.value = !isPasswordVisible.value
  }
</script>
