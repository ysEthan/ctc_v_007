/**
 * 文档管理API接口
 */
import api from './index'

// 文档相关接口
export interface Document {
  id: number
  filename: string
  file_path: string
  file_size: number
  file_prefix?: string
  record_type?: string
  host_node?: string
  cdr_type?: string
  version?: string
  file_date?: string
  status: 'pending' | 'processing' | 'success' | 'failed'
  total_iccid_count: number
  processed_iccid_count: number
  success_iccid_count: number
  failed_iccid_count: number
  progress_percentage: number
  success_rate: number
  created_at: string
  updated_at: string
  processed_at?: string
  error_message?: string
}

export interface DocumentListResponse {
  count: number
  next?: string
  previous?: string
  results: Document[]
}

export interface DocumentStatistics {
  total_documents: number
  pending_documents: number
  processing_documents: number
  success_documents: number
  failed_documents: number
  total_iccid_processed: number
  total_iccid_success: number
  total_iccid_failed: number
  success_rate: number
  avg_processing_time: number
}

// 错误案例相关接口
export interface BadCase {
  id: number
  document: number
  iccid: string
  api_type: 'user' | 'subscription' | 'usage'
  trans_id?: string
  status_code?: number
  response_data?: any
  error_message?: string
  retry_count: number
  last_retry_at?: string
  can_retry: boolean
  created_at: string
  updated_at: string
}

export interface BadCaseListResponse {
  count: number
  next?: string
  previous?: string
  results: BadCase[]
}

export interface BadCaseStatistics {
  total_bad_cases: number
  user_api_errors: number
  subscription_api_errors: number
  usage_api_errors: number
  retryable_cases: number
  error_by_status_code: Record<string, number>
}

// 文档管理API
export const documentApi = {
  // 获取文档列表
  getDocuments: (params?: {
    page?: number
    page_size?: number
    status?: string
    record_type?: string
    file_date?: string
    host_node?: string
    search?: string
    ordering?: string
  }) => {
    return api.get<DocumentListResponse>('/document/', { params })
  },

  // 获取文档详情
  getDocument: (id: number) => {
    return api.get<Document>(`/document/${id}/`)
  },

  // 搜索文档
  searchDocuments: (params?: {
    page?: number
    page_size?: number
    status?: string
    record_type?: string
    date_from?: string
    date_to?: string
    search?: string
    ordering?: string
  }) => {
    return api.get<DocumentListResponse>('/document/search/', { params })
  },

  // 获取文档统计信息
  getDocumentStatistics: () => {
    return api.get<DocumentStatistics>('/document/statistics/')
  },

  // 重试失败的文档
  retryDocument: (documentId: number) => {
    return api.post(`/document/${documentId}/retry/`)
  },

  // 获取错误案例列表
  getBadCases: (params?: {
    page?: number
    page_size?: number
    api_type?: string
    status_code?: number
    retry_count?: number
    search?: string
    ordering?: string
  }) => {
    return api.get<BadCaseListResponse>('/document/badcases/', { params })
  },

  // 获取错误案例详情
  getBadCase: (id: number) => {
    return api.get<BadCase>(`/document/badcases/${id}/`)
  },

  // 获取错误案例统计信息
  getBadCaseStatistics: () => {
    return api.get<BadCaseStatistics>('/document/badcases/statistics/')
  },

  // 重试错误案例
  retryBadCase: (badCaseId: number) => {
    return api.post(`/document/badcases/${badCaseId}/retry/`)
  },

  // 扫描新文档
  scanDocuments: () => {
    return api.post('/document/scan/')
  }
}
