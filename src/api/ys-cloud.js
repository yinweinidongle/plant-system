import httpClient from '../utils/http-client'

// 萤石云 API 配置
const YS_CONFIG = {
  appKey: import.meta.env.VITE_YS_APP_KEY,
  appSecret: import.meta.env.VITE_YS_APP_SECRET
}

export const ysCloudApi = {
  // 获取访问令牌
  getAccessToken: () => {
    return httpClient.post('https://open.ys7.com/api/lapp/token/get', {
      appKey: YS_CONFIG.appKey,
      appSecret: YS_CONFIG.appSecret
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  }
} 