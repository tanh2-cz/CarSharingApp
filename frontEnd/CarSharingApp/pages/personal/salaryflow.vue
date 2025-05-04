<template>
  <view class="salaryflow-container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/icon_back.png" class="back-icon"></image>
      </view>
      <text class="title">工资流水</text>
    </view>

    <!-- 时间筛选 -->
    <view class="time-filter">
      <view class="filter-button" @tap="showTimeFilter">
        <text>选择时间</text>
      </view>
    </view>

    <!-- 流水列表 -->
    <scroll-view scroll-y class="flow-list">
      <view class="flow-item" v-for="(flow, index) in filteredFlows" :key="index" @tap="goToFlowDetail(flow)">
        <text class="flow-date">{{ flow.date }}</text>
        <text class="flow-amount">¥{{ flow.amount }}</text>
        <text :class="['flow-type', getTypeClass(flow.type)]">{{ flow.type }}</text>
      </view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      flows: [
        { id: '2001', date: '2025-04-29', amount: 100, type: '拼车收入' },
        { id: '2002', date: '2025-04-28', amount: 80, type: '拼车收入' },
        { id: '2003', date: '2025-04-27', amount: 50, type: '提现' }
      ]
    };
  },
  computed: {
    filteredFlows() {
      return this.flows; // 待实现时间筛选逻辑
    }
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    showTimeFilter() {
      uni.showToast({ title: '时间筛选功能待实现', icon: 'none' });
    },
    goToFlowDetail(flow) {
      uni.navigateTo({ url: `/pages/personal/salaryflow/detail?id=${flow.id}` });
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
.salaryflow-container {
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

.time-filter {
  margin-top: 100rpx;
  padding: 20rpx 30rpx;
  background: #fff;
  display: flex;
  justify-content: flex-end;
}

.filter-button {
  padding: 20rpx 40rpx;
  background: #409eff;
  border-radius: 40rpx;
}

.filter-button text {
  font-size: 28rpx;
  color: #fff;
}

.flow-list {
  flex: 1;
  margin-top: 20rpx;
  background: #fff;
  padding: 20rpx;
}

.flow-item {
  padding: 30rpx;
  margin-bottom: 20rpx;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 4rpx 6rpx rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.flow-date, .flow-amount, .flow-type {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 10rpx;
}

/* 流水类型颜色区分 */
.income {
  color: #4CAF50; /* Green for income */
}

.withdrawal {
  color: #2196F3; /* Blue for withdrawal */
}
</style>
