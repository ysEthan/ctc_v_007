<template>
  <div class="usage-list">
    <div class="page-header">
      <h1>用量管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增用量
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
            placeholder="请输入产品ID、订阅ID或访问地MCC"
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
        
        <el-form-item label="用量类型">
          <el-select v-model="searchForm.usageType" placeholder="请选择" clearable>
            <el-option label="数据" value="dat" />
            <el-option label="短信" value="sms" />
            <el-option label="语音" value="voc" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="呼叫类型">
          <el-select v-model="searchForm.callType" placeholder="请选择" clearable>
            <el-option label="主叫" value="0" />
            <el-option label="被叫" value="1" />
            <el-option label="全部" value="*" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="usageList"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="usageDate" label="用量日期" width="120" fixed="left" />
        
        <el-table-column prop="productId" label="产品ID" width="120" />
        <el-table-column prop="subscriptionId" label="订阅ID" width="200" />
        
        <el-table-column prop="usageType_display" label="用量类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getUsageTypeTagType(row.usageType)">
              {{ row.usageType_display }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="callType_display" label="呼叫类型" width="100" />
        
        <el-table-column prop="visitMcc" label="访问地MCC" width="120" />
        <el-table-column prop="visitMnc" label="访问地MNC" width="120" />
        
        <el-table-column prop="usage" label="用量值" width="120" />
        <el-table-column prop="unit_display" label="单位" width="80" />
        
        <el-table-column prop="formatted_usage" label="格式化用量" width="150" />
        
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download, Search } from '@element-plus/icons-vue'
import { usageApi, type Usage } from '@/api/usage'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const usageList = ref<Usage[]>([])

// 搜索表单
const searchForm = reactive({
  search: '',
  usageType: '',
  callType: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 选中的行
const selectedRows = ref<Usage[]>([])

// 获取用量列表
const fetchUsageList = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }
    
    const response = await usageApi.getUsages(params)
    usageList.value = response.results
    pagination.total = response.count
  } catch (error) {
    console.error('获取用量列表失败:', error)
    ElMessage.error('获取用量列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchUsageList()
}

// 重置搜索
const handleReset = () => {
  Object.assign(searchForm, {
    search: '',
    usageType: '',
    callType: ''
  })
  pagination.page = 1
  fetchUsageList()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchUsageList()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchUsageList()
}

// 表格选择
const handleSelectionChange = (selection: Usage[]) => {
  selectedRows.value = selection
}

// 新增
const handleAdd = () => {
  ElMessage.info('新增功能待实现')
}

// 查看
const handleView = (row: Usage) => {
  ElMessage.info('查看功能待实现')
}

// 编辑
const handleEdit = (row: Usage) => {
  ElMessage.info('编辑功能待实现')
}

// 删除
const handleDelete = async (row: Usage) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除这条用量记录吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await usageApi.deleteUsage(row.id)
    ElMessage.success('删除成功')
    fetchUsageList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用量失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 导出
const handleExport = async () => {
  try {
    const blob = await usageApi.exportUsage()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `usage_export_${new Date().toISOString().split('T')[0]}.xlsx`
    link.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

// 获取用量类型标签类型
const getUsageTypeTagType = (usageType?: string) => {
  switch (usageType) {
    case 'dat': return 'primary'  // 数据
    case 'sms': return 'success'  // 短信
    case 'voc': return 'warning'  // 语音
    default: return ''
  }
}

// 格式化日期时间
const formatDateTime = (dateTime?: string) => {
  if (!dateTime) return '-'
  
  try {
    return new Date(dateTime).toLocaleString()
  } catch {
    return dateTime
  }
}

// 初始化
onMounted(() => {
  fetchUsageList()
})
</script>

<style scoped>
.usage-list {
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

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
