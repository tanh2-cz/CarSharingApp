<template>
  <view class="personal-container">
    <!-- 用户信息 -->
    <view class="user-info">
      <image src="/static/image/user_avatar.jpg" class="avatar"></image>
      <view class="user-details">
        <text class="username">拼车达人</text>
        <text class="level">等级：Lv10</text>
        <text class="status">身份：司机</text>
      </view>
    </view>

    <!-- 统计数据 -->
    <view class="stats">
      <view class="stat-item">
        <text class="stat-value">10.0</text>
        <text class="stat-label">信用积分</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">56.7</text>
        <text class="stat-label">出行里程</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">5</text>
        <text class="stat-label">拼车次数</text>
      </view>
    </view>

    <!-- 功能入口 -->
    <view class="menu-list">
      <view class="menu-item" @tap="goToOrders">
        <image src="/static/image/icon_orders.png" class="menu-icon"></image>
        <text class="menu-text">钱包</text>
      </view>
      <view class="menu-item" @tap="goToHistory">
        <image src="/static/image/icon_history.png" class="menu-icon"></image>
        <text class="menu-text">历史订单</text>
      </view>
      <view class="menu-item" @tap="goToVerify">
        <image src="/static/image/icon_verify.png" class="menu-icon"></image>
        <text class="menu-text">账号与安全</text>
      </view>
      <view class="menu-item" @tap="goToSalaryFlow">
        <image src="/static/image/icon_salary.png" class="menu-icon"></image>
        <text class="menu-text">工资流水</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  methods: {
    goToOrders() {
      uni.navigateTo({ url: '/pages/personal/orders' });
    },
    goToHistory() {
      uni.navigateTo({ url: '/pages/personal/orders' });
    },
    goToVerify() {
      uni.navigateTo({ url: '/pages/personal/account-security' }); // 实现跳转到账号与安全页面
    },
    goToSalaryFlow() {
      uni.navigateTo({ url: '/pages/personal/salaryflow' });
    }
  }
};
</script>

<style scoped>
.personal-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.user-info {
  margin-top: 100rpx;
  padding: 40rpx;
  background: #fff;
  display: flex;
  align-items: center;
  border-radius: 12rpx;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.1);
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  margin-right: 30rpx;
  border: 2rpx solid #409eff; /* 边框颜色 */
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 38rpx;
  font-weight: bold;
  color: #333;
}

.level, .status {
  font-size: 28rpx;
  color: #666;
  margin-top: 10rpx;
}

.stats {
  padding: 30rpx;
  background: #fff;
  display: flex;
  justify-content: space-around;
  margin-top: 30rpx;
  border-radius: 12rpx;
  box-shadow: 0 4rpx 6rpx rgba(0, 0, 0, 0.1);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 24rpx;
  color: #999;
  margin-top: 10rpx;
}

.menu-list {
  margin-top: 30rpx;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 4rpx 6rpx rgba(0, 0, 0, 0.1);
}

.menu-item {
  padding: 40rpx;
  border-bottom: 1rpx solid #eee;
  display: flex;
  align-items: center;
  border-radius: 12rpx;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-icon {
  width: 48rpx;
  height: 48rpx;
  margin-right: 20rpx;
}

.menu-text {
  font-size: 32rpx;
  color: #333;
}
</style>
