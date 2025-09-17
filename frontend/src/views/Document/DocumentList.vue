<template>
  <div class="document-list">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>文件管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="refreshData">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
            <el-button type="success" @click="scanDocuments">
              <el-icon><Search /></el-icon>
              扫描新文件
            </el-button>
          </div>
        </div>
      </template>

      <!-- 统计信息 -->
      <div class="statistics-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ statistics.total_documents }}</div>
                <div class="stat-label">总文档数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number pending">{{ statistics.pending_documents }}</div>
                <div class="stat-label">待处理</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number success">{{ statistics.success_documents }}</div>
                <div class="stat-label">处理成功</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number failed">{{ statistics.failed_documents }}</div>
                <div class="stat-label">处理失败</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 搜索和筛选 -->
      <div class="filter-section">
        <el-form :model="searchForm" inline>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="选择状态" clearable>
              <el-option label="待处理" value="pending" />
              <el-option label="处理中" value="processing" />
              <el-option label="处理成功" value="success" />
              <el-option label="处理失败" value="failed" />
            </el-select>
          </el-form-item>
          <el-form-item label="记录类型">
            <el-select v-model="searchForm.record_type" placeholder="选择类型" clearable>
              <el-option label="数据用量" value="data" />
              <el-option label="语音用量" value="voice" />
              <el-option label="短信中心" value="smsc" />
            </el-select>
          </el-form-item>
          <el-form-item label="文件名">
            <el-input
              v-model="searchForm.search"
              placeholder="搜索文件名"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="resetSearch">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 文档列表 -->
      <el-table
        v-loading="loading"
        :data="documents"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="filename" label="文件名" min-width="200" />
        <el-table-column prop="record_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getRecordTypeTag(row.record_type)">
              {{ getRecordTypeText(row.record_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="file_date" label="文件日期" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="进度" width="120">
          <template #default="{ row }">
            <el-progress
              :percentage="row.progress_percentage"
              :status="getProgressStatus(row.status)"
              :stroke-width="8"
            />
          </template>
        </el-table-column>
        <el-table-column label="成功率" width="100">
          <template #default="{ row }">
            <span :class="getSuccessRateClass(row.success_rate)">
              {{ row.success_rate.toFixed(1) }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="total_iccid_count" label="ICCID总数" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewDocument(row)"
            >
              查看
            </el-button>
            <el-button
              v-if="row.status === 'failed'"
              type="warning"
              size="small"
              @click="retryDocument(row)"
            >
              重试
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 文档详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="文档详情"
      width="80%"
      :before-close="handleCloseDetail"
    >
      <DocumentDetail v-if="selectedDocument" :document="selectedDocument" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Search } from '@element-plus/icons-vue'
import { documentApi, type Document, type DocumentStatistics } from '@/api/document'
import DocumentDetail from './DocumentDetail.vue'

// 响应式数据
const loading = ref(false)
const documents = ref<Document[]>([])
const statistics = ref<DocumentStatistics>({
  total_documents: 0,
  pending_documents: 0,
  processing_documents: 0,
  success_documents: 0,
  failed_documents: 0,
  total_iccid_processed: 0,
  total_iccid_success: 0,
  total_iccid_failed: 0,
  success_rate: 0,
  avg_processing_time: 0
})

// 搜索表单
const searchForm = reactive({
  status: '',
  record_type: '',
  search: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 详情对话框
const detailDialogVisible = ref(false)
const selectedDocument = ref<Document | null>(null)

// 计算属性
const searchParams = computed(() => ({
  page: pagination.page,
  page_size: pagination.pageSize,
  ...searchForm
}))

// 方法
const loadDocuments = async () => {
  try {
    loading.value = true
    const response = await documentApi.getDocuments(searchParams.value)
    documents.value = response.data.results
    pagination.total = response.data.count
  } catch (error) {
    console.error('加载文档列表失败:', error)
    ElMessage.error('加载文档列表失败')
  } finally {
    loading.value = false
  }
}

const loadStatistics = async () => {
  try {
    const response = await documentApi.getDocumentStatistics()
    statistics.value = response.data
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

const refreshData = () => {
  loadDocuments()
  loadStatistics()
}

const scanDocuments = async () => {
  try {
    ElMessage.info('正在扫描新文件...')
    await documentApi.scanDocuments()
    ElMessage.success('扫描完成')
    refreshData()
  } catch (error) {
    console.error('扫描文档失败:', error)
    ElMessage.error('扫描文档失败')
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadDocuments()
}

const resetSearch = () => {
  Object.assign(searchForm, {
    status: '',
    record_type: '',
    search: ''
  })
  pagination.page = 1
  loadDocuments()
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  loadDocuments()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  loadDocuments()
}

const viewDocument = (document: Document) => {
  selectedDocument.value = document
  detailDialogVisible.value = true
}

const retryDocument = async (document: Document) => {
  try {
    await ElMessageBox.confirm(
      `确定要重试文档 "${document.filename}" 吗？`,
      '确认重试',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await documentApi.retryDocument(document.id)
    ElMessage.success('重试任务已提交')
    refreshData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重试文档失败:', error)
      ElMessage.error('重试文档失败')
    }
  }
}

const handleCloseDetail = () => {
  detailDialogVisible.value = false
  selectedDocument.value = null
}

// 工具方法
const getStatusTag = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: 'warning',
    processing: 'primary',
    success: 'success',
    failed: 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    success: '处理成功',
    failed: '处理失败'
  }
  return statusMap[status] || status
}

const getRecordTypeTag = (type: string) => {
  const typeMap: Record<string, string> = {
    data: 'primary',
    voice: 'success',
    smsc: 'warning'
  }
  return typeMap[type] || 'info'
}

const getRecordTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    data: '数据',
    voice: '语音',
    smsc: '短信'
  }
  return typeMap[type] || type
}

const getProgressStatus = (status: string) => {
  if (status === 'success') return 'success'
  if (status === 'failed') return 'exception'
  return undefined
}

const getSuccessRateClass = (rate: number) => {
  if (rate >= 90) return 'success-rate-high'
  if (rate >= 70) return 'success-rate-medium'
  return 'success-rate-low'
}

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadDocuments()
  loadStatistics()
})
</script>

<style scoped>
.document-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.statistics-section {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-number.pending {
  color: #e6a23c;
}

.stat-number.success {
  color: #67c23a;
}

.stat-number.failed {
  color: #f56c6c;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.filter-section {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.pagination-section {
  margin-top: 20px;
  text-align: right;
}

.success-rate-high {
  color: #67c23a;
  font-weight: bold;
}

.success-rate-medium {
  color: #e6a23c;
  font-weight: bold;
}

.success-rate-low {
  color: #f56c6c;
  font-weight: bold;
}
</style>
