<template>
  <view class="orders-container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/icon_back.png" class="back-icon"></image>
      </view>
      <text class="title">所有订单</text>
    </view>

    <!-- 搜索和过滤 -->
    <view class="search-filter">
      <input type="text" v-model="searchQuery" placeholder="搜索订单..." class="search-input" />
      <view class="filter-button" @tap="showFilter">
        <text>筛选</text>
      </view>
    </view>

    <!-- 订单列表 -->
    <scroll-view scroll-y class="order-list">
      <view class="order-item" v-for="(order, index) in filteredOrders" :key="index" @tap="goToOrderDetail(order)">
        <text class="order-id">订单号: {{ order.id }}</text>
        <text class="order-date">{{ order.date }}</text>
        <text class="order-amount">金额: ¥{{ order.amount }}</text>
        <view class="order-status">
          <image :src="getStatusIcon(order.status)" class="status-icon" />
          <text>{{ order.status }}</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      orders: [
        { id: '1001', date: '2025-04-29', amount: 50, status: '已完成' },
        { id: '1002', date: '2025-04-28', amount: 30, status: '待支付' },
        { id: '1003', date: '2025-04-27', amount: 70, status: '已取消' }
      ]
    };
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => order.id.includes(this.searchQuery));
    }
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    showFilter() {
      uni.showToast({ title: '筛选功能待实现', icon: 'none' });
    },
    goToOrderDetail(order) {
      uni.navigateTo({ url: `/pages/personal/orders/detail?id=${order.id}` });
    },
    getStatusIcon(status) {
      // 根据订单状态返回对应图标
      switch (status) {
        case '已完成':
          return '/static/image/check-icon.png'; // 完成图标
        case '待支付':
          return '/static/image/clock-icon.png'; // 时钟图标
        case '已取消':
          return '/static/image/cancel-icon.png'; // 叉图标
        default:
          return '/static/image/default-icon.png'; // 默认图标
      }
    }
  }
};
</script>

<style scoped>
.orders-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.top-bar {
  padding: 20rpx 30rpx;
  background: #fff;
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.back-button {
  margin-right: 20rpx;
}

.back-icon {
  width: 40rpx;
  height: 40rpx;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.search-filter {
  margin-top: 100rpx;
  padding: 20rpx 30rpx;
  background: #fff;
  display: flex;
  align-items: center;
}

.search-input {
  flex: 1;
  height: 80rpx;
  padding: 0 20rpx;
  background: #f5f5f5;
  border-radius: 40rpx;
  font-size: 28rpx;
  border: 1rpx solid #ccc;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #409eff;
}

.filter-button {
  margin-left: 20rpx;
  padding: 20rpx 40rpx;
  background: #409eff;
  border-radius: 40rpx;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

.filter-button text {
  font-size: 28rpx;
  color: #fff;
}

.order-list {
  flex: 1;
  margin-top: 20rpx;
  background: #fff;
  padding: 20rpx;
}

.order-item {
  padding: 30rpx;
  margin-bottom: 20rpx;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 4rpx 6rpx rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.order-id, .order-date, .order-amount, .order-status {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 10rpx;
}

.order-id {
  font-weight: bold;
}

.order-amount {
  color: #409eff;
}

.order-status {
  display: flex;
  align-items: center;
}

.status-icon {
  width: 24rpx;
  height: 24rpx;
  margin-right: 10rpx;
}
</style>
