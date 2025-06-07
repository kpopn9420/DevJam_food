<template>
  <main class="flex items-center justify-center h-screen">
    <article
      class="max-w-lg text-center mb-10 grid grid-cols-1 md:grid-cols-[auto,auto,auto] mx-auto gap-4 items-center"
    >
      <h1 class="text-5xl font-light mb-2 md:mb-0 items-center">404</h1>
      <div class="block md:hidden w-full border-t-2 border-gray-300" />
      <div class="hidden md:block md:h-16 border-l-2 border-gray-300 mx-0" />
      <p class="text-gray-500 mb-4 md:mb-0 md:text-justify items-center">
        看來這裡沒有你要找的東西... <br />
        要不要<router-link to="/" class="text-blue-500 font-medium hover:underline hover:text-blue-700">
          回首頁 </router-link
        >呢？
      </p>
    </article>
  </main>
</template>
