<template>
	<view class="wallet-container">
		<!-- 顶部导航栏 -->
		<view class="top-bar">
			<view class="back-button" @tap="goBack">
				<image src="/static/image/icon_back.png" class="back-icon"></image>
			</view>
			<text class="title">钱包</text>
		</view>

		<view class="balance-card">
			<text class="balance">{{ totalAssets }}</text>
			<text class="assets-label">钱包余额</text>

			<view class="function-cards">
				<view class="function-card" @tap="handlePaymentTap">
					<image src="/static/image/icon_payment.png" class="function-icon"></image>
					<text class="function-name">收付款</text>
				</view>
				<view class="function-card" @tap="handleBankCardTap">
					<image src="/static/image/icon_bankcard.png" class="function-icon"></image>
					<text class="function-name">银行卡</text>
				</view>
			</view>
		</view>

		<!-- 子功能列表 -->
		<view class="sub-functions">
			<view class="sub-function-item1" @tap="handleBillDetailsTap">
				<text class="sub-function-name">账单明细</text>
				<image src="/static/image/arrow_right.png" class="sub-function-arrow"></image>
			</view>
			<view class="sub-function-item2" @tap="handleMyCashTap">
				<text class="sub-function-name">我的零钱</text>
				<view class="function-money">
					<text>￥{{ totalAssets }}</text>
					<image src="/static/image/arrow_right.png" class="sub-function-arrow"></image>
				</view>
			</view>
			<view class="sub-function-item2" @tap="handleMyWeChatTap">
				<text class="sub-function-name">我的微信</text>
				<view class="status-indicator added">
					<text>已添加</text>
					<image src="/static/image/arrow_right.png" class="status-arrow"></image>
				</view>
			</view>
			<view class="sub-function-item2" @tap="handleMyAlipayTap">
				<text class="sub-function-name">我的支付宝</text>
				<view class="status-indicator not-added">
					<text>未添加</text>
					<image src="/static/image/arrow_right.png" class="status-arrow"></image>
				</view>
			</view>
			<view class="sub-function-item3" @tap="handlePaymentSettingsTap">
				<text class="sub-function-name">支付设置</text>
				<image src="/static/image/arrow_right.png" class="sub-function-arrow"></image>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				totalAssets: '2025.51', // 总资产金额
			};
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			handlePaymentTap() {
				uni.showToast({
					title: '点击了收付款功能',
					icon: 'none',
				});
			},
			handleBankCardTap() {
				uni.showToast({
					title: '点击了银行卡功能',
					icon: 'none',
				});
			},
			handleBillDetailsTap() {
				uni.showToast({
					title: '点击了账单明细功能',
					icon: 'none',
				});
			},
			handleMyCashTap() {
				uni.navigateTo({ url: '/pages/personal/pocketmoney' });
			},
			handleMyBankCardTap() {
				uni.showToast({
					title: '点击了我的银行卡功能',
					icon: 'none',
				});
			},
			handleMyWeChatTap() {
				uni.showToast({
					title: '点击了我的微信功能',
					icon: 'none',
				});
			},
			handleMyAlipayTap() {
				uni.showToast({
					title: '点击了我的支付宝功能',
					icon: 'none',
				});
			},
			handlePaymentSettingsTap() {
				uni.showToast({
					title: '点击了支付设置功能',
					icon: 'none',
				});
			},
		},
	};
</script>

<style scoped>
	.wallet-container {
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

	/* 钱包余额卡片 */
	.balance-card {
		background: #ff4f00;
		color: #fff;
		padding: 30rpx 0rpx 0rpx;
		text-align: center;
		margin-top: 95rpx;
		border-bottom-left-radius:20rpx;
		border-bottom-right-radius:20rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		position: relative;
	}

	.balance {
		font-size: 48rpx;
		font-weight: bold;
		margin-bottom: 10rpx;
	}

	.assets-label {
		font-size: 24rpx;
		margin-bottom: 30rpx;
	}

	.function-cards {
		left: 0;
		right: 0;
		display: flex;
		justify-content: space-between;
		width: 103%;
		margin-top: 20rpx;
	}

	.function-card {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.7);
		padding: 20rpx 0rpx;
		border-radius: 20rpx;
		margin: 0 2rpx;
		box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
	}

	.function-icon {
		width: 40rpx;
		height: 40rpx;
		margin-bottom: 10rpx;
	}

	.function-name {
		font-size: 28rpx;
		color: #000
	}

	/* 子功能列表 */
	.sub-functions {
		margin-top: 20rpx;
		padding: 10rpx 0rpx;
	}

	.sub-function-item1 {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx 20rpx 30rpx 40rpx;
		background: #fff;
		margin-bottom: 20rpx;
	}
	
	.sub-function-item2 {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx 20rpx 30rpx 40rpx;
		background: #fff;
		margin-bottom: 5rpx;
	}
	
	.function-money {
		display: flex;
		align-items: center;
		font-size: 26rpx;
		margin-left: auto;
	}
	
	.sub-function-item3 {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx 20rpx 30rpx 40rpx;
		background: #fff;
		margin-top: 20rpx;
	}

	.sub-function-name {
		font-size: 28rpx;
	}

	.sub-function-arrow,
	.status-arrow {
		width: 24rpx;
		height: 24rpx;
		margin-left:10rpx
	}

	
	.status-indicator {
		display: flex;
		align-items: center;
		font-size: 24rpx;
		margin-left: auto;
	}

	.added {
		color: #3cb371;
		/* 绿色 */
	}

	.not-added {
		color: #f44336;
		/* 红色 */
	}
</style>