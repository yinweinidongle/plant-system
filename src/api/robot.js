import httpClient from '../utils/http-client'

const baseURL = '/robot'

export const robotApi = {
  // 连接/断开机械臂
  toggleConnection: (status) => {
    return httpClient.post(`${baseURL}/connection`, { status })
  },

  // 更新单个关节角度
  updateJoint: (jointIndex, angle) => {
    return httpClient.post(`${baseURL}/joint`, {
      joint: jointIndex,
      angle: angle
    })
  },

  // 获取所有关节状态
  getJointsStatus: () => {
    return httpClient.get(`${baseURL}/status`)
  },

  // 紧急停止
  emergencyStop: () => {
    return httpClient.post(`${baseURL}/emergency-stop`)
  }
} 