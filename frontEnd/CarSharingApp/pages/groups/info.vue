<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <text class="title">消息</text>
      <view class="search-bar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜索消息"
          class="search-input"
        />
        <image src="/static/image/icon_search.png" class="search-icon"></image>
      </view>
      <view class="action-buttons">
        <image
          src="/static/image/icon_add.png"
          class="add-icon"
          @tap="showAddOptions"
        ></image>
      </view>
    </view>

    <!-- 分类切换按钮 -->
    <view class="group-tabs">
      <view
        class="tab-item"
        :class="{ active: activeTab === 'joined' }"
        @tap="switchTab('joined')"
      >
        我加入的群聊
      </view>
      <view
        class="tab-item"
        :class="{ active: activeTab === 'created' }"
        @tap="switchTab('created')"
      >
        我创建的群聊
      </view>
    </view>

    <scroll-view scroll-y class="chat-list" :scroll-with-animation="true">
      <movable-area
        class="movable-area"
        v-for="(chat, index) in filteredChatList"
        :key="index"
      >
        <movable-view
          class="movable-view"
          direction="horizontal"
          :x="chat.x"
          @change="onChange($event, index)"
          @touchend="onTouchEnd(index)"
        >
          <!-- 主内容 -->
          <view
            class="chat-item"
            @tap="goToChat(chat)"
            :style="{ animationDelay: `${index * 0.05}s` }"
          >
            <view class="chat-icon" v-show="chat.icon">
              <image :src="chat.icon" class="icon"></image>
              <view class="badge" v-if="chat.unreadCount > 0">{{
                chat.unreadCount
              }}</view>
            </view>
            <view class="chat-info">
              <view class="chat-header">
                <text class="chat-name">{{ chat.name }}</text>
                <text class="time">{{ formatTime(chat.time) }}</text>
              </view>
              <text class="message">{{ chat.lastMessage }}</text>
            </view>
          </view>

          <!-- 右侧操作按钮 -->
          <view class="actions" v-show="chat.icon">
            <view class="action-btn unread" @tap="unreadChat(index)"
              >标为未读</view
            >
            <view class="action-btn ignore" @tap="ignoreChat(index)">忽略</view>
            <view class="action-btn delete" @tap="deleteChat(index)">删除</view>
          </view>
        </movable-view>
      </movable-area>
    </scroll-view>

    <!-- 加号弹窗 -->
    <view class="modal" v-if="showAddModal" @tap="closeAddModal">
      <view class="modal-content" @tap.stop>
        <view class="modal-item" @tap="createChat">
          <image
            src="/static/image/icon_group_create.png"
            class="modal-icon"
          ></image>
          <text>新建群聊</text>
        </view>
        <view class="modal-item" @tap="joinChat">
          <image
            src="/static/image/icon_group_join.png"
            class="modal-icon"
          ></image>
          <text>加入群聊</text>
        </view>
        <view class="modal-item cancel" @tap="closeAddModal">
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
      activeTab: "created", // 当前激活的标签
      chatList: [
        {
          id: 1,
          name: "拼车群1",
          icon: "/static/image/group1.png",
          lastMessage: "我们几点上车？",
          unreadCount: 7,
          time: "星期二",
          type: "created", // 添加类型标记
        },
        {
          id: 2,
          name: "拼车群2",
          icon: "/static/image/group2.png",
          lastMessage: "请大家支付一下。",
          unreadCount: 7,
          time: "星期二",
          type: "joined",
        },
        {
          id: 3,
          name: "拼车群3",
          icon: "/static/image/group3.png",
          lastMessage: "当天你还需要购票",
          unreadCount: 1,
          time: "星期二",
          type: "joined",
        },
        {
          id: 4,
          name: "拼车群4",
          icon: "/static/image/group4.png",
          lastMessage: "龙泉广场集合。",
          unreadCount: 1,
          time: "星期二",
          type: "joined",
        },
        {
          id: 5,
          name: "出租车交通动态",
          icon: "/static/image/group5.png",
          lastMessage: "打车-支付成功。",
          unreadCount: 7,
          time: "星期五",
          type: "created", // 添加类型标记
        },
        {
          id: 6,
          name: "拼车群5",
          icon: "/static/image/group6.png",
          lastMessage: "还有谁是到北京博物馆的？",
          time: "2025/02/15",
          type: "joined",
        },
        {
          id: 7,
          name: "简单出行服务",
          icon: "/static/image/group7.png",
          lastMessage: "帮宁返程火车票优惠订",
          time: "2025/02/02",
          type: "joined",
        },
        {
          id: 8,
          name: "简单酒店",
          icon: "/static/image/group8.png",
          lastMessage: "帮宁双程全家游，优惠品质好房专享低价～",
          time: "2025/01/30",
          type: "created", // 添加类型标记
        },
        {
          id: 9,
          name: "房卡证",
          icon: "/static/image/group9.png",
          lastMessage: "升限额-我想以帮您看一下房子",
          time: "2024/12/08",
          type: "joined",
        },
        {
          id: 10,
          name: "飞机票",
          icon: "/static/image/group10.png",
          lastMessage: "升限额-我想以帮您看一下房子",
          time: "2024/12/08",
          type: "joined",
        },
        {
          id: 11,
          name: "拼车群6",
          icon: "/static/image/group11.png",
          lastMessage: "我想以帮您看一下房子",
          time: "2024/12/08",
          type: "joined",
        },
        {
          id: 12,
          name: "拼车群7",
          icon: "/static/image/group12.png",
          lastMessage: "看一下",
          time: "2024/12/08",
          type: "joined",
        },
        {
          id: 13,
          name: "",
          icon: "",
          lastMessage: "",
          time: "",
          type: "joined",
        },
        {
          id: 14,
          name: "",
          icon: "",
          lastMessage: "",
          time: "",
          type: "joined",
        },
      ],
      showAddModal: false,
      startX: 0, // 记录触摸起始位置,
      searchQuery: "",
    };
  },
  computed: {
    filteredChatList() {
      return this.chatList.filter((chat) => chat.type === this.activeTab);
    },
  },
  methods: {
    switchTab(tab) {
      this.activeTab = tab;
    },
    showFilter() {
      uni.showToast({
        title: "筛选功能待实现",
        icon: "none",
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
        title: "新建群聊功能待实现",
        icon: "none",
      });
    },
    joinChat() {
      this.closeAddModal();
      uni.showToast({
        title: "加入群聊功能待实现",
        icon: "none",
      });
    },
    goToChat(chat) {
      chat.unreadCount = 0; //unreadCount进去之后就清零了
      uni.navigateTo({
        url: `/pages/groups/chat?id=${chat.id}`,
      });
    },

    formatTime(time) {
      // 这里可以添加更复杂的时间格式化逻辑
      return time;
    },
    // 滑动事件
    onChange(e, index) {
      this.chatList[index].x = e.detail.x;
    },

    onTouchEnd(index) {
      const threshold = -150; // 滑动阈值
      const maxDistance = -300; // 最大滑动距离

      // 如果已经滑动超过阈值，直接显示全部按钮
      if (this.chatList[index].x < threshold) {
        this.chatList[index].x = maxDistance;
      } else {
        this.chatList[index].x = 0; // 恢复原状
      }
    },

    // 删除聊天
    deleteChat(index) {
      uni.showModal({
        title: "提示",
        content: "确定删除此聊天吗？",
        success: (res) => {
          if (res.confirm) {
            this.chatList.splice(index, 1);
          } else {
            this.chatList[index].x = 0; // 恢复原状
          }
          this.chatList[index].x = 0;
        },
      });
    },

    // 忽略聊天
    ignoreChat(index) {
      this.chatList[index].unreadCount = 0;
      uni.showToast({ title: "已忽略", icon: "success" });
      this.chatList[index].x = 0;
    },
    //标为未读
    unreadChat(index) {
      if (this.chatList[index].unreadCount == 0) {
        this.chatList[index].unreadCount = 1;
        uni.showToast({
          title: "已标为未读",
          icon: "success",
        });
      } else {
        uni.showToast({
          title: "本就为未读-操作无效",
          icon: "none",
        });
      }

      this.chatList[index].x = 0;
    },
  },
};
</script>

<style scoped>
/* 基础样式 */
:root {
  --primary-color: #4a8cff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #ff4757;
  --light-color: #f8f9fa;
  --dark-color: #343a40;
  --border-radius: 12rpx;
  --box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
  --transition: all 0.3s ease;
}

.container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f8f8;
  position: relative;
}

/* 顶部导航栏 */
.top-bar {
  padding: 30rpx 40rpx;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
  position: fixed;
  z-index: 10;
  width: 100%;
  height: 4%;
  background-color: #28a745;
}

.title {
  font-size: 38rpx;
  font-weight: 600;
  color: #333;
  letter-spacing: 1rpx;
}

.action-buttons {
  display: flex;
  align-items: center;
  width: 15%;
  height: 100%;
  /* background-color: #34aadc; */
  justify-content: left;
  margin-left: 5%;
}

.filter-icon,
.add-icon {
  width: 44rpx;
  height: 44rpx;
  transition: var(--transition);
}

.filter-icon:active,
.add-icon:active {
  transform: scale(0.9);
  opacity: 0.8;
}

/* 聊天列表 */
.chat-list {
  flex: 1;
  background: #fff;
  padding: 20rpx 0;
  margin-top: 12%;
  margin-bottom: 10%;
  width: 100%;
}

.chat-item {
  padding: 30rpx;
  border-bottom: 2rpx solid #f0f0f0;
  display: flex;
  align-items: center;
  transition: var(--transition);
  animation: fadeInUp 0.3s forwards;
  opacity: 0;
  width: 92%;
  /* background-color: #333; */
}

.chat-item:active {
  background-color: #f8f8f8;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-icon {
  position: relative;
  margin-right: 25rpx;
}

.icon {
  width: 90rpx;
  height: 90rpx;
  border-radius: 50%;
  background: #f0f0f0;
  box-shadow: var(--box-shadow);
}

.badge {
  position: absolute;
  top: -10rpx;
  right: -10rpx;
  background: var(--danger-color);
  color: #fff;
  font-size: 22rpx;
  font-weight: 600;
  border-radius: 50%;
  padding: 8rpx;
  min-width: 36rpx;
  height: 36rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
  background-color: red;
}

.chat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  /* background-color: #28a745; */
  width: 50%;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.chat-name {
  font-size: 34rpx;
  font-weight: 500;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 400rpx;
}

.time {
  font-size: 26rpx;
  color: #999;
  font-weight: 400;
}

.message {
  font-size: 28rpx;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 模态框 */
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
  align-items: flex-end;
  opacity: 0;
  animation: fadeIn 0.2s forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: #fff;
  border-radius: 30rpx 30rpx 0 0;
  width: 100%;
  padding: 40rpx 0;
  transform: translateY(100%);
  animation: slideUp 0.3s forwards;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.modal-item {
  padding: 30rpx 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.modal-item:active {
  background-color: #f5f5f5;
}

.modal-item text {
  font-size: 34rpx;
  color: #333;
  margin-left: 20rpx;
}

.modal-icon {
  width: 40rpx;
  height: 40rpx;
}

.modal-item.cancel {
  margin-top: 20rpx;
  padding-top: 40rpx;
  border-top: 1rpx solid #f0f0f0;
}

.modal-item.cancel text {
  color: var(--danger-color);
  font-weight: 500;
}

/* 可滑动区域样式 */
.movable-area {
  width: 100%;
  height: 160rpx;
  position: relative;
  /* background-color: #34aadc; */
}

.movable-view {
  width: 150%;
  height: 100%;
  display: flex;
}

/* 操作按钮区域 */
.actions {
  width: 50%;
  height: 100%;
  display: flex;
  /* justify-content: flex-end; 从右边开始填方块 左边留白 */
  background-color: #4a8cff;
}

.action-btn {
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28rpx;
}

.delete {
  background-color: #ff3b30;
}

.ignore {
  background-color: #ff9500;
}

.unread {
  background-color: #34aadc;
}

.search-bar {
  flex: 1;
  background: #fff;
  border-radius: 25rpx;
  display: flex;
  align-items: center;
  height: 100%;
  border: 4rpx solid #ccc;
  margin-left: 5%;
  width: 60%;
}

.search-icon {
  width: 50rpx;
  height: 50rpx;
  margin-right: 20rpx;
  /* background-color: #333; */
}

.search-input {
  flex: 1;
  font-size: 30rpx;
  color: #333;
  /* background-color: #28a745; */
  margin-left: 7%;
}

/* 分类切换按钮样式 */
.group-tabs {
  display: flex;
  justify-content: space-around;
  background: #fff;
  padding: 20rpx;
  margin-top: 120rpx;
  border-bottom: 1rpx solid #eee;
}

.tab-item {
  padding: 15rpx 30rpx;
  font-size: 28rpx;
  color: #666;
  position: relative;
  transition: all 0.3s;
}

.tab-item.active {
  color: #28a745;
  font-weight: 500;
}

.tab-item.active::after {
  content: "";
  position: absolute;
  bottom: -10rpx;
  left: 50%;
  transform: translateX(-50%);
  width: 40rpx;
  height: 4rpx;
  background: #28a745;
  border-radius: 2rpx;
}

/* 调整列表上边距 */
.chat-list {
  margin-top: 0;
}
</style>
