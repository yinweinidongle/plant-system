<template>
  <div class="camera-view">
    <div class="camera-header">
      <span class="camera-title">{{ title }}</span>
      <div class="camera-controls">
        <el-select v-model="selectedDevice" placeholder="选择摄像头" :disabled="isRecording">
          <el-option
            v-for="device in devices"
            :key="device.deviceId"
            :label="device.label"
            :value="device.deviceId"
          />
        </el-select>
        <el-button 
          :type="isStreaming ? 'danger' : 'primary'"
          @click="toggleStream"
          :disabled="!selectedDevice"
        >
          {{ isStreaming ? '停止' : '开始' }}
        </el-button>
        <el-button 
          :type="isRecording ? 'danger' : 'success'"
          @click="toggleRecording"
          :disabled="!isStreaming"
        >
          {{ isRecording ? '停止录制' : '开始录制' }}
        </el-button>
        <el-button 
          type="primary" 
          @click="toggleFullscreen"
          :disabled="!isStreaming"
        >
          <el-icon><FullScreen /></el-icon>
        </el-button>
      </div>
    </div>
    <div class="video-container" ref="videoContainer">
      <video ref="videoElement" autoplay playsinline></video>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { FullScreen } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const videoElement = ref(null)
const videoContainer = ref(null)
const selectedDevice = ref('')
const devices = ref([])
const isStreaming = ref(false)
const isRecording = ref(false)
const mediaRecorder = ref(null)
const stream = ref(null)

// 获取可用摄像头列表
const getDevices = async () => {
  try {
    const deviceList = await navigator.mediaDevices.enumerateDevices()
    devices.value = deviceList.filter(device => device.kind === 'videoinput')
  } catch (error) {
    ElMessage.error('获取摄像头列表失败')
    console.error(error)
  }
}

// 开启/关闭摄像头流
const toggleStream = async () => {
  if (isStreaming.value) {
    stopStream()
  } else {
    try {
      stream.value = await navigator.mediaDevices.getUserMedia({
        video: {
          deviceId: selectedDevice.value
        }
      })
      videoElement.value.srcObject = stream.value
      isStreaming.value = true
    } catch (error) {
      ElMessage.error('开启摄像头失败')
      console.error(error)
    }
  }
}

// 停止摄像头流
const stopStream = () => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    videoElement.value.srcObject = null
    stream.value = null
    isStreaming.value = false
  }
}

// 开始/停止录制
const toggleRecording = () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

// 开始录制
const startRecording = () => {
  try {
    const chunks = []
    mediaRecorder.value = new MediaRecorder(stream.value)
    
    mediaRecorder.value.ondataavailable = (e) => {
      if (e.data.size > 0) {
        chunks.push(e.data)
      }
    }

    mediaRecorder.value.onstop = () => {
      const blob = new Blob(chunks, { type: 'video/mp4' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `recording_${new Date().toISOString()}.mp4`
      a.click()
      URL.revokeObjectURL(url)
    }

    mediaRecorder.value.start()
    isRecording.value = true
  } catch (error) {
    ElMessage.error('开始录制失败')
    console.error(error)
  }
}

// 停止录制
const stopRecording = () => {
  if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
    mediaRecorder.value.stop()
    isRecording.value = false
  }
}

// 切换全屏
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    videoContainer.value.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

onMounted(() => {
  getDevices()
})

onBeforeUnmount(() => {
  stopStream()
  if (isRecording.value) {
    stopRecording()
  }
})
</script>

<style scoped>
.camera-view {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.camera-title {
  font-size: 1.2em;
  font-weight: bold;
}

.camera-controls {
  display: flex;
  gap: 10px;
}

.video-container {
  width: 100%;
  flex: 1;
  background: #000;
  border-radius: 4px;
  overflow: hidden;
}

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

:deep(.el-select) {
  width: 150px;
}
</style> 