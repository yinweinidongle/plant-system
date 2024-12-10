<template>
  <div class="transport-control">
    <div class="control-header">
      <h3>传送带控制面板</h3>
      <el-tag :type="isRunning ? 'success' : 'danger'" class="status-tag">
        {{ isRunning ? '运行中' : '已停止' }}
      </el-tag>
    </div>

    <div class="control-buttons">
      <el-button
        type="success"
        :disabled="isRunning"
        :loading="loading"
        size="large"
        @click="startConveyor"
      >
        <el-icon><VideoPlay /></el-icon>
        开启传送带
      </el-button>

      <el-button
        type="danger"
        :disabled="!isRunning"
        :loading="loading"
        size="large"
        @click="stopConveyor"
      >
        <el-icon><VideoPause /></el-icon>
        停止传送带
      </el-button>
    </div>

    <div class="status-panel">
      <div class="status-item">
        <span class="label">运行时间：</span>
        <span class="value">{{ runningTime }}</span>
      </div>
      <div class="status-item">
        <span class="label">当前速度：</span>
        <span class="value">{{ speed }} m/s</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { VideoPlay, VideoPause } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { conveyorApi } from '../api/conveyor'

const isRunning = ref(false)
const loading = ref(false)
const speed = ref(0)
const runningTime = ref('00:00:00')
let timer = null
let startTime = null

// 开启传送带
const startConveyor = async () => {
  try {
    loading.value = true
    await conveyorApi.start()
    isRunning.value = true
    startTime = new Date()
    startTimer()
    speed.value = 0.6
    ElMessage.success('传送带已开启')
  } catch (error) {
    ElMessage.error(`开启失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

// 停止传送带
const stopConveyor = async () => {
  try {
    loading.value = true
    await conveyorApi.stop()
    isRunning.value = false
    stopTimer()
    speed.value = 0
    ElMessage.success('传送带已停止')
  } catch (error) {
    ElMessage.error(`停止失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

// 更新运行时间
const updateRunningTime = () => {
  if (!startTime) return
  const now = new Date()
  const diff = now - startTime
  const hours = Math.floor(diff / 3600000)
  const minutes = Math.floor((diff % 3600000) / 60000)
  const seconds = Math.floor((diff % 60000) / 1000)
  runningTime.value = `${hours.toString().padStart(2, '0')}:${minutes
    .toString()
    .padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

// 启动定时器
const startTimer = () => {
  stopTimer()
  timer = setInterval(updateRunningTime, 1000)
}

// 停止定时器
const stopTimer = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

// 获取传送带状态
const getConveyorStatus = async () => {
  try {
    const status = await conveyorApi.getStatus()
    isRunning.value = status.running
    speed.value = status.speed
    if (status.running && status.startTime) {
      startTime = new Date(status.startTime)
      startTimer()
    }
  } catch (error) {
    console.error('获取传送带状态失败:', error)
  }
}

onMounted(() => {
  //getConveyorStatus()
})

onUnmounted(() => {
  stopTimer()
})
</script>

<style scoped>
.transport-control {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h3 {
  margin: 0;
  color: #2c3e50;
}

.status-tag {
  font-size: 0.9em;
  padding: 0 12px;
}

.control-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  padding: 20px 0;
}

.control-buttons .el-button {
  width: 160px;
  height: 50px;
  font-size: 1.1em;
}

.control-buttons .el-icon {
  margin-right: 8px;
  font-size: 1.2em;
}

.status-panel {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 15px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.status-item:last-child {
  border-bottom: none;
}

.status-item .label {
  color: #606266;
  font-size: 0.9em;
}

.status-item .value {
  font-weight: bold;
  color: #409EFF;
}
</style> 