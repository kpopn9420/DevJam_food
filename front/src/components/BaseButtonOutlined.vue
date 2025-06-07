<template>
  <router-link :to="link">
    <button
      :class="[
        'leading-none border-solid bg-transparent block outline-none flex-shrink-0 bg-opacity-10 hover:bg-opacity-10 hover:shadow-md transition-all duration-100 ease-in-out',
        borderColor,
        hoverBackgroundColor,
        textColor,
        sizeClasses[size],
        borderSize,
      ]"
      type="button"
    >
      <div :class="['justify-center items-center flex', size === 'sm' || size === 'md' ? 'px-2' : 'px-4']">
        {{ buttonText }}
      </div>
    </button>
  </router-link>
</template>

<script setup>
  import { RouterLink } from 'vue-router'

  defineProps({
    link: {
      type: String,
      default: '',
    },
    buttonText: {
      type: String,
      default: '按鈕',
    },
    borderColor: {
      type: String,
      default: 'border-gray-300 hover:border-gray-500',
    },
    hoverBackgroundColor: {
      type: String,
      default: 'hover:bg-gray-300',
    },
    textColor: {
      type: String,
      default: 'text-gray-500 hover:text-gray-700',
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['lg', 'md', 'sm', 'xs'].includes(value),
    },
    borderSize: {
      type: String,
      default: 'border',
    },
  })

  const sizeClasses = {
    lg: 'h-12 px-3 py-4 rounded-md text-base',
    md: 'h-10 px-3 py-2 rounded-lg text-base',
    sm: 'h-8 px-2 py-2 rounded-full text-sm',
    xs: 'h-6 px-2 py-1 text-xs',
  }
</script>
