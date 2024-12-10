<template>
  <div class="ys-view">
    <div class="camera-header">
      <span class="camera-title">{{ title }}</span>
      <!-- <div class="camera-controls">
        <el-button
          :type="isPlaying ? 'danger' : 'primary'" 
          @click="togglePlay"
        >
          {{ isPlaying ? '停止' : '开始' }}
        </el-button>
        <el-button
          :type="isRecording ? 'danger' : 'success'"
          @click="toggleRecording"
          :disabled="!isPlaying"
        >
          {{ isRecording ? '停止录制' : '开始录制' }}
        </el-button>
        <el-button
          type="primary"
          @click="toggleFullscreen"
          :disabled="!isPlaying"
        >
          <el-icon><FullScreen /></el-icon>
        </el-button>
      </div> -->
    </div>
    <div class="video-container" ref="videoContainer">
      <div id="video-player"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { FullScreen } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import EZUIKit from 'ezuikit-js'
import { ysCloudApi } from '../api/ys-cloud'

// Configure WebAssembly MIME type and instantiation
if (import.meta.env.DEV) {
  const wasm = document.createElement('script')
  wasm.type = 'application/wasm'
  document.head.appendChild(wasm)
  
  // Configure WebAssembly to use ArrayBuffer instantiation
  WebAssembly.instantiateStreaming = async (response, importObject) => {
    const buffer = await response.arrayBuffer()
    return WebAssembly.instantiate(buffer, importObject)
  }
}

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const videoContainer = ref(null)
const isPlaying = ref(false)
const isRecording = ref(false)
const player = ref(null)

// 初始化萤石云播放器
const initPlayer = async () => {
  try {
    // 获取访问令牌
    const response = await ysCloudApi.getAccessToken()
    if (response.code !== '200') {
      throw new Error(response.msg || '获取访问令牌失败')
    }
    
    const accessToken = response.data.accessToken
    
    // 使用默认设备ID构建URL
    const deviceUrl = `ezopen://open.ys7.com/BE1298292/1.hd.live`
    
    // 销毁旧的播放器实例
    if (player.value) {
      player.value.destroy()
    }
    
    // 创建新的播放器实例
    player.value = new EZUIKit.EZUIKitPlayer({
      id: 'video-player',
      accessToken,
      url: deviceUrl,
      template: 'simple',
      autoplay: true,
      handleStart: () => {
        console.log('开始播放')
        isPlaying.value = true
      },
      handleError: (e) => {
        console.error('播放器错误:', e)
        ElMessage.error('播放器错误：' + e.msg)
        isPlaying.value = false
      },
      handleSuccess: () => {
        console.log('播放器初始化成功')
      },
      decoderPath: 'https://open.ys7.com/sdk/js/1.4/ezuikit.js',
      width: videoContainer.value?.clientWidth || 800,
      height: videoContainer.value?.clientHeight || 600
    })
  } catch (error) {
    ElMessage.error('初始化播放器失败：' + error.message)
    console.error('初始化播放器错误:', error)
    isPlaying.value = false
  }
}

// 开始/停止播放
const togglePlay = async () => {
  if (isPlaying.value) {
    try {
      if (player.value) {
        isPlaying.value = false
        await player.value.stop()
        player.value.destroy()
        player.value = null
      }
    } catch (error) {
      ElMessage.error('停止播放失败')
      console.error('停止播放错误:', error)
    }
  } else {
    try {
      await initPlayer()
    } catch (error) {
      ElMessage.error('开始播放失败')
      console.error('开始播放错误:', error)
      isPlaying.value = false
    }
  }
}

// 开始/停止录制
const toggleRecording = async () => {
  if (!player.value) {
    ElMessage.error('播放器未初始化')
    return
  }

  if (isRecording.value) {
    try {
      await player.value.stopRecord()
      isRecording.value = false
      ElMessage.success('录制已停止')
    } catch (error) {
      ElMessage.error('停止录制失败')
      console.error('停止录制错误:', error)
    }
  } else {
    try {
      await player.value.startRecord()
      isRecording.value = true
      ElMessage.success('开始录制')
    } catch (error) {
      ElMessage.error('开始录制失败')
      console.error('开始录制错误:', error)
    }
  }
}

// 切换全屏
const toggleFullscreen = () => {
  if (document.fullscreenElement) {
    document.exitFullscreen()
  } else {
    videoContainer.value.requestFullscreen()
  }
}

onMounted(() => {
  initPlayer()
})

onBeforeUnmount(() => {
  if (player.value) {
    player.value.destroy()
  }
})
</script>

<style scoped>
.ys-view {
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.camera-header {
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  border-bottom: 1px solid #eee;
}

.camera-title {
  font-size: 16px;
  font-weight: bold;
}

.camera-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.video-container {
  flex: 1;
  position: relative;
  background-color: #000;
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

#video-player {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 确保视频元素正确显示 */
#video-player video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
