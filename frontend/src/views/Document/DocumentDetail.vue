<template>
  <div class="document-detail">
    <el-descriptions :column="2" border>
      <el-descriptions-item label="文件名">
        {{ document.filename }}
      </el-descriptions-item>
      <el-descriptions-item label="文件大小">
        {{ formatFileSize(document.file_size) }}
      </el-descriptions-item>
      <el-descriptions-item label="记录类型">
        <el-tag :type="getRecordTypeTag(document.record_type)">
          {{ getRecordTypeText(document.record_type) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="主机节点">
        {{ document.host_node }}
      </el-descriptions-item>
      <el-descriptions-item label="CDR类型">
        {{ document.cdr_type }}
      </el-descriptions-item>
      <el-descriptions-item label="版本">
        {{ document.version }}
      </el-descriptions-item>
      <el-descriptions-item label="文件日期">
        {{ document.file_date }}
      </el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="getStatusTag(document.status)">
          {{ getStatusText(document.status) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="创建时间">
        {{ formatDateTime(document.created_at) }}
      </el-descriptions-item>
      <el-descriptions-item label="处理完成时间">
        {{ document.processed_at ? formatDateTime(document.processed_at) : '-' }}
      </el-descriptions-item>
    </el-descriptions>

    <!-- 处理统计 -->
    <div class="statistics-section">
      <h3>处理统计</h3>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ document.total_iccid_count }}</div>
              <div class="stat-label">ICCID总数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ document.processed_iccid_count }}</div>
              <div class="stat-label">已处理</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number success">{{ document.success_iccid_count }}</div>
              <div class="stat-label">成功处理</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number failed">{{ document.failed_iccid_count }}</div>
              <div class="stat-label">处理失败</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 进度和成功率 -->
    <div class="progress-section">
      <h3>处理进度</h3>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="progress-item">
            <div class="progress-label">处理进度</div>
            <el-progress
              :percentage="document.progress_percentage"
              :status="getProgressStatus(document.status)"
              :stroke-width="20"
            />
          </div>
        </el-col>
        <el-col :span="12">
          <div class="progress-item">
            <div class="progress-label">成功率</div>
            <el-progress
              :percentage="document.success_rate"
              :status="getSuccessRateStatus(document.success_rate)"
              :stroke-width="20"
            />
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 错误信息 -->
    <div v-if="document.error_message" class="error-section">
      <h3>错误信息</h3>
      <el-alert
        :title="document.error_message"
        type="error"
        :closable="false"
        show-icon
      />
    </div>

    <!-- 错误案例列表 -->
    <div v-if="badCases.length > 0" class="badcases-section">
      <h3>错误案例</h3>
      <el-table :data="badCases" stripe>
        <el-table-column prop="iccid" label="ICCID" width="200" />
        <el-table-column prop="api_type" label="API类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getApiTypeTag(row.api_type)">
              {{ getApiTypeText(row.api_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status_code" label="状态码" width="100" />
        <el-table-column prop="retry_count" label="重试次数" width="100" />
        <el-table-column prop="error_message" label="错误信息" min-width="200" />
        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button
              v-if="row.can_retry"
              type="warning"
              size="small"
              @click="retryBadCase(row)"
            >
              重试
            </el-button>
            <span v-else class="no-retry">不可重试</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { documentApi, type Document, type BadCase } from '@/api/document'

// Props
interface Props {
  document: Document
}

const props = defineProps<Props>()

// 响应式数据
const badCases = ref<BadCase[]>([])

// 方法
const loadBadCases = async () => {
  try {
    const response = await documentApi.getBadCases({
      document: props.document.id
    })
    badCases.value = response.data.results
  } catch (error) {
    console.error('加载错误案例失败:', error)
  }
}

const retryBadCase = async (badCase: BadCase) => {
  try {
    await ElMessageBox.confirm(
      `确定要重试错误案例 "${badCase.iccid}" 吗？`,
      '确认重试',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await documentApi.retryBadCase(badCase.id)
    ElMessage.success('重试任务已提交')
    loadBadCases()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重试错误案例失败:', error)
      ElMessage.error('重试错误案例失败')
    }
  }
}

// 工具方法
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

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

const getSuccessRateStatus = (rate: number) => {
  if (rate >= 90) return 'success'
  if (rate >= 70) return 'warning'
  return 'exception'
}

const getApiTypeTag = (type: string) => {
  const typeMap: Record<string, string> = {
    user: 'primary',
    subscription: 'success',
    usage: 'warning'
  }
  return typeMap[type] || 'info'
}

const getApiTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    user: '用户信息',
    subscription: '订阅信息',
    usage: '用量信息'
  }
  return typeMap[type] || type
}

// 生命周期
onMounted(() => {
  loadBadCases()
})
</script>

<style scoped>
.document-detail {
  padding: 20px;
}

.statistics-section,
.progress-section,
.error-section,
.badcases-section {
  margin-top: 30px;
}

.statistics-section h3,
.progress-section h3,
.error-section h3,
.badcases-section h3 {
  margin-bottom: 20px;
  color: #303133;
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

.progress-item {
  margin-bottom: 20px;
}

.progress-label {
  margin-bottom: 10px;
  font-weight: bold;
  color: #303133;
}

.no-retry {
  color: #909399;
  font-size: 12px;
}
</style>
