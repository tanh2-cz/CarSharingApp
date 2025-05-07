<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script>
	export default {
		name: "App",
		onLaunch: function() {
			console.log('App Launch');
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		},
		// 全局变量, 这个属性名称只能为 globalData
		globalData: {
			base_url: 'http://localhost:5555', // 端口改成了 5555
			api_key: '81708c4f856b6a0c5722ae083d93afa6'
		}
	}
</script>

<style>
	/*每个页面公共css */
</style>
