<template>
  <div class="subscription-list">
    <div class="page-header">
      <h1>订阅管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增订阅
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入订阅ID、产品ID或品牌"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button @click="handleSearch">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="订阅状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="订阅中" value="0" />
            <el-option label="未激活" value="1" />
            <el-option label="正常" value="2" />
            <el-option label="已过期" value="3" />
            <el-option label="退订中" value="4" />
            <el-option label="已锁定" value="5" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="产品标志">
          <el-select v-model="searchForm.productFlag" placeholder="请选择" clearable>
            <el-option label="基础套餐" value="0" />
            <el-option label="附加包" value="1" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="品牌">
          <el-input v-model="searchForm.brand" placeholder="请输入品牌" clearable />
        </el-form-item>
        
        <el-form-item label="优先级">
          <el-select v-model="searchForm.priority" placeholder="请选择" clearable>
            <el-option label="最高" value="20" />
            <el-option label="高" value="30" />
            <el-option label="中" value="40" />
            <el-option label="低" value="50" />
            <el-option label="最低" value="80" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 统计信息 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="3">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ statistics.total }}</div>
            <div class="stat-label">总计</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value subscribing">{{ statistics.subscribing }}</div>
            <div class="stat-label">订阅中</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value inactive">{{ statistics.inactive }}</div>
            <div class="stat-label">未激活</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value normal">{{ statistics.normal }}</div>
            <div class="stat-label">正常</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value expired">{{ statistics.expired }}</div>
            <div class="stat-label">已过期</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value unsubscribing">{{ statistics.unsubscribing }}</div>
            <div class="stat-label">退订中</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value locked">{{ statistics.locked }}</div>
            <div class="stat-label">已锁定</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="subscriptionList"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="subscriptionId" label="订阅ID" width="200" fixed="left">
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">
              {{ row.subscriptionId }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="userId" label="用户ID" width="100" />
        <el-table-column prop="acctId" label="账户ID" width="100" />
        <el-table-column prop="brand" label="品牌" width="100" />
        <el-table-column prop="productId" label="产品ID" width="120" />
        
        <el-table-column prop="productFlag_display" label="产品标志" width="100">
          <template #default="{ row }">
            <el-tag :type="row.productFlag === '1' ? 'success' : 'primary'">
              {{ row.productFlag_display }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status_display" label="订阅状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ row.status_display }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="priority_display" label="优先级" width="80" />
        
        <el-table-column prop="effTime" label="生效时间" width="150">
          <template #default="{ row }">
            {{ formatDateTime(row.effTime) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="expTime" label="过期时间" width="150">
          <template #default="{ row }">
            {{ formatDateTime(row.expTime) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="150">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleView(row)">查看</el-button>
            <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <SubscriptionForm
      v-model:visible="formVisible"
      :form-data="currentSubscription"
      :is-edit="isEdit"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download, Search } from '@element-plus/icons-vue'
import { subscriptionApi, type Subscription, type SubscriptionStatistics } from '@/api/subscription'
import SubscriptionForm from './SubscriptionForm.vue'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const subscriptionList = ref<Subscription[]>([])
const statistics = ref<SubscriptionStatistics>({
  total: 0,
  subscribing: 0,
  inactive: 0,
  normal: 0,
  expired: 0,
  unsubscribing: 0,
  locked: 0
})

// 搜索表单
const searchForm = reactive({
  search: '',
  status: '',
  productFlag: '',
  brand: '',
  priority: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 表单相关
const formVisible = ref(false)
const currentSubscription = ref<Subscription | null>(null)
const isEdit = ref(false)

// 选中的行
const selectedRows = ref<Subscription[]>([])

// 获取订阅列表
const fetchSubscriptionList = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }
    
    const response = await subscriptionApi.getSubscriptions(params)
    subscriptionList.value = response.results
    pagination.total = response.count
  } catch (error) {
    console.error('获取订阅列表失败:', error)
    ElMessage.error('获取订阅列表失败')
  } finally {
    loading.value = false
  }
}

// 获取统计信息
const fetchStatistics = async () => {
  try {
    const data = await subscriptionApi.getSubscriptionStatistics()
    statistics.value = data
  } catch (error) {
    console.error('获取统计信息失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchSubscriptionList()
}

// 重置搜索
const handleReset = () => {
  Object.assign(searchForm, {
    search: '',
    status: '',
    productFlag: '',
    brand: '',
    priority: ''
  })
  pagination.page = 1
  fetchSubscriptionList()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchSubscriptionList()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchSubscriptionList()
}

// 表格选择
const handleSelectionChange = (selection: Subscription[]) => {
  selectedRows.value = selection
}

// 新增
const handleAdd = () => {
  currentSubscription.value = null
  isEdit.value = false
  formVisible.value = true
}

// 查看
const handleView = (row: Subscription) => {
  router.push(`/subscription/${row.id}`)
}

// 编辑
const handleEdit = (row: Subscription) => {
  currentSubscription.value = { ...row }
  isEdit.value = true
  formVisible.value = true
}

// 删除
const handleDelete = async (row: Subscription) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除订阅 "${row.subscriptionId}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await subscriptionApi.deleteSubscription(row.id)
    ElMessage.success('删除成功')
    fetchSubscriptionList()
    fetchStatistics()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除订阅失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 导出
const handleExport = async () => {
  try {
    const blob = await subscriptionApi.exportSubscription()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `subscription_export_${new Date().toISOString().split('T')[0]}.xlsx`
    link.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

// 表单成功回调
const handleFormSuccess = () => {
  formVisible.value = false
  fetchSubscriptionList()
  fetchStatistics()
}

// 获取状态标签类型
const getStatusTagType = (status?: string) => {
  switch (status) {
    case '0': return 'info'     // 订阅中
    case '1': return 'warning'  // 未激活
    case '2': return 'success'  // 正常
    case '3': return 'danger'   // 已过期
    case '4': return 'warning'  // 退订中
    case '5': return 'danger'   // 已锁定
    default: return ''
  }
}

// 格式化日期时间
const formatDateTime = (dateTime?: string) => {
  if (!dateTime) return '-'
  
  // 如果是14位数字格式 (yyyyMMddHHmmss)
  if (dateTime.length === 14 && /^\d{14}$/.test(dateTime)) {
    const year = dateTime.substring(0, 4)
    const month = dateTime.substring(4, 6)
    const day = dateTime.substring(6, 8)
    const hour = dateTime.substring(8, 10)
    const minute = dateTime.substring(10, 12)
    const second = dateTime.substring(12, 14)
    return `${year}-${month}-${day} ${hour}:${minute}:${second}`
  }
  
  // 如果是ISO格式
  try {
    return new Date(dateTime).toLocaleString()
  } catch {
    return dateTime
  }
}

// 初始化
onMounted(() => {
  fetchSubscriptionList()
  fetchStatistics()
})
</script>

<style scoped>
.subscription-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #2c3e50;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.search-card {
  margin-bottom: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-value.subscribing {
  color: #409eff;
}

.stat-value.inactive {
  color: #909399;
}

.stat-value.normal {
  color: #67c23a;
}

.stat-value.expired {
  color: #f56c6c;
}

.stat-value.unsubscribing {
  color: #e6a23c;
}

.stat-value.locked {
  color: #f56c6c;
}

.stat-label {
  color: #606266;
  font-size: 12px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
