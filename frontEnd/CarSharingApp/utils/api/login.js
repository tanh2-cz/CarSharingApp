// 引入 request 文件
import request from '../request.js'

// 登录接口
export default (params) => { // 默认导出 export default
	// console.log(调试信息, 例如传入的参数);
	return request({
		url: '/login',
		method: 'post', // post get put delete
		queryParams: {
			...params.queryParams
		},
		data: params.data,
		header: {
			"Content-Type": 'application/json', // 内容格式 一般取值为 json 或者 表单
		},
	})
}
