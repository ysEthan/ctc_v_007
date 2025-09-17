<template>
  <div class="cug-list">

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item>
          <el-input
            v-model="searchForm.date"
            placeholder="用量日期"
            clearable
            @keyup.enter="handleSearch"
            style="width: 120px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="searchForm.iccid"
            placeholder="ICCID"
            clearable
            @keyup.enter="handleSearch"
            style="width: 190px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="searchForm.subscriptionId"
            placeholder="订阅ID"
            clearable
            @keyup.enter="handleSearch"
            style="width: 190px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="searchForm.productId"
            placeholder="产品ID"
            clearable
            @keyup.enter="handleSearch"
            style="width: 110px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="searchForm.mccMnc"
            placeholder="MCC-MNC"
            clearable
            @keyup.enter="handleSearch"
            style="width: 120px"
          />
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
        :data="cugList"
        stripe
        border
      >
        
        <el-table-column prop="usageDate" label="用量日期" width="120" fixed="left" />
        
        <el-table-column prop="iccid" label="ICCID" width="200" />
        <el-table-column prop="subscriptionId" label="订阅ID" width="200" />
        <el-table-column prop="productId" label="产品ID" width="120" />
        
        <!-- 隐藏的列：用量类型、呼叫类型、访问地MCC -->
        <!--
        <el-table-column prop="usageType_display" label="用量类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getUsageTypeTagType(row.usageType)">
              {{ row.usageType_display }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="callType_display" label="呼叫类型" width="100" />
        
        <el-table-column prop="visitMcc" label="访问地MCC" width="120" />
        -->
        <el-table-column prop="visitMnc" label="MCC-MNC" width="120">
          <template #default="{ row }">
            {{ formatMccMnc(row.visitMnc) }}
          </template>
        </el-table-column>
        
        <!-- 隐藏用量值列 -->
        <!--
        <el-table-column prop="usage" label="用量值" width="120" />
        -->
        <!-- 隐藏单位列 -->
        <!--
        <el-table-column prop="unit_display" label="单位" width="80" />
        -->
        
        <el-table-column prop="formatted_usage" label="用量（MB）" width="150">
          <template #default="{ row }">
            {{ formatUsageValue(row.formatted_usage) }}
          </template>
        </el-table-column>
        
        <!-- 隐藏创建时间列 -->
        <!--
        <el-table-column prop="created_at" label="创建时间" width="150">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        -->
        
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-dropdown @command="(command) => handleOperation(command, row)">
              <el-button size="small">
                操作<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="view">查看</el-dropdown-item>
                  <el-dropdown-item command="edit">编辑</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
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
import { Search, ArrowDown } from '@element-plus/icons-vue'
import { usageApi, type Usage } from '@/api/usage'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const cugList = ref<Usage[]>([])

// 搜索表单
const searchForm = reactive({
  date: '',
  iccid: '',
  subscriptionId: '',
  productId: '',
  mccMnc: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 获取CUG详单列表
const fetchCUGList = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }
    
    const response = await usageApi.getUsages(params)
    cugList.value = response.results
    pagination.total = response.count
  } catch (error) {
    console.error('获取CUG详单列表失败:', error)
    ElMessage.error('获取CUG详单列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchCUGList()
}

// 重置搜索
const handleReset = () => {
  Object.assign(searchForm, {
    date: '',
    iccid: '',
    subscriptionId: '',
    productId: '',
    mccMnc: ''
  })
  pagination.page = 1
  fetchCUGList()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchCUGList()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchCUGList()
}



// 处理下拉菜单操作
const handleOperation = (command: string, row: Usage) => {
  switch (command) {
    case 'view':
      handleView(row)
      break
    case 'edit':
      handleEdit(row)
      break
    case 'delete':
      handleDelete(row)
      break
  }
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
      `确定要删除这条CUG详单记录吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await usageApi.deleteUsage(row.id)
    ElMessage.success('删除成功')
    fetchCUGList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除CUG详单失败:', error)
      ElMessage.error('删除失败')
    }
  }
}


// 格式化MCC-MNC显示
const formatMccMnc = (mnc?: string) => {
  if (!mnc) return '-'
  
  // 如果长度大于等于5位，在前3位和后2位之间添加"-"
  if (mnc.length >= 5) {
    return mnc.slice(0, 3) + '-' + mnc.slice(3, 5)
  }
  
  return mnc
}

// 格式化用量值，移除MB单位
const formatUsageValue = (usage?: string) => {
  if (!usage) return '-'
  
  // 移除"MB"单位，保留数值部分
  return usage.replace(/\s*MB$/, '')
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
  fetchCUGList()
})
</script>

<style scoped>
.cug-list {
  padding: 20px;
}


.search-card {
  margin-bottom: 20px;
}

/* 紧凑筛选区域：减少外边距与内边距，保持控件尺寸不变 */
:deep(.search-card .el-card__body) {
  padding: 8px 12px; /* 默认20px，压缩为约一半 */
  padding-left: 20px; /* 左侧略加一点，让输入框与表格对齐 */
}

:deep(.search-card .el-form) {
  margin-bottom: 0; /* 去掉表单底部空隙 */
}

:deep(.search-card .el-form-item) {
  margin-right: 8px; /* 默认大约16px，压缩 */
  margin-bottom: 0; /* 去掉行间距，降低整体高度 */
}

/* 保持控件高度不变，仅微调附加按钮的内边距使版面更紧凑 */
:deep(.search-card .el-input-group__append .el-button) {
  padding-left: 10px;
  padding-right: 10px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* Responsive Table 样式 - 参考Bootstrap风格 */
:deep(.el-table) {
  font-size: 14px;
  border: 1px solid #ddd;
  border-collapse: collapse;
  background-color: #fff;
}

:deep(.el-table .el-table__header) {
  background-color: #f8f8f8;
}

:deep(.el-table .el-table__header th) {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  font-weight: bold;
  color: #333;
  padding: 6px 12px;
  height: 32px;
  text-align: left;
}

:deep(.el-table .el-table__header .cell) {
  padding: 6px 12px;
  line-height: 1.3;
  font-weight: bold;
}

:deep(.el-table .el-table__row) {
  height: 29px;
  border-bottom: 1px solid #ddd;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f5f5;
}

:deep(.el-table .el-table__body tr td) {
  border: 1px solid #ddd;
  padding: 0;
  vertical-align: middle;
}

:deep(.el-table .el-table__body tr td .cell) {
  padding: 4px 12px;
  line-height: 1.3;
}

/* 条纹样式 */
:deep(.el-table .el-table__row--striped) {
  background-color: #f9f9f9;
}

:deep(.el-table .el-table__row--striped:hover) {
  background-color: #f5f5f5;
}

/* 表格边框 */
:deep(.el-table--border) {
  border: 1px solid #ddd;
}

:deep(.el-table--border .el-table__cell) {
  border-right: 1px solid #ddd;
}

:deep(.el-table--border .el-table__header .el-table__cell) {
  border-right: 1px solid #ddd;
}

/* 紧凑按钮样式 */
:deep(.el-table .el-button--small) {
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 3px;
}

/* 下拉按钮样式 */
:deep(.el-table .el-dropdown .el-button) {
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 3px;
}
</style>
