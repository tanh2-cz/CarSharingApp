<template>
  <view class="flow-detail-container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/icon_back.png" class="back-icon"></image>
      </view>
      <text class="title">流水详情</text>
    </view>

    <!-- 流水信息 -->
    <view class="flow-info">
      <view class="info-item">
        <text class="label">流水ID</text>
        <text class="value">{{ flow.id }}</text>
      </view>
      <view class="info-item">
        <text class="label">日期</text>
        <text class="value">{{ flow.date }}</text>
      </view>
      <view class="info-item">
        <text class="label">金额</text>
        <text class="value">¥{{ flow.amount }}</text>
      </view>
      <view class="info-item">
        <text class="label">类型</text>
        <text class="value">{{ flow.type }}</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      flow: {}
    };
  },
  onLoad(options) {
    const flows = [
      { id: '2001', date: '2025-04-29', amount: 100, type: '拼车收入' },
      { id: '2002', date: '2025-04-28', amount: 80, type: '拼车收入' },
      { id: '2003', date: '2025-04-27', amount: 50, type: '提现' }
    ];
    this.flow = flows.find(flow => flow.id === options.id) || {};
  },
  methods: {
    goBack() {
      uni.navigateBack();
    }
  }
};
</script>

<style scoped>
.flow-detail-container {
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

.flow-info {
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
</style>