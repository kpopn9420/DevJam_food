<script setup>
  import { defineProps, ref, watch, onMounted, onUnmounted } from 'vue'

  const props = defineProps({
    bgColor: {
      type: String,
      default: 'bg-blue-500',
    },
    hoverColor: {
      type: String,
      default: 'hover:bg-blue-700',
    },
    width: {
      type: String,
      default: 'w-full',
    },
    textColor: {
      type: String,
      default: 'text-white',
    },
    buttonText: {
      type: String,
      default: '按鈕',
    },
    size: {
      type: String,
      default: 'lg',
      validator: (value) => ['lg', 'md', 'sm'].includes(value),
    },
    countdownTime: {
      type: Number,
      default: 0,
    },
    isCounting: {
      type: Boolean,
      default: false,
    },
  })

  const sizeClasses = {
    lg: 'h-12 px-3 py-4 rounded-md',
    md: 'h-10 px-2 py-3 rounded-lg',
    sm: 'h-8 px-2 py-2 rounded-full',
  }

  const countdown = ref(0)
  const isDisabled = ref(false)
  let timer = null

  const startCountdown = () => {
    if (!props.isCounting) return

    countdown.value = props.countdownTime - 1
    isDisabled.value = true

    timer = setInterval(() => {
      if (countdown.value > 0) {
        countdown.value -= 1
      } else {
        isDisabled.value = false
        clearInterval(timer)
      }
    }, 1000)
  }

  watch(
    () => props.isCounting,
    (newVal) => {
      if (newVal) {
        startCountdown()
      } else {
        clearInterval(timer)
        isDisabled.value = false
      }
    }
  )

  onUnmounted(() => {
    if (timer) clearInterval(timer)
  })

  onMounted(() => {
    if (props.isCounting) {
      startCountdown()
    }
  })

  const emit = defineEmits(['click'])
  const handleClick = () => {
    if (!isDisabled.value) {
      emit('click')
      startCountdown()
    }
  }
</script>

<template>
  <div
    :class="[
      'justify-center items-center inline-flex cursor-pointer transition-all duration-100',
      width,
      bgColor,
      isDisabled ? 'cursor-not-allowed' : hoverColor,
      sizeClasses[props.size],
    ]"
    :style="{ opacity: isDisabled ? 0.6 : 1 }"
    @click="handleClick"
  >
    <div :class="['justify-center items-center flex', size === 'sm' || size === 'md' ? 'px-2' : 'px-4']">
      <div
        :class="[
          'text-white font-medium leading-none text-center tracking-wide',
          size === 'sm' ? 'text-sm' : 'text-base',
        ]"
      >
        {{ props.isCounting && isDisabled ? `重新傳送連結(${countdown + 1})` : props.buttonText }}
        <slot></slot>
      </div>
    </div>
  </div>
</template>
