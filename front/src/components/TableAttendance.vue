<!-- eslint-disable vue/no-unused-vars -->
<template>
  <div class="overflow-x-auto rounded-md border">
    <table class="min-w-full bg-white shadow-md rounded-lg">
      <thead class="bg-gray-100">
        <tr>
          <th
            class="px-6 py-3 text-center md:text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-3/12 md:w-1/5"
          >
            {{ columnOne }}
          </th>
          <th
            class="px-6 py-3 text-center md:text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-6/12 md:w-2/5"
          >
            {{ columnTwo }}
          </th>
          <th
            class="px-6 py-3 text-center md:text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-4/12 md:w-2/5"
          >
            {{ columnThree }}
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200 align-middle flex-col items-center">
        <tr v-for="item in itemsPaginated" :key="item.name">
          <td class="px-6 py-4 whitespace-nowrap justify-start">
            <div class="flex items-center text-center max-md:space-y-2 max-md:flex-col">
              <img :src="item.avatar" alt="" class="w-10 h-10 rounded-full md:mr-3" />
              <div>
                <div class="text-sm font-medium text-gray-900">{{ item.name }}</div>
              </div>
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-center">
            <RadioGroup v-model="item.status">
              <RadioGroupLabel class="sr-only">出席狀況</RadioGroupLabel>
              <div class="flex flex-wrap gap-2">
                <RadioGroupOption
                  v-for="status in attendanceStatuses"
                  :key="status.name"
                  v-slot="{ active, checked }"
                  as="template"
                  :value="status.name"
                >
                  <div
                    :class="[
                      checked ? checkedColor(status) : hoverColor(status),
                      checked ? 'text-white' : textColor(status),
                      'relative flex cursor-pointer rounded-lg px-3 py-2 border hover:shadow-md focus:outline-none transition-colors',
                      { 'opacity-75': checked },
                    ]"
                  >
                    <div class="flex w-full items-center justify-between">
                      <div class="flex items-center">
                        <div class="text-sm">
                          <RadioGroupLabel class="font-medium text-center">
                            {{ status.name }}
                          </RadioGroupLabel>
                          <RadioGroupDescription as="span" class="inline">
                            <span>{{ status.description }}</span>
                          </RadioGroupDescription>
                        </div>
                      </div>
                      <div class="shrink-0 ml-2" :class="[checked ? 'text-white' : textColor(status)]">
                        <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none">
                          <circle cx="12" cy="12" r="12" fill="#fff" fill-opacity="0.2" />
                          <path
                            d="M7 13l3 3 7-7"
                            stroke="#fff"
                            stroke-width="1.5"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          />
                        </svg>
                      </div>
                    </div>
                  </div>
                </RadioGroupOption>
              </div>
            </RadioGroup>
          </td>
          <td class="px-6 py-4 items-center text-center">
            <BaseInputPlace v-model="item.detail" :label-visible="false" placeholder="請輸入額外資訊" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <PageSelector :total-pages="totalPages" :current-page="currentPage" @page-changed="updateCurrentPage" />
</template>

<script setup>
  import { computed, ref } from 'vue'
  import { RadioGroup, RadioGroupDescription, RadioGroupLabel, RadioGroupOption } from '@headlessui/vue'
  import BaseInputPlace from './BaseInputPlace.vue'
  import PageSelector from './BasePaginator.vue'

  const props = defineProps({
    columnOne: {
      type: String,
      default: '學生姓名',
    },
    columnTwo: {
      type: String,
      default: '出席狀況',
    },
    columnThree: {
      type: String,
      default: '備註',
    },
    items: {
      type: Array,
      default: () => [],
    },
  })

  const totalPages = computed(() => Math.ceil(props.items.length / itemsPerPage))

  // 出席狀況選項
  const attendanceStatuses = [
    { name: '出席', description: '' },
    { name: '遲到', description: '' },
    { name: '請假', description: '' },
    { name: '曠課', description: '' },
  ]

  // 顏色函數
  const hoverColor = (status) => {
    const colors = {
      出席: 'hover:bg-green-300 hover:border-green-200 hover:bg-opacity-30 hover:shadow-green-100',
      遲到: 'hover:bg-amber-300 hover:border-amber-200 hover:bg-opacity-30 hover:shadow-amber-100',
      請假: 'hover:bg-blue-300 hover:border-blue-200 hover:bg-opacity-30 hover:shadow-blue-100',
      曠課: 'hover:bg-red-300 hover:border-red-200 hover:bg-opacity-30 hover:shadow-red-100',
    }
    return colors[status.name] || ''
  }

  const checkedColor = (status) => {
    const colors = {
      出席: 'bg-green-600 text-white',
      遲到: 'bg-amber-500 text-white',
      請假: 'bg-blue-700 text-white',
      曠課: 'bg-red-600 text-white',
    }
    return colors[status.name] || ''
  }

  const textColor = (status) => {
    const colors = {
      出席: 'text-gray-700 hover:text-green-700',
      遲到: 'text-gray-700 hover:text-amber-700',
      請假: 'text-gray-700 hover:text-blue-700',
      曠課: 'text-gray-700 hover:text-red-700',
    }
    return colors[status.name] || ''
  }

  const itemsPerPage = 10
  const currentPage = ref(1)

  const updateCurrentPage = (page) => {
    currentPage.value = page
  }

  const itemsPaginated = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    const end = start + itemsPerPage
    return props.items.slice(start, end)
  })
</script>
