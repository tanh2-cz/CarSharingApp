// 全局请求封装

// 请求超出时间
const timeout = 2000000

const defaultHeaders = {
  "Content - Type": "application/json"
};

export default (params) => {
	// 下面两行换了个位置发现不报错了 
	const app = getApp();
	const base_url = app.globalData.base_url;
	console.log(params);
	return new Promise((resolve, reject) => {
		let url = base_url + params.url;
		console.log('rrrr', url);
		if (params.queryParams && params.method === 'get') {
			const queryString = Object.keys(params.queryParams).map(key => {
				return `${key}=${params.queryParams[key]}`;
			}).join('&');
			url += `?${queryString}`;
		}
		console.log('sss', url);
		uni.request({
			url: url,
			method: params.method || "get",
			header: {
				...params.header
			},
			data: params.data || {},
			timeout: timeout,
			sslVerify:false,
			success(response) {
				// 根据返回的状态码做出对应的操作
				console.log(response)
				if (response.statusCode === 200) {
					if(response.data.code===200){
						resolve(response.data);
					}
					else{
						console.log('aaaa????')
						reject(response.data.msg);
					}
					
				} else {
					uni.clearStorageSync()
					switch (response.statusCode) {
						case 401:
							uni.showModal({
								title: "提示",
								content: "请登录",
								showCancel: false,
								success() {
									setTimeout(() => {
										uni.navigateTo({
											url: "/pages/login/login",
										})
									}, 1000);
								},
							});
							break;
						case 404:
							uni.showToast({
								title: '请求地址不存在...',
								duration: 2000,
							})
							break;
						default:
							uni.showToast({
								title: '请重试...',
								duration: 2000,
							})
							break;
					}
					reject(new Error(`请求失败，状态码：${response.statusCode}`));
				}
			},
			fail(err) {
				if (err.errMsg.indexOf('request:fail') !== -1) {
					uni.showToast({
						title: '网络异常',
						icon: "error",
						duration: 2000
					})
				} else {
					uni.showToast({
						title: '未知异常',
						duration: 2000
					})
				}
				reject(err);
			}
		});
	});
};