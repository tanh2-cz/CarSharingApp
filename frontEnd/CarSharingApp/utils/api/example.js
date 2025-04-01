// exp 1: 一个文件放一种类型的多个api
// 引入 request 文件
import request from '../request.js'
export const login = (params) => {
	return request({
		url: '/login',
		method: 'post',
		data: params,
		header: {
			"Content-Type": 'application/json'
		},
	})
}

// 登出
export const logout =(params) => {
	return request({
		url: '/logout',
		method: 'post',
		data: params,
		header: {
			"Content-Type": 'application/json'
		},
	})
}
// exp 1 引入方式
// import { login } from 'api文件相对地址'

//
//
//
//
//
//
//







// exp 2: 一个文件只放一个api 也就是一个函数
// 引入 request 文件
import request from '../request.js'

// 上传
export default (params) => { // 默认导出 export default
	// console.log(调试信息, 例如传入的参数);
	return request({
		url: '/work/sync',
		method: 'post', // post get put delete
		queryParams: {
			...params.queryParams
		},
		data: params.data,
		header: {
			"Content-Type": 'application/json', // 内容格式 一般取值为 json 或者 表单
			"Authorization": params.token,      // 前后端通信的令牌
		},
	})
}
// exp 2 引入方式
// import '随便给api取的一个名字' from 'api文件相对地址'

//
//
//

// api 使用方式
...
import { login } from 'api文件相对地址' // 引入
...
// 定义传给 api 的参数
const params = {
	token: '...',
	userName: 'admin',
	password: '123',
}
...
// 把参数传给api, 调用api
await login(params).then((res) => {
	// res 是响应结果
	// 处理响应结果
}).err((error) => {
	// error 是报错信息
	// 处理报错
})
...