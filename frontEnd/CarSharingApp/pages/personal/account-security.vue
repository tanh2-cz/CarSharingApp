<template>
  <view class="account-security-container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/icon_back.png" class="back-icon"></image>
      </view>
      <text class="title">账号安全</text>
    </view>

    <!-- 账号信息 -->
    <view class="section">
      <text class="section-title">账号信息</text>
      <view class="info-item">
        <text class="info-label">昵称:</text>
        <text class="info-value">{{ nickname }}</text>
        <button class="edit-button" @tap="showEditModal('nickname')">修改</button>
      </view>
      <view class="info-item">
        <text class="info-label">身份:</text>
        <text class="info-value">{{ identity }}</text>
        <button class="edit-button" @tap="showEditModal('identity')">修改</button>
      </view>
      <view class="info-item">
        <text class="info-label">绑定手机号:</text>
        <text class="info-value">{{ phoneNumber }}</text>
        <button class="edit-button" @tap="showEditModal('phoneNumber')">修改</button>
      </view>
      <view class="info-item">
        <text class="info-label">邮箱:</text>
        <text class="info-value">{{ email }}</text>
        <button class="edit-button" @tap="showEditModal('email')">修改</button>
      </view>
    </view>

    <!-- 安全设置 -->
    <view class="section">
      <text class="section-title">安全设置</text>
      <view class="info-item">
        <text class="info-label">密码</text>
        <text class="info-value">********</text>
        <button class="edit-button" @tap="showPasswordModal">修改</button>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout">
      <button class="logout-button" @tap="logout">退出登录</button>
    </view>

    <!-- 修改密码弹窗 -->
    <view v-if="showPasswordModalFlag" class="modal">
      <view class="modal-content">
        <text class="modal-title">修改密码</text>
        <view class="input-item">
          <text class="input-label">旧密码</text>
          <input v-model="oldPassword" class="input-field" type="password" placeholder="请输入旧密码" />
        </view>
        <view class="input-item">
          <text class="input-label">新密码</text>
          <input v-model="newPassword" class="input-field" type="password" placeholder="请输入新密码" />
        </view>
        <view class="input-item">
          <text class="input-label">确认新密码</text>
          <input v-model="confirmPassword" class="input-field" type="password" placeholder="请确认新密码" />
        </view>
        <view class="button-group">
          <button class="confirm-button" @tap="confirmPasswordChange">确认修改</button>
          <button class="cancel-button" @tap="cancelPasswordChange">取消</button>
        </view>
      </view>
    </view>

    <!-- 修改信息弹窗 -->
    <view v-if="showEditModalFlag" class="modal">
      <view class="modal-content">
        <text class="modal-title">修改{{ editFieldLabel }}</text>
        <view class="input-item">
          <input v-model="editValue" class="input-field" :type="editField === 'phoneNumber' ? 'number' : 'text'" :placeholder="'请输入' + editFieldLabel" />
        </view>
        <view class="button-group">
          <button class="confirm-button" @tap="confirmEdit">确认修改</button>
          <button class="cancel-button" @tap="cancelEdit">取消</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      nickname: '拼车达人', // 默认昵称
      identity: '司机', // 默认身份
      phoneNumber: '+86 13812341234', // 默认手机号
      email: 'example@example.com', // 默认邮箱
      showPasswordModalFlag: false, // 控制修改密码弹窗显示与隐藏
      oldPassword: '', // 旧密码
      newPassword: '', // 新密码
      confirmPassword: '', // 确认新密码
      showEditModalFlag: false, // 控制修改信息弹窗显示与隐藏
      editField: '', // 当前修改的字段（nickname, identity, phoneNumber, email）
      editValue: '', // 当前输入的值
      editFieldLabel: '' // 当前字段的标签
    };
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    showEditModal(field) {
      // 显示修改信息弹窗
      this.editField = field;
      this.editFieldLabel = field === 'nickname' ? '昵称' : field === 'identity' ? '身份' : field === 'phoneNumber' ? '绑定手机号' : '邮箱';
      this.editValue = this[field]; // 设置初始值
      this.showEditModalFlag = true;
    },
    confirmEdit() {
      // 确认修改信息
      if (!this.editValue) {
        uni.showToast({
          title: `${this.editFieldLabel}不能为空`,
          icon: 'none'
        });
        return;
      }
      uni.showToast({
        title: '修改功能待实现',
        icon: 'none'
      });
      this.cancelEdit(); // 关闭弹窗
    },
    cancelEdit() {
      // 关闭修改信息弹窗
      this.showEditModalFlag = false;
      this.editValue = '';
      this.editField = '';
      this.editFieldLabel = '';
    },
    showPasswordModal() {
      // 显示修改密码弹窗
      this.showPasswordModalFlag = true;
    },
    confirmPasswordChange() {
      // 简单的密码确认逻辑
      if (this.newPassword !== this.confirmPassword) {
        uni.showToast({
          title: '新密码与确认密码不一致',
          icon: 'none'
        });
        return;
      }
      uni.showToast({
        title: '修改功能待实现',
        icon: 'none'
      });
      this.cancelPasswordChange(); // 关闭弹窗
    },
    cancelPasswordChange() {
      // 关闭修改密码弹窗
      this.showPasswordModalFlag = false;
      // 清空输入框
      this.oldPassword = '';
      this.newPassword = '';
      this.confirmPassword = '';
    },
    logout() {
      uni.showToast({
        title: '退出登录功能待实现',
        icon: 'none'
      });
    }
  }
};
</script>

<style scoped>
.account-security-container {
  padding: 30rpx;
  background: #f5f5f5;
  margin-top: 100rpx; /* 为顶部导航栏留出空间 */
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

.section {
  margin-bottom: 40rpx;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.1);
  padding: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 15rpx 0;
  border-bottom: 1rpx solid #eee;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 28rpx;
  color: #666;
  width: 150rpx;
}

.info-value {
  font-size: 28rpx;
  color: #333;
  flex: 1;
}

.edit-button {
  font-size: 24rpx;
  color: #409eff;
  background: none;
  border: 1rpx solid #409eff;
  padding: 10rpx 20rpx;
  border-radius: 8rpx;
}

.logout {
  margin-top: 40rpx;
  display: flex;
  justify-content: center;
}

.logout-button {
  width: 80%;
  padding: 20rpx;
  background: #f56c6c;
  color: #fff;
  font-size: 32rpx;
  border-radius: 40rpx;
  border: none;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.1);
}

/* 弹窗样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 12rpx;
  width: 80%;
  max-width: 500rpx;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
  text-align: center;
}

.input-item {
  margin-bottom: 20rpx;
}

.input-label {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.input-field {
  font-size: 28rpx;
  padding: 10rpx;
  width: 100%;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.confirm-button, .cancel-button {
  width: 48%;
  padding: 20rpx;
  border-radius: 40rpx;
  font-size: 32rpx;
  border: none;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.1);
}

.confirm-button {
  background-color: #409eff;
  color: #fff;
}

.cancel-button {
  background-color: #f56c6c;
  color: #fff;
}
</style>