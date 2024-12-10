import request from "../utils/request";


// 计算长宽面积
export function compute(params) {
  return request({
    url: "/api/plyAnalysis",
    method: "get",
    params,
  });
}