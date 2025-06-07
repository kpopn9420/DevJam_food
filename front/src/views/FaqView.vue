<template>
  <PageLayout headline="常見問題">
    <div class="mb-2"></div>
    <div class="grid sm:flex sm:grid-cols-[auto, auto]">
      <PageMenu class="mb-4">
        <PageMenuItem headline="常見問題" :is-active="isFaq" :is-clicked="setFaq"></PageMenuItem>
        <PageMenuItem headline="回報問題" :is-active="!isFaq" :is-clicked="setReport"></PageMenuItem>
      </PageMenu>
      <div class="space-y-2 sm:ml-4 sm:w-full mb-4 flex-wrap">
        <DisclosureInfo
          v-for="(item, index) in items"
          :key="index"
          :shadow="true"
          :headline="item.question"
          :content="item.answer"
          :border="true"
          :show-date="false"
          :editable="false"
          :max-width="'100'"
        />
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRoute } from 'vue-router'
  import PageLayout from '@/components/PageLayout.vue'
  import PageMenu from '@/components/PageMenu.vue'
  import PageMenuItem from '@/components/PageMenuItem.vue'
  import router from '@/router'
  import DisclosureInfo from '@/components/DisclosureInfo.vue'

  const faq = ref([
    { question: '過去課程可以存放多久？', answer: '只存到上學期的資料' },
    {
      question: '什麼時候可以進入點名系統 & 分組系統？',
      answer: '須先進入任一堂課程才會有對應到該課程的資料',
    },
    {
      question: '如何簽到？',
      answer: '學生可掃描老師顯示的QR code點名 或 由老師手動按下每個學生的狀態，送出後即繳交資料',
    },
    {
      question: '討論區的LLM 模型由誰切換？',
      answer: '只有老師可以切換，若是個人AI聊天室則可由使用者自行切換',
    },
  ])

  const items = faq.value
  const route = useRoute()
  const isFaq = ref(route.path === '/faq')

  const setFaq = () => {
    router.push('/faq')
  }

  const setReport = () => {
    router.push('/report')
  }
</script>
