<template>
  <svg class="w-20 h-20 mx-auto" viewBox="0 0 36 36">
    <circle class="stroke-gray-300" stroke-width="3.8" fill="none" cx="18" cy="18" r="16" />

    <circle
      class="stroke-blue-500 transition-[stroke-dasharray] duration-500 ease-in-out"
      :stroke-dasharray="`${computedPercentage}, 100`"
      stroke-width="3.8"
      stroke-linecap="round"
      fill="none"
      cx="18"
      cy="18"
      r="16"
    />

    <text
      x="18"
      y="18"
      class="text-center text-base font-bold fill-current"
      dominant-baseline="middle"
      text-anchor="middle"
    >
      {{ computedPercentage }}%
    </text>
  </svg>
</template>

<script setup>
  import { computed } from 'vue'

  const props = defineProps({
    percentage: {
      type: Number,
      default: 0,
    },
  })

  const computedPercentage = computed(() => {
    return Math.min(100, Math.max(0, props.percentage))
  })
</script>
