// 引入 request 文件
import request from '../request.js'

// 登录接口
export default (params) => { // 默认导出 export default
	console.log(params);
	return request({
		url: '/signup',
		method: 'post', // post get put delete
		queryParams: {
			...params.queryParams
		},
		data: params.data,
		header: {
			"Content-Type": 'application/json', // 内容格式 一般取值为 json 或者 表单
			'Access-Control-Allow-Origin': '*'
		},
	})
}
