import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  phone: string
  avatar: string
  user_type: 'super_admin' | 'admin' | 'user'
  user_type_display: string
  status: 'active' | 'inactive' | 'banned'
  status_display: string
  email_verified: boolean
  last_login: string
  created_at: string
  updated_at: string
}

export const useUserStore = defineStore('user', () => {
  // 用户信息
  const user = ref<User | null>(null)
  
  // 加载状态
  const loading = ref(false)
  
  // 计算属性
  const isLoggedIn = computed(() => !!user.value)
  const isSuperAdmin = computed(() => user.value?.user_type === 'super_admin')
  const isAdmin = computed(() => user.value?.user_type === 'super_admin' || user.value?.user_type === 'admin')
  const isActiveUser = computed(() => user.value?.status === 'active' && user.value?.email_verified)
  
  // 设置用户信息
  const setUser = (userData: User) => {
    user.value = userData
  }
  
  // 清除用户信息
  const clearUser = () => {
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
  
  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      loading.value = true
      const response = await authApi.getUserInfo()
      setUser(response)
      return response
    } catch (error) {
      console.error('获取用户信息失败:', error)
      clearUser()
      throw error
    } finally {
      loading.value = false
    }
  }
  
  // 更新用户信息
  const updateUserInfo = async (userData: Partial<User>) => {
    try {
      loading.value = true
      const response = await authApi.updateUser(userData)
      if (user.value) {
        user.value = { ...user.value, ...response }
      }
      return response
    } catch (error) {
      console.error('更新用户信息失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  // 修改密码
  const changePassword = async (passwordData: {
    old_password: string
    new_password: string
    new_password_confirm: string
  }) => {
    try {
      loading.value = true
      await authApi.changePassword(passwordData)
      return true
    } catch (error) {
      console.error('修改密码失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  // 登出
  const logout = async () => {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('登出失败:', error)
    } finally {
      clearUser()
    }
  }
  
  // 检查权限
  const hasPermission = (permission: string) => {
    if (!user.value) return false
    
    // 超级管理员拥有所有权限
    if (isSuperAdmin.value) return true
    
    // 管理员权限检查
    if (permission.startsWith('admin:') && isAdmin.value) return true
    
    // 普通用户权限检查
    if (permission.startsWith('user:') && isActiveUser.value) return true
    
    return false
  }
  
  // 检查用户类型
  const hasUserType = (userType: 'super_admin' | 'admin' | 'user') => {
    return user.value?.user_type === userType
  }
  
  return {
    // 状态
    user,
    loading,
    
    // 计算属性
    isLoggedIn,
    isSuperAdmin,
    isAdmin,
    isActiveUser,
    
    // 方法
    setUser,
    clearUser,
    fetchUserInfo,
    updateUserInfo,
    changePassword,
    logout,
    hasPermission,
    hasUserType
  }
})
