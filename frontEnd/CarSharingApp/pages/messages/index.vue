<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <view class="top-bar">
      <text class="title">拼车</text>
      <view class="search-bar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜索消息"
          class="search-input"
        />
        <image src="/static/image/icon_search.png" class="search-icon"></image>
      </view>
      <view class="filter-buttons" @tap="toggleFilter">
        <image
          src="/static/image/icon_filter.png"
          class="filter-icon"
          @tap="showFilter"
        ></image>
      </view>
    </view>

    <!-- 搜索条件弹出框 -->
    <view class="filter-panel" v-if="showFilter">
      <view class="filter-content">
        <view class="filter-header">
          <text>高级筛选</text>
          <image
            src="/static/icon_close.png"
            class="close-icon"
            @tap="toggleFilter"
          ></image>
        </view>

        <!-- 修改后的地点选择块 -->
        <view class="location-block">
          <text class="location-block-title">起点-目的地</text>
          <view class="location-inputs">
            <view class="location-input-group">
              <text class="location-label">起点</text>
              <input
                type="text"
                v-model="filter.startLocation"
                placeholder="请输入出发地"
                class="filter-input"
              />
            </view>
            <text style="color: #999">→</text>
            <view class="location-input-group">
              <text class="location-label">终点</text>
              <input
                type="text"
                v-model="filter.endLocation"
                placeholder="请输入目的地"
                class="filter-input"
              />
            </view>
          </view>
        </view>

        <!-- 修改时间选择部分 -->
        <view class="filter-item">
          <text>出发时间</text>
          <view class="time-range">
            <view class="time-input-group">
              <text class="time-label">开始时间</text>
              <picker
                mode="time"
                :value="filter.startTime"
                @change="updateStartTime"
              >
                <view class="picker">{{ filter.startTime || "请选择" }}</view>
              </picker>
            </view>
            <text style="color: #999; margin: 0 20rpx">-</text>
            <view class="time-input-group">
              <text class="time-label">结束时间</text>
              <picker
                mode="time"
                :value="filter.endTime"
                @change="updateEndTime"
              >
                <view class="picker">{{ filter.endTime || "请选择" }}</view>
              </picker>
            </view>
          </view>
        </view>
        <!-- 价格区间选择 -->
        <view class="filter-item">
          <text class="section-title">价格区间</text>
          <view class="price-options">
            <view
              v-for="(option, index) in priceRanges"
              :key="index"
              :class="[
                'price-option',
                filter.priceRange === option.value ? 'active' : '',
              ]"
              @tap="selectPriceRange(option.value)"
            >
              {{ option.label }}
            </view>
          </view>
        </view>

        <button class="apply-btn" @tap="applyFilter">应用筛选</button>
      </view>
    </view>

    <!-- 拼车通知列表 -->
    <scroll-view scroll-y class="ride-list">
      <view
        class="ride-item"
        v-for="(ride, index) in filteredRides"
        :key="index"
      >
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
          <button
            v-if="ride.status === 0"
            class="status-button disabled"
            disabled
          >
            已加群
          </button>
          <button v-else class="status-button" @click="goToGroupDetails(ride)">
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
      searchQuery: "",
      showFilter: false,
      filter: {
        startLocation: "",
        endLocation: "",
        startTime: "", // 修改为开始时间
        endTime: "", // 添加结束时间
        priceRange: "", // 添加价格区间选项
      },
      priceRanges: [
        { label: "全部", value: "all" },
        { label: "20¥以下", value: "-20" },
        { label: "20¥-30¥", value: "20-30" },
        { label: "30¥-40¥", value: "30-40" },
        { label: "40¥-50¥", value: "40-50" },
        { label: "50¥-70¥", value: "50-70" },
        { label: "70¥-100¥", value: "70-100" },
        { label: "100¥以上", value: "100-" },
      ],
      rides: [
        {
          id: 1,
          startLocation: "上海大学",
          endLocation: "虹桥机场",
          time: "14:30",
          price: 50,
          status: "待接单",
        },
        {
          id: 2,
          startLocation: "浦东机场",
          endLocation: "人民广场",
          time: "16:00",
          price: 80,
          status: "已接单",
        },
        {
          id: 3,
          startLocation: "徐家汇",
          endLocation: "静安寺",
          time: "09:00",
          price: 30,
          status: "待接单",
        },
        {
          id: 4,
          startLocation: "同济大学",
          endLocation: "五角场",
          time: "09:00",
          price: 30,
          status: "待接单",
        },
        {
          id: 5,
          startLocation: "五角场",
          endLocation: "上海交通大学",
          time: "09:00",
          price: 30,
          status: "待接单",
        },
        {
          id: 6,
          startLocation: "嘉定",
          endLocation: "豫园",
          time: "09:00",
          price: 30,
          status: "待接单",
        },
        {
          id: 7,
          startLocation: "徐家汇",
          endLocation: "嘉定",
          time: "09:00",
          price: 30,
          status: "待接单",
        },
        {
          id: 0,
          startLocation: "徐家汇",
          endLocation: "嘉定",
          time: "09:00",
          price: 30,
          status: "待接单",
        },
      ],
      filteredRides: [],
    };
  },
  onLoad() {
    this.filteredRides = this.rides; // 初始显示所有拼车消息
  },
  methods: {
    goToGroupDetails(ride) {
      uni.navigateTo({
        url: `/pages/groupDetails/index?id=${ride.id}`,
      });
    },
    toggleFilter() {
      this.showFilter = !this.showFilter;
    },
    updateStartTime(e) {
      this.filter.startTime = e.detail.value;
    },
    updateEndTime(e) {
      this.filter.endTime = e.detail.value;
    },
    selectPriceRange(value) {
      this.filter.priceRange = value;
    },
    applyFilter() {
      this.filteredRides = this.rides.filter((ride) => {
        const matchStart = this.filter.startLocation
          ? ride.startLocation.includes(this.filter.startLocation)
          : true;
        const matchEnd = this.filter.endLocation
          ? ride.endLocation.includes(this.filter.endLocation)
          : true;

        // 修改时间匹配逻辑
        let matchTime = true;
        if (this.filter.startTime && this.filter.endTime) {
          const rideTime = ride.time;
          matchTime =
            rideTime >= this.filter.startTime &&
            rideTime <= this.filter.endTime;
        }

        // 添加价格匹配逻辑
        let matchPrice = true;
        if (this.filter.priceRange && this.filter.priceRange !== "all") {
          const [min, max] = this.filter.priceRange.split("-");
          if (max === "up") {
            matchPrice = ride.price >= Number(min);
          } else {
            matchPrice = ride.price >= Number(min) && ride.price <= Number(max);
          }
        }

        const matchQuery = this.searchQuery
          ? ride.startLocation.includes(this.searchQuery) ||
            ride.endLocation.includes(this.searchQuery)
          : true;
        return matchStart && matchEnd && matchTime && matchPrice && matchQuery;
      });
      this.showFilter = false;
    },
    viewRideDetail(ride) {
      uni.showToast({
        title: `查看拼车单简略信息待实现: ${ride.id}`,
        icon: "none",
      });
    },
    updateRideStatus(rideId, status) {
      const index = this.filteredRides.findIndex((ride) => ride.id === rideId);
      if (index !== -1) {
        this.filteredRides[index].status = status.isJoined ? 0 : 1;
      }
    },
  },
};
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
  margin-left: 7%;
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
  background: rgba(0, 0, 0, 0.3); /* 增加透明度 */
  z-index: 999; /* 降低筛选面板的z-index */
  display: flex;
  justify-content: center; /* 改为居中 */
  align-items: flex-start; /* 从顶部开始 */
}

.filter-content {
  width: 90%; /* 调整宽度 */
  max-height: 80vh; /* 最大高度 */
  background: rgba(255, 255, 255, 1); /* 半透明背景 */
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  border-radius: 0 0 20rpx 20rpx; /* 底部圆角 */
  margin-top: 15%; /* 从顶部开始 */
  backdrop-filter: blur(10px); /* 背景模糊效果 */
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1); /* 阴影效果 */
  animation: slideDown 0.3s ease-out; /* 添加动画 */
  overflow-y: auto; /* 内容过多时可滚动 */
}

/* 添加滑入动画 */
@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
  padding-bottom: 20rpx;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.1); /* 添加分隔线 */
}

.filter-header text {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.close-icon {
  width: 40rpx;
  height: 40rpx;
}

.filter-item {
  margin-bottom: 40rpx;
}

/* 添加地点选择块的样式 */
.location-block {
  margin-bottom: 40rpx;
}

.location-block-title {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
}

.location-inputs {
  display: flex;
  align-items: center;
  gap: 20rpx;
  background: #f5f5f5;
  border-radius: 12rpx;
  padding: 20rpx;
}

.location-input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.location-label {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.filter-item text {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 10rpx;
}

.filter-input,
.picker {
  background: #f5f5f5;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #333;
}

.apply-btn {
  background: #28a745;
  color: #fff;
  font-size: 32rpx;
  padding: 5rpx 20rpx;
  border-radius: 12rpx;
  margin-top: auto;
  border: none;
}

.ride-list {
  flex: 1;
  background: #fff;
  flex: 1;
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
  margin: 2%;
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
  color: #007bff; /* 蓝色提示颜色 */
  font-family: "SimHei", sans-serif; /* 调整字体类型 */
  font-weight: bold; /* 加粗 */
  margin-left: 2%;
}

.text-price {
  font-size: 30rpx;
  color: #28a745; /* 绿色提示颜色 */
  margin-left: 10%; /* 左边距 */
  font-family: "SimHei", sans-serif; /* 调整字体类型 */
  font-weight: bold; /* 加粗 */
}

.start,
.end {
  font-size: 36rpx; /* 字体大小 */
  color: #333; /* 字体颜色 */
  font-weight: bold; /* 加粗 */
  font-family: "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif; /* 设置中文字体 */
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

.ride-status {
  margin-right: 2%;
}

.status-button {
  width: 120%;
  height: 40%;
  border-radius: 4rpx;
  font-size: 26rpx;
  color: #fff;
  font-family: "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif; /* 设置中文字体 */
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

/* 添加新的样式用于时间选择器 */
.uni-picker-container {
  z-index: 1002 !important; /* 确保时间选择器显示在最上层 */
}

.time-range {
  display: flex;
  align-items: center;
  background: #f5f5f5;
  border-radius: 12rpx;
  padding: 20rpx;
}

.time-input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.time-label {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.price-options {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
  margin-top: 10rpx;
}

.price-option {
  padding: 15rpx 25rpx;
  background: #f5f5f5;
  border-radius: 8rpx;
  font-size: 26rpx;
  color: #666;
  transition: all 0.3s ease;
}

.price-option.active {
  background: #28a745;
  color: #fff;
}

.section-title {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
}
</style>
