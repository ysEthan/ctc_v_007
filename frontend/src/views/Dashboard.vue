<template>
  <div class="dashboard">
    <!-- 页面头部 -->
    <div class="pageheader">
      <h1>仪表板</h1>
      <p class="description">欢迎使用 CTC 通用网页系统模板</p>
      <div class="breadcrumb-wrapper hidden-xs">
        <span class="label">当前位置:</span>
        <ol class="breadcrumb">
          <li class="active">仪表板</li>
        </ol>
      </div>
    </div>

    <!-- 主要内容 -->
    <section id="main-content" class="animated fadeInUp">
      <!-- 统计卡片 -->
      <div class="row">
        <div class="col-md-12 col-lg-6">
          <div class="row">
            <div class="col-md-6">
              <el-card class="stat-card success">
                <div class="stat-content">
                  <el-icon class="stat-icon"><TrendCharts /></el-icon>
                  <div class="stat-info">
                    <span class="total">¥3,200</span>
                    <span class="title">收入</span>
                  </div>
                </div>
              </el-card>
            </div>
            <div class="col-md-6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <el-icon class="stat-icon"><Service /></el-icon>
                  <div class="stat-info">
                    <span class="total">1,230</span>
                    <span class="title">支持</span>
                  </div>
                </div>
              </el-card>
            </div>
            <div class="col-md-6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <el-icon class="stat-icon"><Message /></el-icon>
                  <div class="stat-info">
                    <span class="total">1,680</span>
                    <span class="title">消息</span>
                  </div>
                </div>
              </el-card>
            </div>
            <div class="col-md-6">
              <el-card class="stat-card info">
                <div class="stat-content">
                  <el-icon class="stat-icon"><User /></el-icon>
                  <div class="stat-info">
                    <span class="total">12,680</span>
                    <span class="title">注册用户</span>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </div>

        <!-- 浏览器统计 -->
        <div class="col-xs-12 col-sm-6 col-md-6 col-lg-3">
          <el-card class="chart-card">
            <template #header>
              <h3 class="panel-title">浏览器统计</h3>
            </template>
            <div class="chart-content">
              <div class="row">
                <div class="col-xs-6">
                  <ul class="browser-list">
                    <li><el-icon class="success-color"><CircleFilled /></el-icon> Chrome</li>
                    <li><el-icon class="primary-color"><CircleFilled /></el-icon> IE</li>
                    <li><el-icon class="warning-color"><CircleFilled /></el-icon> Safari</li>
                    <li><el-icon class="info-color"><CircleFilled /></el-icon> Firefox</li>
                    <li><el-icon class="default-color"><CircleFilled /></el-icon> 其他</li>
                  </ul>
                </div>
                <div class="col-xs-6">
                  <div class="chart-container">
                    <div ref="browserChart" class="chart-placeholder"></div>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 月度目标 -->
        <div class="col-xs-12 col-sm-6 col-md-6 col-lg-3">
          <el-card class="gauge-card">
            <template #header>
              <h3 class="panel-title">月度目标</h3>
            </template>
            <div class="gauge-content">
              <div class="gauge-wrapper">
                <div ref="gaugeChart" class="gauge-placeholder"></div>
              </div>
              <div class="goal-wrapper">
                <span class="gauge-value">¥3,200</span>
                <span class="goal-value">目标: ¥5,000</span>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 服务器统计 -->
      <div class="row">
        <div class="col-md-12 col-lg-12">
          <el-card class="server-stats-card">
            <template #header>
              <h3 class="panel-title">服务器统计</h3>
              <div class="reportdate">
                <el-icon><Calendar /></el-icon>
                <span>1月1日 - 6月30日</span>
              </div>
            </template>
            <div class="server-stats-content">
              <div class="row">
                <div class="col-md-12 col-lg-4">
                  <ul class="progress-list">
                    <li>
                      <span class="text-left">网络使用率</span>
                      <el-progress :percentage="65" color="#67c23a" />
                    </li>
                    <li>
                      <span class="text-left">CPU负载</span>
                      <el-progress :percentage="40" color="#409eff" />
                    </li>
                  </ul>
                  <p class="description-text">
                    系统运行正常，各项指标均在正常范围内。建议定期监控系统性能。
                  </p>
                </div>
                <div class="col-md-12 col-lg-8">
                  <div class="row">
                    <div class="col-md-12 col-lg-6">
                      <div class="chart-container">
                        <div ref="lineChart" class="chart-placeholder"></div>
                      </div>
                    </div>
                    <div class="col-md-12 col-lg-6">
                      <div class="chart-container">
                        <div ref="barChart" class="chart-placeholder"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 聊天和日历 -->
      <div class="row">
        <div class="col-xs-12 col-sm-12 col-md-12 col-lg-4">
          <el-card class="chat-widget">
            <template #header>
              <h3 class="panel-title">聊天</h3>
            </template>
            <div class="chat-content">
              <div class="chat-message">
                <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
                <div class="message-content">
                  <p>你好！系统运行正常，有什么需要帮助的吗？</p>
                </div>
              </div>
              <div class="chat-message user">
                <div class="message-content">
                  <p>谢谢，系统运行得很好！</p>
                </div>
                <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
              </div>
            </div>
            <div class="chat-input">
              <el-input
                v-model="chatMessage"
                placeholder="说点什么..."
                @keyup.enter="sendMessage"
              >
                <template #append>
                  <el-button @click="sendMessage">发送</el-button>
                </template>
              </el-input>
            </div>
          </el-card>
        </div>

        <div class="col-xs-12 col-sm-12 col-md-6 col-lg-4">
          <el-card class="calendar-widget">
            <template #header>
              <h3 class="panel-title">日历</h3>
            </template>
            <div class="calendar-content">
              <el-calendar v-model="calendarValue" />
            </div>
          </el-card>
        </div>

        <div class="col-xs-12 col-sm-12 col-md-6 col-lg-4">
          <el-card class="weather-widget">
            <template #header>
              <h3 class="panel-title">天气</h3>
            </template>
            <div class="weather-content">
              <div class="row">
                <div class="col-xs-6">
                  <h3 class="text-center title">今天</h3>
                  <div class="text-center">
                    <el-icon class="weather-icon"><Sunny /></el-icon>
                    <div class="temp">22°C</div>
                  </div>
                </div>
                <div class="col-xs-6">
                  <h3 class="text-center title">今晚</h3>
                  <div class="text-center">
                    <el-icon class="weather-icon"><Moon /></el-icon>
                    <div class="temp">15°C</div>
                  </div>
                </div>
              </div>
            </div>
            <div class="weather-footer">
              <div class="row">
                <div class="col-xs-6 col-sm-6 col-md-2" v-for="day in weatherDays" :key="day.day">
                  <h6 class="text-center small-thin uppercase">{{ day.day }}</h6>
                  <div class="text-center">
                    <el-icon class="weather-icon-small">{{ day.icon }}</el-icon>
                    <span>{{ day.temp }}°C</span>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const chatMessage = ref('')
const calendarValue = ref(new Date())

const weatherDays = ref([
  { day: '周一', icon: 'Cloudy', temp: 18 },
  { day: '周二', icon: 'Rainy', temp: 16 },
  { day: '周三', icon: 'Sunny', temp: 20 },
  { day: '周四', icon: 'Cloudy', temp: 19 },
  { day: '周五', icon: 'Sunny', temp: 23 },
  { day: '周六', icon: 'Rainy', temp: 17 }
])

const browserChart = ref<HTMLElement>()
const gaugeChart = ref<HTMLElement>()
const lineChart = ref<HTMLElement>()
const barChart = ref<HTMLElement>()

const sendMessage = () => {
  if (chatMessage.value.trim()) {
    console.log('发送消息:', chatMessage.value)
    chatMessage.value = ''
  }
}

const initCharts = () => {
  // 浏览器统计饼图
  if (browserChart.value) {
    const chart = echarts.init(browserChart.value)
    chart.setOption({
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          { value: 35, name: 'Chrome' },
          { value: 25, name: 'IE' },
          { value: 20, name: 'Safari' },
          { value: 15, name: 'Firefox' },
          { value: 5, name: '其他' }
        ]
      }]
    })
  }

  // 仪表盘
  if (gaugeChart.value) {
    const chart = echarts.init(gaugeChart.value)
    chart.setOption({
      series: [{
        type: 'gauge',
        progress: {
          show: true
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}%'
        },
        data: [{
          value: 64,
          name: '完成度'
        }]
      }]
    })
  }

  // 折线图
  if (lineChart.value) {
    const chart = echarts.init(lineChart.value)
    chart.setOption({
      xAxis: {
        type: 'category',
        data: ['1月', '2月', '3月', '4月', '5月', '6月']
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        data: [120, 200, 150, 80, 70, 110],
        type: 'line',
        smooth: true
      }]
    })
  }

  // 柱状图
  if (barChart.value) {
    const chart = echarts.init(barChart.value)
    chart.setOption({
      xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        data: [120, 200, 150, 80, 70, 110, 130],
        type: 'bar'
      }]
    })
  }
}

onMounted(() => {
  setTimeout(() => {
    initCharts()
  }, 100)
})
</script>

<style scoped>
.dashboard {
  padding: 15px 20px;
  min-height: calc(100vh - 110px);
}

.pageheader {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e5e5e5;
}

.pageheader h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #2c3e50;
}

.description {
  color: #666;
  margin: 0 0 15px 0;
}

.breadcrumb-wrapper {
  font-size: 12px;
  color: #999;
}

.breadcrumb {
  display: inline-block;
  list-style: none;
  padding: 0;
  margin: 0;
}

.breadcrumb li {
  display: inline;
}

.breadcrumb li.active {
  color: #3498db;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin: -10px;
}

.col-md-6, .col-md-12, .col-lg-3, .col-lg-4, .col-lg-6, .col-lg-8, .col-lg-12 {
  padding: 10px;
}

.col-md-6 { width: 50%; }
.col-md-12 { width: 100%; }
.col-lg-3 { width: 25%; }
.col-lg-4 { width: 33.333333%; }
.col-lg-6 { width: 50%; }
.col-lg-8 { width: 66.666667%; }
.col-lg-12 { width: 100%; }

.stat-card {
  margin-bottom: 15px;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-card.success {
  border-left: 4px solid #67c23a;
}

.stat-card.info {
  border-left: 4px solid #409eff;
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  font-size: 40px;
  margin-right: 20px;
  color: #3498db;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.total {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.title {
  font-size: 14px;
  color: #666;
}

.chart-card, .gauge-card, .server-stats-card {
  margin-bottom: 15px;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.panel-title {
  margin: 0;
  font-size: 16px;
  color: #2c3e50;
}

.reportdate {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
  font-size: 12px;
}

.browser-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.browser-list li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 12px;
}

.browser-list .el-icon {
  margin-right: 8px;
}

.success-color { color: #67c23a; }
.primary-color { color: #409eff; }
.warning-color { color: #e6a23c; }
.info-color { color: #909399; }
.default-color { color: #c0c4cc; }

.chart-placeholder, .gauge-placeholder {
  width: 100%;
  height: 120px;
}

.gauge-wrapper {
  text-align: center;
  margin-bottom: 20px;
}

.goal-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.gauge-value {
  font-size: 18px;
  font-weight: bold;
  color: #3498db;
}

.goal-value {
  font-size: 14px;
  color: #666;
}

.progress-list {
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
}

.progress-list li {
  margin-bottom: 15px;
}

.text-left {
  display: block;
  margin-bottom: 5px;
  font-size: 12px;
  color: #666;
}

.description-text {
  font-size: 12px;
  color: #666;
  line-height: 1.5;
  margin: 0;
}

.chat-widget, .calendar-widget, .weather-widget {
  margin-bottom: 15px;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chat-content {
  padding: 20px;
  max-height: 200px;
  overflow-y: auto;
}

.chat-message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.chat-message.user {
  justify-content: flex-end;
}

.message-content {
  background: #f5f5f5;
  padding: 10px 15px;
  border-radius: 10px;
  margin: 0 10px;
  max-width: 70%;
}

.message-content p {
  margin: 0;
  font-size: 14px;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #e5e5e5;
}

.calendar-content {
  padding: 20px;
}

.weather-content {
  padding: 20px;
}

.title {
  font-size: 14px;
  color: #666;
  margin: 0 0 10px 0;
}

.weather-icon {
  font-size: 40px;
  color: #f39c12;
  margin-bottom: 10px;
}

.temp {
  font-size: 18px;
  font-weight: bold;
  color: #2c3e50;
}

.weather-footer {
  padding: 20px;
  border-top: 1px solid #e5e5e5;
}

.weather-icon-small {
  font-size: 20px;
  color: #f39c12;
  margin-bottom: 5px;
}

.small-thin {
  font-size: 10px;
  font-weight: 300;
  margin: 0 0 5px 0;
}

.uppercase {
  text-transform: uppercase;
}

.text-center {
  text-align: center;
}

@media (max-width: 768px) {
  .dashboard {
    margin-left: 0;
  }
  
  .col-md-6, .col-lg-3, .col-lg-4, .col-lg-6, .col-lg-8 {
    width: 100%;
  }
}
</style>
