<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script>
export default {
  name: "App",
  onLaunch: function () {
    console.log("App Launch");
  },
  onShow: function () {
    console.log("App Show");
  },
  onHide: function () {
    console.log("App Hide");
  },
  // 全局变量, 这个属性名称只能为 globalData
  globalData: {
    // base url 一定是 10.0.2.2 表示在模拟器看来 主机的代理 ip 地址
    base_url: "http://10.0.2.2:5555", // 端口改成了 5555
    // base_url: "http://127.0.0.1:5555",
    api_key: "81708c4f856b6a0c5722ae083d93afa6",
  },
};
</script>

<style>
/*每个页面公共css */
</style>
