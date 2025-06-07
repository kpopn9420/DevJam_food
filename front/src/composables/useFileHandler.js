import { ref } from 'vue'

export function useFileHandler(notificationCallback) {
  const fileData = ref({})
  const fileType = ref('')
  const isFileOpen = ref(false)

  const initializeFileData = (fileTypes) => {
    fileTypes.forEach((type) => {
      if (!fileData.value[type]) {
        fileData.value[type] = { file: null, url: null }
      }
    })
  }

  const openFile = (type) => {
    if (!fileData.value[type]) {
      console.error(`File type "${type}" is not initialized.`)
      return
    }
    fileType.value = type
    isFileOpen.value = true
  }

  const closeFile = () => {
    isFileOpen.value = false
    fileType.value = ''
  }

  const drop = (event) => {
    const file = event.dataTransfer.files[0]
    const url = URL.createObjectURL(file)
    if (fileType.value && fileData.value[fileType.value]) {
      fileData.value[fileType.value] = { file, url }
    }
  }

  const selectedFile = (event) => {
    const file = event.target.files[0]
    const url = URL.createObjectURL(file)
    if (fileType.value && fileData.value[fileType.value]) {
      fileData.value[fileType.value] = { file, url }
    }
  }

  const deleteFile = (type) => {
    if (fileData.value[type]) {
      fileData.value[type] = { file: null, url: null }
      notificationCallback?.({
        type: 'success',
        headline: '成功',
        content: '檔案已成功移除！',
      })
    }
  }

  const saveFile = async (handlers = {}) => {
    const currentFile = fileData.value[fileType.value]?.file
    if (!currentFile) {
      notificationCallback?.({
        type: 'error',
        headline: '錯誤',
        content: '請先選擇檔案。',
      })
      return
    }

    try {
      if (handlers[fileType.value]) {
        await handlers[fileType.value](currentFile)
      } else {
        console.warn(`No handler provided for file type: ${fileType.value}`)
      }

      notificationCallback?.({
        type: 'success',
        headline: '成功',
        content: '檔案已成功儲存！',
      })
      closeFile()
    } catch (error) {
      console.error('檔案儲存失敗', error)
      notificationCallback?.({
        type: 'error',
        headline: '錯誤',
        content: '檔案儲存失敗！',
      })
    }
  }

  return {
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
  }
}
