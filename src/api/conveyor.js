import httpClient from '../utils/http-client'

const baseURL = '/plc'

export const conveyorApi = {
  // 开启传送带
  start: () => {
    return httpClient.get(`${baseURL}/start`)
  },

  // 停止传送带
  stop: () => {
    return httpClient.get(`${baseURL}/stop`)
  },

  // 获取传送带状态
  getStatus: () => {
    return httpClient.get(`${baseURL}/status`)
  }
} 