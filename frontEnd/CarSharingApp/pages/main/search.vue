<template>
    <view class="container">
        <!-- 搜索框 -->
        <view class="search-bar-container">
            <view class="search-input-wrapper">
                <view 
                    class="icon-dot" 
                    :class="{ 'green-dot': searchType === 'startPoint', 'red-dot': searchType === 'endPoint' }"
                ></view>
                <input 
                    ref="searchInput"
                    class="search-input" 
                    type="text" 
                    v-model="searchQuery" 
                    :placeholder="placeholderText"
                    @confirm="handleSearchConfirm" />
            </view>
            <text class="cancel-btn" @click="handleCancel">取消</text>
        </view>

        <!-- 快捷地址 -->
        <view v-if="!showResults" class="shortcuts">
            <view class="shortcut-item home-item" @click="selectShortcut('home')">
                <image class="icon" src="/static/image/icon_home.png"></image>
                <text class="item-text">
                    <text class="shortcut-label">家</text>
                    <text class="shortcut-desc">同济大学嘉定校区</text>
                </text>
            </view>
        
            <!-- 分隔线 -->
            <view class="divider"></view>
        
            <view class="shortcut-item school-item" @click="selectShortcut('school')">
                <image class="icon" src="/static/image/icon_school.png"></image>
                <text class="item-text">
                    <text class="shortcut-label">学校</text>
                    <text class="shortcut-desc">同济大学四平路校区</text>
                </text>
            </view>
        </view>
        
        <!-- 历史记录 -->
        <view v-if="!searchQuery && !showResults" class="history">
            <view v-for="(item, index) in historyList" :key="index" class="history-item" @click="selectHistory(item)">
                <image class="icon" src="/static/image/icon_location.png"></image>
                <text class="item-text">{{ item.name }}</text>
            </view>
        </view>
        
        <!-- 搜索结果 -->
        <view v-if="showResults" class="results">
            <view v-for="(result, index) in searchResults" :key="index" class="result-item" @click="selectResult(result)">
                <image class="icon" src="/static/image/icon_location.png"></image>
                <text class="item-text">{{ result.name }}</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            searchType: 'startPoint',
            placeholderText: '',
            searchQuery: '', // 初始为空，不会显示内容
            showResults: false,
            searchResults: [],
            historyList: [
                { name: '上海虹桥国际机场' },
                { name: '上海浦东机场' },
                { name: '上海国际赛车场' },
                { name: '上海南翔印象城' }
            ]
        };
    },
    onLoad(options) {
        this.searchType = options.searchType || 'startPoint';
        this.placeholderText = this.searchType === 'startPoint' ? '请输入起点' : '请输入终点';
		const app = getApp();
		this.api_key = app.globalData.api_key;
    },
    methods: {
        // 点击取消按钮返回首页
        handleCancel() {
            uni.navigateBack();
        },

        selectShortcut(type) {
            let name = type === 'home' ? '同济大学嘉定校区' : '同济大学四平路校区';
            this.searchQuery = name;
            this.$nextTick(() => {
                this.handleSearchConfirm();     // 触发搜索
            });
        },
        
        selectHistory(item) {
            this.searchQuery = item.name;
            this.$nextTick(() => {
                this.handleSearchConfirm();     // 触发搜索
            });
        },

        // 搜索框回车事件
        async handleSearchConfirm() {
            const query = this.searchQuery.trim();
            if (!query) return;

            const geocodeUrl = `https://restapi.amap.com/v3/geocode/geo?key=${this.api_key}&address=${encodeURIComponent(query)}`;

            uni.request({
                url: geocodeUrl,
                method: 'GET',
                success: (res) => {
                    if (res.data.status === "1" && res.data.geocodes && res.data.geocodes.length > 0) {
                        const location = res.data.geocodes[0].location.split(',');
                        const lng = parseFloat(location[0]);
                        const lat = parseFloat(location[1]);

                        const addressName = res.data.geocodes[0].formatted_address || query;

                        this.searchResults = [{
                            name: addressName,
                            lng,
                            lat
                        }];
                        this.showResults = true;
                    } else {
                        uni.showToast({ title: '未找到相关地点', icon: 'none' });
                    }
                },
                fail: (err) => {
                    uni.showToast({ title: '网络请求失败', icon: 'none' });
                    console.error('地理编码请求失败:', err);
                }
            });
        },
	    selectResult(result) {
	        uni.$emit('updateLocation', {
	            type: this.searchType,
	            location: result.name,
	            lngLat: [result.lng, result.lat]
	        });
	
	        uni.navigateBack(); // 返回首页
	    }
    }
};
</script>

<style>
.container {
    background-color: #f5f5f5;
    padding: 20rpx;
    height: 100vh;
    box-sizing: border-box;
}

.icon {
    width: 40rpx;
    height: 40rpx;
    vertical-align: middle;
    margin-right: 30rpx;
}

.item-text {
    font-size: 28rpx;
    line-height: 36rpx;
    white-space: normal;
    text-align: left; 
    word-break: break-all;
}

.search-bar-container {
    display: flex;
    align-items: center;
	margin-top: 20rpx;
    margin-bottom: 20rpx;
}

.search-input-wrapper {
    position: relative;
    flex: 1;
    height: 70rpx;
    border-radius: 40rpx;
    background-color: #fff;
    padding-left: 50rpx; 
}

.icon-dot {
    position: absolute;
    left: 25rpx;
    top: 50%;
    transform: translateY(-50%);
    width: 20rpx;
    height: 20rpx;
    border-radius: 50%;
    z-index: 1;
}

.green-dot {
    background-color: #00c800;
}

.red-dot {
    background-color: #e60000;
}

.search-input {
    height: 100%;
    font-size: 30rpx;
    padding: 0 20rpx;
    box-sizing: border-box;
}

.cancel-btn {
    color: #007AFF;
    font-size: 30rpx;
    margin-left: 20rpx;
}

.divider {
    width: 3rpx;
    height: 100rpx;
    background-color: #bbb;
	margin-top: 10rpx;
}

.shortcuts {
    display: flex;
    justify-content: space-between;
    margin-top: 20rpx;
    background-color: #fff; 
    border-radius: 20rpx;
    padding: 15rpx 20rpx;
}

.shortcut-item {
    display: flex;
    align-items: center;
    padding: 20rpx 0;
}

.shortcut-label {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.shortcut-desc {
    font-size: 24rpx;
    color: #999;
}

.history {
    margin-top: 30rpx;
    background-color: #fff;
    border-radius: 20rpx;
    padding: 20rpx;
}

.history-item {
    display: flex;
    align-items: flex-start;
    padding: 35rpx  10rpx;
	font-size: 28rpx;
    border-bottom: 2rpx solid #eee;
}


.history-item:last-child {
    border-bottom: none;
}

.results {
    margin-top: 30rpx;
    background-color: #fff;
    border-radius: 20rpx;
    padding: 20rpx;
}

.result-item {
    display: flex;
    align-items: flex-start;
    padding: 20rpx 0;
    border-bottom: 1rpx solid #eee;
}

.result-item:last-child {
    border-bottom: none;
}
</style>