<template>
  <div>
    <a
      :href="link"
      :target="target"
      :class="[
        'h-12 rounded-md justify-center items-center inline-flex cursor-pointer hover:underline',
        'focus:outline-none',
        textColor,
      ]"
    >
      {{ text }}
    </a>
  </div>
</template>

<script setup>
  import { defineProps } from 'vue'

  defineProps({
    text: {
      type: String,
      required: true,
    },
    link: {
      type: String,
      required: true,
    },
    px: {
      type: String,
      default: 'px-3',
    },
    textColor: {
      type: String,
      default: 'text-blue-500 hover:text-blue-700',
    },
    target: {
      type: String,
      default: '_self',
    },
  })
</script>
