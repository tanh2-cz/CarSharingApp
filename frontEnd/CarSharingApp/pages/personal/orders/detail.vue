<template>
	<view class="order-detail-container">
		<!-- 顶部导航栏 -->
		<view class="top-bar">
			<view class="back-button" @tap="goBack">
				<image src="/static/image/icon_back.png" class="back-icon"></image>
			</view>
			<text class="title">订单详情</text>
		</view>

		<!-- 关键信息展示区 -->
		<view class="key-info-section">
			<image src="/static/image/driver_avatar.png" class="driver-avatar" />
			<text class="driver-name">{{ order.driverName }}</text>
			<text class="amount-bold">¥{{ order.amount }}</text>
		</view>

		<!-- 订单详情 -->
		<view class="order-details">
			<view class="detail-item">
				<text class="label">当前状态</text>
				<text :class="['value', getStatusClass(order.status)]">{{ order.status }}</text>
			</view>
			<view class="detail-item">
				<text class="label">支付时间</text>
				<text class="value">{{ order.date }}</text>
			</view>
			<view class="detail-item">
				<text class="label">支付方式</text>
				<text class="value">{{ order.paymentMethod }}</text>
			</view>
			<view class="detail-item">
				<text class="label">行程起点</text>
				<text class="value">{{ order.startAddress }}</text>
			</view>
			<view class="detail-item">
				<text class="label">行程终点</text>
				<text class="value">{{ order.endAddress }}</text>
			</view>
			<view class="detail-item">
				<text class="label">车牌号码</text>
				<text class="value">{{ order.licensePlateNumber }}</text>
			</view>
			<view class="detail-item">
				<text class="label">司机电话</text>
				<text class="value">{{ order.driverPhone }}</text>
			</view>
			<view class="detail-item">
				<text class="label">交易单号</text>
				<text class="value">{{ order.id }}</text>
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
			const orders = [{
					id: '1001',
					date: '2025-04-29 10:00:32',
					amount: 50,
					status: '已完成',
					paymentMethod: '微信支付',
					startAddress: '上海市静安区南京西路1788号',
					endAddress: '上海市浦东新区张江高科技园区博云路2号',
					licensePlateNumber: '沪A12345',
					driverName: '李师傅',
					driverPhone: '13812345678'
				},
				{
					id: '1002',
					date: '2025-04-28  12:10:35',
					amount: 30,
					status: '待支付',
					paymentMethod: '无',
					startAddress: '上海市徐汇区淮海中路999号',
					endAddress: '上海市杨浦区五角场万达广场B座',
					licensePlateNumber: '沪B67890',
					driverName: '肖师傅',
					driverPhone: '13998765432'
				},
				{
					id: '1003',
					date: '2025-04-27  18:00:54',
					amount: 70,
					status: '已取消',
					paymentMethod: '无',
					startAddress: '上海市黄浦区外滩金融中心',
					endAddress: '上海市长宁区虹桥机场T2航站楼',
					licensePlateNumber: '沪A54321',
					driverName: '王师傅',
					driverPhone: '18876543210'
				}
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

	.driver-avatar {
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
		margin-bottom: 40rpx;
		margin-top: 50rpx;
	}

	.driver-name {
		font-size: 28rpx;
		color: #333;
		margin-bottom: 20rpx;
	}

	.amount-bold {
		font-size: 48rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 30rpx;
	}

	/* 订单详情 */
	.order-details {
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

	/* Order status colors */
	.completed {
		color: #4CAF50;
		/* Green for completed */
	}

	.pending {
		color: #FFC107;
		/* Yellow for pending */
	}

	.cancelled {
		color: #F44336;
		/* Red for cancelled */
	}
</style>