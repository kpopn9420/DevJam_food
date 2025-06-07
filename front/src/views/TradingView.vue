<template>
  <BaseBanner
    :is-open="notificationData.open.value"
    :type="notificationData.type.value"
    :headline="notificationData.headline.value"
    :content="notificationData.content.value"
    @close="notificationData.open.value = false"
  />
  <PageLayout headline="">
    <div class="flex justify-start items-center space-x-2 mb-4">
        <div class="mt-auto">
          <BaseButtonOutlined
            button-text="+ 新增剩食"
            size="md"
            link=""
            border-color="border-blue-500"
            text-color="text-blue-500"
            @click="AddFood"
          ></BaseButtonOutlined>
          <PageDialog :is-open="AddFoodDialog" dialog-title="新增剩食" @close="CancelFood">
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
            <div class="flex items-center justify-start mb-2">
              <BaseButtonOutlined
                button-text="上傳照片"
                size="md"
                link=""
                border-color="border-blue-500"
                text-color="text-blue-500"
                @click="openFile('FoodPicture')"
              ></BaseButtonOutlined>
              <div v-if="!fileData?.FoodPicture?.file" class="px-3"></div>
              <div v-else class="px-3 flex items-center">
                {{ fileData.FoodPicture.file?.name || '無名稱檔案' }}
                <TrashIcon class="px-1 w-8 h-8 text-gray-500" @click="deleteFile('FoodPicture')" />
              </div>
            </div>
            <PageDialog dialog-title="上傳照片" :is-open="isFileOpen" @close="closeFile">
                <div class="mb-4">
                  <InputFile :file-types="'jpg, jpeg, png'" @drop.prevent="drop" @change="selectedFile" />
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
            <div class="mt-4">
              <BaseButtonFilled button-text="儲存" class="w-full" @click="addAnnouncement" />
            </div>
          </PageDialog>
        </div>
        <InputSearch size="md" placeholder="Search Food Category / Store..." class="mt-4 w-1/3" />
        <CheckBox v-model="isTosAgreed" class="mt-4">
            依距離排序
        </CheckBox>
    </div>
    <div class="text-center max-w-2xl mx-auto my-8 px-4">
        <h2 class="text-3xl font-bold text-gray-900 mt-2 mb-4">Food Menu</h2>
        <p class="text-gray-600 text-lg leading-relaxed">
            Discover our delicious selection of carefully crafted dishes, each prepared with
            the finest ingredients and attention to detail.
        </p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <Card
            v-for="n in 12"
            :key="n"
            title="Delicious Pizza"
            role="viewer"
            description="A cheesy and delightful pizza topped with pepperoni."
        />
    </div>
  </PageLayout>
</template>

<script setup>
  import { ref } from 'vue'

  import PageLayout from '@/components/PageLayout.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseInputText from '@/components/BaseInputText.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import BaseButtonOutlined from '@/components/BaseButtonOutlined.vue'
  import BaseBanner from '@/components/BaseBanner.vue'
  import InputSearch from '@/components/InputSearch.vue'
  import SelectDate from '@/components/selectDate.vue'
  import CheckBox from '@/components/InputCheck.vue'
  import Card from '@/components/Card.vue'
  import InputFile from '@/components/InputFile.vue'
  import { useFileHandler } from '@/composables/useFileHandler'
  import { TrashIcon } from '@heroicons/vue/24/outline'

  const notificationData = {
    open: ref(false),
    type: ref('info'),
    headline: ref('系統通知'),
    content: ref('這是一則系統通知'),
  }

  // 彈出式通知的資料
  const notificationHandler = (notification) => {
    notificationData.open.value = true
    notificationData.type.value = notification.type
    notificationData.headline.value = notification.headline
    notificationData.content.value = notification.content
  }

  const AddFoodDialog = ref(false)

  const AddFood = () => {
    AddFoodDialog.value = true
  }

  const CancelFood = () => {
    AddFoodDialog.value = false
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

  initializeFileData(['FoodPicture'])
  const saveHandlers = {
    FoodPicture: async (file) => {
      console.log('Saving PDF Course file:', file)
      console.log('File name:', file.name)
    }
  }

  const handleSaveFile = () => {
    console.log(fileData)
    console.log(fileData.name)
    saveFile(saveHandlers)
  }
  
</script>
