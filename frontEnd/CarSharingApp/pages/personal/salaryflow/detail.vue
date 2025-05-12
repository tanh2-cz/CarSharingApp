<template>
  <view class="flow-detail-container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/image/icon_back.png" class="back-icon"></image>
      </view>
      <text class="title">流水详情</text>
    </view>

 <!-- 关键信息展示区 -->
    <view class="key-info-section">
      <!-- 根据流水类型显示不同的头像 -->
      <image 
        v-if="flow.type === '拼车收入'" 
        src="/static/image/car_income_avatar.png" 
        class="flow-avatar" 
      />
      <image 
        v-if="flow.type === '提现'" 
        src="/static/image/withdraw_avatar.png" 
        class="flow-avatar" 
      />

      <text class="amount-bold">¥{{ flow.amount }}</text>
      <text class="flow-id">流水ID: {{ flow.id }}</text>
    </view>

    <!-- 流水详情 -->
    <view class="flow-details">
      <view class="detail-item">
        <text class="label">日期</text>
        <text class="value">{{ flow.date }}</text>
      </view>
      <view class="detail-item">
        <text class="label">金额</text>
        <text class="value">¥{{ flow.amount }}</text>
      </view>
      <view class="detail-item">
        <text class="label">类型</text>
        <text :class="['value', getTypeClass(flow.type)]">{{ flow.type }}</text>
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
      { id: '2001', date: '2025-01-05', amount: 120, type: '拼车收入' },
      { id: '2002', date: '2025-01-18', amount: 90, type: '拼车收入' },
      { id: '2003', date: '2025-01-20', amount: 60, type: '提现' },
      { id: '2004', date: '2025-02-03', amount: 150, type: '拼车收入' },
      { id: '2005', date: '2025-02-17', amount: 100, type: '提现' },
      { id: '2006', date: '2025-02-28', amount: 130, type: '拼车收入' },
      { id: '2007', date: '2025-03-05', amount: 160, type: '拼车收入' },
      { id: '2008', date: '2025-03-15', amount: 95, type: '提现' },
      { id: '2009', date: '2025-03-22', amount: 80, type: '拼车收入' },
      { id: '2010', date: '2025-04-02', amount: 200, type: '拼车收入' },
      { id: '2011', date: '2025-04-14', amount: 110, type: '拼车收入' },
      { id: '2012', date: '2025-04-20', amount: 90, type: '提现' },
      { id: '2013', date: '2025-05-01', amount: 300, type: '拼车收入' },
      { id: '2014', date: '2025-05-10', amount: 60, type: '拼车收入' },
      { id: '2015', date: '2025-05-22', amount: 100, type: '提现' },
      { id: '2016', date: '2025-06-03', amount: 180, type: '拼车收入' },
      { id: '2017', date: '2025-06-17', amount: 70, type: '提现' },
      { id: '2018', date: '2025-06-29', amount: 150, type: '拼车收入' },
      { id: '2019', date: '2025-07-08', amount: 220, type: '拼车收入' },
      { id: '2020', date: '2025-07-19', amount: 50, type: '提现' },
      { id: '2021', date: '2025-08-02', amount: 140, type: '拼车收入' },
      { id: '2022', date: '2025-08-18', amount: 100, type: '拼车收入' },
      { id: '2023', date: '2025-08-28', amount: 60, type: '提现' },
      { id: '2024', date: '2025-09-04', amount: 175, type: '拼车收入' },
      { id: '2025', date: '2025-09-21', amount: 90, type: '拼车收入' },
      { id: '2026', date: '2025-10-10', amount: 200, type: '拼车收入' },
      { id: '2027', date: '2025-10-18', amount: 80, type: '提现' },
      { id: '2028', date: '2025-11-11', amount: 160, type: '拼车收入' },
      { id: '2029', date: '2025-11-25', amount: 70, type: '提现' },
      { id: '2030', date: '2025-12-05', amount: 190, type: '拼车收入' }
    ];
    this.flow = flows.find(flow => flow.id === options.id) || {};
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    getTypeClass(type) {
      if (type === '拼车收入') {
        return 'income'; // 拼车收入的类名
      } else if (type === '提现') {
        return 'withdrawal'; // 提现的类名
      }
      return '';
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

/* 关键信息展示区 */
.key-info-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 95rpx;
  padding: 30rpx;
  background: #fff;
}

.flow-avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  margin-bottom: 40rpx;
  margin-top: 50rpx;
}

.amount-bold {
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
}

.flow-id {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 30rpx;
}

/* 流水详情 */
.flow-details {
  margin-top: 20rpx;
  padding: 30rpx;
  background: #fff;
}

.detail-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-top: 1rpx solid #eee;
  border-bottom: 1rpx solid #eee;
}

.label {
  font-size: 24rpx;
  color: #999;
  margin-left: 30rpx;
  margin-right: 30rpx;
}

.value {
  font-size: 24rpx;
  color: #333;
  text-align: left;
  white-space: pre-line;
}

/* 流水类型颜色 */
.income {
  color: #4CAF50; /* Green for income */
}

.withdrawal {
  color: #2196F3; /* Blue for withdrawal */
}
</style>
