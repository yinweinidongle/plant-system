<template>
  <div class="conveyor-diagram">
    <h3>传送带状态图</h3>
    <div class="canvas-container">
      <canvas ref="canvasRef" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'

const canvasRef = ref(null)
let animationId = null
let offset = 0
let boxes = []
let flashOpacity = 0
let isRecording = false
let recordingBox = null
let isPausing = false
let pauseTimer = null
let cameraBlinkState = false
let cameraBlinkTimer = null
let boxBlinkState = false
let boxBlinkTimer = null

// 拍照点位置（在顶部传送带的中间位置）
const getCameraPosition = (width, height) => {
  const margin = 40
  const beltWidth = width - margin * 2
  return {
    x: margin + beltWidth / 2,
    y: margin
  }
}

// 检查是否在拍照点位置
const checkPhotoPosition = (boxX, boxY, cameraX, cameraY) => {
  const threshold = 1
  return Math.abs(boxX - cameraX) < threshold && Math.abs(boxY - cameraY) < threshold+20
}

// 初始化箱子位置
const initBoxes = (width, height) => {
  const trackLength = (width - 80) * 2 + (height - 160)
  const spacing = trackLength / 3
  
  boxes = [
    { pos: 0, color: '#67C23A', lastPhoto: 0, visible: true },
    { pos: spacing, color: '#E6A23C', lastPhoto: 0, visible: true },
    { pos: spacing * 2, color: '#F56C6C', lastPhoto: 0, visible: true }
  ]
}

// 开始暂停倒计时
const startPause = (box, x, y) => {
  isPausing = true
  pauseTimer = setTimeout(() => {
    isPausing = false
    startRecording(box, x, y)
  }, 500) // 延长停留时间到3秒
}

// 开始相机闪烁
const startCameraBlink = () => {
  if (cameraBlinkTimer) return
  cameraBlinkTimer = setInterval(() => {
    cameraBlinkState = !cameraBlinkState
  }, 500)
}

// 停止相机闪烁
const stopCameraBlink = () => {
  if (cameraBlinkTimer) {
    clearInterval(cameraBlinkTimer)
    cameraBlinkTimer = null
    cameraBlinkState = false
  }
}

// 开始花盆闪烁
const startBoxBlink = () => {
  if (boxBlinkTimer) return
  boxBlinkTimer = setInterval(() => {
    boxBlinkState = !boxBlinkState
  }, 300)
}

// 停止花盆闪烁
const stopBoxBlink = () => {
  if (boxBlinkTimer) {
    clearInterval(boxBlinkTimer)
    boxBlinkTimer = null
    boxBlinkState = false
  }
}

// 开始录制动作
const startRecording = (box, x, y) => {
  isRecording = true
  recordingBox = { ...box, x, y }
  startCameraBlink()
  startBoxBlink()
  
  // 3秒后结束录制
  setTimeout(() => {
    stopRecording()
  }, 3000)
}

// 结束录制动作
const stopRecording = () => {
  isRecording = false
  recordingBox = null
  stopCameraBlink()
  stopBoxBlink()
}

// 绘制录制指示器
const drawRecordingIndicator = (ctx, x, y) => {
  ctx.fillStyle = '#F56C6C'
  ctx.beginPath()
  ctx.arc(x, y - 50, 8, 0, Math.PI * 2)
  ctx.fill()
  
  ctx.font = '14px Arial'
  ctx.fillStyle = '#F56C6C'
  ctx.textAlign = 'center'
  ctx.fillText('录制中...', x, y - 65)
}

// 计算箱子在传送带上的实际坐标
const getBoxCoordinates = (position, width, height) => {
  const margin = 40
  const beltWidth = width - margin * 2
  const beltHeight = height - margin * 2
  const topY = margin + 20 // 传送带整体下移20像素
  const bottomY = height - margin + 20 // 底部也相应下移20像素
  const leftX = margin
  const rightX = width - margin

  // 计算传送带各段长度
  const topLength = beltWidth
  const rightLength = topLength + beltHeight
  const bottomLength = rightLength + beltWidth

  if (position < topLength) {
    // 顶部段
    return { x: leftX + position, y: topY }
  } else if (position < rightLength) {
    // 右侧段
    return { x: rightX, y: topY + (position - topLength) }
  } else if (position < bottomLength) {
    // 底部段
    return { x: rightX - (position - rightLength), y: bottomY }
  } else {
    // 左侧段
    return { x: leftX, y: bottomY - (position - bottomLength) }
  }
}

// 绘制拍照点的代码
const drawCameraPoint = (ctx, x, y, beltWidth) => {
  // 只在非闪烁状态或未录制时绘制
  if (!isRecording || !cameraBlinkState) {
    // 根据状态选择颜色
    ctx.fillStyle = isRecording ? '#F56C6C' : '#409EFF'
    ctx.beginPath()
    ctx.arc(x, y - beltWidth/2 - 10, 6, 0, Math.PI * 2)
    ctx.fill()

    // 绘制相机图标
    ctx.strokeStyle = isRecording ? '#F56C6C' : '#409EFF'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(x - 10, y - beltWidth/2 - 20)
    ctx.lineTo(x + 10, y - beltWidth/2 - 20)
    ctx.lineTo(x + 10, y - beltWidth/2 - 30)
    ctx.lineTo(x - 10, y - beltWidth/2 - 30)
    ctx.closePath()
    ctx.stroke()
  }
}

// 绘制传送带和移动的花盆
const draw = (ctx, width, height) => {
  // 清空画布
  ctx.clearRect(0, 0, width, height)

  const margin = 40
  const beltWidth = 40

  // 绘制传送带外框
  ctx.strokeStyle = '#909399'
  ctx.lineWidth = 2
  ctx.beginPath()
  // 外框
  ctx.strokeRect(margin, margin + 20, width - margin * 2, height - margin * 2) // 下移20像素
  // 内框
  ctx.strokeRect(
    margin + beltWidth,
    margin + beltWidth + 20, // 下移20像素
    width - (margin + beltWidth) * 2,
    height - (margin + beltWidth) * 2
  )

  // 为传送带添加浅色填充
  ctx.fillStyle = '#F5F7FA'
  ctx.fillRect(margin, margin + 20, width - margin * 2, height - margin * 2) // 下移20像素
  ctx.fillStyle = '#FFFFFF'
  ctx.fillRect(
    margin + beltWidth,
    margin + beltWidth + 20, // 下移20像素
    width - (margin + beltWidth) * 2,
    height - (margin + beltWidth) * 2
  )

  // 绘制拍照点
  const { x: cameraX, y: cameraY } = getCameraPosition(width, height)
  drawCameraPoint(ctx, cameraX, cameraY, beltWidth)

  // 如果有闪光效果，绘制闪光
  if (flashOpacity > 0) {
    ctx.fillStyle = `rgba(255, 255, 255, ${flashOpacity})`
    ctx.fillRect(cameraX - 20, cameraY - beltWidth/2 - 40, 40, 40)
    flashOpacity -= 0.1
  }

  // 如果正在录制，绘制录制指示器
  if (isRecording) {
    drawRecordingIndicator(ctx, cameraX, cameraY - beltWidth/2)
  }

  // 绘制花盆
  const potSize = 22 // 缩小花盆尺寸
  boxes.forEach(box => {
    if (!isRecording && !isPausing) {
      // 正常移动
      box.pos += 1
      const trackLength = (width - 80) * 2 + (height - 160)
      if (box.pos >= trackLength) {
        box.pos = 0
        box.lastPhoto = 0
      }
    }

    const { x, y } = getBoxCoordinates(box.pos, width, height)
    
    // 检查是否需要开始录制
    if (!isPausing && !isRecording && box.lastPhoto === 0 && 
        checkPhotoPosition(x, y, cameraX, cameraY)) {
      box.lastPhoto = 1
      startPause(box, x, y)
    }

    // 判断是否需要绘制花盆(在录制状态下闪烁)
    const shouldDraw = !isRecording || 
                      box.color !== recordingBox?.color || 
                      (box.color === recordingBox?.color && boxBlinkState)

    if (shouldDraw) {
      // 绘制花盆和植物
      // 花盆主体
      ctx.beginPath()
      ctx.moveTo(x - potSize/3, y - potSize/3)
      ctx.lineTo(x + potSize/3, y - potSize/3)
      ctx.lineTo(x + potSize/4, y + potSize/3)
      ctx.lineTo(x - potSize/4, y + potSize/3)
      ctx.closePath()
      
      ctx.fillStyle = box.color
      ctx.fill()
      ctx.strokeStyle = '#606266'
      ctx.lineWidth = 2
      ctx.stroke()
      
      // 花盆底座
      ctx.beginPath()
      ctx.moveTo(x - potSize/4, y + potSize/3)
      ctx.lineTo(x + potSize/4, y + potSize/3)
      ctx.lineTo(x + potSize/5, y + potSize/3 + 3)
      ctx.lineTo(x - potSize/5, y + potSize/3 + 3)
      ctx.closePath()
      ctx.fillStyle = box.color
      ctx.fill()
      ctx.stroke()

      // 植物
      ctx.beginPath()
      ctx.moveTo(x, y - potSize/3)
      ctx.bezierCurveTo(x - potSize/4, y - potSize/2, x - potSize/4, y - potSize, x, y - potSize)
      ctx.bezierCurveTo(x + potSize/4, y - potSize, x + potSize/4, y - potSize/2, x, y - potSize/3)
      ctx.fillStyle = '#4CAF50'
      ctx.fill()

      // 花朵
      ctx.beginPath()
      ctx.arc(x, y - potSize, potSize/6, 0, Math.PI * 2)
      ctx.fillStyle = '#FF9800'
      ctx.fill()
    }
  })
}

// 获取花盆颜色描述
const getBoxColor = (color) => {
  switch (color) {
    case '#67C23A': return '绿色'
    case '#E6A23C': return '黄色'
    case '#F56C6C': return '红色'
    default: return ''
  }
}

// 动画循环
const animate = () => {
  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')

  offset -= 1
  if (offset <= -30) offset = 0

  draw(ctx, canvas.width, canvas.height)
  animationId = requestAnimationFrame(animate)
}

// 调整画布大小
const resizeCanvas = () => {
  const canvas = canvasRef.value
  const container = canvas.parentElement
  const dpr = window.devicePixelRatio || 1
  
  canvas.width = container.clientWidth * dpr
  canvas.height = container.clientHeight * dpr
  
  const ctx = canvas.getContext('2d')
  ctx.scale(dpr, dpr)
  
  canvas.style.width = `${container.clientWidth}px`
  canvas.style.height = `${container.clientHeight}px`

  initBoxes(canvas.width / dpr, canvas.height / dpr)
}

onMounted(() => {
  window.addEventListener('resize', resizeCanvas)
  resizeCanvas()
  animate()
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeCanvas)
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (pauseTimer) {
    clearTimeout(pauseTimer)
  }
  if (cameraBlinkTimer) {
    clearInterval(cameraBlinkTimer)
  }
  if (boxBlinkTimer) {
    clearInterval(boxBlinkTimer)
  }
})
</script>

<style scoped>
.conveyor-diagram {
  height: 110%;
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

h3 {
  margin: 0 0 15px 0;
  color: #2c3e50;
}

.canvas-container {
  flex: 1;
  background: #f8f9fa;
  border-radius: 4px;
  overflow: hidden;
}

canvas {
  width: 100%;
  height: 110%;
}
</style> 