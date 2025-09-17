<template>
  <header id="header">
    <ul class="nav navbar-nav navbar-left">
      <li class="toggle-navigation toggle-left">
        <button class="sidebar-toggle" @click="toggleSidebar">
          <el-icon>
            <ArrowLeft v-if="!sidebarCollapsed" />
            <ArrowRight v-else />
          </el-icon>
        </button>
      </li>
      <li class="hidden-xs hidden-sm">
        <el-input
          v-model="searchText"
          placeholder="搜索项目..."
          class="search-input"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button @click="handleSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </li>
    </ul>
    
    <ul class="nav navbar-nav navbar-right">
      <li class="dropdown profile hidden-xs" v-if="userStore.isLoggedIn">
        <el-dropdown @command="handleCommand">
          <span class="meta">
            <el-avatar :size="32" :src="userStore.user?.avatar" class="user-avatar">
              {{ userStore.user?.username?.charAt(0).toUpperCase() }}
            </el-avatar>
            <span class="text">{{ userStore.user?.username || '用户' }}</span>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>
                个人资料
              </el-dropdown-item>
              <el-dropdown-item command="settings">
                <el-icon><Setting /></el-icon>
                账户设置
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </li>
      <li v-else class="login-link">
        <el-button type="primary" @click="goToLogin">登录</el-button>
      </li>
      <li class="toggle-fullscreen hidden-xs">
        <button type="button" class="btn btn-default expand" @click="toggleFullscreen">
          <el-icon><FullScreen /></el-icon>
        </button>
      </li>
    </ul>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const searchText = ref('')

const props = defineProps<{
  sidebarCollapsed: boolean
}>()

const emit = defineEmits<{
  toggleSidebar: []
  toggleProfile: []
}>()

const toggleSidebar = () => {
  emit('toggleSidebar')
}

const toggleProfile = () => {
  emit('toggleProfile')
}

const handleSearch = () => {
  // TODO: 实现搜索功能
  // console.log('搜索:', searchText.value)
}

const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm(
          '确定要退出登录吗？',
          '确认退出',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        await userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch (error) {
        // 用户取消
      }
      break
  }
}

const goToLogin = () => {
  router.push('/login')
}

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}
</script>

<style scoped>
#header {
  position: fixed;
  top: 0;
  left: 202px;
  right: 0;
  height: 50px;
  background: #fff;
  border-bottom: 1px solid #e5e5e5;
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: left 0.3s ease;
}


.nav {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar-left {
  flex: 1;
}

.navbar-right {
  gap: 15px;
}

.nav li {
  margin-right: 15px;
}

.sidebar-toggle {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.sidebar-toggle:hover {
  background-color: #f5f5f5;
}

.sidebar-toggle .el-icon {
  transition: transform 0.3s ease;
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.arrow-rotated {
  transform: rotate(180deg);
}

.btn {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:hover {
  background-color: #f5f5f5;
}

.search-input {
  width: 300px;
}

.meta {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.meta:hover {
  background-color: #f5f5f5;
}


.text {
  margin-right: 8px;
  color: #2c3e50;
  font-weight: 500;
}

.user-avatar {
  margin-right: 8px;
}

.login-link {
  margin-right: 15px;
}


.hidden-xs {
  display: block;
}

@media (max-width: 768px) {
  .hidden-xs {
    display: none;
  }
  
  .hidden-sm {
    display: none;
  }
  
  #header {
    left: 0;
  }
  
  .search-input {
    width: 200px;
  }
}
</style>
