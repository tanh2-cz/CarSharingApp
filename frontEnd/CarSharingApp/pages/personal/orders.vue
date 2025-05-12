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
			<input type="text" v-model="searchQuery" placeholder="输入订单号搜索订单..." class="search-input" />
			<view class="filter-button" @tap="showFilter">
				<image src="/static/image/icon_filter_blue.png" class="filter-icon" />
			</view>
		</view>

		<!-- 筛选面板 -->
		<view v-if="showFilterPanel" class="filter-panel">
			<!-- 关闭按钮 -->
			<image src="/static/image/icon_close.png" class="filter-close-icon" @tap="closeFilterPanel" />

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
				<button class="apply-button" @tap="applyFilters">应用</button>
				<button class="reset-button" @tap="resetFilters">重置</button>
			</view>
		</view>

		<!-- 订单列表 -->
		<scroll-view scroll-y class="order-list">
			<view class="order-item" v-for="(order, index) in filteredOrders" :key="index"
				@tap="goToOrderDetail(order)">
				<!-- 最上方一横排内容 -->
				<view class="order-top-row">
					<text class="order-id-bold">订单号 {{ order.id }}</text>
					<view class="order-status">
						<image :src="getStatusIcon(order.status)" class="status-icon" />
						<text>{{ order.status }}</text>
					</view>
				</view>
				<!-- 水平和垂直居中的一列内容 -->
				<view class="order-middle-column">
					<text class="order-date-gray">{{ order.date }}</text>
					<text class="order-amount-bold">¥{{ order.amount }}</text>
					<view class="order-details">
						<text class="order-details-text">订单详情</text>
						<image src="/static/image/arrow_right.png" class="order-details-icon" />
					</view>
				</view>
				<!-- 最下方两行内容 -->
				<view class="order-bottom-row">
					<view class="address-item">
						<text class="address-label">起点地址</text>
						<text class="address-detail">{{ order.startAddress }}</text>
					</view>
					<view class="address-item">
						<text class="address-label">终点地址</text>
						<text class="address-detail">{{ order.endAddress }}</text>
					</view>
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
				orders: [{
						id: '1001',
						date: '2025-04-29',
						amount: 50,
						status: '已完成',
						paymentMethod: '微信支付',
						startAddress: '上海市静安区南京西路1788号',
						endAddress: '上海市浦东新区张江高科技园区博云路2号',
						licensePlateNumber: '沪A12345',
						driverName:'李师傅',
						driverPhone: '13812345678'
					},
					{
						id: '1002',
						date: '2025-04-28',
						amount: 30,
						status: '待支付',
						paymentMethod: '无',
						startAddress: '上海市徐汇区淮海中路999号',
						endAddress: '上海市杨浦区五角场万达广场B座',
						licensePlateNumber: '沪B67890',
						driverName:'肖师傅',
						driverPhone: '13998765432'
					},
					{
						id: '1003',
						date: '2025-04-27',
						amount: 70,
						status: '已取消',
						paymentMethod: '无',
						startAddress: '上海市黄浦区外滩金融中心',
						endAddress: '上海市长宁区虹桥机场T2航站楼',
						licensePlateNumber: '沪A54321',
						driverName:'王师傅',
						driverPhone: '18876543210'
					}
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
				uni.navigateTo({
					url: `/pages/personal/orders/detail?id=${order.id}`
				});
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
		margin-top: 95rpx;
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
		border: 1rpx solid #eee;
	}

	.search-input:focus {
		border-color: #409eff;
	}

	.filter-button {
		margin-left: 20rpx;
		padding: 20rpx;
		display: flex;
		align-items: center;
	}

	.filter-icon {
		width: 48rpx;
		height: 48rpx;
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
		background: #e9e9e9;
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
		justify-content: flex-end;
		margin-top: 20rpx;
	}

	.apply-button,
	.reset-button {
		padding: 0rpx 30rpx;
		font-size: 30rpx;
		border-radius: 24rpx;
		color: #fff;
		border: none;
		box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.08);
		margin: 0;
	}

	.apply-button {
		margin-right: 20rpx;
		background: #409eff;
	}

	.reset-button {
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
		padding: 30rpx 50rpx;
		margin-bottom: 30rpx;
		margin-right: 45rpx;
		background: #fff;
		border-radius: 12rpx;
		box-shadow: 0 0 10rpx rgba(0, 0, 0, 0.1);
		display: flex;
		flex-direction: column;
	}

	/* 订单卡片最上方一横排样式 */
	.order-top-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
	}

	.order-id-bold {
		font-weight: bold;
		font-size: 28rpx;
	}

	/* 订单卡片水平和垂直居中的一列样式 */
	.order-middle-column {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.order-date-gray {
		font-size: 22rpx;
		color: #666;
	}

	.order-amount-bold {
		font-weight: bold;
		font-size: 50rpx;
		color: #333;
		margin-top: 15rpx;
		margin-bottom: 15rpx;
	}

	.order-details {
		display: flex;
		align-items: center;
	}

	.order-details-text {
		font-size: 20rpx;
		color: #666;
		margin-right: 5rpx;
	}

	.order-details-icon {
		width: 20rpx;
		height: 20rpx;
	}

	/* 订单卡片最下方两行样式 */
	.order-bottom-row {
		display: flex;
		flex-direction: column;
		margin-top: 40rpx;
	}

	.address-item {
		display: flex;
		margin-bottom: 10rpx;
	}

	.address-label {
		font-size: 20rpx;
		color: #666;
		margin-right: 10rpx;
	}

	.address-detail {
		font-size: 20rpx;
		color: #333;
	}

	.status-icon {
		width: 24rpx;
		height: 24rpx;
		margin-right: 10rpx;
	}
</style>