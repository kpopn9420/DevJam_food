<template>
  <PageLayout headline="回報問題">
    <div class="mb-2"></div>
    <div class="grid sm:flex sm:grid-cols-[auto, auto]">
      <PageMenu class="mb-4">
        <PageMenuItem headline="常見問題" :is-active="isFaq" :is-clicked="setFaq"></PageMenuItem>
        <PageMenuItem headline="回報問題" :is-active="!isFaq" :is-clicked="setReport"></PageMenuItem>
      </PageMenu>
      <div class="sm:ml-4 sm:w-full flex-wrap">
        <ContentBox headline="回報問題">
          <div class="w-full flex-col flex space-y-4">
            <div class="flex flex-row w-full space-x-4">
              <BaseInputPlace label="姓" placeholder="example:紀"></BaseInputPlace>
              <BaseInputPlace label="名" placeholder="example:博文"></BaseInputPlace>
            </div>
            <BaseInputPlace label="電子郵件地址" placeholder="example:neokent@gmail.com"></BaseInputPlace>
            <BaseSelectorAutofill headline="問題類型" :options="customOptions" />
            <BaseInputText label="問題描述" placeholder="example:無法連線伺服器"></BaseInputText>
            <BaseButtonFilled class="ml-auto" width="w-fit" size="md" button-text="送出"></BaseButtonFilled>
          </div>
        </ContentBox>
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
  import ContentBox from '@/components/ContentBox.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseInputText from '@/components/BaseInputText.vue'
  import BaseSelectorAutofill from '@/components/BaseSelectorAutofill.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'

  const customOptions = [
    { id: 1, name: '無法連線伺服器' },
    { id: 2, name: '無法登入帳號' },
    { id: 3, name: '無法使用功能' },
    { id: 4, name: '其他問題' },
  ]

  const route = useRoute()
  const isFaq = ref(route.path === '/faq')

  const setFaq = () => {
    router.push('/faq')
  }

  const setReport = () => {
    router.push('/report')
  }
</script>
