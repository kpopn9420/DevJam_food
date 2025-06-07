<script setup>
  import { ref } from 'vue'

  const companyName = ref('ClassBud')
  const year = ref(new Date().getFullYear())
  const contactInfo = ref({
    title: '聯絡我們',
    email: 'example@example.com',
    phone: '02-1234-5678',
  })
</script>

<template>
  <div
    class="w-full h-26 px-20 py-12 bg-gray-500 flex flex-col md:flex-row justify-center items-center gap-10"
  >
    <div class="flex-grow text-white text-sm font-normal leading-tight text-center md:text-left">
      {{ companyName }} @ {{ year }}. All rights reserved.
    </div>
    <div class="flex-grow text-center md:text-right text-sm text-white">
      <span class="font-semibold">{{ contactInfo.title }}</span
      ><br />
      <span>{{ contactInfo.email }}</span
      ><br />
      <span>{{ contactInfo.phone }}</span>
    </div>
  </div>
</template>
