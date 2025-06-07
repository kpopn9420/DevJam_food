<script setup>
  import { ref } from 'vue'
  import BaseButtonOutlined from './BaseButtonOutlined.vue'

  const websiteName = ref('ClassBud')
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
        <BaseButtonOutlined
          link="/faq"
          size="md"
          button-text="常見問題"
          border-color="border-blue-500 hover:border-blue-700"
          hover-background-color="bg-blue-100 hover:bg-blue-300"
          text-color="text-blue-500 hover:text-blue-700"
        />
      </div>
    </div>
  </nav>
</template>
