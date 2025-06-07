import { computed } from 'vue'

export function useSemester() {
  const currentDate = new Date()
  const currentYear = currentDate.getFullYear()
  const currentMonth = currentDate.getMonth() + 1

  const semester = computed(() => {
    if (currentMonth >= 2 && currentMonth <= 6) {
      return 'Spring'
    } else if (currentMonth >= 7 && currentMonth <= 8) {
      return 'Summer'
    } else {
      return 'Fall'
    }
  })

  const academicYear = computed(() => currentYear.toString())

  return {
    semester,
    academicYear,
  }
}
