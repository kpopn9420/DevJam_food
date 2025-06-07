<template>
  <div class="w-full">
    <div :class="['mx-auto w-full rounded-lg bg-white p-2', border ? 'border' : '']">
      <Disclosure v-slot="{ open }">
        <div class="flex">
          <DisclosureButton
            class="flex w-full items-center justify-between rounded-md px-4 py-2 text-left text-base font-medium text-gray-900 hover:bg-blue-200 hover:text-blue-700 hover:bg-opacity-20 focus:outline-none focus-visible:ring focus-visible:ring-purple-500/75 transition-all duration-200"
          >
            <div class="flex items-center">
              <span v-if="isActive" class="relative flex h-2.5 w-2.5 mr-4">
                <span
                  :class="[
                    'animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75',
                  ]"
                ></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-600"></span>
              </span>
              <span>{{ localHeadline }}</span>
            </div>
            <div class="flex">
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

        <DisclosurePanel class="px-4 pb-2 pt-4 text-sm text-gray-500">
          {{ localContent }}
          <div v-if="link" class="mt-2">
            問卷連結: <BaseLink :link="link" :text="link" target="_blank"/>
          </div>
          <p class="mb-2">LLM 模型: {{ LLM_model }}</p>
          <BaseButtonFilled
            button-text="進入討論區"
            size="md"
            class="cursor-pointer"
            @click="$router.push({ name: 'StudentDiscuss', params: { id: courseId } })"
          />
        </DisclosurePanel>
      </Disclosure>
    </div>
  </div>
  <PageDialog class="hidden" :dialog-title="dialogTitle" :is-open="isDialog" @close="closeDialog">
    <div class="space-y-4">
      <BaseInputPlace
        v-model="headlineEdit"
        label="主題名稱"
        placeholder="Please enter the topic..."
      ></BaseInputPlace>
      <BaseInputText
        v-model="contentEdit"
        label="細節補充"
        placeholder="Write Something..."
        class="resize-y"
      ></BaseInputText>
      <BaseSelector
        size="md"
        headline="LLM模型"
        :options="modelOptions"
        :selection="modelOptions.findIndex((option) => option.value === selectedModel)"
        class="mb-4 w-auto"
        @update:model="onModelChange"
      />
      <div class="flex items-center justify-start mb-2">
        <BaseButtonOutlined
          button-text="修改教案"
          size="md"
          link=""
          border-color="border-blue-500"
          text-color="text-blue-500"
          @click="openFile('PDFCourse')"
        ></BaseButtonOutlined>
        <div v-if="!fileData?.PDFCourse?.file" class="px-3">非必填，填了可經LLM分析引導學生討論</div>
        <div v-else class="px-3 flex items-center">
          hi
          <TrashIcon class="px-1 w-8 h-8 text-gray-500" @click="deleteFile('PDFCourse')" />
        </div>
      </div>
      <BaseInputPlace label="問題連結" placeholder="https://...."></BaseInputPlace>
      <div class="flex items-center justify-start mb-2">
        <BaseButtonOutlined
          button-text="新增附件"
          size="md"
          link=""
          border-color="border-blue-500"
          text-color="text-blue-500"
          @click="openFile('relatedData')"
        ></BaseButtonOutlined>
        <PageDialog dialog-title="上傳檔案" :is-open="isFileOpen" @close="closeFile">
          <div class="mb-4">
            <InputFile :file-types="'ppt, pdf'" @drop.prevent="drop" @change="selectedFile" />
          </div>
          <div v-if="fileData[fileType]?.file" class="text-sm text-gray-600 mt-2">
            <p>檔案名稱：{{ fileData[fileType]?.file?.name }}</p>
            <p>檔案大小：{{ (fileData[fileType]?.file?.size / 1024).toFixed(2) }} KB</p>
          </div>
          <div v-if="fileData[fileType]?.url" class="mt-4">
            <p class="text-sm text-gray-600">檔案預覽：</p>
            <a :href="fileData[fileType]?.url" target="_blank" class="text-blue-500 hover:underline"
              >點此查看檔案</a
            >
          </div>
          <div class="mt-4">
            <BaseButtonFilled button-text="儲存檔案" @click="handleSaveFile" />
          </div>
        </PageDialog>
        <div v-if="!fileData?.relatedData?.file" class="px-3">非必填</div>
        <div v-else class="px-3 flex items-center">
          hi
          <TrashIcon class="px-1 w-8 h-8 text-gray-500" @click="deleteFile('relatedData')" />
        </div>
      </div>
      <div class="flex justify-between mt-4 space-x-2">
        <BaseButtonFilled
          button-text="刪除"
          bg-color="bg-red-500"
          hover-color="hover:bg-red-700"
          class="w-44 h-12"
          @click="deleteTopic"
        />
        <BaseButtonFilled button-text="儲存" class="w-44 h-12" @click="editTopic" />
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
  import BaseButtonOutlined from './BaseButtonOutlined.vue'
  import BaseInputText from './BaseInputText.vue'
  import BaseLink from './BaseLink.vue'
  import InputFile from '@/components/InputFile.vue'
  import BaseSelector from './BaseSelector.vue'
  import { TrashIcon } from '@heroicons/vue/24/outline'
  import { useFileHandler } from '@/composables/useFileHandler'

  const props = defineProps({
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
    isActive: {
      type: Boolean,
      default: false,
    },
    link: {
      type: String,
      required: true,
    },
  })

  const isDialog = ref(false)

  const localHeadline = ref(props.headline)
  const localContent = ref(props.content)
  const LLM_model = ref('llama 3.1 8B')

  const openDialog = () => {
    headlineEdit.value = localHeadline.value
    contentEdit.value = localContent.value
    isDialog.value = true
  }

  const closeDialog = () => {
    localHeadline.value = headlineEdit.value
    localContent.value = contentEdit.value
    isDialog.value = false
  }

  const notificationData = {
    open: ref(false),
    type: ref('info'),
    headline: ref('系統通知'),
    content: ref('這是一則系統通知'),
  }

  const notificationHandler = (notification) => {
    notificationData.open.value = true
    notificationData.type.value = notification.type
    notificationData.headline.value = notification.headline
    notificationData.content.value = notification.content
  }

  const {
    fileData,
    fileType,
    isFileOpen,
    initializeFileData,
    openFile,
    closeFile,
    drop,
    selectedFile,
    deleteFile,
    saveFile,
  } = useFileHandler(notificationHandler)

  initializeFileData(['PDFCourse', 'relatedData'])
  const saveHandlers = {
    PDFCourse: async (file) => {
      console.log('Saving PDF Course file:', file)
      console.log('File name:', file.name)
    },
    relatedData: async (file) => {
      console.log('Saving related data file:', file)
      console.log('File name:', file.name)
    },
  }

  const handleSaveFile = () => {
    console.log(fileData)
    console.log(fileData.name)
    saveFile(saveHandlers)
  }

  const headlineEdit = ref(props.headline)
  const contentEdit = ref(props.content)
  const editTopic = () => {
    localHeadline.value = headlineEdit.value
    localContent.value = contentEdit.value
    closeDialog()
  }
  const selectedModel = ref('llama3.1_8B')
  const modelOptions = [
    { id: 1, title: 'llama 3.1 8B', value: 'llama3.1_8B' },
    { id: 2, title: 'llama 3.2 1B', value: 'llama3.2_1B' },
  ]

  const onModelChange = (option) => {
    selectedModel.value = option.value
  }
  const emit = defineEmits(['delete'])
  const deleteTopic = () => {
    emit('delete', props.id)
    closeDialog()
  }
</script>
