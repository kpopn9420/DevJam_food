<template>
  <div :class="['mb-3', isOwnMessage ? 'text-right' : 'text-left']">
    <div class="text-xs text-gray-500">
      <span v-if="!isOwnMessage">{{ userId }}</span>
      {{ time }}
    </div>
    <div
      class="px-3 py-2 rounded-xl inline-block max-w-sm md:max-w-lg mt-1 break-words"
      :class="[isOwnMessage ? 'bg-blue-500' : 'bg-gray-200']"
    >
      <template v-if="text">
        <div :class="isOwnMessage ? 'text-white' : 'text-gray-700'">
          {{ text }}
        </div>
      </template>
      <template v-if="audioUrl">
        <audio :src="audioUrl" controls></audio>
      </template>
    </div>
  </div>
</template>

<script setup>
  defineProps({
    text: {
      type: String,
      default: '',
    },
    audioUrl: {
      type: String,
      default: null,
    },
    time: {
      type: String,
      required: true,
    },
    isOwnMessage: {
      type: Boolean,
      default: false,
    },
    userId: {
      type: String,
      default: '',
    },
  })
</script>
