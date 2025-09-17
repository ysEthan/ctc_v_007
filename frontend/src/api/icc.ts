import api from './index'

export interface ICC {
  id: number
  userid?: number
  custid?: number
  acctid?: number
  paidFlag?: '0' | '1'
  paidFlag_display?: string
  imsi?: string
  iccid: string
  msisdn?: string
  brand?: string
  rateplanId?: string
  lifeCycle?: '0' | '1' | '2' | '3' | '4' | '5'
  lifeCycle_display?: string
  lifeCycleTime?: string
  suspendReason?: '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
  suspendReason_display?: string
  activeType?: string
  validityUnit?: 'H' | 'D' | 'M' | 'N'
  validityUnit_display?: string
  validityTime?: number
  activeTime?: string
  activeDeadline?: string
  hlrState?: 'A' | 'B' | 'G' | 'D' | 'I'
  hlrState_display?: string
  effTime?: string
  expTime?: string
  createTime?: string
  created_at: string
  updated_at: string
}

export interface ICCCreateRequest {
  userid?: number
  custid?: number
  acctid?: number
  paidFlag?: '0' | '1'
  imsi?: string
  iccid: string
  msisdn?: string
  brand?: string
  rateplanId?: string
  lifeCycle?: '0' | '1' | '2' | '3' | '4' | '5'
  lifeCycleTime?: string
  suspendReason?: '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
  activeType?: string
  validityUnit?: 'H' | 'D' | 'M' | 'N'
  validityTime?: number
  activeTime?: string
  activeDeadline?: string
  hlrState?: 'A' | 'B' | 'G' | 'D' | 'I'
  effTime?: string
  expTime?: string
  createTime?: string
}

export interface ICCUpdateRequest extends Partial<ICCCreateRequest> {
  // ICCID不允许更新
}

export interface ICCListResponse {
  count: number
  next?: string
  previous?: string
  results: ICC[]
}

export interface ICCStatistics {
  total: number
  active: number
  inactive: number
  suspended: number
  expired: number
  deleted: number
}

export const iccApi = {
  // 获取ICC列表
  getICCs: async (params?: {
    page?: number
    page_size?: number
    search?: string
    lifeCycle?: string
    paidFlag?: string
    brand?: string
    hlrState?: string
    ordering?: string
  }): Promise<ICCListResponse> => {
    const response = await api.get('/icc/', { params })
    return response.data
  },

  // 获取ICC详情
  getICC: async (id: number): Promise<ICC> => {
    const response = await api.get(`/icc/${id}/`)
    return response.data
  },

  // 创建ICC
  createICC: async (data: ICCCreateRequest): Promise<ICC> => {
    const response = await api.post('/icc/', data)
    return response.data
  },

  // 更新ICC
  updateICC: async (id: number, data: ICCUpdateRequest): Promise<ICC> => {
    const response = await api.patch(`/icc/${id}/`, data)
    return response.data
  },

  // 删除ICC（软删除）
  deleteICC: async (id: number): Promise<void> => {
    await api.delete(`/icc/${id}/`)
  },

  // 搜索ICC
  searchICCs: async (q: string): Promise<ICC[]> => {
    const response = await api.get('/icc/search/', { params: { q } })
    return response.data
  },

  // 获取ICC统计信息
  getICCStatistics: async (): Promise<ICCStatistics> => {
    const response = await api.get('/icc/statistics/')
    return response.data
  },

  // 批量导入ICC
  bulkImportICC: async (file: File): Promise<{ message: string; success: boolean }> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/icc/bulk-import/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // 导出ICC数据
  exportICC: async (): Promise<Blob> => {
    const response = await api.get('/icc/export/', {
      responseType: 'blob'
    })
    return response.data
  }
}
