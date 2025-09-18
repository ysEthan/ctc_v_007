<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <div class="logo">
          <el-icon><Grid /></el-icon>
          <span>CTC</span>BOARD
        </div>
        <h2>用户登录</h2>
        <p>欢迎回来，请登录您的账户</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username_or_email">
          <el-input
            v-model="loginForm.username_or_email"
            placeholder="请输入用户名或邮箱"
            size="large"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            :prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <div class="login-options">
            <el-checkbox v-model="loginForm.remember_me">
              记住登录状态
            </el-checkbox>
            <el-link type="primary" @click="handleForgotPassword">
              忘记密码？
            </el-link>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <p>
          还没有账户？
          <el-link type="primary" @click="goToRegister">
            立即注册
          </el-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Lock, Grid } from '@element-plus/icons-vue'
import { authApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref()

// 加载状态
const loading = ref(false)

// 登录表单数据
const loginForm = reactive({
  username_or_email: '',
  password: '',
  remember_me: false
})

// 表单验证规则
const loginRules = {
  username_or_email: [
    { required: true, message: '请输入用户名或邮箱', trigger: 'blur' },
    { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 128, message: '密码长度在 6 到 128 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    const response = await authApi.login(loginForm)
    
    // 保存token和用户信息
    localStorage.setItem('access_token', response.access)
    localStorage.setItem('refresh_token', response.refresh)
    
    // 更新用户状态
    userStore.setUser(response.user)
    
    ElMessage.success('登录成功')
    
    // 跳转到首页或之前访问的页面
    const redirect = router.currentRoute.value.query.redirect as string
    router.push(redirect || '/dashboard')
    
  } catch (error: any) {
    console.error('登录失败:', error)
    
    // 处理具体的错误信息
    const errorData = error.response?.data
    let errorMessage = '登录失败，请检查用户名和密码'
    
    if (errorData) {
      // 处理字段特定的错误
      if (errorData.username_or_email) {
        errorMessage = errorData.username_or_email[0] || '用户名或邮箱错误'
      } else if (errorData.password) {
        errorMessage = errorData.password[0] || '密码错误'
      } else if (errorData.non_field_errors) {
        errorMessage = errorData.non_field_errors[0] || '登录失败'
      } else if (errorData.detail) {
        errorMessage = errorData.detail
      }
    }
    
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

// 忘记密码
const handleForgotPassword = () => {
  ElMessageBox.prompt('请输入您的邮箱地址', '重置密码', {
    confirmButtonText: '发送重置邮件',
    cancelButtonText: '取消',
    inputPattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    inputErrorMessage: '请输入有效的邮箱地址'
  }).then(async ({ value }) => {
    try {
      // 这里应该调用重置密码API
      ElMessage.success('重置密码邮件已发送，请查收邮箱')
    } catch (error) {
      ElMessage.error('发送失败，请稍后重试')
    }
  }).catch(() => {
    // 用户取消
  })
}

// 跳转到注册页面
const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 20px;
}

.logo .el-icon {
  margin-right: 8px;
  font-size: 28px;
}

.logo span {
  color: #3498db;
}

.login-header h2 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

.login-header p {
  margin: 0;
  color: #7f8c8d;
  font-size: 14px;
}

.login-form {
  margin-bottom: 20px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
}

.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.login-footer p {
  margin: 0;
  color: #7f8c8d;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-box {
    padding: 30px 20px;
  }
  
  .login-header h2 {
    font-size: 20px;
  }
  
  .logo {
    font-size: 20px;
  }
}

/* 动画效果 */
.login-box {
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
