<template>
  <div
    class="relative w-full max-w-sm rounded-lg border border-dashed border-indigo-200 shadow-md overflow-hidden bg-white hover:shadow-lg transition"
  >
    <!-- Header: Title + Image -->
    <div class="p-4 pb-0">
      <!-- Title -->
      <h2 class="text-sm font-medium text-gray-900 mb-2">
        {{ title }}
      </h2>

      <!-- Image -->
      <div class="relative aspect-video w-full overflow-hidden rounded-md bg-gray-200">
        <img v-if="imageUrl" :src="imageUrl" :alt="imageAlt || title" class="h-full w-full object-cover" />
        <div v-else class="flex h-full w-full items-center justify-center">
          <div class="rounded-md border-2 border-gray-300 p-4">
            <X class="h-12 w-12 text-gray-400" />
          </div>
        </div>
      </div>
    </div>

    <!-- Footer: Icons + More -->
    <div class="flex justify-between items-center px-4 py-2">
      <!-- 左側：頭像區塊 -->
      <div class="flex items-center space-x-1">
        <div
          v-for="n in 4"
          :key="n"
          class="w-6 h-6 rounded-full bg-gray-200 border border-gray-300 flex items-center justify-center text-xs text-gray-500"
        >
          <UserIcon class="w-3 h-3" />
        </div>
      </div>

      <!-- 右側：Popover -->
      <Popover :options="menuOptions" />
    </div>

    <!-- Description -->
    <div class="px-4 pb-4 text-sm text-gray-600">
      {{ description }}
    </div>
  </div>
  <PageDialog :is-open="showEditDialog" dialog-title="修改商品" @close="showEditDialog = false">
    <div class="mb-4">
      <BaseInputPlace
        v-model="newAnnouncementTitle"
        label="品項名稱"
        placeholder="Please enter the food name..."
      ></BaseInputPlace>
    </div>
    <div class="mb-4">
      <BaseInputPlace
        v-model="newAnnouncementTitle"
        label="數量"
        placeholder="How many..."
      ></BaseInputPlace>
    </div>
    <div class="mb-4">
      <SelectDate
        v-model="newAnnouncementDate"
        label="保存期限"
      />
    </div>
    <div class="mb-4">
      <BaseInputPlace
        v-model="newAnnouncementTitle"
        label="店家名稱"
        placeholder="Please enter the store name..."
      ></BaseInputPlace>
    </div>
    <div class="mb-4">
      <BaseInputPlace
        v-model="newAnnouncementTitle"
        label="地址"
        placeholder="Please enter the address..."
      ></BaseInputPlace>
    </div>
    <div>
      <BaseInputText
        v-model="newAnnouncementContent"
        label="補充說明"
        placeholder="Short description..."
        class="resize-y min-h-32"
      ></BaseInputText>
    </div>
    <div class="mt-4">
      <BaseButtonFilled button-text="儲存" @click="handleSaveFile" />
    </div>
  </PageDialog>
  <PageDialog :is-open="showDeleteDialog" dialog-title="刪除商品" @close="showDeleteDialog = false">
    <div class="text-sm text-gray-700 mb-4">
      確定要刪除此商品嗎？此操作無法撤銷。
    </div>
    <div class="flex justify-end space-x-2">
      <BaseButtonFilled button-text="取消" @click="showDeleteDialog = false" />
      <BaseButtonFilled button-text="刪除" bgColor="bg-red-500" hoverColor="hover:bg-red-700" @click="handleDeleteFile" />
    </div>
  </PageDialog>
  <PageDialog :is-open="showReserveDialog" dialog-title="預約商品" @close="showReserveDialog = false">
    <div class="mb-4">
      <SelectTime
        v-model="newAnnouncementDate"
        label="預約取貨時間"
      />
    </div>
    <div class="mt-4">
      <BaseButtonFilled button-text="預約" @click="showReserveDialog = false" />
    </div>
  </PageDialog>
</template>

<script setup>
  import { ref } from 'vue'
  import Popover from './Popover.vue'
  import { computed } from 'vue'
  import PageDialog from '@/components/PageDialog.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseInputText from '@/components/BaseInputText.vue'
  import SelectDate from '@/components/SelectDate.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import SelectTime from '@/components/SelectTime.vue'
  import { EllipsisHorizontalIcon } from '@heroicons/vue/20/solid'
  import { TrashIcon, PencilIcon, CalendarIcon } from '@heroicons/vue/24/outline'

  const { role } = defineProps({
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    imageUrl: {
      type: String,
      default: '',
    },
    imageAlt: {
      type: String,
      default: '',
    },
    role: {
      type: String,
      default: 'viewer',
    },
  })

  const showEditDialog = ref(false)
  const showDeleteDialog = ref(false)
  const showReserveDialog = ref(false)

  const menuOptions = computed(() => {
    if (role === 'admin') {
      return [
        {
          name: 'Edit',
          description: 'Edit this item',
          href: '#',
          icon: PencilIcon,
          onClick: () => {
            console.log('Before:', showEditDialog.value)
            showEditDialog.value = true
            console.log('After:', showEditDialog.value)
          },
        },
        {
          name: 'Delete',
          description: 'Delete this item',
          href: '#',
          icon: TrashIcon,
          onClick: () => {
            showDeleteDialog.value = true
          },
        },
      ]
    } else {
      return [
        {
          name: 'Reserve',
          description: 'Reserve this item',
          href: '#',
          icon: CalendarIcon,
          onClick: () => {
            showReserveDialog.value = true
          },
        },
      ]
    }
  })
</script>
