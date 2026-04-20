<template>
  <div class="reports-page">
    <el-card class="page-header">
      <div class="header-content">
        <h2>安全报告</h2>
        <p>生成和管理网络安全分析报告</p>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="reports-container">
          <div class="reports-content">
            <div class="reports-header">
              <el-button type="primary" @click="showCreateDialog">
                <el-icon><DocumentAdd /></el-icon>
                生成新报告
              </el-button>
            </div>

            <el-table :data="reports" style="width: 100%" v-loading="loading">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="报告标题" min-width="200" />
              <el-table-column prop="report_type" label="报告类型" width="120">
                <template #default="scope">
                  <el-tag v-if="scope.row.report_type === 'attack_path'" type="danger">攻击路径</el-tag>
                  <el-tag v-else-if="scope.row.report_type === 'technique_detail'" type="warning">技术详情</el-tag>
                  <el-tag v-else-if="scope.row.report_type === 'threat_assessment'" type="info">威胁评估</el-tag>
                  <el-tag v-else type="success">自定义</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="format" label="格式" width="80">
                <template #default="scope">
                  <el-tag type="info">{{ scope.row.format?.toUpperCase() || 'PDF' }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag v-if="scope.row.status === 'completed'" type="success">已完成</el-tag>
                  <el-tag v-else-if="scope.row.status === 'generating'" type="warning">生成中</el-tag>
                  <el-tag v-else-if="scope.row.status === 'failed'" type="danger">失败</el-tag>
                  <el-tag v-else type="info">{{ scope.row.status }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="viewReport(scope.row)">
                    <el-icon><View /></el-icon>
                    查看
                  </el-button>
                  <el-button
                    type="success"
                    size="small"
                    :disabled="scope.row.status !== 'completed'"
                    @click="downloadReport(scope.row)"
                  >
                    <el-icon><Download /></el-icon>
                    下载
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteReport(scope.row)">
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="pagination">
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
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      v-model="createDialogVisible"
      title="生成新报告"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="reportFormRef"
        :model="reportForm"
        :rules="reportFormRules"
        label-width="100px"
      >
        <el-form-item label="报告标题" prop="title">
          <el-input v-model="reportForm.title" placeholder="请输入报告标题" />
        </el-form-item>

        <el-form-item label="报告类型" prop="report_type">
          <el-select v-model="reportForm.report_type" placeholder="请选择报告类型" style="width: 100%">
            <el-option label="攻击路径分析" value="attack_path" />
            <el-option label="技术详情报告" value="technique_detail" />
            <el-option label="威胁评估报告" value="threat_assessment" />
            <el-option label="自定义报告" value="custom" />
          </el-select>
        </el-form-item>

        <el-form-item label="报告格式" prop="format">
          <el-select v-model="reportForm.format" placeholder="请选择报告格式" style="width: 100%">
            <el-option label="PDF" value="pdf" />
            <el-option label="Word" value="word" />
            <el-option label="Excel" value="excel" />
            <el-option label="HTML" value="html" />
          </el-select>
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="reportForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入报告描述"
          />
        </el-form-item>

        <el-form-item label="选择战术" v-if="reportForm.report_type === 'attack_path' || reportForm.report_type === 'threat_assessment'">
          <el-select
            v-model="reportForm.tactic_ids"
            multiple
            placeholder="请选择战术（可选）"
            style="width: 100%"
            collapse-tags
          >
            <el-option
              v-for="tactic in tactics"
              :key="tactic.tactic_id"
              :label="tactic.name"
              :value="tactic.tactic_id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="选择技术" v-if="reportForm.report_type === 'technique_detail'">
          <el-select
            v-model="reportForm.technique_ids"
            multiple
            placeholder="请选择技术（可选）"
            style="width: 100%"
            filterable
            collapse-tags
          >
            <el-option
              v-for="technique in techniques"
              :key="technique.technique_id"
              :label="`${technique.technique_id} - ${technique.name}`"
              :value="technique.technique_id"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateReport" :loading="submitting">
          生成报告
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="viewDialogVisible"
      title="报告详情"
      width="800px"
      destroy-on-close
    >
      <div v-if="currentReport" class="report-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="报告标题" :span="2">
            {{ currentReport.title }}
          </el-descriptions-item>
          <el-descriptions-item label="报告类型">
            {{ getReportTypeName(currentReport.report_type) }}
          </el-descriptions-item>
          <el-descriptions-item label="格式">
            {{ currentReport.format?.toUpperCase() || 'PDF' }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag v-if="currentReport.status === 'completed'" type="success">已完成</el-tag>
            <el-tag v-else-if="currentReport.status === 'generating'" type="warning">生成中</el-tag>
            <el-tag v-else-if="currentReport.status === 'failed'" type="danger">失败</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ formatDate(currentReport.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">
            {{ formatDate(currentReport.updated_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ currentReport.description || '无' }}
          </el-descriptions-item>
          <el-descriptions-item label="页数" v-if="currentReport.page_count">
            {{ currentReport.page_count }}
          </el-descriptions-item>
          <el-descriptions-item label="生成时间" v-if="currentReport.generation_time">
            {{ currentReport.generation_time }}秒
          </el-descriptions-item>
        </el-descriptions>

        <div v-if="currentReport.content" class="report-content" style="margin-top: 20px;">
          <h4>报告内容预览</h4>
          <el-card shadow="never">
            <div v-html="currentReport.content"></div>
          </el-card>
        </div>
      </div>

      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
        <el-button
          type="primary"
          @click="downloadReport(currentReport!)"
          :disabled="currentReport?.status !== 'completed'"
        >
          下载报告
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { DocumentAdd, View, Download, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { getReports, createReport, deleteReport, downloadReport as downloadReportApi, type Report, type ReportGenerateParams } from '@/api/report'
import { getTactics } from '@/api/attack'
import { getTechniques } from '@/api/attack'

const reports = ref<Report[]>([])
const loading = ref(false)
const submitting = ref(false)
const createDialogVisible = ref(false)
const viewDialogVisible = ref(false)
const currentReport = ref<Report | null>(null)

const tactics = ref<any[]>([])
const techniques = ref<any[]>([])

const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const reportFormRef = ref<FormInstance>()

const reportForm = ref<ReportGenerateParams>({
  title: '',
  description: '',
  report_type: 'attack_path',
  format: 'pdf',
  technique_ids: [],
  actor_ids: [],
  tactic_ids: []
})

const reportFormRules: FormRules = {
  title: [
    { required: true, message: '请输入报告标题', trigger: 'blur' },
    { min: 2, max: 200, message: '标题长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  report_type: [
    { required: true, message: '请选择报告类型', trigger: 'change' }
  ],
  format: [
    { required: true, message: '请选择报告格式', trigger: 'change' }
  ]
}

const showCreateDialog = async () => {
  createDialogVisible.value = true
  reportForm.value = {
    title: '',
    description: '',
    report_type: 'attack_path',
    format: 'pdf',
    technique_ids: [],
    actor_ids: [],
    tactic_ids: []
  }

  try {
    const [tacticsRes, techniquesRes] = await Promise.all([
      getTactics({ per_page: 100 }),
      getTechniques({ per_page: 100 })
    ])

    if (tacticsRes.items) {
      tactics.value = tacticsRes.items
    }
    if (techniquesRes.items) {
      techniques.value = techniquesRes.items
    }
  } catch (error) {
    console.error('获取选项失败:', error)
  }
}

const handleCreateReport = async () => {
  if (!reportFormRef.value) return

  try {
    await reportFormRef.value.validate()
  } catch {
    return
  }

  submitting.value = true

  try {
    const response = await createReport(reportForm.value)

    if (response.message) {
      ElMessage.success(response.message)
    } else {
      ElMessage.success('报告创建成功')
    }

    createDialogVisible.value = false
    fetchReports()
  } catch (error: any) {
    ElMessage.error(error.message || '创建报告失败')
  } finally {
    submitting.value = false
  }
}

const viewReport = async (report: Report) => {
  currentReport.value = report
  viewDialogVisible.value = true
}

const handleDownloadReport = async (report: Report) => {
  if (report.status !== 'completed') {
    ElMessage.warning('报告尚未生成完成')
    return
  }

  try {
    await downloadReportApi(report.id)
    ElMessage.success('报告下载已开始')
  } catch (error: any) {
    ElMessage.error(error.message || '下载报告失败')
  }
}

const handleDeleteReport = async (report: Report) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除报告"${report.title}"吗？此操作不可撤销。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteReport(report.id)
    ElMessage.success('报告删除成功')
    fetchReports()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除报告失败')
    }
  }
}

const fetchReports = async () => {
  loading.value = true

  try {
    const response = await getReports({
      page: pagination.value.page,
      per_page: pagination.value.pageSize
    })

    if (response.items) {
      reports.value = response.items
    }
    pagination.value.total = response.total || 0
  } catch (error: any) {
    ElMessage.error(error.message || '获取报告列表失败')
    reports.value = []
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val: number) => {
  pagination.value.pageSize = val
  pagination.value.page = 1
  fetchReports()
}

const handleCurrentChange = (val: number) => {
  pagination.value.page = val
  fetchReports()
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getReportTypeName = (type: string) => {
  const typeMap: Record<string, string> = {
    attack_path: '攻击路径分析',
    technique_detail: '技术详情报告',
    threat_assessment: '威胁评估报告',
    custom: '自定义报告'
  }
  return typeMap[type] || type
}

const downloadReport = (report: Report) => {
  handleDownloadReport(report)
}

const deleteReport = (report: Report) => {
  handleDeleteReport(report)
}

onMounted(() => {
  fetchReports()
})
</script>

<style scoped lang="scss">
.reports-page {
  padding: 20px;

  .page-header {
    margin-bottom: 20px;

    .header-content {
      h2 {
        margin: 0 0 10px 0;
        color: #303133;
        font-size: 24px;
      }

      p {
        margin: 0;
        color: #606266;
        font-size: 14px;
      }
    }
  }

  .reports-container {
    .reports-content {
      .reports-header {
        margin-bottom: 20px;
        display: flex;
        justify-content: flex-end;
      }

      .pagination {
        margin-top: 20px;
        display: flex;
        justify-content: flex-end;
      }
    }
  }
}

.report-detail {
  padding: 10px;
}
</style>