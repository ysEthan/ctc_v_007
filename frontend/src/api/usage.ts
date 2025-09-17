import api from './index'

export interface Usage {
  id: number
  usageDate: string
  iccid?: string
  productId?: string
  subscription?: {
    id: number
    subscriptionId: string
  }
  subscriptionId?: string
  usageType?: 'dat' | 'sms' | 'voc'
  usageType_display?: string
  callType?: '0' | '1' | '*'
  callType_display?: string
  visitMcc?: string
  visitMnc?: string
  usage?: number
  unit?: 'Byte' | 'Minute' | 'String'
  unit_display?: string
  formatted_usage?: string
  created_at: string
  updated_at: string
}

export interface UsageCreateRequest {
  usageDate: string
  productId?: string
  subscription: number  // Subscription ID
  usageType?: 'dat' | 'sms' | 'voc'
  callType?: '0' | '1' | '*'
  visitMcc?: string
  visitMnc?: string
  usage?: number
  unit?: 'Byte' | 'Minute' | 'String'
}

export interface UsageUpdateRequest extends Partial<UsageCreateRequest> {}

export interface UsageListResponse {
  count: number
  next?: string
  previous?: string
  results: Usage[]
}

export interface UsageStatistics {
  data_usage: number
  sms_usage: number
  voice_usage: number
  total_records: number
  period: {
    start_date?: string
    end_date?: string
  }
}

export interface DailyUsageStatistics {
  date: string
  data_usage: number
  sms_usage: number
  voice_usage: number
  total_usage: number
}

export const usageApi = {
  // 获取用量列表
  getUsages: async (params?: {
    page?: number
    page_size?: number
    search?: string
    usageType?: string
    callType?: string
    productId?: string
    subscriptionId?: string
    date?: string
    iccid?: string
    mccMnc?: string
    ordering?: string
  }): Promise<UsageListResponse> => {
    const response = await api.get('/usage/', { params })
    return response.data
  },

  // 获取用量详情
  getUsage: async (id: number): Promise<Usage> => {
    const response = await api.get(`/usage/${id}/`)
    return response.data
  },

  // 创建用量
  createUsage: async (data: UsageCreateRequest): Promise<Usage> => {
    const response = await api.post('/usage/', data)
    return response.data
  },

  // 更新用量
  updateUsage: async (id: number, data: UsageUpdateRequest): Promise<Usage> => {
    const response = await api.patch(`/usage/${id}/`, data)
    return response.data
  },

  // 删除用量
  deleteUsage: async (id: number): Promise<void> => {
    await api.delete(`/usage/${id}/`)
  },

  // 搜索用量
  searchUsages: async (q: string): Promise<Usage[]> => {
    const response = await api.get('/usage/search/', { params: { q } })
    return response.data
  },

  // 获取用量统计信息
  getUsageStatistics: async (params?: {
    start_date?: string
    end_date?: string
    subscription_id?: string
    product_id?: string
  }): Promise<UsageStatistics> => {
    const response = await api.get('/usage/statistics/', { params })
    return response.data
  },

  // 获取每日用量统计
  getDailyUsageStatistics: async (params?: {
    days?: number
    subscription_id?: string
    product_id?: string
  }): Promise<DailyUsageStatistics[]> => {
    const response = await api.get('/usage/daily-statistics/', { params })
    return response.data
  },

  // 批量导入用量
  bulkImportUsage: async (file: File): Promise<{ message: string; success: boolean }> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/usage/bulk-import/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // 导出用量数据
  exportUsage: async (): Promise<Blob> => {
    const response = await api.get('/usage/export/', {
      responseType: 'blob'
    })
    return response.data
  }
}
