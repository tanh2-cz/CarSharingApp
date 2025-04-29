<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <text class="title">消息</text>
      <view class="action-buttons">
        <image src="/static/icon_filter.png" class="filter-icon" @tap="showFilter"></image>
        <image src="/static/icon_add.png" class="add-icon" @tap="showAddOptions"></image>
      </view>
    </view>

    <!-- 群聊列表 -->
    <scroll-view scroll-y class="chat-list">
		<view class="chat-item" v-for="(chat, index) in chatList" :key="index" @tap="goToChat(chat)">
			<view class="chat-icon">
				<image :src="chat.icon" class="icon"></image>
				<view class="badge" v-if="chat.unreadCount > 0">{{ chat.unreadCount }}</view>
			</view>
			<view class="chat-info">
				<view class="chat-header">
					<text class="chat-name">{{ chat.name }}</text>
					<text class="time">{{ chat.time }}</text>
				</view>
				<text class="message">{{ chat.lastMessage }}</text>
			</view>
		</view>
    </scroll-view>

    <!-- 加号弹窗 -->
    <view class="modal" v-if="showAddModal">
      <view class="modal-content">
        <view class="modal-item" @tap="createChat">
          <text>新建群聊</text>
        </view>
        <view class="modal-item" @tap="joinChat">
          <text>加入群聊</text>
        </view>
        <view class="modal-item" @tap="closeAddModal">
          <text>取消</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      chatList: [
        { id: 1, name: '简单运动', icon: '/static/logo.png', lastMessage: '叫一下，你有新的订单机会成功啦！', unreadCount: 7, time: '星期二' },
        { id: 2, name: '简单·超划算', icon: '/static/logo.png', lastMessage: '上海龙华西车道，丽江旺吉额章零售 23.9元', unreadCount: 7, time: '星期二' },
        { id: 3, name: '购票', icon: '/static/logo.png', lastMessage: '当天你还需要购票', unreadCount: 1, time: '星期二' },
        { id: 4, name: '天天知福利', icon: '/static/logo.png', lastMessage: '优惠礼包更多彩礼比！0元奖励你啦！', unreadCount: 1, time: '星期二' },
        { id: 5, name: '公共交通动态', icon: '/static/logo.png', lastMessage: '叫一下，请提供公交交通能推准啦！', unreadCount: 7, time: '星期五' },
        { id: 6, name: '订单提醒', icon: '/static/logo.png', lastMessage: '[7条] 打车-支付成功', time: '2025/02/15' },
        { id: 7, name: '简单出行服务', icon: '/static/logo.png', lastMessage: '[3条] 帮宁返程火车票优惠订', time: '2025/02/02' },
        { id: 8, name: '简单酒店', icon: '/static/logo.png', lastMessage: '[3条] 帮宁双程全家游，优惠品质好房专享低价～', time: '2025/01/30' },
        { id: 9, name: '房卡证', icon: '/static/logo.png', lastMessage: '升限额-我想以帮您看一下房子', time: '2024/12/08' }
      ],
      showAddModal: false
    };
  },
  methods: {
    showFilter() {
      uni.showToast({
        title: '筛选功能待实现',
        icon: 'none'
      });
    },
    showAddOptions() {
      this.showAddModal = true;
    },
    closeAddModal() {
      this.showAddModal = false;
    },
    createChat() {
      this.closeAddModal();
      uni.showToast({
        title: '新建群聊功能待实现',
        icon: 'none'
      });
    },
    joinChat() {
      this.closeAddModal();
      uni.showToast({
        title: '加入群聊功能待实现',
        icon: 'none'
      });
    },
    goToChat(chat) {
      uni.navigateTo({
        url: `/pages/groups/chat?id=${chat.id}`
      });
    }
  }
}
</script>

<style scoped>
.container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.top-bar {
  padding: 20rpx 30rpx;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 36rpx;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  align-items: center;
}

.filter-icon, .add-icon {
  width: 40rpx;
  height: 40rpx;
  margin-left: 20rpx;
}

.chat-list {
  flex: 1;
  background: #fff;
}

.chat-item {
  padding: 30rpx;
  border-bottom: 1rpx solid #eee;
  display: flex;
  align-items: center;
}

.chat-icon {
  position: relative;
  margin-right: 20rpx;
}

.icon {
  width: 80rpx;
  height: 80rpx;
}

.badge {
  position: absolute;
  top: -10rpx;
  right: -10rpx;
  background: #ff4d4f;
  color: #fff;
  font-size: 24rpx;
  border-radius: 50%;
  padding: 5rpx 10rpx;
  min-width: 30rpx;
  text-align: center;
}

.chat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-name {
  font-size: 32rpx;
  color: #333;
}

.time {
  font-size: 24rpx;
  color: #999;
}

.message {
  font-size: 28rpx;
  color: #666;
  margin-top: 10rpx;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bottom-nav {
  display: flex;
  justify-content: space-around;
  padding: 20rpx 0;
  background: #fff;
  border-top: 1rpx solid #eee;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nav-item.active text {
  color: #409eff;
}

.nav-icon {
  width: 48rpx;
  height: 48rpx;
  margin-bottom: 10rpx;
}

.nav-item text {
  font-size: 24rpx;
  color: #666;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  border-radius: 20rpx;
  width: 80%;
  padding: 20rpx 0;
}

.modal-item {
  padding: 30rpx;
  text-align: center;
  border-bottom: 1rpx solid #eee;
}

.modal-item text {
  font-size: 32rpx;
  color: #333;
}

.modal-item:last-child {
  border-bottom: none;
}
</style>