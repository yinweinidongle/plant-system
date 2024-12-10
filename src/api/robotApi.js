import axios from 'axios'

// 创建axios实例

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000', // 替换为实际的机械臂控制API地址
  timeout: 25000,
  headers: {
     "Content-Type":"application/json"
  }
})


// 机械臂控制API
export const robotApi = {
  // 获取当前机械臂状态
  getStatus() {
    return api.get('/robot/status')
  },
  
  // 控制单个关节
  controlJoint(jointId, angle) {
    return api.post('/control/joint', {
      jointId,
      angle
    })
  },
  
  // 控制所有关节
  controlAllJoints(angles) {
    return api.post('/control/all', {
      angles
    })
  },
  
  // 急停
  emergencyStop() {
    return api.post('/emergency-stop')
  },
  
  // 获取机械臂位姿
  getPose() {
    return api.get('/pose')
  },

  // 展台启动
  scStart() {
    return api.get('/plc/start')
  },

  // 拍照
  takePhoto() {
    return api.get('/take-photo')
  },

  // 轨迹移动
  takePath() {
    return api.get('/take-path')
  },

  // 任务处理
  handleTaskJob(taskId) {
    return api.post('/task/job', {
      taskId
    })
  },

  // 修改寄存器地址
  writeRegister(value){
    return api.post('/plc/write_register', {
      value
    })
  },

  // 空间移动控制
  controlMove(params) {
    return api.post('/control/move', params)
  }
} 