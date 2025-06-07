<template>
  <div
    class="w-11/12 max-w-4xl min-h-[350px] max-h-[350px] p-5 bg-gray-100 rounded-lg shadow-lg overflow-y-auto text-center"
  >
    <slot></slot>

    <div v-if="isListening" class="text-blue-500 text-lg my-4">正在輸入語音...</div>
    <div v-if="isTyping" class="text-blue-500 text-lg my-4">正在輸入文字...</div>
  </div>
</template>

<script setup>
  defineProps({
    isListening: {
      type: Boolean,
      default: false,
    },
    isTyping: {
      type: Boolean,
      default: false,
    },
  })
</script>

<style scoped></style>
