<template>
  <PageLayout headline="分組討論">
    <div class="flex items-start space-x-4 justify-between">
      <div class="flex space-x-1 mt-2">
        <BasePaginator
          class="-mt-3 -ml-3 sm:-ml-4"
          :current-page="currentPage"
          :total-pages="totalPages"
          @page-changed="updateCurrentPage"
        >
        </BasePaginator>
      </div>

      <BaseButtonFilled
        :bg-color="discussionActive ? 'bg-red-500' : 'bg-blue-500'"
        :hover-color="discussionActive ? 'hover:bg-red-700' : 'hover:bg-blue-700'"
        width="w-fit"
        size="md"
        text-color="text-white"
        :button-text="discussionActive ? '結束討論' : '開始討論'"
        class="mt-2"
        @click="toggleDiscussion"
      />
    </div>

    <div class="mt-2">
      <div class="flex flex-col flex-1 h-5/6 md:h-4/5 max-w-full">
        <ContentBox :headline="currentGroup">
          <div
            ref="messageContainer"
            class="flex-1 overflow-y-auto flex flex-col items-center w-full px-4 pt-4"
            style="max-height: 85vh"
          >
            <div class="flex flex-col gap-3 w-full max-w-5xl">
              <BaseMessageBox
                v-for="(message, index) in messages"
                :key="index"
                :text="message.text"
                :audio-url="message.audioURL"
                :time="message.time"
                :is-own-message="message.isOwnMessage"
              />
              <div
                v-if="!isViewEnabled"
                class="w-full bg-blue-100 border border-blue-400 text-blue-700 px-4 py-2 rounded-md mt-2"
              >
                <span>LLM：{{ chatSummary }}</span>
              </div>
            </div>
          </div>
        </ContentBox>
      </div>
    </div>
    <div
      class="w-full max-w-3xl mx-auto p-4 rounded-xl border shadow-sm hover:shadow-md focus-within:shadow-md bg-white sticky bottom-4 md:bottom-10 transition-all duration-200"
    >
      <div v-if="isViewEnabled" class="flex items-center space-x-2">
        <div class="relative flex-1">
          <BaseInputPlace
            v-model="userInput"
            label=""
            size="lg"
            :placeholder="isListening ? '正在輸入語音...' : '請按下麥克風圖示以開始'"
            class="w-full cursor-default rounded-lg"
            :is-disabled="isInputDisabled"
            :label-visible="false"
            @keyup.enter="sendMessage"
          />
          <BaseButtonFilled
            :bg-color="isListening ? 'bg-red-500 hover:bg-red-700' : 'bg-blue-500 hover:bg-blue-700'"
            size="md"
            button-text=""
            class="absolute inset-y-0 right-1 top-1 bottom-1 flex items-center rounded-md"
            width="w-auto"
            @click="toggleRecording"
          >
            <StopIcon v-if="isListening" class="h-5 w-5 text-white" />
            <MicrophoneIcon v-else class="h-5 w-5 text-white" />
          </BaseButtonFilled>
        </div>
      </div>
      <div v-else class="w-full bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded-md">
        <span>此討論已被關閉。</span>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
  import { ref, nextTick } from 'vue'
  import PageLayout from '@/components/PageLayout.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import BasePaginator from '@/components/BasePaginator.vue'
  import BaseMessageBox from '@/components/MessageBox.vue'
  import ContentBox from '@/components/ContentBox.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import { MicrophoneIcon, StopIcon } from '@heroicons/vue/24/outline'

  const discussionActive = ref(false)

  const currentPage = ref(1)
  const totalPages = ref(10)
  const currentGroup = ref(`第${currentPage.value}組`)
  const isInputDisabled = ref(true)
  const isListening = ref(false)
  const isViewEnabled = ref(false)
  const userInput = ref('')
  const chatSummary = '這是討論的摘要...'

  const messages = ref([
    {
      text: '說話內容',
      time: new Date().toLocaleString(),
      audioURL: 'path/to/other-person-audio.mpeg',
      isOwnMessage: false,
    },
    {
      text: '說話內容',
      time: new Date().toLocaleString(),
      audioURL: 'path/to/another-person-audio.mpeg',
      isOwnMessage: false,
    },
  ])

  const updateCurrentPage = (page) => {
    currentPage.value = page
    currentGroup.value = `第${currentPage.value}組`
  }

  function toggleDiscussion() {
    discussionActive.value = !discussionActive.value
    isViewEnabled.value = !isViewEnabled.value
  }
  const messageContainer = ref(null)

  // Function to scroll to the bottom of the message container
  const scrollToBottom = () => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  }

  let mediaRecorder = null
  let audioChunks = []

  const toggleRecording = () => {
    if (!('MediaRecorder' in window)) {
      alert('您的瀏覽器不支援錄音功能')
      return
    }

    if (isListening.value) {
      mediaRecorder.stop()
    } else {
      isListening.value = true
      navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then((stream) => {
          mediaRecorder = new MediaRecorder(stream)
          mediaRecorder.start()
          audioChunks = []

          mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data)
          }

          mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' })
            const audioURL = URL.createObjectURL(audioBlob)
            const currentTime = new Date().toLocaleString()
            messages.value.push({
              text: '說話內容',
              time: currentTime,
              audioURL,
              isOwnMessage: true,
            })

            audioChunks = []
            isListening.value = false
            await nextTick()
            scrollToBottom()
          }
        })
        .catch((error) => {
          console.error('錄音錯誤:', error)
          isListening.value = false
        })
    }
  }

  const sendMessage = async () => {
    const currentTime = new Date().toLocaleString()
    if (userInput.value.trim()) {
      messages.value.push({ text: userInput.value, isOwnMessage: true, time: currentTime })
      userInput.value = ''

      await nextTick()
      scrollToBottom()
    }
  }
</script>
