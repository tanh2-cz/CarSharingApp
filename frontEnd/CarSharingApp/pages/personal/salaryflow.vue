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
    <view class="search-filter">
      <view class="filter-button" @tap="showFilter">
        <text>筛选</text>
      </view>
    </view>

    <!-- 筛选面板 -->
    <view v-if="showFilterPanel" class="filter-panel">
      <!-- 关闭按钮 -->
      <image
        src="/static/image/icon_close.png"
        class="filter-close-icon"
        @tap="closeFilterPanel"
      />

      <!-- 日期范围筛选 -->
      <view class="filter-row">
        <text class="filter-label">日期范围:</text>
        <input type="date" v-model="startDate" placeholder="例:2025-04-27" />
        <text>——</text>
        <input type="date" v-model="endDate" placeholder="例:2025-04-28" />
      </view>

      <view class="filter-actions">
        <button @tap="applyFilters">应用</button>
        <button @tap="resetFilters">重置</button>
      </view>
    </view>

    <!-- 流水列表 -->
    <scroll-view scroll-y class="flow-list">
      <!-- 无数据时提示 -->
      <view v-if="filteredFlows.length === 0" class="no-data">
        <text>没有流水记录</text>
      </view>

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
      startDate: '',  // 开始日期
      endDate: '',    // 结束日期
      showFilterPanel: false, // 控制筛选面板显示
      flows: [
        { id: '2001', date: '2025-04-29', amount: 100, type: '拼车收入' },
        { id: '2002', date: '2025-04-28', amount: 80, type: '拼车收入' },
        { id: '2003', date: '2025-04-27', amount: 50, type: '提现' }
      ]
    };
  },
  computed: {
    filteredFlows() {
      return this.flows.filter(flow => {
        const flowDate = new Date(flow.date);
        const startDate = this.startDate ? new Date(this.startDate) : null;
        const endDate = this.endDate ? new Date(this.endDate) : null;

        const withinStartDate = startDate ? flowDate >= startDate : true;
        const withinEndDate = endDate ? flowDate <= endDate : true;

        return withinStartDate && withinEndDate;
      });
    }
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    showFilter() {
      this.showFilterPanel = true;
    },
    applyFilters() {
      this.showFilterPanel = false;
    },
    resetFilters() {
      this.startDate = '';
      this.endDate = '';
      this.showFilterPanel = false;
    },
    closeFilterPanel() {
      this.showFilterPanel = false;
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

.search-filter {
  margin-top: 100rpx;
  padding: 20rpx 30rpx;
  background: #fff;
  display: flex;
  justify-content: flex-end;  /* 确保筛选按钮右对齐 */
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

/* 筛选面板 */
.filter-panel {
  position: relative;
  background: #fff;
  padding: 30rpx;
  border-top: 1px solid #eee;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  margin: 20rpx;
}

.filter-close-icon {
  position: absolute;
  top: 20rpx;
  right: 5rpx;
  width: 40rpx;
  height: 40rpx;
  opacity: 0.6;
  z-index: 10;
}

.filter-close-icon:active {
  opacity: 1;
}

.filter-row {
  display: flex;
  align-items: center;
  font-size: 28rpx;
  margin-bottom: 30rpx;
  flex-wrap: nowrap;
  color: #333;
}

.filter-label {
  width: 160rpx;
  flex-shrink: 0;
}

.filter-row input[type="date"] {
  flex: 1;
  margin: 0 10rpx;
  padding: 20rpx;
  font-size: 28rpx;
  background: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 20rpx;
  box-sizing: border-box;
}

.filter-row input:focus {
  border-color: #409eff;
}

.filter-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20rpx;
}

.filter-actions button {
  flex: 1;
  margin: 0 10rpx;
  padding: 16rpx 0;
  font-size: 26rpx;
  border-radius: 30rpx;
  background: #409eff;
  color: #fff;
  border: none;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.08);
}

.filter-actions button:nth-child(2) {
  background: #f56c6c;
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

.income {
  color: #4CAF50; /* Green for income */
}

.withdrawal {
  color: #2196F3; /* Blue for withdrawal */
}

.no-data {
  text-align: center;
  font-size: 28rpx;
  color: #999;
  margin-top: 50rpx;
}
</style>
