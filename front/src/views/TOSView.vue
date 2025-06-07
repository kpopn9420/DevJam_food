<template>
  <PageLayout headline="隱私權及使用者條款">
    <div class="w-full">
      <span class="text-gray-700 font-bold leading-none">最後更新時間：</span
      ><span class="text-gray-700 font-normal leading-none">{{ time }}</span>
    </div>
    <ContentBox :show-headline="false">
      <div class="w-full flex-col">
        <h2 class="text-lg font-bold w-full">隱私權政策</h2>
        <p class="text-base mb-4">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas commodo magna ut dapibus finibus.
          Sed egestas aliquam eros volutpat tempus. Proin cursus iaculis semper. Aliquam erat volutpat. Morbi
          sed mollis est. Curabitur ullamcorper laoreet enim placerat facilisis. Lorem ipsum dolor sit amet,
          consectetur adipiscing elit.
        </p>
        <h2 class="text-lg font-bold w-full">使用者條款</h2>
        <p class="text-base mb-4">
          Sed dolor leo, faucibus sit amet suscipit ac, luctus vitae ex. Ut ultricies tortor at lorem
          dignissim vehicula eget id odio. Donec sagittis hendrerit consequat. Quisque vehicula in metus ac
          tincidunt. Nunc blandit commodo est, sed hendrerit dolor volutpat eget. Phasellus consectetur neque
          eu nisi rutrum auctor. Donec tempor scelerisque neque, in cursus ipsum egestas et. Maecenas
          fermentum elementum risus, non commodo ex congue vitae. Duis ut pulvinar ante. Cras vitae vulputate
          nisi. Sed eget facilisis dolor, vitae ultricies ipsum. Vivamus quis leo quis justo varius eleifend.
          Maecenas lacinia neque laoreet purus laoreet accumsan. Donec pharetra nibh finibus sapien pretium
          ultricies at et nunc.
        </p>
      </div>
    </ContentBox>
  </PageLayout>
</template>

<script setup>
  import ContentBox from '@/components/ContentBox.vue'
  import PageLayout from '@/components/PageLayout.vue'

  const time = new Date().toLocaleDateString()
</script>
