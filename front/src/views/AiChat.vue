<template>
  <PageLayout :headline="'AI聊天室'" class="h-svh flex">
    <!-- Chat Content Area, taking the remaining horizontal space next to the sidebar -->
    <BaseSelector
      :headline-visible="false"
      size="md"
      :options="modelOptions"
      :selection="modelOptions.findIndex((option) => option.value === selectedModel)"
      class="w-fit"
      @update:model="onModelChange"
    />
    <div class="flex flex-col flex-1 h-5/6 md:h-4/5 max-w-full">
      <!-- Message area, scrollable when overflowed -->
      <div ref="messageContainer" class="flex-1 overflow-y-auto flex flex-col items-center w-full px-4 pt-4">
        <div class="flex flex-col gap-3 w-full max-w-3xl">
          <MessageBox
            v-for="(message, index) in messages"
            :key="index"
            :text="message.text"
            :time="message.time"
            :is-own-message="message.isUser"
          />
        </div>
      </div>
    </div>
    <!-- Input area fixed at the bottom of the main content area -->
    <div
      class="w-full max-w-3xl mx-auto p-4 rounded-xl border shadow-sm hover:shadow-md focus-within:shadow-md bg-white sticky bottom-4 md:bottom-10 transition-all duration-200"
    >
      <div class="flex items-center">
        <div class="relative flex-1">
          <BaseInputText
            v-model="userInput"
            :label-visible="false"
            type="text"
            size="lg"
            placeholder="問我任何問題..."
            :has-inner-button="true"
            :is-chat-text="true"
            :reset="resetTextarea"
            class="w-full"
            @keyup.enter="sendMessage"
          />
          <BaseButtonFilled
            button-text=""
            class="absolute right-1 bottom-1 flex items-center rounded-full"
            width="w-auto"
            size="md"
            @click="sendMessage"
          >
            <IconPaperPlane class="w-6 h-6" />
          </BaseButtonFilled>
        </div>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
  import { ref, nextTick, onMounted } from 'vue'
  import PageLayout from '@/components/PageLayout.vue'
  import MessageBox from '@/components/MessageBox.vue'
  import BaseSelector from '@/components/BaseSelector.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import { IconPaperPlane } from '@iconify-prerendered/vue-jam'
  import BaseInputText from '@/components/BaseInputText.vue'

  // State for messages, input, and model selection
  const messages = ref([
    // { text: '使用者的訊息', isUser: true, time: new Date().toLocaleString() },
    // { text: 'AI回覆', isUser: false, time: new Date().toLocaleString() },
  ])
  const userInput = ref('')
  const selectedModel = ref('llama3.1_8B')
  const modelOptions = [
    { id: 1, title: 'llama 3.1 8B', value: 'llama3.1_8B' },
    { id: 2, title: 'llama 3.2 1B', value: 'llama3.2_1B' },
  ]
  // Reference to the message container for scrolling
  const messageContainer = ref(null)
  const resetTextarea = ref(false)
  const socket = ref(null) // Reference for WebSocket instance

  // Function to scroll to the bottom of the message container
  const scrollToBottom = () => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  }

  var chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  var token = ''
  for (var i = 0; i < 30; i++) {
    token += chars[Math.floor(Math.random() * chars.length)]
  }

  // Initialize WebSocket connection
  const initializeWebSocket = () => {
    socket.value = new WebSocket(`wss://api.swe.verypro.wtf/v1/chat/join?userId=${token}&username=user`) // Replace with the server's WebSocket URL

    socket.value.onopen = () => {
      console.log('WebSocket connection established')
    }

    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('Message received from server:', data.content)

      // Add server response to the chat messages
      messages.value.push({
        text: data.content,
        isUser: false,
        time: new Date().toLocaleString(),
      })
      nextTick(() => scrollToBottom())
    }

    socket.value.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    socket.value.onclose = () => {
      console.log('WebSocket connection closed')
    }
  }

  // Send message to the server
  const sendMessage = async () => {
    const currentTime = new Date().toLocaleString()
    if (userInput.value.trim() !== '') {
      // Add user message to the chat messages
      messages.value.push({ text: userInput.value, isUser: true, time: currentTime })

      // Send message via WebSocket
      if (socket.value && socket.value.readyState === WebSocket.OPEN) {
        socket.value.send(JSON.stringify({ message: userInput.value, model: selectedModel.value }))
      } else {
        console.error('WebSocket is not connected')
        // Simulate AI response after a delay
        setTimeout(async () => {
          messages.value.push({
            text: `WebSocket is not connected`,
            isUser: false,
            time: new Date().toLocaleString(),
          })

          // Wait for DOM update again, then scroll to bottom
          await nextTick()
          scrollToBottom()
        }, 1000)
      }

      userInput.value = ''

      // Wait for DOM update before scrolling to the bottom
      await nextTick()
      scrollToBottom()
    }

    // Reset textarea height after sending the message
    resetTextarea.value = true
    setTimeout(() => {
      resetTextarea.value = false
    }, 0)
  }

  // Update model selection
  const onModelChange = (option) => {
    selectedModel.value = option.value
  }

  // Initialize WebSocket when the component is mounted
  onMounted(() => {
    initializeWebSocket()
  })
</script>
