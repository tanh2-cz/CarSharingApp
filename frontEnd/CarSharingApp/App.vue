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
			base_url: 'http://localhost:8088',
		}
	}
</script>

<style>
	/*每个页面公共css */
</style>
