<template>
  <BaseBanner
    :is-open="notificationData.open.value"
    :type="notificationData.type.value"
    :headline="notificationData.headline.value"
    :content="notificationData.content.value"
    @close="notificationData.open.value = false"
  />

  <PageLayout headline="軟體工程">
    <div class="flex justify-between items-center">
      <div class="text-gray-700 font-bold leading-none">二 10:20~12:10、四 11:20~12:10</div>
      <div class="flex justify-end items-center space-x-2">
        <CourseTab v-if="showButton" v-model="isMenuOpen" />
      </div>
    </div>
    <div class="grid md:flex md:grid-col-[1fr,1fr] w-full mb-4 items-start">
      <div class="w-full p-4 bg-gray-200 rounded-md flex-grow min-h-4/5 mb-4 sm:mr-4 flex flex-col">
        <p class="text-2xl font-semibold pb-2.5">課程公告</p>
        <div class="pb-2 space-y-2 w-full">
          <!--公告列表（沒寫死的版本）-->
          <DisclosureInfo
            v-for="announcement in announcements"
            :id="announcement.id"
            :key="announcement.id"
            :editable="showButton"
            :headline="announcement.title"
            :content="announcement.content"
            dialog-title="編輯公告"
            @delete="deleteInfo"
          >
          </DisclosureInfo>
        </div>
        <!--新增公告的彈出式頁面-->
        <div class="mt-auto">
          <BaseButtonGhost
            v-if="showButton"
            size="md"
            button-text="新增公告"
            text-align="text-left"
            @click="announcementsOpen"
          />
          <PageDialog :is-open="isAnnouncementsOpen" dialog-title="新增公告" @close="announcementsClose">
            <div class="mb-4">
              <BaseInputPlace
                v-model="newAnnouncementTitle"
                label="公告標題"
                placeholder="Please enter the topic..."
              ></BaseInputPlace>
            </div>
            <div class="mb-4">
              <BaseInputText
                v-model="newAnnouncementContent"
                label="公告內文"
                placeholder="Please enter the topic..."
                class="resize-y min-h-32"
              ></BaseInputText>
            </div>
            <div class="mt-4">
              <BaseButtonFilled button-text="儲存" class="w-full" @click="addAnnouncement" />
            </div>
          </PageDialog>
        </div>
      </div>

      <div class="w-full p-4 bg-gray-200 flex-grow mb-4 min-h-4/5 rounded-md flex flex-col">
        <p class="text-2xl font-semibold pb-2.5">課程主題</p>
        <div class="pb-2 space-y-2 w-full">
          <DisclosureTopic
            v-for="topic in topics"
            :id="topic.id"
            :key="topic.id"
            :editable="showButton"
            :headline="topic.title"
            :content="topic.content"
            :is-active="topic.isActive"
            :link="topic.source"
            dialog-title="編輯"
            @delete="deleteTopic"
          ></DisclosureTopic>
        </div>
        <div class="mt-auto">
          <BaseButtonGhost
            v-if="showButton"
            size="md"
            button-text="新增主題"
            text-align="text-center"
            @click="topicsOpen"
          />
          <PageDialog dialog-title="新增主題" :is-open="isTopicsOpen" @close="topicsClose">
            <div class="mb-4">
              <BaseInputPlace
                v-model="newTopicTitle"
                label="主題名稱"
                placeholder="Please enter the topic..."
              />
            </div>
            <div class="mb-4">
              <BaseInputText
                v-model="newTopicContent"
                label="細節補充"
                placeholder="Write Something..."
                class="resize-y"
              />
            </div>
            <BaseSelector
              size="md"
              headline="LLM模型"
              :options="modelOptions"
              :selection="modelOptions.findIndex((option) => option.value === selectedModel)"
              class="mb-4 w-auto"
              @update:model="onModelChange"
            />
            <BaseSelector
              size="md"
              headline="分組版本"
              :options="versionOptions"
              :selection="versionOptions.findIndex((option) => option.value === selectVersion)"
              class="mb-4 w-auto"
              @update:model="onVersionChange"
            />
            <div class="flex items-center justify-start mb-2">
              <BaseButtonOutlined
                button-text="上傳教案"
                size="md"
                link=""
                border-color="border-blue-500"
                text-color="text-blue-500"
                @click="openFile('PDFCourse')"
              ></BaseButtonOutlined>
              <div v-if="!fileData?.PDFCourse?.file" class="px-3">非必填，填了可經LLM分析引導學生討論</div>
              <div v-else class="px-3 flex items-center">
                {{ fileData.PDFCourse.file?.name || '無名稱檔案' }}
                <TrashIcon class="px-1 w-8 h-8 text-gray-500" @click="deleteFile('PDFCourse')" />
              </div>
            </div>
            <div class="mb-4">
              <BaseInputPlace v-model="http" label="問題連結" placeholder="https://...."></BaseInputPlace>
            </div>
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
                {{ fileData.relatedData.file?.name || '無名稱檔案' }}
                <TrashIcon class="px-1 w-8 h-8 text-gray-500" @click="deleteFile('relatedData')" />
              </div>
            </div>
            <div class="flex justify-between mt-4 space-x-2">
              <BaseButtonFilled button-text="儲存" class="w-44 h-12" @click="addTopic" />
            </div>
          </PageDialog>
        </div>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
  import { ref } from 'vue'

  import PageLayout from '@/components/PageLayout.vue'
  import DisclosureInfo from '@/components/DisclosureInfo.vue'
  import DisclosureTopic from '@/components/DisclosureTopic.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseInputText from '@/components/BaseInputText.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import BaseButtonOutlined from '@/components/BaseButtonOutlined.vue'
  import BaseButtonGhost from '@/components/BaseButtonGhost.vue'
  import BaseBanner from '@/components/BaseBanner.vue'
  import InputFile from '@/components/InputFile.vue'
  import BaseSelector from '@/components/BaseSelector.vue'
  import CourseTab from '@/components/CourseTab.vue'
  import { useResourceStore } from '@/stores/resource.js'
  import { TrashIcon } from '@heroicons/vue/24/outline'
  import { useFileHandler } from '@/composables/useFileHandler'

  const resourceStore = useResourceStore()
  const userRole = resourceStore.userInfo.userRole

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

  // 彈出式通知的資料
  const notificationData = {
    open: ref(false),
    type: ref('info'),
    headline: ref('系統通知'),
    content: ref('這是一則系統通知'),
  }

  const announcementsClose = () => {
    isAnnouncementsOpen.value = false
  }

  const announcementsOpen = () => {
    isAnnouncementsOpen.value = true
  }

  const newAnnouncementTitle = ref('')
  const newAnnouncementContent = ref('')
  const isAnnouncementsOpen = ref(false)

  const announcements = ref([
    { id: 1, title: '期末demo', content: '12/27 S301~304 9:00~12:00' },
    { id: 2, title: '期末心得報告', content: '填問卷加總分2分!' },
  ])

  const topics = ref([
    { id: 1, title: 'Waterfall', content: '如果討論正在進行中，旁邊便會有綠色提示特效' },
    { id: 2, title: 'Scrum', content: '一般來說沒有討論的時候會長這樣' },
  ])

  topics.value[0].isActive = true

  const addAnnouncement = () => {
    if (newAnnouncementTitle.value && newAnnouncementContent.value) {
      const newAnnouncement = {
        id: announcements.value.length + 1,
        title: newAnnouncementTitle.value,
        content: newAnnouncementContent.value,
      }
      announcements.value.push(newAnnouncement)
      // Clear the input fields after submission
      newAnnouncementTitle.value = ''
      newAnnouncementContent.value = ''
      announcementsClose()
      notificationData.open.value = true
      notificationData.type.value = 'success'
      notificationData.headline.value = '新增成功'
      notificationData.content.value = '公告新增成功！'
    } else {
      alert('標題 & 內容不得為空白！')
    }
  }

  const newTopicTitle = ref('')
  const newTopicContent = ref('')
  const http = ref('')

  const addTopic = () => {
    if (newTopicTitle.value && newTopicContent) {
      const newTopic = {
        id: topics.value.length + 1,
        title: newTopicTitle.value,
        content: newTopicContent.value,
        source: http.value,
      }
      topics.value.push(newTopic)
      newTopicTitle.value = ''
      newTopicContent.value = ''
      http.value = ''
      topicsClose()
      notificationData.open.value = true
      notificationData.type.value = 'success'
      notificationData.headline.value = '新增成功'
      notificationData.content.value = '主題新增成功！'
    } else {
      alert('標題 & 內容不得為空白！')
    }
  }

  const deleteInfo = (id) => {
    announcements.value = announcements.value.filter((announcement) => announcement.id !== id)
    notificationData.open.value = true
    notificationData.type.value = 'success'
    notificationData.headline.value = '刪除成功'
    notificationData.content.value = '公告刪除成功！'
  }

  const deleteTopic = (id) => {
    topics.value = topics.value.filter((topic) => topic.id !== id)
    notificationData.open.value = true
    notificationData.type.value = 'success'
    notificationData.headline.value = '刪除成功'
    notificationData.content.value = '公告刪除成功！'
  }

  const isTopicsOpen = ref(false)
  const showButton = ref(userRole === 'teacher')

  const topicsOpen = () => {
    isTopicsOpen.value = true
  }
  const topicsClose = () => {
    isTopicsOpen.value = false
  }

  const selectedModel = ref('llama3.1_8B')
  const modelOptions = [
    { id: 1, title: 'llama 3.1 8B', value: 'llama3.1_8B' },
    { id: 2, title: 'llama 3.2 1B', value: 'llama3.2_1B' },
  ]

  const onModelChange = (option) => {
    selectedModel.value = option.value
  }

  const selectVersion = ref('version 1')
  const versionOptions = [
    { id: 1, title: 'version 1', value: 'version 1' },
    { id: 2, title: 'version 2', value: 'version 2' },
  ]
  const onVersionChange = (option) => {
    selectVersion.value = option.value
  }
</script>
