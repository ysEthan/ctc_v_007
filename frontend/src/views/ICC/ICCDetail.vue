<template>
  <div class="icc-detail">
    <div class="page-header">
      <el-button @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>ICC详情</h1>
      <div class="header-actions">
        <el-button type="primary" @click="handleEdit">
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
      </div>
    </div>

    <div v-loading="loading" class="detail-content">
      <el-row :gutter="20">
        <!-- 基础信息 -->
        <el-col :span="12">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>基础信息</span>
              </div>
            </template>
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="ICCID">
                <el-tag type="primary">{{ iccData?.iccid }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="IMSI">
                {{ iccData?.imsi || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="MSISDN">
                {{ iccData?.msisdn || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="品牌">
                {{ iccData?.brand || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="费率计划ID">
                {{ iccData?.rateplanId || '-' }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>

        <!-- 用户信息 -->
        <el-col :span="12">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>用户信息</span>
              </div>
            </template>
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="用户ID">
                {{ iccData?.userid || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="客户ID">
                {{ iccData?.custid || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="账户ID">
                {{ iccData?.acctid || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="付费标志">
                <el-tag :type="iccData?.paidFlag === '1' ? 'success' : 'warning'">
                  {{ iccData?.paidFlag_display || '-' }}
                </el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px;">
        <!-- 生命周期信息 -->
        <el-col :span="12">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>生命周期信息</span>
              </div>
            </template>
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="生命周期状态">
                <el-tag :type="getLifeCycleTagType(iccData?.lifeCycle)">
                  {{ iccData?.lifeCycle_display || '-' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="生命周期时间">
                {{ formatDateTime(iccData?.lifeCycleTime) }}
              </el-descriptions-item>
              <el-descriptions-item label="停机原因">
                {{ iccData?.suspendReason_display || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="激活类型">
                {{ iccData?.activeType || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="设备状态">
                <el-tag :type="getHlrStateTagType(iccData?.hlrState)">
                  {{ iccData?.hlrState_display || '-' }}
                </el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>

        <!-- 有效期信息 -->
        <el-col :span="12">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>有效期信息</span>
              </div>
            </template>
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="有效期单位">
                {{ iccData?.validityUnit_display || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="有效期时长">
                {{ iccData?.validityTime || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="激活时间">
                {{ formatDateTime(iccData?.activeTime) }}
              </el-descriptions-item>
              <el-descriptions-item label="最后激活时间">
                {{ formatDate(iccData?.activeDeadline) }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px;">
        <!-- 时间信息 -->
        <el-col :span="12">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>时间信息</span>
              </div>
            </template>
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="生效时间">
                {{ formatDateTime(iccData?.effTime) }}
              </el-descriptions-item>
              <el-descriptions-item label="过期时间">
                {{ formatDateTime(iccData?.expTime) }}
              </el-descriptions-item>
              <el-descriptions-item label="创建时间">
                {{ formatDateTime(iccData?.createTime) }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>

        <!-- 系统信息 -->
        <el-col :span="12">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>系统信息</span>
              </div>
            </template>
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="记录ID">
                {{ iccData?.id }}
              </el-descriptions-item>
              <el-descriptions-item label="创建时间">
                {{ formatDateTime(iccData?.created_at) }}
              </el-descriptions-item>
              <el-descriptions-item label="更新时间">
                {{ formatDateTime(iccData?.updated_at) }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 编辑对话框 -->
    <ICCForm
      v-model:visible="editVisible"
      :form-data="iccData"
      :is-edit="true"
      @success="handleEditSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Edit } from '@element-plus/icons-vue'
import { iccApi, type ICC } from '@/api/icc'
import ICCForm from './ICCForm.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const iccData = ref<ICC | null>(null)
const editVisible = ref(false)

// 获取ICC详情
const fetchICCDetail = async () => {
  try {
    loading.value = true
    const id = Number(route.params.id)
    const data = await iccApi.getICC(id)
    iccData.value = data
  } catch (error) {
    console.error('获取ICC详情失败:', error)
    ElMessage.error('获取ICC详情失败')
    goBack()
  } finally {
    loading.value = false
  }
}

// 返回
const goBack = () => {
  router.go(-1)
}

// 编辑
const handleEdit = () => {
  editVisible.value = true
}

// 编辑成功
const handleEditSuccess = () => {
  editVisible.value = false
  fetchICCDetail()
}

// 获取生命周期标签类型
const getLifeCycleTagType = (lifeCycle?: string) => {
  switch (lifeCycle) {
    case '1': return 'success'  // 活跃
    case '0': return 'info'     // 未激活
    case '2': return 'warning'  // 已停机
    case '3': return 'danger'   // 已锁定
    case '4': return 'danger'   // 已过期
    case '5': return 'info'     // 已删除
    default: return ''
  }
}

// 获取设备状态标签类型
const getHlrStateTagType = (hlrState?: string) => {
  switch (hlrState) {
    case 'A': return 'success'  // 正常
    case 'B': return 'warning'  // 丢失
    case 'G': return 'warning'  // 暂停
    case 'D': return 'danger'   // 已删除
    case 'I': return 'info'     // 预删除
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

// 格式化日期
const formatDate = (date?: string) => {
  if (!date) return '-'
  
  // 如果是8位数字格式 (yyyyMMdd)
  if (date.length === 8 && /^\d{8}$/.test(date)) {
    const year = date.substring(0, 4)
    const month = date.substring(4, 6)
    const day = date.substring(6, 8)
    return `${year}-${month}-${day}`
  }
  
  return date
}

// 初始化
onMounted(() => {
  fetchICCDetail()
})
</script>

<style scoped>
.icc-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #2c3e50;
  flex: 1;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.detail-content {
  min-height: 400px;
}

.info-card {
  height: 100%;
}

.card-header {
  font-weight: bold;
  color: #2c3e50;
}
</style>
