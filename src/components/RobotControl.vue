<template>
  <div class="robot-control">
    <div class="control-header">
      <div class="step-control">
        <span class="step-label">步进角度：</span>
        <el-radio-group v-model="stepSize" size="small">
          <el-radio-button :label="1">1°</el-radio-button>
          <el-radio-button :label="5">5°</el-radio-button>
          <el-radio-button :label="10">10°</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    <div class="joint-controls">
      <div class="joint-columns">
        <div class="joint-column">
          <div v-for="index in 3" :key="index-1" class="joint-item">
            <div class="joint-header">
              <span>关节 {{ index }}</span>
              <span class="joint-value">{{ joints[index-1].value }}°</span>
            </div>
            <div class="joint-buttons">
              <el-button 
                type="primary" 
                @click="adjustJoint(index-1, -1)" 
                :disabled="!isConnected"
                :loading="isLoading"
                :title="`减少 ${stepSize}°`"
              >
                <el-icon><Remove /></el-icon>
              </el-button>
              <el-slider 
                v-model="joints[index-1].value" 
                :min="joints[index-1].min" 
                :max="joints[index-1].max"
                :disabled="!isConnected"
                :step="stepSize"
                @change="(val) => onJointChange(index-1, val)"
              />
              <el-button 
                type="primary" 
                @click="adjustJoint(index-1, 1)" 
                :disabled="!isConnected"
                :loading="isLoading"
                :title="`增加 ${stepSize}°`"
              >
                <el-icon><Plus /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
        <div class="joint-column">
          <div v-for="index in 3" :key="index+2" class="joint-item">
            <div class="joint-header">
              <span>关节 {{ index + 3 }}</span>
              <span class="joint-value">{{ joints[index+2].value }}°</span>
            </div>
            <div class="joint-buttons">
              <el-button 
                type="primary" 
                @click="adjustJoint(index+2, -1)" 
                :disabled="!isConnected"
                :loading="isLoading"
                :title="`减少 ${stepSize}°`"
              >
                <el-icon><Remove /></el-icon>
              </el-button>
              <el-slider 
                v-model="joints[index+2].value" 
                :min="joints[index+2].min" 
                :max="joints[index+2].max"
                :disabled="!isConnected"
                :step="stepSize"
                @change="(val) => onJointChange(index+2, val)"
              />
              <el-button 
                type="primary" 
                @click="adjustJoint(index+2, 1)" 
                :disabled="!isConnected"
                :loading="isLoading"
                :title="`增加 ${stepSize}°`"
              >
                <el-icon><Plus /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="connection-status">
      <el-tag :type="isConnected ? 'success' : 'danger'">
        {{ isConnected ? '已连接' : '未连接' }}
      </el-tag>
      <el-button 
        type="primary" 
        @click="toggleConnection"
      >
        {{ isConnected ? '断开连接' : '连接机械臂' }}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Remove } from '@element-plus/icons-vue'
import { robotApi } from '../api/robot'
import { ElMessage } from 'element-plus'

const isConnected = ref(false)
const stepSize = ref(1)
const joints = reactive([
  { value: 0, min: -180, max: 180 },
  { value: 0, min: -180, max: 180 },
  { value: 0, min: -180, max: 180 },
  { value: 0, min: -180, max: 180 },
  { value: 0, min: -180, max: 180 },
  { value: 0, min: -180, max: 180 }
])

const toggleConnection = async () => {
  try {
    const newStatus = !isConnected.value
    console.log("new",newStatus)
    await robotApi.toggleConnection(newStatus)
    isConnected.value = newStatus
    ElMessage.success(newStatus ? '已成功连接机械臂' : '已断开连接')

    if (newStatus) {
      // 连接成功后获取当前关节状态
      const status = await robotApi.getJointsStatus()
      status.joints.forEach((angle, index) => {
        joints[index].value = angle
      })
    }
  } catch (error) {
    ElMessage.error(`连接操作失败: ${error.message}`)
    isConnected.value = false
  }
}

const adjustJoint = (index, direction) => {
  const newValue = joints[index].value + (direction * stepSize.value)
  if (newValue >= joints[index].min && newValue <= joints[index].max) {
    joints[index].value = newValue
    onJointChange(index, newValue)
  }
}

const onJointChange = async (index, value) => {
  try {
    await robotApi.updateJoint(index, value)
  } catch (error) {
    ElMessage.error(`更新关节角度失败: ${error.message}`)
    // 恢复到上一个值
    const status = await robotApi.getJointsStatus()
    joints[index].value = status.joints[index]
  }
}

// 组件加载时检查连接状态
onMounted(async () => {
  try {
    const status = await robotApi.getJointsStatus()
    if (status.connected) {
      isConnected.value = true
      status.joints.forEach((angle, index) => {
        joints[index].value = angle
      })
    }
  } catch (error) {
    console.error('获取机械臂状态失败:', error)
  }
})
</script>

<style scoped>
.control-header {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.step-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.step-label {
  font-size: 0.9em;
  color: #606266;
}

:deep(.el-radio-button__inner) {
  padding: 4px 15px;
}

.robot-control {
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.joint-controls {
  flex: 1;
  overflow-y: auto;
}

.joint-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  height: 100%;
}

.joint-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.joint-item {
  border: 1px solid #eee;
  padding: 10px;
  border-radius: 6px;
  background-color: #fafafa;
}

.joint-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-weight: bold;
  font-size: 0.9em;
}

.joint-buttons {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 8px;
  align-items: center;
}

.joint-buttons .el-button {
  padding: 8px;
  height: 32px;
  width: 32px;
}

.joint-buttons :deep(.el-slider) {
  margin: 0;
  --el-slider-height: 4px;
}

.connection-status {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

/* 自定义滚动条样式 */
.joint-controls::-webkit-scrollbar {
  width: 6px;
}

.joint-controls::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.joint-controls::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.joint-controls::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}

@media (max-width: 1400px) {
  .joint-columns {
    grid-template-columns: 1fr;
  }
}

/* 添加加载状态的样式 */
.joint-buttons .el-button.is-loading {
  pointer-events: none;
  opacity: 0.8;
}
</style> 