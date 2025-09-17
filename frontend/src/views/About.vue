<template>
  <div class="about">
    <!-- 页面头部 -->
    <div class="pageheader">
      <h1>关于系统</h1>
      <p class="description">了解 CTC 通用网页系统模板的详细信息</p>
      <div class="breadcrumb-wrapper hidden-xs">
        <span class="label">当前位置:</span>
        <ol class="breadcrumb">
          <li><router-link to="/">仪表板</router-link></li>
          <li class="active">关于</li>
        </ol>
      </div>
    </div>

    <!-- 主要内容 -->
    <section id="main-content" class="animated fadeInUp">
      <div class="row">
        <div class="col-md-12">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>系统信息</span>
              </div>
            </template>
            <div class="info-content">
              <div class="info-item">
                <h3>CTC 通用网页系统模板</h3>
                <p>这是一个基于现代化技术栈构建的通用网页系统模板，旨在为开发者提供一个快速搭建企业级应用的解决方案。</p>
              </div>

              <div class="info-item">
                <h4>技术栈</h4>
                <div class="tech-stack">
                  <div class="tech-category">
                    <h5>前端技术</h5>
                    <ul>
                      <li>Vue 3 - 渐进式JavaScript框架</li>
                      <li>Element Plus - Vue 3 UI组件库</li>
                      <li>Axios - HTTP客户端</li>
                      <li>ECharts - 数据可视化图表库</li>
                      <li>Vue Router - 官方路由管理器</li>
                      <li>Pinia - 状态管理库</li>
                    </ul>
                  </div>
                  
                  <div class="tech-category">
                    <h5>后端技术</h5>
                    <ul>
                      <li>Django 4.x - Python Web框架</li>
                      <li>Django REST Framework - API开发框架</li>
                      <li>SimpleJWT - JWT认证</li>
                      <li>Celery - 分布式任务队列</li>
                      <li>Redis - 缓存和消息代理</li>
                    </ul>
                  </div>
                  
                  <div class="tech-category">
                    <h5>数据存储</h5>
                    <ul>
                      <li>MySQL 8.0 - 关系型数据库</li>
                      <li>Redis - 缓存数据库</li>
                    </ul>
                  </div>
                </div>
              </div>

              <div class="info-item">
                <h4>系统特性</h4>
                <ul class="feature-list">
                  <li>响应式设计，支持多设备访问</li>
                  <li>模块化架构，易于扩展和维护</li>
                  <li>完整的用户认证和权限管理</li>
                  <li>丰富的UI组件和交互效果</li>
                  <li>数据可视化图表支持</li>
                  <li>异步任务处理能力</li>
                  <li>容器化部署支持</li>
                </ul>
              </div>

              <div class="info-item">
                <h4>版本信息</h4>
                <div class="version-info">
                  <p><strong>当前版本：</strong>1.0.0</p>
                  <p><strong>发布日期：</strong>2024年</p>
                  <p><strong>开发团队：</strong>CTC开发团队</p>
                  <p><strong>技术支持：</strong>support@ctc.com</p>
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
import { onMounted } from 'vue'

onMounted(() => {
  console.log('About page mounted')
})
</script>

<style scoped>
.about {
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

.breadcrumb li a {
  color: #3498db;
  text-decoration: none;
}

.breadcrumb li.active {
  color: #3498db;
}

.breadcrumb li:not(:last-child)::after {
  content: " / ";
  color: #999;
}

.info-card {
  margin-bottom: 15px;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #2c3e50;
}

.info-content {
  padding: 20px 0;
}

.info-item {
  margin-bottom: 30px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-item h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 24px;
}

.info-item h4 {
  color: #34495e;
  margin-bottom: 15px;
  font-size: 18px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 5px;
}

.info-item h5 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 16px;
}

.info-item p {
  line-height: 1.6;
  color: #666;
  margin-bottom: 15px;
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 15px;
}

.tech-category {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.tech-category ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-category li {
  padding: 8px 0;
  border-bottom: 1px solid #e9ecef;
  color: #666;
}

.tech-category li:last-child {
  border-bottom: none;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  padding: 10px 0;
  padding-left: 25px;
  position: relative;
  color: #666;
  line-height: 1.6;
}

.feature-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #67c23a;
  font-weight: bold;
}

.version-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #67c23a;
}

.version-info p {
  margin: 8px 0;
  color: #666;
}

.version-info strong {
  color: #2c3e50;
}

@media (max-width: 768px) {
  .tech-stack {
    grid-template-columns: 1fr;
  }
  
  .about {
    padding: 10px 15px;
  }
}
</style>