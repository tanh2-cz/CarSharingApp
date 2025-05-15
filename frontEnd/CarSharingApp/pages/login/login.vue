<template>
  <view class="container">
    <image class="bg-image" src="https://picsum.photos/750/1334?blur=5" mode="aspectFill"></image>
    <view class="overlay"></view>
    <view class="form-container">
      <view class="tabs">
        <text :class="{ 'tab': true, 'active': activeTab === 'login' }" @tap="changeTab('login')">登录</text>
        <text :class="{ 'tab': true, 'active': activeTab === 'register' }" @tap="changeTab('register')">注册</text>
      </view>

      <!-- 登录表单 -->
      <view class="form" v-if="activeTab === 'login'">
        <view class="input-group">
          <input type="text" v-model="loginForm.username" placeholder="请输入用户名" class="input" />
        </view>
        <view class="input-group">
          <input type="password" v-model="loginForm.password" placeholder="请输入密码" class="input" />
        </view>
        <button class="btn" @tap="handleLogin">立即登录</button>
      </view>

      <!-- 注册表单 -->
      <view class="form" v-if="activeTab === 'register'">
        <view class="input-group">
          <input type="text" v-model="registerForm.username" placeholder="请输入用户" class="input" />
        </view>
        <view class="input-group">
          <input type="text" v-model="registerForm.phone" placeholder="请输入电话" class="input" />
        </view>
        <view class="input-group">
          <input type="password" v-model="registerForm.password" placeholder="请输入密码" class="input" />
        </view>
        <button class="btn" @tap="handleRegister">立即注册</button>
      </view>
    </view>
  </view>
</template>

<script>
import register from '../../utils/api/register';
import login from '../../utils/api/login';
export default {
	data() {
		return {
			activeTab: 'login',
			loginForm: {
				username: 'admin',
				password: '123'
			},
			registerForm: {
				username: 'admin',
				phone: '1234567890',
				password: '123'
			}
		}
	},
	methods: {
		changeTab(tab) {
			this.activeTab = tab
		},
		handleLogin() {
			// 直接跳转
			// uni.switchTab({
			// 	url: '/pages/main/info'
			// })
			// uni.showToast({
			//   title: '登录功能待实现',
			//   icon: 'none'
			// })
			console.log('登录:', this.loginForm);
			// uni.switchTab({
			// 	url: '/pages/main/info'
			// })
			login({ data: this.loginForm }).then((res) => {
				uni.showToast({
					title: '登录成功',
					icon: 'none'
				})
				uni.switchTab({
					url: '/pages/main/info'
				})
			}).catch((err) => {
				uni.showToast({
					title: '登录失败',
					icon: 'none'
				})
				console.log(err);
			})
			
		},
		handleRegister() {
			// uni.showToast({
			//   title: '注册功能待实现',
			//   icon: 'none'
			// })
			console.log('注册:', this.registerForm)
			register({ data: this.registerForm }).then((res) => {
				uni.showToast({
					title: '注册成功',
					icon: 'none'
				})
				this.changeTab('login');
			}).catch((err) => {
				uni.showToast({
					title: '注册失败',
					icon: 'none'
				})
				console.log(err);
			})
		},
	}
}
</script>

<style scoped>
.container {
  position: relative;
  height: 100vh;
  width: 100%;
}

.bg-image {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 2;
}

.form-container {
  position: relative;
  z-index: 3;
  padding: 40rpx;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 60rpx;
}

.tab {
  font-size: 36rpx;
  color: #ffffff;
  padding: 20rpx 40rpx;
  opacity: 0.7;
}

.tab.active {
  opacity: 1;
  border-bottom: 4rpx solid #409eff;
}

.form {
  background: rgba(255, 255, 255, 0.95);
  padding: 40rpx;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 30rpx;
}

.input {
  background: #f5f7fa;
  padding: 24rpx;
  border-radius: 12rpx;
  font-size: 28rpx;
  color: #333;
}

.btn {
  background: linear-gradient(45deg, #409eff, #67c23a);
  color: #ffffff;
  font-size: 32rpx;
  padding: 24rpx;
  border-radius: 12rpx;
  margin-top: 20rpx;
  border: none;
}

.btn:hover {
  opacity: 0.9;
}
</style>