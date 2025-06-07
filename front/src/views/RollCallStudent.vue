<template>
  <BaseBanner
    class="-z-10"
    :is-open="notificationData.open.value"
    :type="notificationData.type.value"
    :headline="notificationData.headline.value"
    :content="notificationData.content.value"
    @close="notificationData.open.value = false"
  />
  <PageLayout headline="點名系統">
    <div class="w-full align-top justify-between flex">
      <div>
        <span class="text-gray-700 font-bold leading-none">現在時間：</span
        ><span class="text-gray-700 font-normal leading-none">{{ time }}</span>
      </div>
      <BaseButtonFilled
        size="md"
        width="w-fit"
        button-text="QR Code點名"
        class="-mt-4"
        @click="openDialog"
      ></BaseButtonFilled>
    </div>
    <div class="grid sm:flex sm:grid-cols-[auto, auto] items-start">
      <div class="hidden md:flex mr-4 border rounded-md bg-white">
        <DatePicker
          ref="calendar"
          v-model="weekDate"
          borderless
          transparent
          title-position="left"
          :attributes="attrs"
          class="rounded-md p-2 date-picker"
        />
      </div>
      <div class="border w-full rounded-md bg-white">
        <div class="pb-2">
          <DatePicker
            ref="cal"
            v-model="weekDate"
            transparent
            borderless
            expanded
            title-position="left"
            :attributes="attrWeek"
            view="weekly"
            class="p-2 pb-4"
          >
          </DatePicker>
          <div class="w-full h-px bg-gray-200 drop-shadow"></div>
          <div class="p-4 pb-2 space-y-2">
            <RollCallClasses
              v-for="classItem in classes"
              :key="classItem.period"
              :class-period="classItem.period"
              :class-name="classItem.courseId"
              :class-attendance="classItem.attendance"
            />
          </div>
        </div>
      </div>
    </div>
  </PageLayout>

  <PageDialog dialog-title="點名" class="z-10" :is-open="isDialogOpen" @close="closeDialog">
    <PageTabRounded :categories="categories">
      <template #tab1>
        <!-- Content for Tab 1 -->
        <div class="max-w-96 mb-4 rounded-lg items-center">
          <qrcode-stream class="rounded-md h-40" @detect="onDetect"></qrcode-stream>
        </div>
        <BaseButtonFilled button-text="送出" @click="submitCode" />
      </template>
      <template #tab2>
        <!-- Content for Tab 2 -->
        <div class="mb-4">
          <BaseInputPlace v-model="code" label="點名驗證碼" placeholder="請輸入六位數點名驗證碼" />
        </div>
        <BaseButtonFilled button-text="送出" @click="submitCode" />
      </template>
    </PageTabRounded>
  </PageDialog>
</template>

<script setup>
  import 'v-calendar/style.css'
  import { ref, onMounted, watch } from 'vue'
  import { QrcodeStream } from 'vue-qrcode-reader'
  import { DatePicker } from 'v-calendar'
  import RollCall from '@/api/roll-call'
  import PageLayout from '@/components/PageLayout.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import RollCallClasses from '@/components/RollCallCard.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import PageTabRounded from '@/components/PageTabRounded.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseBanner from '@/components/BaseBanner.vue'

  const notificationData = {
    open: ref(false),
    type: ref('error'),
    headline: ref('點名失敗'),
    content: ref('請檢查QR Code或驗證碼是否正確。'),
  }

  // Date for controlling the calendar
  const weekDate = ref(new Date())
  const time = ref(new Date().toLocaleTimeString())

  // Monthly calendar
  const attrs = ref([
    {
      key: 'today',
      dates: weekDate.value,
    },
  ])

  // Weekly calendar
  const attrWeek = ref([
    {
      key: 'today',
      dates: weekDate.value,
    },
  ])

  // ref for monthly calendar
  const calendar = ref(null)
  // ref for weekly calendar
  const cal = ref(null)

  const moveDate = async (date) => {
    if (calendar.value) {
      await calendar.value.move(date)
    }
    if (cal.value) {
      await cal.value.move(date)
    }
  }

  watch(weekDate, async (newDate) => {
    await moveDate(newDate)
    fetchAttendance()
  })

  const classes = ref([])
  const fetchAttendance = async () => {
    try {
      const date = weekDate.value.toISOString().split('T')[0]
      console.log(date)
      const response = await RollCall.getAttendance(date)
      classes.value = response.data.records
    } catch (error) {
      console.error('Failed to fetch student attendance', error)
      classes.value = [
        {
          courseId: 'CS-001',
          day: 3,
          period: 6,
          attendance: 'absent',
        },
      ]
    }
  }

  const code = ref('')
  const onDetect = (scannedCode) => {
    console.log('QR Code detected:', scannedCode)
    code.value = scannedCode
    notificationData.open.value = true
    notificationData.type.value = 'success'
    notificationData.headline.value = 'QR Code掃描成功'
    notificationData.content.value = '請點擊送出按鈕進行點名。'
  }

  const submitCode = async () => {
    try {
      const response = await RollCall.autoRollCallPunch(code.value)
      console.log('Attendance submitted:', response.data)
      notificationData.open.value = true
      notificationData.type.value = 'success'
      notificationData.headline.value = '點名成功'
      notificationData.content.value = '點名資料已成功提交。'
    } catch (error) {
      console.error('Failed to submit attendance', error)
      notificationData.open.value = true
      notificationData.type.value = 'error'
      notificationData.headline.value = '點名失敗'
      notificationData.content.value = '請檢查QR Code或驗證碼是否正確。'
    }
  }

  const categories = {
    'QR Code掃描': {},
    驗證碼輸入: {},
  }

  const isDialogOpen = ref(false)

  const openDialog = () => {
    isDialogOpen.value = true
  }
  const closeDialog = () => {
    isDialogOpen.value = false
  }

  onMounted(() => {
    fetchAttendance()
  })
</script>
