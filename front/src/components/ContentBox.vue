<template>
  <div
    class="p-4 w-full origin-top-left bg-white border flex-col rounded-md justify-start items-start space-y-6 inline-flex transition-all duration-100 max-h-screen"
  >
    <div v-if="showHeadline" class="self-stretch h-5 flex-col justify-center items-start gap-4 flex">
      <div class="text-gray-900 text-lg font-bold leading-tight">{{ headline }}</div>
    </div>
    <div class="self-stretch justify-start items-start gap-12 inline-flex">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
  import { defineProps } from 'vue'
  defineProps({
    headline: {
      type: String,
      default: '',
    },
    showHeadline: {
      type: Boolean,
      default: true, // 預設為顯示
    },
  })
</script>
