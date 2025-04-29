<template>
  <view class="container">
    <!-- 地图区域（占位） -->
    <view class="map-placeholder">
      <text>地图区域（占位，可替换为高德地图组件）</text>
    </view>

    <!-- 搜索框 -->
    <view class="search-bar">
      <view class="search-input" @tap="goToSearch">
        <text class="placeholder">支持地址、公交、地铁</text>
      </view>
    </view>

    <!-- 功能入口 -->
    <scroll-view scroll-y class="function-list">
      <view class="function-grid">
        <view class="function-item" @tap="handleFunction('美食')">
          <image src="/static/icon_food.png" class="icon"></image>
          <text>美食</text>
        </view>
        <view class="function-item" @tap="handleFunction('酒店')">
          <image src="/static/icon_hotel.png" class="icon"></image>
          <text>酒店</text>
        </view>
        <view class="function-item" @tap="handleFunction('景点门票')">
          <image src="/static/icon_ticket.png" class="icon"></image>
          <text>景点门票</text>
        </view>
        <view class="function-item" @tap="handleFunction('加油站点')">
          <image src="/static/icon_gas.png" class="icon"></image>
          <text>加油站点</text>
        </view>
        <view class="function-item" @tap="handleFunction('休闲娱乐')">
          <image src="/static/icon_entertainment.png" class="icon"></image>
          <text>休闲娱乐</text>
        </view>
        <view class="function-item" @tap="handleFunction('超市')">
          <image src="/static/icon_market.png" class="icon"></image>
          <text>超市</text>
        </view>
        <view class="function-item" @tap="handleFunction('火车')">
          <image src="/static/icon_train.png" class="icon"></image>
          <text>火车</text>
        </view>
        <view class="function-item" @tap="handleFunction('livehouse')">
          <image src="/static/icon_livehouse.png" class="icon"></image>
          <text>livehouse</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  methods: {
    goToSearch() {
      uni.navigateTo({
        url: '/pages/search/search'
      });
    },
    handleFunction(type) {
      uni.showToast({
        title: `点击了${type}功能`,
        icon: 'none'
      });
    },
	clk() {
		uni.getLocation({
		  type: 'wgs84',
		  geocode:true,
		  success: function(res) {
		    console.log('经度：' + res.longitude)
		    console.log('纬度：' + res.latitude)
		  },
		  fail: function(res) {
		    console.log('定位失败')
		  }
		})
	}
  }
}
</script>

<style scoped>
.container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.map-placeholder {
  flex: 1;
  background: #e0e0e0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 28rpx;
  color: #666;
}

.search-bar {
  padding: 20rpx;
  background: #fff;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

.search-input {
  background: #f5f5f5;
  border-radius: 50rpx;
  padding: 20rpx 30rpx;
  display: flex;
  align-items: center;
}

.placeholder {
  color: #999;
  font-size: 28rpx;
}

.function-list {
  height: 400rpx;
  background: #fff;
}

.function-grid {
  display: flex;
  flex-wrap: wrap;
  padding: 20rpx;
}

.function-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30rpx;
}

.icon {
  width: 60rpx;
  height: 60rpx;
  margin-bottom: 10rpx;
}

.function-item text {
  font-size: 24rpx;
  color: #333;
}
</style>