// 引入 request 文件
import request from '../request.js'

// 获取orderinfo接口
export default () => { // 默认导出 export default
    // console.log(调试信息, 例如传入的参数);
    return request({
        url: '/order',
        method: 'post', // post get put delete
        queryParams: {
            // 传入的参数
        },
        header: {
            "Content-Type": 'application/json', // 内容格式 一般取值为 json 或者 表单
        },
    })
}
