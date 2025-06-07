<script setup>
  import { computed } from 'vue'
  import { useRoute, RouterView } from 'vue-router'
  import BaseFooter from '@/components/BaseFooter.vue'
  import BaseHeader from '@/components/BaseHeader.vue'
  const route = useRoute()
  const showHeader = computed(() => {
    return (
      route.path === '/login' ||
      route.path === '/register' ||
      route.path === '/forget-password' ||
      route.path === '/reset-password' ||
      route.path === '/set-password' ||
      route.path === '/check-email'
    )
  })
</script>

<template>
  <div class="bg-gray-50">
    <BaseHeader v-if="showHeader" class="sticky top-0" />
    <RouterView />
    <BaseFooter />
  </div>
</template>
