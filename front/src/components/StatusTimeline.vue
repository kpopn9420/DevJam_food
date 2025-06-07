<template>
  <div class="my-4">
    <h2 class="text-lg font-semibold">{{ headline }}</h2>
    <div class="relative flex items-center h-6 mt-2">
      <div
        v-for="(status, index) in statuses"
        :key="index"
        :class="{
          'bg-green-500': status.status === 'operational',
          'bg-red-500': status.status === 'failure',
        }"
        :style="{ flexGrow: index === statuses.length - 1 ? '1' : '1', height: '100%' }"
        class="relative"
      >
        <div
          v-if="status.tooltip"
          class="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-white text-gray-800 text-sm p-1 rounded shadow-lg"
        >
          {{ status.tooltip }}
        </div>
      </div>
    </div>
    <div class="flex justify-between text-gray-500 text-xs mt-2">
      <span>90 days ago</span>
      <span>now</span>
    </div>
  </div>
</template>

<script setup>
  const props = defineProps({
    headline: {
      type: String,
      required: true,
    },
    statuses: {
      type: Array,
      required: true,
    },
  })

  console.log(props.headline)
  console.log(props.statuses)
</script>
