<template>
  <PageLayout headline="">
    <div class="grid sm:flex sm:grid-cols-[auto, auto]">
      <PageMenu class="mb-4">
        <PageMenuItem headline="平台數據" :is-active="pageNum === 0" @click="setPage(0)" />
        <PageMenuItem headline="log紀錄" :is-active="pageNum === 2" @click="setPage(1)" />
      </PageMenu>
      <div class="sm:flex sm:flex-col sm:flex-grow space-y-4 sm:mr-4 mb-4 flex-wrap">
        <template v-if="pageNum === 0">
          <div class="flex justify-around mb-4 text-center">
            <div>
              <div class="text-4xl font-bold">{{ totalUsers }}</div>
              <div class="text-gray-500">總用戶</div>
            </div>
            <div>
              <div class="text-4xl font-bold">{{ activeUsers }}</div>
              <div class="text-gray-500">活躍用戶</div>
            </div>
            <div>
              <div class="relative w-20 h-20 mx-auto">
                <CircularProgress :percentage="activeUsersPercentage" />
              </div>
              <div class="text-gray-500">活躍用戶佔比</div>
            </div>
          </div>
          <StatusTimeline headline="API" :statuses="apiStatuses" />
          <StatusTimeline headline="Server" :statuses="serverStatuses" />
        </template>
        <template v-else-if="pageNum === 1">
          <div class="mx-4">
            <!-- <BaseButtonOutlined
              button-text="匯出.csv"
              border-color="border-blue-500 hover:border-blue-700"
              hover-background-color="bg-blue-100 hover:bg-blue-300"
              text-color="text-blue-500 hover:text-blue-700"
            ></BaseButtonOutlined> -->
            <div class="m-4"></div>
            <div class="flex">
              <BaseSelectorAutofill
                v-model="choose"
                :options="parts"
                headline="類別"
                placeholder="請選擇要查詢的類別"
                class="w-full"
              ></BaseSelectorAutofill>
              <BaseButtonFilled button-text="查詢" width="w-1/12" class="mx-2 my-7"></BaseButtonFilled>
            </div>
            <div class="m-4"></div>
            <DataTable :headers="tableHeaders" :data="tableData"></DataTable>
          </div>
        </template>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
  import { ref, computed } from 'vue'
  import PageLayout from '@/components/PageLayout.vue'
  import PageMenu from '@/components/PageMenu.vue'
  import PageMenuItem from '@/components/PageMenuItem.vue'
  // import BaseButtonOutlined from '@/components/BaseButtonOutlined.vue'
  import BaseSelectorAutofill from '@/components/BaseSelectorAutofill.vue'
  import DataTable from '@/components/DataTable.vue'
  import CircularProgress from '@/components/CircularProgress.vue'
  import StatusTimeline from '@/components/StatusTimeline.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'

  const pageNum = ref(0)
  const setPage = (num) => {
    pageNum.value = num
  }

  const totalUsers = ref(100)
  const activeUsers = ref(67)
  const activeUsersPercentage = computed(() => {
    if (totalUsers.value === 0) return 0
    return (activeUsers.value / totalUsers.value) * 100
  })

  const apiStatuses = [
    { status: 'operational', daysAgo: 90 },
    { status: 'failure', daysAgo: 60, tooltip: 'Failure API: Login API, Upload File API' },
    { status: 'operational', daysAgo: 0 },
  ]

  const serverStatuses = [
    { status: 'operational', daysAgo: 90 },
    { status: 'failure', daysAgo: 70, tooltip: 'Failure Server: Cache Server' },
    { status: 'operational', daysAgo: 40 },
    { status: 'failure', daysAgo: 30, tooltip: 'Failure Server: Database Server, Cache Server' },
    { status: 'operational', daysAgo: 0 },
  ]

  const choose = ref('')
  const parts = [
    { id: 0, name: 'Auth Service' },
    { id: 1, name: 'Roll-call Service' },
    { id: 2, name: 'Discussion Service' },
    { id: 3, name: 'Course Service' },
    { id: 4, name: 'Resource Service' },
    { id: 5, name: 'Public Key Store' },
    { id: 6, name: 'LLM' },
  ]

  const tableHeaders = ['日期', '類別', '程度', '訊息']
  const tableData = [
    ['2024-10-31', '登入', 'warning', 'some warning messages'],
    ['2024-10-31', '登入', 'warning', 'some warning messages'],
    ['2024-10-31', '登入', 'warning', 'some warning messages'],
  ]
</script>
