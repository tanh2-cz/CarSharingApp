<template>
  <view class="container">
    <!-- 顶部信息栏 -->
    <view class="header">
      <view class="back-button" @tap="goBack">
        <image src="/static/image/icon_back.png" class="back-icon"></image>
      </view>
      <view class="group-title">拼车群</view>
      <view class="member-count">4人</view>
    </view>

    <!-- 群成员头像区域 -->
    <view class="members-section">
      <view class="section-header">
        <text class="block-title">群成员</text>
        <view class="more-link" @tap="showMoreMembers">
          查看更多
          <text class="arrow">→</text>
        </view>
      </view>
      <view class="members-grid">
        <view
          class="member-item"
          v-for="(member, index) in groupMembers"
          :key="index"
        >
          <image :src="member.avatar" class="member-avatar"></image>
          <text class="member-name">{{ member.name }}</text>
        </view>
      </view>
    </view>

    <!-- 拼车信息区域 -->
    <!-- 地点信息板块 -->
    <view class="info-block">
      <view class="block-title">行程信息</view>
      <view class="location-info">
        <view class="location-item">
          <text class="label">出发地点：</text>
          <text class="value">{{ rideInfo.startLocation }}</text>
        </view>
        <view class="location-item">
          <text class="label">目的地：</text>
          <text class="value">{{ rideInfo.endLocation }}</text>
        </view>
        <button class="map-btn" @tap="showMap">去看地图</button>
      </view>
    </view>

    <!-- 时间信息板块 -->
    <view class="info-block">
      <view class="block-title">时间安排</view>
      <view class="time-info">
        <view class="time-item">
          <text class="label">出发日期：</text>
          <text class="value">{{ rideInfo.date }}</text>
        </view>
        <view class="time-item">
          <text class="label">出发时间：</text>
          <text class="value">{{ rideInfo.time }}</text>
        </view>
        <view class="time-item">
          <text class="label">弹性时间：</text>
          <text class="value">{{ rideInfo.flexTime }}</text>
        </view>
      </view>
    </view>

    <!-- 人数价格板块 -->
    <view class="info-block">
      <view class="block-title">拼车详情</view>
      <view class="price-info">
        <view class="price-item">
          <text class="label">每人费用：</text>
          <text class="price-value">¥{{ rideInfo.price }}</text>
        </view>
        <view class="price-item">
          <text class="label">限载人数：</text>
          <text class="value">{{ rideInfo.maxPassengers }}人</text>
        </view>
        <view class="price-item">
          <text class="label">已付人数：</text>
          <text class="value">{{ rideInfo.paidCount }}人</text>
        </view>
        <view class="price-item">
          <text class="label">发车人数：</text>
          <text class="value">{{ rideInfo.minPassengers }}人</text>
        </view>
        <view class="discount-info" v-if="rideInfo.paidCount >= 3">
          <text class="discount-text">* 已达到3人，每人可优惠¥5</text>
        </view>
      </view>
    </view>

    <!-- 备注板块 -->
    <view class="info-block">
      <view class="block-title">群公告</view>
      <view class="notes-content">
        {{ rideInfo.notes }}
      </view>
    </view>

    <!-- 评价与反馈板块 -->
    <view class="info-block">
      <view class="block-title">评价与反馈</view>
      <button class="feedback-btn" @tap="showFeedback">填写反馈</button>
    </view>

    <!-- 底部按钮 -->
    <view class="bottom-buttons">
      <button
        :class="['join-btn', isJoined ? 'disabled' : '']"
        @tap="joinGroup"
        :disabled="isJoined"
      >
        {{ isJoined ? "已拼" : "加群" }}
      </button>
      <button
        :class="['pay-btn', isPaid ? 'disabled' : '']"
        @tap="handlePayment"
        :disabled="isPaid"
      >
        {{ isPaid ? "已付" : "支付" }}
      </button>
    </view>

    <!-- 地图弹窗 -->
    <view class="map-popup" v-if="showMapPopup" @tap="hideMap">
      <view class="map-container">
        <!-- 这里放地图组件 -->
        <map class="map"></map>
      </view>
    </view>

    <!-- 反馈表单弹窗 -->
    <view class="feedback-popup" v-if="showFeedbackForm" @tap="hideFeedback">
      <view class="feedback-form" @tap.stop>
        <view class="form-header">
          <text>反馈表单</text>
          <text class="close-btn" @tap="hideFeedback">×</text>
        </view>
        <input
          type="text"
          v-model="feedback.content"
          placeholder="请输入您的反馈"
          class="feedback-input"
        />
        <button class="submit-btn" @tap="submitFeedback">提交反馈</button>
      </view>
    </view>
  </view>

  <view class="member-list-popup" v-if="showMemberList" @tap="hideMemberList">
    <view class="member-list-content" @tap.stop>
      <view class="member-list-header">
        <text class="close-btn" @tap="hideMemberList">×</text>
        <text class="header-title">群成员列表</text>
      </view>
      <scroll-view scroll-y class="member-list">
        <view
          class="member-list-item"
          v-for="(member, index) in groupMembers"
          :key="index"
        >
          <image :src="member.avatar" class="member-list-avatar"></image>
          <text class="member-list-name">{{ member.name }}</text>
          <text class="member-role" v-if="index === 0">群主</text>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      rideId: {},
      isJoined: false,
      isPaid: false,
      showMemberList: false, // Add this line to define showMemberList
      groupMembers: [
        { name: "张三", avatar: "/static/image/person1.png" },
        { name: "李四", avatar: "/static/image/person2.png" },
        { name: "王五", avatar: "/static/image/person3.png" },
        { name: "赵六", avatar: "/static/image/person4.png" },
      ],
      showMapPopup: false,
      showFeedbackForm: false,
      feedback: {
        content: "",
      },
      rideInfo: {
        startLocation: "上海大学",
        endLocation: "虹桥机场",
        date: "2024-01-20",
        time: "14:30",
        flexTime: "±15分钟",
        price: 50,
        maxPassengers: 4,
        paidCount: 2,
        minPassengers: 3,
        notes:
          "⭐⭐⭐⭐⭐各位拼车成员们，希望大家能准时到达集合地点，我们的有一定的弹性时间，但是过了弹性时间，我们会准时出发，不等人，错过的成员费用不予退还，您若有特殊情况请提前告知，谢谢您的配合！❤❤❤",
      },
    };
  },
  methods: {
    loadRideInfo(id) {
      // 这里可以调用API获取拼车信息
      console.log("加载拼车信息:", id);
    },
    handlePayment() {
      if (!this.isJoined) {
        uni.showToast({
          title: "请先加入群聊",
          icon: "none",
        });
        return;
      }
      // 这里添加支付逻辑
      uni.showToast({
        title: "支付成功",
        icon: "success",
      });
      this.isPaid = true;
    },
    joinGroup() {
      uni.showToast({
        title: "加入成功",
        icon: "success",
      });
      this.isJoined = true;
    },
    goBack() {
      // 返回前保存状态
      const pages = getCurrentPages();
      const prevPage = pages[pages.length - 2];
      if (prevPage) {
        // 更新上一页的数据
        prevPage.$vm.updateRideStatus &&
          prevPage.$vm.updateRideStatus(this.rideId, {
            isJoined: this.isJoined,
            isPaid: this.isPaid,
          });
      }
      uni.navigateBack();
    },
    showMap() {
      this.showMapPopup = true;
    },
    hideMap() {
      this.showMapPopup = false;
    },
    showFeedback() {
      this.showFeedbackForm = true;
    },
    hideFeedback() {
      this.showFeedbackForm = false;
    },
    submitFeedback() {
      // 处理反馈提交
      uni.showToast({
        title: "反馈提交成功",
        icon: "success",
      });
      this.hideFeedback();
    },
    showMoreMembers() {
      this.showMemberList = true;
    },
    hideMemberList() {
      this.showMemberList = false;
    },
  },
};
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20rpx;
}

.header {
  background: #fff;
  padding: 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  position: relative;
}

.back-button {
  position: absolute;
  left: 30rpx;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}

.back-icon {
  width: 40rpx;
  height: 40rpx;
}

.group-title {
  flex: 1;
  text-align: center;
  font-size: 36rpx;
  font-weight: bold;
}

.member-count {
  color: #666;
  font-size: 28rpx;
}

.members-section {
  background: #fff;
  padding: 30rpx;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.more-link {
  font-size: 28rpx;
  color: #333;
  text-decoration: underline;
  display: flex;
  align-items: center;
}

.arrow {
  margin-left: 8rpx;
}

.info-block {
  background: #fff;
  padding: 30rpx;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
}

.block-title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
  color: #067786;
}

.location-info,
.time-info,
.price-info {
  padding: 20rpx 0;
}

.location-item,
.time-item,
.price-item {
  display: flex;
  margin-bottom: 16rpx;
}

.map-btn,
.feedback-btn {
  background: #8e9fbd;
  color: #ffffff;
  font-weight: bold;
  font-size: 34rpx;
  padding: 4rpx 16rpx;
  border-radius: 8rpx;
  margin-top: 25rpx;
  width: auto;
}

.price-value {
  color: #ff6b6b;
  font-size: 32rpx;
  font-weight: bold;
}

.discount-info {
  margin-top: 16rpx;
  color: #ff6b6b;
  font-size: 26rpx;
}

.notes-content {
  padding: 20rpx;
  background: #f9f9f9;
  border-radius: 8rpx;
  font-size: 34rpx;
  color: #666;
}

.map-popup,
.feedback-popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.map-container {
  width: 90%;
  height: 70%;
  background: #fff;
  border-radius: 12rpx;
  overflow: hidden;
}

.map {
  width: 100%;
  height: 100%;
}

.feedback-form {
  width: 80%;
  background: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
}

.form-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.close-btn {
  font-size: 40rpx;
  color: #999;
}

.feedback-input {
  border: 2rpx solid #eee;
  padding: 20rpx;
  border-radius: 8rpx;
  margin-bottom: 30rpx;
}

.submit-btn {
  background: #28a745;
  color: #fff;
}
.members-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16rpx;
  padding: 16rpx 0;
}

.member-item {
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.member-avatar {
  width: 100rpx; /* 增加头像尺寸 */
  height: 100rpx; /* 增加头像尺寸 */
  border-radius: 50%;
  margin-bottom: 8rpx;
  border: 2rpx solid #eee;
}

.member-name {
  font-size: 24rpx; /* 增加名字字体大小 */
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.bottom-buttons {
  /* 移除 fixed 定位 */
  margin: 40rpx;
  display: flex;
  gap: 20rpx;
}

.join-btn,
.pay-btn {
  flex: 1;
  font-size: 32rpx;
  padding: 4rpx 6rpx;
  border-radius: 12rpx;
  color: #fff;
  transition: all 0.3s ease;
}

.join-btn {
  background: #28a745; /* 未加群时的绿色 */
}

.pay-btn {
  background: #dc3545; /* 未支付时的红色 */
}

.disabled {
  background: #cccccc !important; /* 已加群/已支付时的灰色 */
  opacity: 0.7;
  cursor: not-allowed;
}
</style>

<style scoped>
.member-list-popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.member-list-content {
  width: 90%;
  height: 80%;
  background: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.member-list-header {
  padding: 30rpx;
  display: flex;
  align-items: center;
  border-bottom: 2rpx solid #eee;
  position: relative;
}

.header-title {
  flex: 1;
  text-align: center;
  font-size: 36rpx;
  font-weight: bold;
}

.close-btn {
  position: absolute;
  left: 30rpx;
  font-size: 40rpx;
  color: #999;
}

.member-list {
  flex: 1;
  padding: 20rpx;
}

.member-list-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  border-bottom: 2rpx solid #f5f5f5;
}

.member-list-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin-right: 20rpx;
}

.member-list-name {
  flex: 1;
  font-size: 32rpx;
  color: #333;
}

.member-role {
  font-size: 30rpx;
  color: #28a745;
  margin-right: 10%;
  /* background-color: #333; */
}
</style>
