<template>
	<view class="money-container">
		<!-- 顶部导航栏 -->
		<view class="top-bar">
			<view class="back-button" @tap="goBack">
				<image src="/static/image/icon_back.png" class="back-icon"></image>
			</view>
			<text class="title">我的零钱</text>
		</view>

		<!-- 零钱信息容器 -->
		<view class="money-info-container">
			<image src="/static/image/icon_money.png" class="money-icon"></image>
			<text class="money-title">我的零钱</text>
			<text class="money-balance">¥{{ moneyBalance }}</text>
		</view>

		<!-- 充值和提现按钮容器 -->
		<view class="button-container">
			<button class="recharge-button" @tap="handleRechargeTap">充值</button>
			<button class="withdraw-button" @tap="handleWithdrawTap">提现</button>
		</view>

		<text class="faq-text" @tap="handleFaqTap">常见问题</text>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				moneyBalance: '2025.51', // 零钱余额
			};
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			handleRechargeTap() {
				uni.showToast({
					title: '点击了充值功能',
					icon: 'none',
				});
			},
			handleWithdrawTap() {
				uni.showToast({
					title: '点击了提现功能',
					icon: 'none',
				});
			},
			handleFaqTap() {
				uni.showToast({
					title: '点击了常见问题功能',
					icon: 'none'
				});
			}
		},
	};
</script>

<style>
	.money-container {
		height: 100vh;
		display: flex;
		flex-direction: column;
		background: #fff;
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

	/* 零钱信息容器 */
	.money-info-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		margin-top: 200rpx;
	}

	.money-icon {
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
		margin-bottom: 20rpx;
	}

	.money-title {
		font-size: 32rpx;
		color: #333;
		margin-bottom: 20rpx;
	}

	.money-balance {
		font-size: 48rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 20rpx;
	}

	/* 充值和提现按钮容器 */
	.button-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-top: auto;
		/* 确保按钮在底部 */
		padding: 30rpx;
	}

	.recharge-button {
		background: #00c553;
		color: #fff;
		font-size: 28rpx;
		padding: 10rpx 0;
		width: 40%;
		border-radius: 20rpx;
		margin-bottom: 30rpx;
	}

	.withdraw-button {
		background: #f2f2f2;
		color: #333;
		font-size: 28rpx;
		padding: 10rpx 0;
		width: 40%;
		border-radius: 20rpx;
		margin-bottom: 50rpx;
	}
	
	.faq-text {
	  font-size: 24rpx;
	  color: #1976d2; /* 蓝色 */
	  text-align: center;
	 margin-bottom: 100rpx;
	}
</style>