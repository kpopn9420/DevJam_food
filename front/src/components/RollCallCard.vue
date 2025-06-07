<template>
  <div
    class="w-full p-4 rounded-lg border items-center hover:shadow-md transition-all duration-200"
    :class="attendanceColor[classAttendance]"
  >
    <div class="justify-between flex align-middle items-center">
      <div class="justify-stretch align-middle items-center flex">
        <p class="font-bold font-mono text-2xl mr-10 ml-4" :class="attendancePeriod[classAttendance]">
          {{ classPeriod }}
        </p>
        <p :class="attendanceName[classAttendance]">{{ className }}</p>
      </div>
      <div
        class="flex rounded-full w-16 h-6 justify-center items-center text-center text-xs"
        :class="attendanceDetailColor[classAttendance]"
      >
        <span class="text-center text-white align-baseline">{{ attendanceDetail[classAttendance] }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
  defineProps({
    classPeriod: {
      type: String,
      default: '1',
    },
    className: {
      type: String,
      default: '範例課程',
    },
    classAttendance: {
      type: String,
      default: 'none',
      validator: (value) => ['onTime', 'late', 'leave', 'absent', 'none'].includes(value),
    },
  })

  const attendanceColor = {
    leave: 'bg-blue-300 border-blue-200 bg-opacity-30 hover:shadow-blue-100',
    late: 'bg-amber-300 border-amber-200 bg-opacity-30 hover:shadow-amber-100',
    absent: 'bg-red-300 border-red-200 bg-opacity-30 hover:shadow-red-100',
    onTime: 'bg-green-300 border-green-200 bg-opacity-30 hover:shadow-green-100',
    none: 'bg-gray-300 border-gray-200 bg-opacity-30 hover:shadow-gray-100',
  }

  const attendancePeriod = {
    leave: 'text-blue-800',
    late: 'text-amber-800',
    absent: 'text-red-800',
    onTime: 'text-green-800',
    none: 'text-gray-800',
  }

  const attendanceName = {
    leave: 'text-blue-900 text-opacity-80',
    late: 'text-amber-900 text-opacity-80',
    absent: 'text-red-900 text-opacity-80',
    onTime: 'text-green-900 text-opacity-80',
    none: 'text-gray-900 text-opacity-80',
  }

  const attendanceDetailColor = {
    leave: 'bg-blue-700 bg-opacity-70',
    late: 'bg-amber-700 bg-opacity-70',
    absent: 'bg-red-700 bg-opacity-70',
    onTime: 'bg-green-700 bg-opacity-70',
    none: 'bg-gray-700 bg-opacity-70',
  }

  const attendanceDetail = {
    leave: '請假',
    late: '遲到',
    absent: '未到',
    onTime: '有到',
    none: '無資料',
  }
</script>
