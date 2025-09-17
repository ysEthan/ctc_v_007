<template>
  <div class="subscription-detail">
    <div class="page-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/subscription' }">订阅管理</el-breadcrumb-item>
        <el-breadcrumb-item>订阅详情</el-breadcrumb-item>
      </el-breadcrumb>
      
      <div class="header-actions">
        <el-button @click="goBack">返回</el-button>
        <el-button type="primary" @click="editSubscription">编辑</el-button>
      </div>
    </div>

    <el-card v-loading="loading" class="detail-card">
      <template #header>
        <div class="card-header">
          <span>订阅详情</span>
          <el-tag :type="getStatusType(subscription?.status)" v-if="subscription">
            {{ getStatusText(subscription.status) }}
          </el-tag>
        </div>
      </template>

      <div v-if="subscription" class="detail-content">
        <el-row :gutter="24">
          <el-col :span="12">
            <div class="detail-section">
              <h3>基本信息</h3>
              <el-descriptions :column="1" border>
                <el-descriptions-item label="订阅ID">
                  {{ subscription.subscriptionId }}
                </el-descriptions-item>
                <el-descriptions-item label="ICC卡">
                  {{ subscription.icc?.iccid || 'N/A' }}
                </el-descriptions-item>
                <el-descriptions-item label="用户ID">
                  {{ subscription.userId || 'N/A' }}
                </el-descriptions-item>
                <el-descriptions-item label="账户ID">
                  {{ subscription.acctId || 'N/A' }}
                </el-descriptions-item>
                <el-descriptions-item label="品牌">
                  {{ subscription.brand || 'N/A' }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-col>
          
          <el-col :span="12">
            <div class="detail-section">
              <h3>产品信息</h3>
              <el-descriptions :column="1" border>
                <el-descriptions-item label="产品ID">
                  {{ subscription.productId || 'N/A' }}
                </el-descriptions-item>
                <el-descriptions-item label="产品标志">
                  {{ getProductFlagText(subscription.productFlag) }}
                </el-descriptions-item>
                <el-descriptions-item label="订阅状态">
                  {{ getStatusText(subscription.status) }}
                </el-descriptions-item>
                <el-descriptions-item label="状态时间">
                  {{ formatDateTime(subscription.statusTime) }}
                </el-descriptions-item>
                <el-descriptions-item label="优先级">
                  {{ getPriorityText(subscription.priority) }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="24" style="margin-top: 24px;">
          <el-col :span="12">
            <div class="detail-section">
              <h3>有效期信息</h3>
              <el-descriptions :column="1" border>
                <el-descriptions-item label="最后激活时间">
                  {{ formatDate(subscription.activeDeadline) }}
                </el-descriptions-item>
                <el-descriptions-item label="有效期单位">
                  {{ getValidityUnitText(subscription.validityUnit) }}
                </el-descriptions-item>
                <el-descriptions-item label="有效期时间">
                  {{ subscription.validityTime || 'N/A' }}
                </el-descriptions-item>
                <el-descriptions-item label="生效时间">
                  {{ formatDateTime(subscription.effTime) }}
                </el-descriptions-item>
                <el-descriptions-item label="过期时间">
                  {{ formatDateTime(subscription.expTime) }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-col>
          
          <el-col :span="12">
            <div class="detail-section">
              <h3>其他信息</h3>
              <el-descriptions :column="1" border>
                <el-descriptions-item label="创建时间">
                  {{ formatDateTime(subscription.createTime) }}
                </el-descriptions-item>
                <el-descriptions-item label="变更原因">
                  {{ getChangeReasonText(subscription.changeReason) }}
                </el-descriptions-item>
                <el-descriptions-item label="记录创建时间">
                  {{ formatDateTime(subscription.created_at) }}
                </el-descriptions-item>
                <el-descriptions-item label="记录更新时间">
                  {{ formatDateTime(subscription.updated_at) }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-col>
        </el-row>
      </div>

      <div v-else-if="!loading" class="empty-state">
        <el-empty description="订阅信息不存在" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { subscriptionApi } from '@/api/subscription'
import type { Subscription } from '@/api/subscription'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const subscription = ref<Subscription | null>(null)

// 获取订阅详情
const fetchSubscriptionDetail = async () => {
  const id = route.params.id as string
  if (!id) {
    ElMessage.error('订阅ID不能为空')
    return
  }

  loading.value = true
  try {
    const response = await subscriptionApi.getSubscription(parseInt(id))
    subscription.value = response
  } catch (error: any) {
    ElMessage.error(error.response?.data?.message || '获取订阅详情失败')
  } finally {
    loading.value = false
  }
}

// 返回列表
const goBack = () => {
  router.push('/subscription')
}

// 编辑订阅
const editSubscription = () => {
  router.push(`/subscription/${route.params.id}/edit`)
}

// 格式化日期时间
const formatDateTime = (dateTime: string | null) => {
  if (!dateTime) return 'N/A'
  if (dateTime.length === 14) {
    // yyyyMMddHHmmss 格式
    const year = dateTime.substring(0, 4)
    const month = dateTime.substring(4, 6)
    const day = dateTime.substring(6, 8)
    const hour = dateTime.substring(8, 10)
    const minute = dateTime.substring(10, 12)
    const second = dateTime.substring(12, 14)
    return `${year}-${month}-${day} ${hour}:${minute}:${second}`
  }
  return dateTime
}

// 格式化日期
const formatDate = (date: string | null) => {
  if (!date) return 'N/A'
  if (date.length === 8) {
    // yyyyMMdd 格式
    const year = date.substring(0, 4)
    const month = date.substring(4, 6)
    const day = date.substring(6, 8)
    return `${year}-${month}-${day}`
  }
  return date
}

// 获取状态文本
const getStatusText = (status: string | null) => {
  const statusMap: Record<string, string> = {
    '0': '订阅中',
    '1': '未激活',
    '2': '正常',
    '3': '已过期',
    '4': '退订中',
    '5': '已锁定'
  }
  return statusMap[status || ''] || '未知'
}

// 获取状态类型
const getStatusType = (status: string | null) => {
  const typeMap: Record<string, string> = {
    '0': 'warning',
    '1': 'info',
    '2': 'success',
    '3': 'danger',
    '4': 'warning',
    '5': 'danger'
  }
  return typeMap[status || ''] || 'info'
}

// 获取产品标志文本
const getProductFlagText = (flag: string | null) => {
  const flagMap: Record<string, string> = {
    '0': '基础套餐',
    '1': '附加包'
  }
  return flagMap[flag || ''] || '未知'
}

// 获取优先级文本
const getPriorityText = (priority: string | null) => {
  const priorityMap: Record<string, string> = {
    '20': '最高',
    '30': '高',
    '40': '中',
    '50': '低',
    '80': '最低'
  }
  return priorityMap[priority || ''] || '未知'
}

// 获取有效期单位文本
const getValidityUnitText = (unit: string | null) => {
  const unitMap: Record<string, string> = {
    'H': '小时',
    'D': '日历日',
    'M': '日历月',
    'N': '永不过期'
  }
  return unitMap[unit || ''] || '未知'
}

// 获取变更原因文本
const getChangeReasonText = (reason: string | null) => {
  const reasonMap: Record<string, string> = {
    '1': '使用中',
    '2': '速度受限',
    '3': '已用尽',
    '4': '未激活，已过期',
    '5': '未激活，已退订',
    '6': '已激活，已过期',
    '7': '已激活，已退订'
  }
  return reasonMap[reason || ''] || '未知'
}

onMounted(() => {
  fetchSubscriptionDetail()
})
</script>

<style scoped>
.subscription-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.detail-card {
  min-height: 600px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-content {
  padding: 20px 0;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h3 {
  margin: 0 0 16px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

:deep(.el-descriptions__label) {
  font-weight: 600;
  color: #606266;
}

:deep(.el-descriptions__content) {
  color: #303133;
}
</style>
