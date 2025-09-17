<template>
  <div class="help">
    <!-- 页面头部 -->
    <div class="pageheader">
      <h1>帮助中心</h1>
      <p class="description">获取使用 CTC 通用网页系统模板的帮助信息</p>
      <div class="breadcrumb-wrapper hidden-xs">
        <span class="label">当前位置:</span>
        <ol class="breadcrumb">
          <li><router-link to="/">仪表板</router-link></li>
          <li class="active">帮助</li>
        </ol>
      </div>
    </div>

    <!-- 主要内容 -->
    <section id="main-content" class="animated fadeInUp">
      <div class="row">
        <div class="col-md-12">
          <el-card class="help-card">
            <template #header>
              <div class="card-header">
                <span>使用指南</span>
              </div>
            </template>
            <div class="help-content">
              <div class="help-section">
                <h3>快速开始</h3>
                <div class="help-item">
                  <h4>1. 系统登录</h4>
                  <p>使用管理员账户登录系统，默认用户名和密码请咨询系统管理员。</p>
                </div>
                
                <div class="help-item">
                  <h4>2. 导航菜单</h4>
                  <p>左侧导航菜单包含系统的主要功能模块，点击菜单项可以展开子菜单。</p>
                </div>
                
                <div class="help-item">
                  <h4>3. 仪表板</h4>
                  <p>仪表板显示系统的主要统计信息和图表，帮助您快速了解系统状态。</p>
                </div>
              </div>

              <div class="help-section">
                <h3>功能说明</h3>
                <div class="help-item">
                  <h4>UI组件</h4>
                  <p>提供丰富的用户界面组件，包括按钮、表单、表格、图表等，帮助您快速构建用户界面。</p>
                </div>
                
                <div class="help-item">
                  <h4>邮件系统</h4>
                  <p>内置邮件功能，支持发送和接收邮件，方便系统内部沟通。</p>
                </div>
                
                <div class="help-item">
                  <h4>地图功能</h4>
                  <p>集成地图服务，支持谷歌地图和矢量地图，可用于位置展示和地理信息管理。</p>
                </div>
              </div>

              <div class="help-section">
                <h3>常见问题</h3>
                <div class="faq-list">
                  <div class="faq-item">
                    <h4>Q: 如何修改系统配置？</h4>
                    <p>A: 系统配置可以通过管理后台进行修改，或者直接编辑配置文件。建议在修改前备份原始配置。</p>
                  </div>
                  
                  <div class="faq-item">
                    <h4>Q: 忘记密码怎么办？</h4>
                    <p>A: 请联系系统管理员重置密码，或者使用密码重置功能（如果已启用）。</p>
                  </div>
                  
                  <div class="faq-item">
                    <h4>Q: 系统支持哪些浏览器？</h4>
                    <p>A: 系统支持现代浏览器，包括Chrome、Firefox、Safari、Edge等。建议使用最新版本以获得最佳体验。</p>
                  </div>
                  
                  <div class="faq-item">
                    <h4>Q: 如何备份数据？</h4>
                    <p>A: 系统提供自动备份功能，也可以手动导出数据。建议定期备份重要数据。</p>
                  </div>
                </div>
              </div>

              <div class="help-section">
                <h3>技术支持</h3>
                <div class="support-info">
                  <div class="contact-item">
                    <h4>📧 邮箱支持</h4>
                    <p>support@ctc.com</p>
                  </div>
                  
                  <div class="contact-item">
                    <h4>📞 电话支持</h4>
                    <p>400-123-4567</p>
                  </div>
                  
                  <div class="contact-item">
                    <h4>🕒 服务时间</h4>
                    <p>周一至周五 9:00-18:00</p>
                  </div>
                  
                  <div class="contact-item">
                    <h4>📚 文档中心</h4>
                    <p><a href="#" target="_blank">查看完整文档</a></p>
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
import { onMounted } from 'vue'

onMounted(() => {
  console.log('Help page mounted')
})
</script>

<style scoped>
.help {
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

.help-card {
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

.help-content {
  padding: 20px 0;
}

.help-section {
  margin-bottom: 40px;
}

.help-section:last-child {
  margin-bottom: 0;
}

.help-section h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 22px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

.help-item {
  margin-bottom: 25px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.help-item:last-child {
  margin-bottom: 0;
}

.help-item h4 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 16px;
}

.help-item p {
  line-height: 1.6;
  color: #666;
  margin: 0;
}

.faq-list {
  display: grid;
  gap: 15px;
}

.faq-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #67c23a;
}

.faq-item h4 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 16px;
}

.faq-item p {
  line-height: 1.6;
  color: #666;
  margin: 0;
}

.support-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.contact-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #e6a23c;
  text-align: center;
}

.contact-item h4 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 16px;
}

.contact-item p {
  color: #666;
  margin: 0;
}

.contact-item a {
  color: #3498db;
  text-decoration: none;
}

.contact-item a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .support-info {
    grid-template-columns: 1fr;
  }
  
  .help {
    padding: 10px 15px;
  }
}
</style>
