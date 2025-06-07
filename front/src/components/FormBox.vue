<template>
  <div
    class="flex flex-col items-center min-h-20 justify-center px-16 py-20 rounded-2xl border border-gray-100 shadow-lg bg-white"
  >
    <p class="text-4xl font-bold text-center mb-2 -mt-6">{{ props.headline }}</p>
    <p class="text-lg font-normal text-center text-gray-700">
      <span>{{ subtitle1 }}</span>
      <span><br /></span>
      <span>{{ subtitle2 }}</span>
    </p>
    <div class="m-2" />
    <slot></slot>
  </div>
</template>

<script setup>
  import { defineProps } from 'vue'

  const props = defineProps({
    headline: {
      type: String,
      required: true,
    },
    subtitle1: {
      type: String,
      required: true,
    },
    subtitle2: {
      type: String,
      required: false,
      default: '',
    },
  })
</script>
