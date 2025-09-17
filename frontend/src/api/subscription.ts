import api from './index'

export interface Subscription {
  id: number
  subscriptionId: string
  icc?: {
    id: number
    iccid: string
    imsi?: string
    msisdn?: string
  }
  userId?: number
  acctId?: number
  brand?: string
  productId?: string
  productFlag?: '0' | '1'
  productFlag_display?: string
  status?: '0' | '1' | '2' | '3' | '4' | '5'
  status_display?: string
  statusTime?: string
  activeDeadline?: string
  validityUnit?: 'H' | 'D' | 'M' | 'N'
  validityUnit_display?: string
  validityTime?: number
  effTime?: string
  expTime?: string
  createTime?: string
  priority?: '20' | '30' | '40' | '50' | '80'
  priority_display?: string
  changeReason?: '1' | '2' | '3' | '4' | '5' | '6' | '7'
  changeReason_display?: string
  created_at: string
  updated_at: string
}

export interface SubscriptionCreateRequest {
  subscriptionId: string
  icc: number  // ICC ID
  userId?: number
  acctId?: number
  brand?: string
  productId?: string
  productFlag?: '0' | '1'
  status?: '0' | '1' | '2' | '3' | '4' | '5'
  statusTime?: string
  activeDeadline?: string
  validityUnit?: 'H' | 'D' | 'M' | 'N'
  validityTime?: number
  effTime?: string
  expTime?: string
  createTime?: string
  priority?: '20' | '30' | '40' | '50' | '80'
  changeReason?: '1' | '2' | '3' | '4' | '5' | '6' | '7'
}

export interface SubscriptionUpdateRequest extends Partial<SubscriptionCreateRequest> {
  // subscriptionId不允许更新
}

export interface SubscriptionListResponse {
  count: number
  next?: string
  previous?: string
  results: Subscription[]
}

export interface SubscriptionStatistics {
  total: number
  subscribing: number
  inactive: number
  normal: number
  expired: number
  unsubscribing: number
  locked: number
}

export const subscriptionApi = {
  // 获取订阅列表
  getSubscriptions: async (params?: {
    page?: number
    page_size?: number
    search?: string
    status?: string
    productFlag?: string
    brand?: string
    priority?: string
    ordering?: string
  }): Promise<SubscriptionListResponse> => {
    const response = await api.get('/subscription/', { params })
    return response.data
  },

  // 获取订阅详情
  getSubscription: async (id: number): Promise<Subscription> => {
    const response = await api.get(`/subscription/${id}/`)
    return response.data
  },

  // 创建订阅
  createSubscription: async (data: SubscriptionCreateRequest): Promise<Subscription> => {
    const response = await api.post('/subscription/', data)
    return response.data
  },

  // 更新订阅
  updateSubscription: async (id: number, data: SubscriptionUpdateRequest): Promise<Subscription> => {
    const response = await api.patch(`/subscription/${id}/`, data)
    return response.data
  },

  // 删除订阅（软删除）
  deleteSubscription: async (id: number): Promise<void> => {
    await api.delete(`/subscription/${id}/`)
  },

  // 搜索订阅
  searchSubscriptions: async (q: string): Promise<Subscription[]> => {
    const response = await api.get('/subscription/search/', { params: { q } })
    return response.data
  },

  // 获取订阅统计信息
  getSubscriptionStatistics: async (): Promise<SubscriptionStatistics> => {
    const response = await api.get('/subscription/statistics/')
    return response.data
  },

  // 批量导入订阅
  bulkImportSubscription: async (file: File): Promise<{ message: string; success: boolean }> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/subscription/bulk-import/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // 导出订阅数据
  exportSubscription: async (): Promise<Blob> => {
    const response = await api.get('/subscription/export/', {
      responseType: 'blob'
    })
    return response.data
  }
}
