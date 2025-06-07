<template>
  <table class="min-w-full border-collapse border-none">
    <thead>
      <tr>
        <th
          v-for="header in headers"
          :key="header"
          class="border-b-2 border-gray-300 px-4 py-2 text-left bg-gray-300"
        >
          {{ header }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, rowIndex) in data" :key="rowIndex">
        <td v-for="(cell, cellIndex) in row" :key="cellIndex" class="px-4 py-2 border-b border-gray-200">
          {{ cell }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  export default {
    props: {
      headers: {
        type: Array,
        required: true,
      },
      data: {
        type: Array,
        required: true,
      },
    },
  }
</script>
