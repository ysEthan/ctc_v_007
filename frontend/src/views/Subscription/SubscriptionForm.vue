<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑订阅' : '新增订阅'"
    width="800px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="订阅ID" prop="subscriptionId">
            <el-input
              v-model="form.subscriptionId"
              placeholder="请输入订阅ID"
              :disabled="isEdit"
              maxlength="64"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="用户ID" prop="userId">
            <el-input-number
              v-model="form.userId"
              placeholder="请输入用户ID"
              :min="0"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="账户ID" prop="acctId">
            <el-input-number
              v-model="form.acctId"
              placeholder="请输入账户ID"
              :min="0"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="品牌" prop="brand">
            <el-input
              v-model="form.brand"
              placeholder="请输入品牌"
              maxlength="50"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="产品ID" prop="productId">
            <el-input
              v-model="form.productId"
              placeholder="请输入产品ID"
              maxlength="16"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品标志" prop="productFlag">
            <el-select v-model="form.productFlag" placeholder="请选择产品标志" style="width: 100%">
              <el-option label="基础套餐" value="0" />
              <el-option label="附加包" value="1" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="订阅状态" prop="status">
            <el-select v-model="form.status" placeholder="请选择订阅状态" style="width: 100%">
              <el-option label="订阅中" value="0" />
              <el-option label="未激活" value="1" />
              <el-option label="正常" value="2" />
              <el-option label="已过期" value="3" />
              <el-option label="退订中" value="4" />
              <el-option label="已锁定" value="5" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="优先级" prop="priority">
            <el-select v-model="form.priority" placeholder="请选择优先级" style="width: 100%">
              <el-option label="最高" value="20" />
              <el-option label="高" value="30" />
              <el-option label="中" value="40" />
              <el-option label="低" value="50" />
              <el-option label="最低" value="80" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="有效期单位" prop="validityUnit">
            <el-select v-model="form.validityUnit" placeholder="请选择有效期单位" style="width: 100%">
              <el-option label="小时" value="H" />
              <el-option label="日历日" value="D" />
              <el-option label="日历月" value="M" />
              <el-option label="永不过期" value="N" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="有效期时长" prop="validityTime">
            <el-input-number
              v-model="form.validityTime"
              placeholder="请输入有效期时长"
              :min="0"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="生效时间" prop="effTime">
            <el-input
              v-model="form.effTime"
              placeholder="格式：yyyyMMddHHmmss"
              maxlength="14"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="过期时间" prop="expTime">
            <el-input
              v-model="form.expTime"
              placeholder="格式：yyyyMMddHHmmss"
              maxlength="14"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="状态时间" prop="statusTime">
            <el-input
              v-model="form.statusTime"
              placeholder="格式：yyyyMMddHHmmss"
              maxlength="14"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="最后激活时间" prop="activeDeadline">
            <el-input
              v-model="form.activeDeadline"
              placeholder="格式：yyyyMMdd"
              maxlength="8"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="变更原因" prop="changeReason">
            <el-select v-model="form.changeReason" placeholder="请选择变更原因" style="width: 100%">
              <el-option label="使用中" value="1" />
              <el-option label="速度受限" value="2" />
              <el-option label="已用尽" value="3" />
              <el-option label="未激活，已过期" value="4" />
              <el-option label="未激活，已退订" value="5" />
              <el-option label="已激活，已过期" value="6" />
              <el-option label="已激活，已退订" value="7" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="创建时间" prop="createTime">
            <el-input
              v-model="form.createTime"
              placeholder="格式：yyyyMMddHHmmss"
              maxlength="14"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" :loading="loading" @click="handleSubmit">
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch, nextTick, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { subscriptionApi, type Subscription, type SubscriptionCreateRequest, type SubscriptionUpdateRequest } from '@/api/subscription'

interface Props {
  visible: boolean
  formData?: Subscription | null
  isEdit: boolean
}

interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const formRef = ref()
const loading = ref(false)

// 表单数据
const form = reactive<SubscriptionCreateRequest & SubscriptionUpdateRequest>({
  subscriptionId: '',
  userId: undefined,
  acctId: undefined,
  brand: '',
  productId: '',
  productFlag: undefined,
  status: undefined,
  statusTime: '',
  activeDeadline: '',
  validityUnit: undefined,
  validityTime: undefined,
  effTime: '',
  expTime: '',
  createTime: '',
  priority: undefined,
  changeReason: undefined
})

// 表单验证规则
const rules = {
  subscriptionId: [
    { required: true, message: '请输入订阅ID', trigger: 'blur' },
    { max: 64, message: '订阅ID长度不能超过64个字符', trigger: 'blur' }
  ],
  effTime: [
    { pattern: /^\d{14}$/, message: '生效时间格式：yyyyMMddHHmmss', trigger: 'blur' }
  ],
  expTime: [
    { pattern: /^\d{14}$/, message: '过期时间格式：yyyyMMddHHmmss', trigger: 'blur' }
  ],
  statusTime: [
    { pattern: /^\d{14}$/, message: '状态时间格式：yyyyMMddHHmmss', trigger: 'blur' }
  ],
  activeDeadline: [
    { pattern: /^\d{8}$/, message: '最后激活时间格式：yyyyMMdd', trigger: 'blur' }
  ],
  createTime: [
    { pattern: /^\d{14}$/, message: '创建时间格式：yyyyMMddHHmmss', trigger: 'blur' }
  ]
}

// 计算属性
const dialogVisible = computed(() => props.visible)

// 监听表单数据变化
watch(() => props.formData, (newData) => {
  if (newData) {
    Object.assign(form, {
      subscriptionId: newData.subscriptionId,
      userId: newData.userId,
      acctId: newData.acctId,
      brand: newData.brand || '',
      productId: newData.productId || '',
      productFlag: newData.productFlag,
      status: newData.status,
      statusTime: newData.statusTime || '',
      activeDeadline: newData.activeDeadline || '',
      validityUnit: newData.validityUnit,
      validityTime: newData.validityTime,
      effTime: newData.effTime || '',
      expTime: newData.expTime || '',
      createTime: newData.createTime || '',
      priority: newData.priority,
      changeReason: newData.changeReason
    })
  } else {
    resetForm()
  }
}, { immediate: true })

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    subscriptionId: '',
    userId: undefined,
    acctId: undefined,
    brand: '',
    productId: '',
    productFlag: undefined,
    status: undefined,
    statusTime: '',
    activeDeadline: '',
    validityUnit: undefined,
    validityTime: undefined,
    effTime: '',
    expTime: '',
    createTime: '',
    priority: undefined,
    changeReason: undefined
  })
  
  nextTick(() => {
    formRef.value?.clearValidate()
  })
}

// 关闭对话框
const handleClose = () => {
  emit('update:visible', false)
  resetForm()
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    if (props.isEdit && props.formData) {
      await subscriptionApi.updateSubscription(props.formData.id, form)
      ElMessage.success('更新成功')
    } else {
      await subscriptionApi.createSubscription(form)
      ElMessage.success('创建成功')
    }
    
    emit('success')
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('操作失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
