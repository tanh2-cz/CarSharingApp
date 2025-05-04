<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <view class="top-bar">
      <text class="title">拼车</text>
	  <view class="search-bar">
	  		<input type="text" v-model="searchQuery" placeholder="搜索消息" class="search-input" />
	  		<image src="/static/image/icon_search.png" class="search-icon"></image>
	  </view>
      <view class="filter-buttons" @tap="toggleFilter">
        <image src="/static/image/icon_filter.png" class="filter-icon" @tap="showFilter"></image>
      </view>
    </view>

    <!-- 搜索条件弹出框 -->
    <view class="filter-panel" v-if="showFilter">
      <view class="filter-content">
        <view class="filter-header">
          <text>高级筛选</text>
          <image src="/static/icon_close.png" class="close-icon" @tap="toggleFilter"></image>
        </view>
        <view class="filter-item">
          <text>出发地</text>
          <input type="text" v-model="filter.startLocation" placeholder="请输入出发地" class="filter-input" />
        </view>
        <view class="filter-item">
          <text>目的地</text>
          <input type="text" v-model="filter.endLocation" placeholder="请输入目的地" class="filter-input" />
        </view>
        <view class="filter-item">
          <text>出发时间</text>
          <picker mode="time" :value="filter.time" @change="updateTime">
            <view class="picker">{{ filter.time || "请选择时间" }}</view>
          </picker>
        </view>
		<!-- 价位 -->
        <button class="apply-btn" @tap="applyFilter">应用筛选</button>
      </view>
    </view>

    <!-- 拼车通知列表 -->
    <scroll-view scroll-y class="ride-list">
      <view class="ride-item" v-for="(ride, index) in filteredRides" :key="index" @tap="viewRideDetail(ride)">
        <view class="ride-info">
          <view class="route">
            <text class="start">{{ ride.startLocation }}</text>
            <text> → </text>
            <text class="end">{{ ride.endLocation }}</text>
          </view>
          <view class="text-details">
            <text class="text-time">出发时间: {{ ride.time }}</text>
            <text class="text-price">价格: ¥{{ ride.price }}</text>
          </view>
        </view>
		<!-- 司机视角 待接单 已接单 -->
<!--        <view class="ride-status">
          <text>{{ ride.status }}</text>
        </view> -->
		<!-- 用户视角 是否已加入群聊 群聊按钮 -->
		<view class="ride-status">
		  <button v-if="ride.status === 0" class="status-button disabled" disabled>
		    已加群
		  </button>
		  <button v-else class="status-button" @click="goToGroupDetails">
		    加群去拼车
		  </button>
		</view>
		
      </view>
      <view class="no-data" v-if="!filteredRides.length">暂无拼车消息</view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      showFilter: false,
      filter: {
        startLocation: '',
        endLocation: '',
        time: ''
      },
      rides: [
        { id: 1, startLocation: '上海大学', endLocation: '虹桥机场', time: '14:30', price: 50, status: '待接单' },
        { id: 2, startLocation: '浦东机场', endLocation: '人民广场', time: '16:00', price: 80, status: '已接单' },
        { id: 3, startLocation: '徐家汇', endLocation: '静安寺', time: '09:00', price: 30, status: '待接单' },
		{ id: 4, startLocation: '同济大学', endLocation: '五角场', time: '09:00', price: 30, status: '待接单' },
		{ id: 5, startLocation: '五角场', endLocation: '上海交通大学', time: '09:00', price: 30, status: '待接单' },
		{ id: 6, startLocation: '嘉定', endLocation: '豫园', time: '09:00', price: 30, status: '待接单' },
		{ id: 7, startLocation: '徐家汇', endLocation: '嘉定', time: '09:00', price: 30, status: '待接单' },
		{ id: 0, startLocation: '徐家汇', endLocation: '嘉定', time: '09:00', price: 30, status: '待接单' },
      ],
      filteredRides: []
    };
  },
  onLoad() {
    this.filteredRides = this.rides; // 初始显示所有拼车消息
  },
  methods: {
    toggleFilter() {
      this.showFilter = !this.showFilter;
    },
    updateTime(e) {
      this.filter.time = e.detail.value;
    },
	goToGroupDetails() {
	    // 假设详情页面的路由路径为 /details
		uni.showToast({
		  title: '查看群聊详细信息待实现',
		  icon: 'none'
		});
		},
	    // uni.navigateTo({
	    //   url: '/pages/details/details'
	    // });
    applyFilter() {
      // 筛选逻辑
      this.filteredRides = this.rides.filter(ride => {
        const matchStart = this.filter.startLocation ? ride.startLocation.includes(this.filter.startLocation) : true;
        const matchEnd = this.filter.endLocation ? ride.endLocation.includes(this.filter.endLocation) : true;
        const matchTime = this.filter.time ? ride.time === this.filter.time : true;
        const matchQuery = this.searchQuery ? (ride.startLocation.includes(this.searchQuery) || ride.endLocation.includes(this.searchQuery)) : true;
        return matchStart && matchEnd && matchTime && matchQuery;
      });
      this.showFilter = false;
    },
    viewRideDetail(ride) {
		//预计下面弹出来一个简略的信息，点击其他地方自动收回去，然后点击加群可以显示详细信息，专门一个页面显示
      uni.showToast({
        title: `查看拼车单简略信息待实现: ${ride.id}`,
        icon: 'none'
      });
    }
  }
}
</script>

<style scoped>
.container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
  position: relative;
}

.top-bar {
  padding: 30rpx 40rpx;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
  position: fixed;
  z-index: 10;
  width: 100%;
  height: 4%;
  background-color: #28a745;
}

.title {
  font-size: 38rpx;
  font-weight: 600;
  color: #333;
  letter-spacing: 1rpx;
}

.search-bar {
  flex: 1;
  background: #fff;
  border-radius: 25rpx;
  display: flex;
  align-items: center;
  height: 100%;
  border: 4rpx solid #ccc;
  margin-left: 5%;
  width: 60%;
}

.search-icon {
  width: 50rpx;
  height: 50rpx;
  margin-right: 20rpx;
  /* background-color: #333; */
}

.search-input {
  flex: 1;
  font-size: 30rpx;
  color: #333;
  /* background-color: #28a745; */
  margin-left:7%;
}

.filter-btn {
  margin-left: 20rpx;
}

.filter-icon {
  width: 48rpx;
  height: 48rpx;
}

.filter-panel {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: flex-start;
}

.filter-content {
  width: 70%;
  height: 100%;
  background: #fff;
  padding: 40rpx;
  display: flex;
  flex-direction: column;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
}

.filter-header text {
  font-size: 36rpx;
  font-weight: bold;
}

.close-icon {
  width: 40rpx;
  height: 40rpx;
}

.filter-item {
  margin-bottom: 40rpx;
}

.filter-item text {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 10rpx;
}

.filter-input, .picker {
  background: #f5f5f5;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #333;
}

.apply-btn {
  background: #409eff;
  color: #fff;
  font-size: 32rpx;
  padding: 20rpx;
  border-radius: 12rpx;
  margin-top: auto;
  border: none;
}

.ride-list {
  flex: 1;
  background: #fff;  flex: 1;
  background: #fff;
  padding: 20rpx 0;
  margin-top: 12%;
  margin-bottom: 10%;
  width: 100%;
}

.ride-item {
  padding: 30rpx; /* 内边距 */
  border-bottom: 1rpx solid #eee; /* 底部边框 */
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff; /* 背景颜色 */
  border-radius: 12rpx; /* 圆角 */
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08); /* 阴影 */
  margin-bottom: 20rpx; /* 卡片之间的间距 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 过渡效果 */
  position: relative; /* 相对定位 */
  margin:2%;
  width: 88%;
}

.ride-item:hover {
  transform: translateY(-10rpx); /* 鼠标悬停时向上移动 */
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.12); /* 鼠标悬停时阴影加深 */
}

.ride-info {
  display: flex;
  flex-direction: column;
  /* background-color: #999; */
  width: 80%;
}

.route {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
  justify-content: flex-start; /* 水平起始对齐 */
  /* background-color: #eee; */
}

.text-details {
  display: flex;
  align-items: center;
}

.text-time {
  font-size: 30rpx;
  color: #007BFF; /* 蓝色提示颜色 */
  font-family: 'SimHei', sans-serif; /* 调整字体类型 */
  font-weight: bold; /* 加粗 */
  margin-left: 2%;
}

.text-price {
  font-size: 30rpx;
  color: #28A745; /* 绿色提示颜色 */
  margin-left: 10%; /* 左边距 */
  font-family:  'SimHei', sans-serif; /* 调整字体类型 */
  font-weight: bold; /* 加粗 */
}

.start, .end {
  font-size: 36rpx; /* 字体大小 */
  color: #333; /* 字体颜色 */
  font-weight: bold; /* 加粗 */
  font-family: 'PingFang SC', 'Microsoft YaHei', 'SimHei', sans-serif; /* 设置中文字体 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 显示省略号 */
  white-space: nowrap; /* 不换行 */
}

.route text {
  margin: 0 10rpx;
  color: #000;
}


.no-data {
  padding: 40rpx;
  text-align: center;
  font-size: 28rpx;
  color: #999;
}

.filter-buttons {
  display: flex;
  align-items: center;
  width: 15%;
  height: 100%;
  /* background-color: #34aadc; */
  justify-content: left;
  margin-left: 5%;
}

.filter-icon {
  width: 44rpx;
  height: 44rpx;
  transition: var(--transition);
}

.filter-icon:active {
  transform: scale(0.9);
  opacity: 0.8;
}

.ride-status{
	margin-right: 2%;
}

.status-button {
  width:120%;
  height:40%;
  border-radius: 4rpx;
  font-size: 26rpx;
  color: #fff;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'SimHei', sans-serif; /* 设置中文字体 */
  background-color: #ffaa00;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.status-button.disabled {
  background-color: #ccc; /* 灰色 */
  cursor: not-allowed;
}

.status-button:active {
  background-color: #ffaa7f; /* 按下时的深蓝色 */
}
</style>