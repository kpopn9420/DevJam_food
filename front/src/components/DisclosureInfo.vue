<template>
  <div class="w-full">
    <div
      :class="[
        'mx-auto w-full rounded-lg bg-white p-2 transition-all duration-200',
        border ? 'border' : '',
        shadow ? 'hover:shadow-md focus-within:shadow-md peer-open:shadow-md' : '',
      ]"
    >
      <Disclosure v-slot="{ open }">
        <div class="flex">
          <DisclosureButton
            :class="[
              'flex w-full items-center justify-between rounded-md px-4 py-2 text-left text-gray-900 hover:bg-blue-200 hover:text-blue-700 hover:bg-opacity-20 focus:outline-none focus-visible:ring focus-visible:ring-purple-500/75 transition-all duration-200',
              headlineFontSize,
              headlineFontWeight,
            ]"
          >
            <span class="break-words whitespace-normal max-w-[50%]">{{ localHeadline }}</span>
            <div class="flex items-center">
              <span v-if="showDate" class="align-right text-gray-500 mr-2">{{ date }}</span>
              <ChevronUpIcon
                v-if="!editable"
                :class="
                  open ? 'rotate-180 transform transition-all duration-200' : 'transition-all duration-200'
                "
                class="h-6 w-6 text-gray-500"
              />
            </div>
          </DisclosureButton>
          <BaseButtonGhost
            v-if="editable"
            size="md"
            width="w-fit"
            button-text=""
            icon-name="IconPencil"
            bg-color="bg-gray-100 bg-opacity-50"
            hover-color="hover:bg-gray-200 hover:bg-opacity-50"
            text-color="text-gray-500"
            @click="openDialog"
          />
        </div>

        <DisclosurePanel
          class="px-4 pb-2 pt-4 text-sm text-gray-500 break-words whitespace-normal"
          :class="`max-w-[${maxWidth}%]`"
        >
          {{ localContent }}
          <slot></slot>
        </DisclosurePanel>
      </Disclosure>
    </div>
  </div>
  <PageDialog class="hidden" :dialog-title="dialogTitle" :is-open="isDialog" @close="closeDialog">
    <div class="space-y-4">
      <BaseInputPlace v-model="headlineEdit" label="標題" placeholder="請輸入標題..." />
      <BaseInputText v-model="contentEdit" label="內容" placeholder="請輸入內容..." />
      <div class="mt-2 flex space-x-2">
        <BaseButtonFilled
          button-text="刪除"
          bg-color="bg-red-500 hover:bg-red-700"
          width="w-full"
          @click="deleteInfo"
        />
        <BaseButtonFilled button-text="確認" width="w-full" @click="editInfo" />
      </div>
    </div>
  </PageDialog>
</template>

<script setup>
  import { ref, defineEmits } from 'vue'
  import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
  import { ChevronUpIcon } from '@heroicons/vue/20/solid'
  import BaseButtonGhost from './BaseButtonGhost.vue'
  import PageDialog from './PageDialog.vue'
  import BaseInputPlace from './BaseInputPlace.vue'
  import BaseButtonFilled from './BaseButtonFilled.vue'
  import BaseInputText from './BaseInputText.vue'

  const props = defineProps({
    headlineFontSize: {
      type: String,
      default: 'text-base',
    },
    headlineFontWeight: {
      type: String,
      default: 'font-medium',
    },
    headline: {
      type: String,
      required: true,
      default: '標題',
    },
    content: {
      type: String,
      required: true,
      default: '內容',
    },
    showDate: {
      type: Boolean,
      default: true,
    },
    date: {
      type: String,
      default: '2024/11/11',
    },
    editable: {
      type: Boolean,
      default: true,
    },
    dialogTitle: {
      type: String,
      default: '編輯',
    },
    id: {
      type: Number,
      required: true,
    },
    border: {
      type: Boolean,
      default: false,
    },
    shadow: {
      type: Boolean,
      default: false,
    },
    maxWidth: {
      type: String,
      default: '50', // 預設為 '50' 對應於 Tailwind 類別 max-w-[50%]
    },
  })

  const isDialog = ref(false)

  const localHeadline = ref(props.headline)
  const localContent = ref(props.content)

  const headlineEdit = ref(props.headline)
  const contentEdit = ref(props.content)

  const editInfo = () => {
    localHeadline.value = headlineEdit.value
    localContent.value = contentEdit.value
    closeDialog()
  }

  const emit = defineEmits(['delete'])

  const deleteInfo = () => {
    emit('delete', props.id)
    closeDialog()
  }

  const openDialog = () => {
    isDialog.value = true
  }

  const closeDialog = () => {
    isDialog.value = false
  }
</script>
