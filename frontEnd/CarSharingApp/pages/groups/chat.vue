<template>
  <view class="chat-container">
    <!-- 顶部导航栏 -->
    <view class="chat-top-bar">
      <view class="back-button" @tap="goBack">
        <image src="/static/image/icon_back.png" class="back-icon"></image>
      </view>
      <text class="chat-title">{{ chatInfo.name }}</text>
    </view>

    <!-- 聊天消息列表 -->
    <scroll-view scroll-y class="message-list" :scroll-top="scrollTop" @scrolltolower="loadMoreMessages">
      <view class="message-wrapper" v-for="(message, index) in messages" :key="index">
        <view class="message-time" v-if="message.showTime">{{ message.time }}</view>
        <view :class="['message-item', message.isSelf ? 'self' : 'other']">
          <image :src="message.avatar" class="avatar"></image>
          <view class="message-content">
            <text>{{ message.content }}</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 输入框 -->
    <view class="input-bar">
      <input
        type="text"
        v-model="inputMessage"
        placeholder="输入消息..."
        class="message-input"
        @confirm="sendMessage"
      />
      <view class="send-button" @tap="sendMessage">
        <text>发送</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      chatInfo: {}, // 聊天信息，从消息界面传递
      messages: [], // 聊天消息列表
      inputMessage: '', // 输入框内容
      scrollTop: 0, // 滚动位置
      page: 1, // 消息分页
      chatList: [
        { id: 1, name: '拼车群1', icon: '/static/image/group1.png', lastMessage: '我们几点上车？', unreadCount: 7, time: '星期二' },
        { id: 2, name: '拼车群2', icon: '/static/image/group2.png', lastMessage: '请大家支付一下。', unreadCount: 7, time: '星期二' },
        { id: 3, name: '拼车群3', icon: '/static/image/group3.png', lastMessage: '当天你还需要购票', unreadCount: 1, time: '星期二' },
        { id: 4, name: '拼车群4', icon: '/static/image/group4.png', lastMessage: '龙泉广场集合。', unreadCount: 1, time: '星期二' },
        { id: 5, name: '出租车交通动态', icon: '/static/image/group5.png', lastMessage: '打车-支付成功。', unreadCount: 7, time: '星期五' },
        { id: 6, name: '拼车群5', icon: '/static/image/group6.png', lastMessage: '还有谁是到北京博物馆的？', time: '2025/02/15' },
        { id: 7, name: '简单出行服务', icon: '/static/image/group7.png', lastMessage: '帮宁返程火车票优惠订', time: '2025/02/02' },
        { id: 8, name: '简单酒店', icon: '/static/image/group8.png', lastMessage: '帮宁双程全家游，优惠品质好房专享低价～', time: '2025/01/30' },
        { id: 9, name: '房卡证', icon: '/static/image/group9.png', lastMessage: '升限额-我想以帮您看一下房子', time: '2024/12/08' },
		{ id: 10, name: '飞机票', icon: '/static/image/group10.png', lastMessage: '升限额-我想以帮您看一下房子', time: '2024/12/08' },
		{ id: 11, name: '拼车群6', icon: '/static/image/group11.png', lastMessage: '我想以帮您看一下房子', time: '2024/12/08' },
		{ id: 12, name: '拼车群7', icon: '/static/image/group12.png', lastMessage: '看一下', time: '2024/12/08' },
		{ id: 13, name: '', icon: '', lastMessage: '', time: '' },
		{ id: 14, name: '', icon: '', lastMessage: '', time: '' },
      ],
    };
  },
  onLoad(options) {
    // 从消息界面获取 chat id
    const chatId = options.id;
    // 根据 id 查找聊天信息
    this.chatInfo = this.chatList.find(chat => chat.id == chatId) || {};
    // 初始化消息数据（示例数据）
    this.loadMessages();
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    loadMessages() {
      // 模拟加载消息数据
      const newMessages = [
        {
          id: 1,
          content: '你好，我们拼车去机场吗？',
          time: '2025-04-29 10:00',
          showTime: true,
          isSelf: false,
          avatar: this.chatInfo.icon
        },
        {
          id: 2,
          content: '好的，什么时候出发？',
          time: '2025-04-29 10:05',
          showTime: false,
          isSelf: true,
          avatar: '/static/user_avatar.png' // 自己的头像
        },
        {
          id: 3,
          content: '下午2点可以吗？',
          time: '2025-04-29 10:10',
          showTime: true,
          isSelf: false,
          avatar: this.chatInfo.icon
        }
      ];
      this.messages = [...newMessages, ...this.messages];
      // 滚动到底部
      this.$nextTick(() => {
        this.scrollTop = this.messages.length * 1000;
      });
    },
    loadMoreMessages() {
      // 加载更多消息（分页）
      uni.showToast({
        title: '加载更多消息功能待实现',
        icon: 'none'
      });
    },
    sendMessage() {
      if (!this.inputMessage.trim()) return;
      const newMessage = {
        id: this.messages.length + 1,
        content: this.inputMessage,
        time: this.formatTime(new Date()),
        showTime: true,
        isSelf: true,
        avatar: '/static/user_avatar.png'
      };
      this.messages.push(newMessage);
      this.inputMessage = '';
      // 滚动到底部
      this.$nextTick(() => {
        this.scrollTop = this.messages.length * 1000;
      });
    },
    formatTime(date) {
      // 格式化时间
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    }
  }
};
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.chat-top-bar {
  padding: 20rpx 30rpx;
  background: #fff;
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
  height: 8%;
}

.back-button {
  margin-right: 20rpx;
}

.back-icon {
  width: 40rpx;
  height: 40rpx;
}

.chat-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.message-list {
  flex: 1;
  padding: 20rpx;
  background: #f5f5f5;
}

.message-wrapper {
  margin-bottom: 20rpx;
}

.message-time {
  text-align: center;
  font-size: 28rpx;
  color: #999;
  margin-bottom: 10rpx;
}

.message-item {
  display: flex;
  align-items: flex-start;
}

.message-item.self {
  flex-direction: row-reverse;
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin: 0 20rpx;
}

.message-content {
  max-width: 60%;
  padding: 20rpx;
  border-radius: 20rpx;
  background: #fff;
  font-size: 32rpx;
  color: #333;
}

.message-item.self .message-content {
  background: #409eff;
  color: #fff;
}

.input-bar {
  padding: 20rpx 30rpx;
  background: #fff;
  display: flex;
  align-items: center;
  border-top: 1rpx solid #eee;
}

.message-input {
  flex: 1;
  height: 80rpx;
  padding: 0 20rpx;
  background: #f5f5f5;
  border-radius: 40rpx;
  font-size: 32rpx;
}

.send-button {
  margin-left: 20rpx;
  padding: 20rpx 40rpx;
  background: #409eff;
  border-radius: 40rpx;
}

.send-button text {
  font-size: 32rpx;
  color: #fff;
}
</style>