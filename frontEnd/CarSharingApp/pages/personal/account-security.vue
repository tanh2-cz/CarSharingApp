<template>
  <view class="account-security-container">
    <view class="top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/image/icon_back.png" class="back-icon"></image>
      </view>
      <text class="title">账号安全</text>
    </view>

    <view class="section">
      <text class="section-title">账号信息</text>
      <view class="info-item">
        <text class="info-label">昵称:</text>
        <text class="info-value">{{ nickname }}</text>
        <button class="edit-button" @tap="showEditModal('nickname')">
          <text>修改</text>
          <image src="/static/image/icon_arrow_right.png" class="edit-arrow-icon"></image>
        </button>
      </view>
      <view class="info-item">
        <text class="info-label">身份:</text>
        <text class="info-value">{{ identity }}</text>
        <button class="edit-button" @tap="showEditModal('identity')">
          <text>修改</text>
          <image src="/static/image/icon_arrow_right.png" class="edit-arrow-icon"></image>
        </button>
      </view>
      <view class="info-item">
        <text class="info-label">手机号:</text>
        <text class="info-value">{{ phoneNumber }}</text>
        <button class="edit-button" @tap="showEditModal('phoneNumber')">
          <text>修改</text>
          <image src="/static/image/icon_arrow_right.png" class="edit-arrow-icon"></image>
        </button>
      </view>
      <view class="info-item">
        <text class="info-label">邮箱:</text>
        <text class="info-value">{{ email }}</text>
        <button class="edit-button" @tap="showEditModal('email')">
          <text>修改</text>
          <image src="/static/image/icon_arrow_right.png" class="edit-arrow-icon"></image>
        </button>
      </view>
    </view>

    <view class="section">
      <text class="section-title">安全设置</text>
      <view class="info-item">
        <text class="info-label">密码</text>
        <text class="info-value">********</text>
        <button class="edit-button" @tap="showPasswordModal">
          <text>修改</text>
          <image src="/static/image/icon_arrow_right.png" class="edit-arrow-icon"></image>
        </button>
      </view>
    </view>

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
      this.editField = field;
      this.editFieldLabel = field === 'nickname' ? '昵称' : field === 'identity' ? '身份' : field === 'phoneNumber' ? '绑定手机号' : '邮箱';
      this.editValue = this[field];
      this.showEditModalFlag = true;
    },
    confirmEdit() {
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
      this.cancelEdit();
    },
    cancelEdit() {
      this.showEditModalFlag = false;
      this.editValue = '';
      this.editField = '';
      this.editFieldLabel = '';
    },
    showPasswordModal() {
      this.showPasswordModalFlag = true;
    },
    confirmPasswordChange() {
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
      this.cancelPasswordChange();
    },
    cancelPasswordChange() {
      this.showPasswordModalFlag = false;
      this.oldPassword = '';
      this.newPassword = '';
      this.confirmPassword = '';
    }
  }
};
</script>

<style scoped>
.account-security-container {
  padding: 30rpx;
  background: #ffffff;
  margin-top: 100rpx; 
  padding-bottom: 30rpx;
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
.section:last-child {
  margin-bottom: 0;
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
  font-size: 28rpx;
  color: #409eff;
  background: transparent;
  border: none;
  padding: 0;
  margin-left: 10rpx;
  display: flex;
  align-items: center; /* 这对于图片和文字的垂直对齐很重要 */
  outline: none;
  line-height: normal;
}
.edit-button::after {
  border: none;
}

/* 移除了之前的 .arrow-icon 文本箭头样式 */
/* 如果您之前有 .arrow-icon 样式，可以删除或注释掉 */
/* .arrow-icon {
  margin-left: 8rpx;
  font-size: 28rpx;
  color: #409eff;
} */

/* 新增：修改按钮中的箭头图标样式 */
.edit-arrow-icon {
  width: 24rpx;  /* 图标宽度，请根据您的图标实际大小调整 */
  height: 24rpx; /* 图标高度，请根据您的图标实际大小调整 */
  margin-left: 8rpx; /* 图标与“修改”文字的间距 */
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
  margin-bottom: 30rpx;
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
  box-sizing: border-box;
  height: 70rpx;
  display: flex;
  align-items: center;
}

.input-field:focus {
  border-color: #409eff;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 40rpx;
}

.confirm-button {
  width: 48%;
  padding: 14rpx; 
  border-radius: 8rpx;
  font-size: 28rpx; 
  border: none;
  background-color: #409eff;
  color: #fff;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
  line-height: normal;
}

.cancel-button {
  width: 48%;
  padding: 14rpx;
  border-radius: 8rpx;
  font-size: 28rpx;
  background-color: #fff;
  color: #409eff;
  border: 1rpx solid #409eff;
  box-shadow: none;
  line-height: normal;
}
</style>