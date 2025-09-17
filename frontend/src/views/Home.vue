<template>
  <div class="home">
    <div class="welcome-section">
      <h1>欢迎来到 CTC 系统</h1>
      <p v-if="!userStore.isLoggedIn">请登录以访问完整功能</p>
      <p v-else>欢迎回来，{{ userStore.user?.username }}！</p>
    </div>
    
    <div class="content-section">
      <h2>系统概述</h2>
      <p>本系统基于现代化的技术栈构建，提供稳定可靠的服务。</p>
      
      <div class="info-cards">
        <div class="info-card">
          <h3>快速开始</h3>
          <p v-if="!userStore.isLoggedIn">请先注册或登录账户</p>
          <p v-else>点击左侧导航菜单开始使用系统功能</p>
        </div>
        
        <div class="info-card">
          <h3>技术支持</h3>
          <p>如有问题，请查看帮助页面或联系技术支持</p>
        </div>
      </div>
      
      <!-- 未登录用户的操作按钮 -->
      <div v-if="!userStore.isLoggedIn" class="auth-actions">
        <el-button type="primary" @click="goToLogin">登录</el-button>
        <el-button type="success" @click="goToRegister">注册</el-button>
      </div>
      
      <!-- 已登录用户的操作按钮 -->
      <div v-else class="user-actions">
        <el-button type="primary" @click="goToDashboard">进入仪表板</el-button>
        <el-button @click="goToProfile">个人资料</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 导航方法
const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const goToDashboard = () => {
  router.push('/dashboard')
}

const goToProfile = () => {
  // TODO: 实现个人资料页面
  console.log('跳转到个人资料页面')
}

onMounted(() => {
  // 如果用户已登录，尝试获取用户信息
  if (localStorage.getItem('access_token') && !userStore.isLoggedIn) {
    userStore.fetchUserInfo().catch(() => {
      // 如果获取用户信息失败，清除token
      userStore.clearUser()
    })
  }
})
</script>

<style scoped>
.home {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-section h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.welcome-section p {
  color: #7f8c8d;
  font-size: 1.2rem;
  line-height: 1.6;
}

.content-section {
  margin-bottom: 40px;
}

.content-section h2 {
  color: #34495e;
  font-size: 1.8rem;
  margin-bottom: 16px;
}

.content-section p {
  color: #5d6d7e;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 30px;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.info-card {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 8px;
  border-left: 4px solid #3498db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info-card h3 {
  color: #2c3e50;
  font-size: 1.3rem;
  margin-bottom: 12px;
}

.info-card p {
  color: #5d6d7e;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}

.auth-actions, .user-actions {
  margin-top: 30px;
  text-align: center;
}

.auth-actions .el-button, .user-actions .el-button {
  margin: 0 10px;
  min-width: 120px;
}

@media (max-width: 768px) {
  .home {
    padding: 20px 15px;
  }
  
  .welcome-section h1 {
    font-size: 2rem;
  }
  
  .info-cards {
    grid-template-columns: 1fr;
  }
  
  .auth-actions .el-button, .user-actions .el-button {
    margin: 5px;
    min-width: 100px;
  }
}
</style>
