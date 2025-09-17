<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑ICC' : '新增ICC'"
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
          <el-form-item label="ICCID" prop="iccid">
            <el-input
              v-model="form.iccid"
              placeholder="请输入20位ICCID"
              :disabled="isEdit"
              maxlength="20"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="IMSI" prop="imsi">
            <el-input
              v-model="form.imsi"
              placeholder="请输入15位IMSI"
              maxlength="15"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="MSISDN" prop="msisdn">
            <el-input
              v-model="form.msisdn"
              placeholder="请输入MSISDN"
              maxlength="15"
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
          <el-form-item label="用户ID" prop="userid">
            <el-input-number
              v-model="form.userid"
              placeholder="请输入用户ID"
              :min="0"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="客户ID" prop="custid">
            <el-input-number
              v-model="form.custid"
              placeholder="请输入客户ID"
              :min="0"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="账户ID" prop="acctid">
            <el-input-number
              v-model="form.acctid"
              placeholder="请输入账户ID"
              :min="0"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="付费标志" prop="paidFlag">
            <el-select v-model="form.paidFlag" placeholder="请选择付费标志" style="width: 100%">
              <el-option label="预付费" value="0" />
              <el-option label="后付费" value="1" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="费率计划ID" prop="rateplanId">
            <el-input
              v-model="form.rateplanId"
              placeholder="请输入费率计划ID"
              maxlength="16"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="生命周期状态" prop="lifeCycle">
            <el-select v-model="form.lifeCycle" placeholder="请选择生命周期状态" style="width: 100%">
              <el-option label="未激活" value="0" />
              <el-option label="活跃" value="1" />
              <el-option label="已停机" value="2" />
              <el-option label="已锁定" value="3" />
              <el-option label="已过期" value="4" />
              <el-option label="已删除" value="5" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="停机原因" prop="suspendReason">
            <el-select v-model="form.suspendReason" placeholder="请选择停机原因" style="width: 100%">
              <el-option label="客户要求，默认选项" value="1" />
              <el-option label="丢失" value="2" />
              <el-option label="客户要求并保留电话号码" value="3" />
              <el-option label="欠费（未付租金）" value="4" />
              <el-option label="超过用户过期时间" value="5" />
              <el-option label="SIM卡与手机分离" value="6" />
              <el-option label="欠费（未付账单）" value="7" />
              <el-option label="保留" value="8" />
              <el-option label="其他" value="9" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="激活类型" prop="activeType">
            <el-input
              v-model="form.activeType"
              placeholder="请输入激活类型"
              maxlength="1"
            />
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
          <el-form-item label="激活时间" prop="activeTime">
            <el-input
              v-model="form.activeTime"
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
          <el-form-item label="设备状态" prop="hlrState">
            <el-select v-model="form.hlrState" placeholder="请选择设备状态" style="width: 100%">
              <el-option label="正常" value="A" />
              <el-option label="丢失" value="B" />
              <el-option label="暂停" value="G" />
              <el-option label="已删除" value="D" />
              <el-option label="预删除" value="I" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="生命周期时间" prop="lifeCycleTime">
            <el-input
              v-model="form.lifeCycleTime"
              placeholder="格式：yyyyMMddHHmmss"
              maxlength="14"
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

      <el-form-item label="创建时间" prop="createTime">
        <el-input
          v-model="form.createTime"
          placeholder="格式：yyyyMMddHHmmss"
          maxlength="14"
        />
      </el-form-item>
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
import { iccApi, type ICC, type ICCCreateRequest, type ICCUpdateRequest } from '@/api/icc'

interface Props {
  visible: boolean
  formData?: ICC | null
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
const form = reactive<ICCCreateRequest & ICCUpdateRequest>({
  userid: undefined,
  custid: undefined,
  acctid: undefined,
  paidFlag: undefined,
  imsi: '',
  iccid: '',
  msisdn: '',
  brand: '',
  rateplanId: '',
  lifeCycle: undefined,
  lifeCycleTime: '',
  suspendReason: undefined,
  activeType: '',
  validityUnit: undefined,
  validityTime: undefined,
  activeTime: '',
  activeDeadline: '',
  hlrState: undefined,
  effTime: '',
  expTime: '',
  createTime: ''
})

// 表单验证规则
const rules = {
  iccid: [
    { required: true, message: '请输入ICCID', trigger: 'blur' },
    { len: 20, message: 'ICCID必须是20位数字', trigger: 'blur' },
    { pattern: /^\d{20}$/, message: 'ICCID必须是20位数字', trigger: 'blur' }
  ],
  imsi: [
    { len: 15, message: 'IMSI必须是15位数字', trigger: 'blur' },
    { pattern: /^\d{15}$/, message: 'IMSI必须是15位数字', trigger: 'blur' }
  ],
  msisdn: [
    { pattern: /^\d{1,15}$/, message: 'MSISDN必须是1-15位数字', trigger: 'blur' }
  ],
  activeTime: [
    { pattern: /^\d{14}$/, message: '激活时间格式：yyyyMMddHHmmss', trigger: 'blur' }
  ],
  activeDeadline: [
    { pattern: /^\d{8}$/, message: '最后激活时间格式：yyyyMMdd', trigger: 'blur' }
  ],
  lifeCycleTime: [
    { pattern: /^\d{14}$/, message: '生命周期时间格式：yyyyMMddHHmmss', trigger: 'blur' }
  ],
  effTime: [
    { pattern: /^\d{14}$/, message: '生效时间格式：yyyyMMddHHmmss', trigger: 'blur' }
  ],
  expTime: [
    { pattern: /^\d{14}$/, message: '过期时间格式：yyyyMMddHHmmss', trigger: 'blur' }
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
      userid: newData.userid,
      custid: newData.custid,
      acctid: newData.acctid,
      paidFlag: newData.paidFlag,
      imsi: newData.imsi || '',
      iccid: newData.iccid,
      msisdn: newData.msisdn || '',
      brand: newData.brand || '',
      rateplanId: newData.rateplanId || '',
      lifeCycle: newData.lifeCycle,
      lifeCycleTime: newData.lifeCycleTime || '',
      suspendReason: newData.suspendReason,
      activeType: newData.activeType || '',
      validityUnit: newData.validityUnit,
      validityTime: newData.validityTime,
      activeTime: newData.activeTime || '',
      activeDeadline: newData.activeDeadline || '',
      hlrState: newData.hlrState,
      effTime: newData.effTime || '',
      expTime: newData.expTime || '',
      createTime: newData.createTime || ''
    })
  } else {
    resetForm()
  }
}, { immediate: true })

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    userid: undefined,
    custid: undefined,
    acctid: undefined,
    paidFlag: undefined,
    imsi: '',
    iccid: '',
    msisdn: '',
    brand: '',
    rateplanId: '',
    lifeCycle: undefined,
    lifeCycleTime: '',
    suspendReason: undefined,
    activeType: '',
    validityUnit: undefined,
    validityTime: undefined,
    activeTime: '',
    activeDeadline: '',
    hlrState: undefined,
    effTime: '',
    expTime: '',
    createTime: ''
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
      await iccApi.updateICC(props.formData.id, form)
      ElMessage.success('更新成功')
    } else {
      await iccApi.createICC(form)
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
