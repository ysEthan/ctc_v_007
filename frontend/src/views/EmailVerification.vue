<template>
  <div class="verification-container">
    <div class="verification-box">
      <div class="verification-header">
        <div class="logo">
          <el-icon><Grid /></el-icon>
          <span>CTC</span>BOARD
        </div>
        <h2>邮箱验证</h2>
        <p>请查收您的邮箱并输入验证码</p>
      </div>
      
      <div class="email-info">
        <el-icon class="email-icon"><Message /></el-icon>
        <span>验证码已发送至：{{ email }}</span>
      </div>
      
      <el-form
        ref="verificationFormRef"
        :model="verificationForm"
        :rules="verificationRules"
        class="verification-form"
        @submit.prevent="handleVerification"
      >
        <el-form-item prop="verification_code">
          <el-input
            v-model="verificationForm.verification_code"
            placeholder="请输入6位验证码"
            size="large"
            maxlength="6"
            class="verification-input"
            @input="handleCodeInput"
            @keyup.enter="handleVerification"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="verification-button"
            :loading="loading"
            @click="handleVerification"
          >
            {{ loading ? '验证中...' : '验证邮箱' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="verification-footer">
        <div class="resend-section">
          <p>没有收到验证码？</p>
          <el-button
            type="text"
            :disabled="countdown > 0"
            @click="handleResend"
          >
            {{ countdown > 0 ? `${countdown}秒后重新发送` : '重新发送验证码' }}
          </el-button>
        </div>
        
        <div class="back-section">
          <el-button type="text" @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回登录
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Message, Grid, ArrowLeft } from '@element-plus/icons-vue'
import { authApi } from '@/api/auth'

const router = useRouter()
const route = useRoute()

// 表单引用
const verificationFormRef = ref()

// 加载状态
const loading = ref(false)

// 倒计时
const countdown = ref(0)
let countdownTimer: NodeJS.Timeout | null = null

// 邮箱地址
const email = ref('')

// 验证表单数据
const verificationForm = reactive({
  verification_code: ''
})

// 表单验证规则
const verificationRules = {
  verification_code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码必须是6位数字', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: '验证码只能是数字', trigger: 'blur' }
  ]
}

// 处理验证码输入
const handleCodeInput = (value: string) => {
  // 只允许输入数字
  verificationForm.verification_code = value.replace(/\D/g, '')
}

// 处理邮箱验证
const handleVerification = async () => {
  if (!verificationFormRef.value) return
  
  try {
    const valid = await verificationFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    await authApi.verifyEmail(verificationForm.verification_code)
    
    ElMessage.success('邮箱验证成功！')
    
    // 跳转到登录页面
    router.push('/login')
    
  } catch (error: any) {
    console.error('验证失败:', error)
    ElMessage.error(error.response?.data?.error || '验证失败，请检查验证码')
  } finally {
    loading.value = false
  }
}

// 重新发送验证码
const handleResend = async () => {
  try {
    await authApi.resendVerification({ email: email.value })
    
    ElMessage.success('验证码已重新发送')
    
    // 开始倒计时
    startCountdown()
    
  } catch (error: any) {
    console.error('重新发送失败:', error)
    ElMessage.error(error.response?.data?.detail || '发送失败，请稍后重试')
  }
}

// 开始倒计时
const startCountdown = () => {
  countdown.value = 60
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer!)
      countdownTimer = null
    }
  }, 1000)
}

// 返回登录
const goBack = () => {
  router.push('/login')
}

// 组件挂载时获取邮箱地址
onMounted(() => {
  email.value = route.query.email as string || ''
  if (!email.value) {
    ElMessage.warning('邮箱地址不存在，请重新注册')
    router.push('/register')
    return
  }
  
  // 开始倒计时
  startCountdown()
})

// 组件卸载时清理定时器
onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
.verification-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.verification-box {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.verification-header {
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

.verification-header h2 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

.verification-header p {
  margin: 0;
  color: #7f8c8d;
  font-size: 14px;
}

.email-info {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 30px;
  color: #495057;
  font-size: 14px;
}

.email-icon {
  margin-right: 8px;
  color: #3498db;
  font-size: 16px;
}

.verification-form {
  margin-bottom: 30px;
}

.verification-input {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  letter-spacing: 8px;
}

.verification-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
}

.verification-footer {
  text-align: center;
}

.resend-section {
  margin-bottom: 20px;
}

.resend-section p {
  margin: 0 0 10px 0;
  color: #7f8c8d;
  font-size: 14px;
}

.back-section {
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .verification-box {
    padding: 30px 20px;
  }
  
  .verification-header h2 {
    font-size: 20px;
  }
  
  .logo {
    font-size: 20px;
  }
  
  .verification-input {
    font-size: 20px;
    letter-spacing: 6px;
  }
}

/* 动画效果 */
.verification-box {
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

/* 验证码输入框特殊样式 */
:deep(.verification-input .el-input__inner) {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  letter-spacing: 8px;
  font-family: 'Courier New', monospace;
}

@media (max-width: 480px) {
  :deep(.verification-input .el-input__inner) {
    font-size: 20px;
    letter-spacing: 6px;
  }
}
</style>
