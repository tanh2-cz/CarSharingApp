<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <view class="top-bar">
      <view class="search-bar">
        <image src="/static/icon_search.png" class="search-icon"></image>
        <input type="text" v-model="searchQuery" placeholder="搜索拼车消息" class="search-input" />
      </view>
      <view class="filter-btn" @tap="toggleFilter">
        <image src="/static/icon_filter.png" class="filter-icon"></image>
      </view>
    </view>

    <!-- 搜索条件弹出框 -->
    <view class="filter-panel" v-if="showFilter">
      <view class="filter-content">
        <view class="filter-header">
          <text>筛选条件</text>
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
          <text class="time">出发时间: {{ ride.time }}</text>
          <text class="price">价格: ¥{{ ride.price }}</text>
        </view>
        <view class="ride-status">
          <text>{{ ride.status }}</text>
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
        { id: 3, startLocation: '徐家汇', endLocation: '静安寺', time: '09:00', price: 30, status: '待接单' }
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
      uni.showToast({
        title: `查看拼车单: ${ride.id}`,
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
}

.top-bar {
  padding: 20rpx 30rpx;
  background: linear-gradient(45deg, #409eff, #67c23a);
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

.search-bar {
  flex: 1;
  background: #fff;
  border-radius: 50rpx;
  padding: 20rpx 30rpx;
  display: flex;
  align-items: center;
}

.search-icon {
  width: 40rpx;
  height: 40rpx;
  margin-right: 20rpx;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  color: #333;
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
  background: #fff;
}

.ride-item {
  padding: 30rpx;
  border-bottom: 1rpx solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ride-info {
  display: flex;
  flex-direction: column;
}

.route {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.start, .end {
  font-size: 32rpx;
  color: #333;
  max-width: 200rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.route text {
  margin: 0 10rpx;
  color: #999;
}

.time, .price {
  font-size: 24rpx;
  color: #999;
  margin-top: 5rpx;
}

.ride-status text {
  font-size: 24rpx;
  color: #409eff;
}

.no-data {
  padding: 40rpx;
  text-align: center;
  font-size: 28rpx;
  color: #999;
}
</style>