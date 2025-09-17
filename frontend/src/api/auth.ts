import api from './index'
import type { User } from '@/stores/user'

export interface LoginCredentials {
  username_or_email: string
  password: string
  remember_me?: boolean
}

export interface RegisterCredentials {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name?: string
  last_name?: string
  phone?: string
}

export interface TokenResponse {
  access: string
  refresh: string
  user: User
}

export interface LoginResponse extends TokenResponse {}

export interface RegisterResponse {
  message: string
  user_id: number
  email: string
}

export interface VerificationRequest {
  verification_code: string
}

export interface ResendVerificationRequest {
  email: string
}

export interface PasswordChangeRequest {
  old_password: string
  new_password: string
  new_password_confirm: string
}

export const authApi = {
  // 用户注册
  register: async (credentials: RegisterCredentials): Promise<RegisterResponse> => {
    const response = await api.post('/auth/register/', credentials)
    return response.data
  },

  // 用户登录
  login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
    const response = await api.post('/auth/login/', credentials)
    return response.data
  },

  // 用户登出
  logout: async (): Promise<void> => {
    const refreshToken = localStorage.getItem('refresh_token')
    if (refreshToken) {
      await api.post('/auth/logout/', { refresh: refreshToken })
    }
  },

  // 刷新token
  refreshToken: async (refreshToken: string): Promise<TokenResponse> => {
    const response = await api.post('/auth/token/refresh/', { refresh: refreshToken })
    return response.data
  },

  // 获取用户信息
  getUserInfo: async (): Promise<User> => {
    const response = await api.get('/auth/user-info/')
    return response.data
  },

  // 更新用户信息
  updateUser: async (userData: Partial<User>): Promise<User> => {
    const response = await api.patch('/auth/update/', userData)
    return response.data
  },

  // 修改密码
  changePassword: async (passwordData: PasswordChangeRequest): Promise<void> => {
    await api.post('/auth/change-password/', passwordData)
  },

  // 邮箱验证
  verifyEmail: async (verificationCode: string): Promise<void> => {
    await api.post('/auth/verify-email/', { verification_code: verificationCode })
  },

  // 重新发送验证邮件
  resendVerification: async (data: ResendVerificationRequest): Promise<void> => {
    await api.post('/auth/resend-verification/', data)
  },

  // 健康检查
  healthCheck: async () => {
    const response = await api.get('/health/')
    return response.data
  }
}
