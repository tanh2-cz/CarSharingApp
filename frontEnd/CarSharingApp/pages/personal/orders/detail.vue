<template>
  <view class="order-detail-container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/image/icon_back.png" class="back-icon"></image>
      </view>
      <text class="title">订单详情</text>
    </view>

    <!-- 订单信息 -->
    <view class="order-info">
      <view class="info-item">
        <text class="label">订单号</text>
        <text class="value">{{ order.id }}</text>
      </view>
      <view class="info-item">
        <text class="label">日期</text>
        <text class="value">{{ order.date }}</text>
      </view>
      <view class="info-item">
        <text class="label">金额</text>
        <text class="value">¥{{ order.amount }}</text>
      </view>
      <view class="info-item">
        <text class="label">状态</text>
        <text :class="['value', getStatusClass(order.status)]">{{ order.status }}</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      order: {}
    };
  },
  onLoad(options) {
    const orders = [
      { id: '1001', date: '2025-04-29', amount: 50, status: '已完成' },
      { id: '1002', date: '2025-04-28', amount: 30, status: '待支付' },
      { id: '1003', date: '2025-04-27', amount: 70, status: '已取消' }
    ];
    this.order = orders.find(order => order.id === options.id) || {};
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    getStatusClass(status) {
      if (status === '已完成') {
        return 'completed';
      } else if (status === '待支付') {
        return 'pending';
      } else if (status === '已取消') {
        return 'cancelled';
      }
      return '';
    }
  }
};
</script>

<style scoped>
.order-detail-container {
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

.order-info {
  margin-top: 100rpx;
  padding: 30rpx;
  background: #fff;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
}

.label {
  font-size: 32rpx;
  color: #666;
}

.value {
  font-size: 32rpx;
  color: #333;
}

/* Order status colors */
.completed {
  color: #4CAF50; /* Green for completed */
}

.pending {
  color: #FFC107; /* Yellow for pending */
}

.cancelled {
  color: #F44336; /* Red for cancelled */
}
</style>
