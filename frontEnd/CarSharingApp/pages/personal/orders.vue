<template>
  <view class="orders-container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/image/icon_back.png" class="back-icon"></image>
      </view>
      <text class="title">所有订单</text>
    </view>

    <!-- 搜索和筛选 -->
    <view class="search-filter">
      <input type="text" v-model="searchQuery" placeholder="搜索订单..." class="search-input" />
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

      <!-- 订单状态选择-->
      <picker mode="selector" :range="['', '已完成', '待支付', '已取消']" @change="onStatusChange">
        <view class="filter-row picker-row">
          <text>订单状态: {{ selectedStatus || '全部' }}</text>
          <image src="/static/image/icon_arrow_down.png" class="dropdown-icon" />
        </view>
      </picker>

      <view class="filter-row">
        <text class="filter-label">金额范围:</text>
        <input type="number" v-model.number="minAmount" placeholder="例:30" />
        <text>——</text>
        <input type="number" v-model.number="maxAmount" placeholder="例:50" />
      </view>

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

    <!-- 订单列表 -->
    <scroll-view scroll-y class="order-list">
      <view
        class="order-item"
        v-for="(order, index) in filteredOrders"
        :key="index"
        @tap="goToOrderDetail(order)"
      >
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
      selectedStatus: '',
      minAmount: null,
      maxAmount: null,
      startDate: '',
      endDate: '',
      showFilterPanel: false,
      orders: [
        { id: '1001', date: '2025-04-29', amount: 50, status: '已完成' },
        { id: '1002', date: '2025-04-28', amount: 30, status: '待支付' },
        { id: '1003', date: '2025-04-27', amount: 70, status: '已取消' }
      ]
    };
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => {
        const matchQuery = order.id.includes(this.searchQuery);
        const matchStatus = this.selectedStatus ? order.status === this.selectedStatus : true;
        const matchAmount =
          (!this.minAmount || order.amount >= this.minAmount) &&
          (!this.maxAmount || order.amount <= this.maxAmount);
        const matchDate =
          (!this.startDate || order.date >= this.startDate) &&
          (!this.endDate || order.date <= this.endDate);
        return matchQuery && matchStatus && matchAmount && matchDate;
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
      this.selectedStatus = '';
      this.minAmount = null;
      this.maxAmount = null;
      this.startDate = '';
      this.endDate = '';
      this.showFilterPanel = false;
    },
    closeFilterPanel() {
      this.showFilterPanel = false;
    },
    onStatusChange(e) {
      const options = ['', '已完成', '待支付', '已取消'];
      this.selectedStatus = options[e.detail.value];
    },
    goToOrderDetail(order) {
      uni.navigateTo({ url: `/pages/personal/orders/detail?id=${order.id}` });
    },
    getStatusIcon(status) {
      switch (status) {
        case '已完成':
          return '/static/image/check-icon.png';
        case '待支付':
          return '/static/image/clock-icon.png';
        case '已取消':
          return '/static/image/cancel-icon.png';
        default:
          return '/static/image/default-icon.png';
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
  right: 20rpx;
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

.filter-row input[type="number"],
.filter-row input[type="date"] {
  flex: 1;
  margin: 0 10rpx;
  padding: 20rpx;
  font-size: 28rpx;
  background: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 20rpx;
  box-sizing: border-box;
  min-width: 0;
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

/* 下拉图标样式 */
.picker-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 400rpx;
}

.dropdown-icon {
  width: 24rpx;
  height: 24rpx;
  margin-left: 10rpx;
  opacity: 0.6;
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

.order-id,
.order-date,
.order-amount,
.order-status {
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
