<template>
  <PageLayout headline="點名系統">
    <div class="w-full flex align-top md:justify-between max-md:grid">
      <div class="flex space-x-2 max-md:mb-2">
        <div>
          <span class="text-gray-700 font-bold">日期：</span>
          <span class="text-gray-700">{{ date }}</span>
        </div>
        <div>
          <span class="text-gray-700 font-bold">節次：</span>
          <span class="text-gray-700">第 {{ period }} 節</span>
        </div>
      </div>
      <div class="flex max-md:w-full md:-mt-4 max-md:justify-between max-md:mb-2 md:space-x-2">
        <InputSearch class="w-72" />
        <BaseButtonFilled button-text="QR Code 點名" width="w-auto" size="md" @click="openQRCodeDialog" />
      </div>
    </div>

    <div>
      <AttendanceDisplay :items="students" />
    </div>

    <div class="mt-4 mb-4 items-center grid grid-cols-12 gap-4">
      <div class="col-span-8"></div>
      <div class="col-span-2">
        <BaseButtonFilled class="mb-4" button-text="返回" width="w-full" @click="goToCourseView" />
      </div>
      <div class="col-span-2">
        <BaseButtonFilled class="mb-4" button-text="送出" width="w-full" @click="openSubmitDialog" />
      </div>
    </div>
  </PageLayout>

  <PageDialog
    :is-open="showQRCodeDialog"
    dialog-title="QR Code 點名"
    class="hidden"
    @close="closeQRCodeDialog"
  >
    <div class="w-full text-center justify-center align-center object-center">
      <div>
        <qrcode-vue :value="attendanceCode" size="400" margin="3" />
      </div>
    </div>
    <div class="mb-4 items-center">
      <p class="text-6xl font-semibold text-center font-mono">{{ attendanceCode }}</p>
    </div>
    <BaseButtonFilled
      :button-text="countdown > 0 ? `結束 (${countdown}s)` : '結束'"
      class="bg-red-500 hover:bg-red-700 mt-4"
      @click="manualClose(closeModal)"
    />
  </PageDialog>

  <PageDialog :is-open="showSubmitDialog" dialog-title="提交資料" class="hidden" @close="closeSubmitDialog">
    <div class="text-center">
      <p>確認要提交資料嗎？</p>
      <div class="flex space-x-2">
        <BaseButtonFilled button-text="取消" class="bg-red-500 hover:bg-red-700 mt-4" @click="closeModal" />
        <BaseButtonFilled
          button-text="確認提交"
          class="bg-green-500 hover:bg-green-700 mt-4"
          @click="submitData(closeModal)"
        />
      </div>
    </div>
  </PageDialog>
</template>

<script setup>
  import { ref, watch, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import PageLayout from '@/components/PageLayout.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import InputSearch from '@/components/InputSearch.vue'
  import AttendanceDisplay from '@/components/TableAttendance.vue'
  import RollCall from '@/api/roll-call'
  import QrcodeVue from 'qrcode.vue'

  const route = useRoute()
  const router = useRouter()

  const date = new Date().toISOString().split('T')[0]

  const showQRCodeDialog = ref(false)
  const showSubmitDialog = ref(false)
  const countdown = ref(90)
  let countdownInterval = null

  const attendanceCode = ref('123456')
  const courseId = ref(route.params.id)
  const period = 1
  const students = ref([])

  async function fetchAttendanceRecords() {
    try {
      const response = await RollCall.getCourseAttendance(courseId, date, period)
      students.value = response.data.students.map((student) => ({
        name: student.studentUid, // Student ID (to be replaced with name???)
        status: student.attendance,
        note: student.note || '',
        avatar: '/src/assets/profile-placeholder.jpg',
      }))
      console.log('Fetched attendance records:', students.value)
    } catch (error) {
      console.error('Failed to fetch attendance records:', error)
      students.value = [
        {
          name: '紀博文',
          status: '出席',
          avatar: '/src/assets/profile-placeholder.jpg',
        },
        {
          name: '紀博文',
          status: '出席',
          avatar: '/src/assets/profile-placeholder.jpg',
        },
        {
          name: '紀博文',
          status: '出席',
          avatar: '/src/assets/profile-placeholder.jpg',
        },
      ]
    }
  }

  function goToCourseView() {
    router.push({ name: 'Course', params: { id: courseId.value } })
  }

  async function generateQRCode() {
    try {
      const response = await RollCall.autoRollCallGenerate(courseId)
      attendanceCode.value = response.data.code
      console.log('Generated QR Code:', attendanceCode.value)
    } catch (error) {
      console.error('Failed to generate QR Code:', error)
    }
  }

  async function startRollCallSession() {
    try {
      await RollCall.autoRollCallStart(courseId)
      console.log('Start roll call session API called successfully')
    } catch (error) {
      console.error('Failed to start roll call session', error)
    }
  }

  async function endRollCallSession() {
    try {
      await RollCall.autoRollCallEnd(courseId)
      console.log('End roll call session API called successfully')
    } catch (error) {
      console.error('Failed to end roll call session', error)
    }
  }

  function openQRCodeDialog() {
    showQRCodeDialog.value = true
    countdown.value = 90
    startRollCallSession()
    generateQRCode()
    startCountdown()
  }

  function closeQRCodeDialog() {
    showQRCodeDialog.value = false
    stopCountdown()
    endRollCallSession()
    fetchAttendanceRecords()
  }

  function manualClose() {
    showQRCodeDialog.value = false
    stopCountdown()
    endRollCallSession()
  }

  function startCountdown() {
    countdownInterval = setInterval(() => {
      if (countdown.value > 0) {
        countdown.value--
      } else {
        stopCountdown()
        setTimeout(closeQRCodeDialog, 10000)
      }
    }, 1000)
  }

  function stopCountdown() {
    clearInterval(countdownInterval)
  }

  watch(showQRCodeDialog, (newVal) => {
    if (!newVal) {
      stopCountdown()
    }
  })

  function openSubmitDialog() {
    showSubmitDialog.value = true
  }

  function closeSubmitDialog() {
    showSubmitDialog.value = false
  }

  async function submitData() {
    const payload = {
      students: students.value.map((student) => ({
        studentUid: student.uid,
        attendance: student.status,
        note: student.note || '',
      })),
    }

    try {
      const response = await RollCall.manualRollCall(payload)
      console.log('Submit success:', response.data)
      alert('點名資料提交成功！')
      showSubmitDialog.value = false
    } catch (error) {
      console.error('Failed to submit attendance records:', error)
      alert('上傳失敗，請稍後再試！')
    }
  }

  onMounted(() => {
    fetchAttendanceRecords()
  })
</script>
