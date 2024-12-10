
import axios from "axios";
import { message } from "ant-design-vue";

const service = axios.create({
  baseURL: "/",
  timeout: 1000 * 60 * 5, //5分钟
  headers: { "Content-Type": "application/json" },
});
const whiteList = ["/api/plyAnalysis"];
// 添加请求拦截器
service.interceptors.request.use(
  (config) => {

    if (whiteList.includes(config.url)) {
      config.headers["Content-Type"] =
        "application/x-www-form-urlencoded;charset=UTF-8";
      delete config.headers.token;
    } else {
      if (token) {
        // 在发送请求之前做些什么 token
        config.headers.token = token;
      }
    }

    return config;
  },
  (error) => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 添加响应拦截器
service.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    const res = response.data;

    console.log("lanjie",res)

    return res;

    // if (res.errCode) {
    //   // `token` 过期或者账号已在别处登录
    //   if (res.errCode === 401) {
        
    //     return;
    //   }
    //   if (res.errCode != 200) {
    //     message.error(res.message);
    //     return;
    //   }
    //   return res;
    // } else {
    //   if (res.code == 200) {
    //     return res;
    //   }
    //   return Promise.reject(service.interceptors.response.error);
    // }
  },
  (error) => {
    console.log("err", error);
    // 对响应错误做点什么
    if (error.message.indexOf("timeout") != -1) {
      message.error(this.$t('common.timeout'));
    } else if (error.message == "Network Error") {
      message.error(this.$t('common.networkError'));
    } else {
      message.error(error.response.data.message);
    }
    return Promise.reject(error);
  }
);

export default service;
