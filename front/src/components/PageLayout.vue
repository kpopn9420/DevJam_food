<template>
  <div class="flex h-svh overflow-y-auto">
    <BaseSidebar class="flex sticky top-0" />
    <main class="wrap flex-auto m-4 space-y-2">
      <h1 class="text-4xl font-bold">{{ headline }}</h1>
      <slot class="flex mb-4"></slot>
    </main>
  </div>
</template>

<script setup>
  import BaseSidebar from '@/components/BaseSidebar.vue'
  defineProps({
    headline: {
      type: String,
      default: '標題',
    },
  })
</script>
