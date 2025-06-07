<script setup>
  import { ref } from 'vue'
  import BaseButtonOutlined from './BaseButtonOutlined.vue'

  const websiteName = ref('GreenBite')
</script>

<!--Testing-->
<template>
  <nav
    class="relative flex items-center justify-between h-16 px-2 py-3 bg-white mb-3 border-b border-gray-200"
  >
    <div class="container px-4 mx-auto flex items-center justify-between">
      <div
        class="w-full relative flex justify-between items-center lg:w-full px-4 lg:static lg:items-center lg:justify-between"
      >
        <router-link
          to="/"
          class="items-center text-base font-bold leading-relaxed mr-4 py-2 whitespace-nowrap text-gray-700 flex"
        >
          <img src="/src/assets/logo.png" alt="logo" class="w-6 h-6 mr-2" />
          <span class="cursor-pointer hover:text-gray-900">
            {{ websiteName }}
          </span>
        </router-link>
      </div>
    </div>
  </nav>
</template>
