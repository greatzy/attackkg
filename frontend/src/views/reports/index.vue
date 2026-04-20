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
              <el-button type="primary" @click="generateReport">
                <el-icon><DocumentAdd /></el-icon>
                生成新报告
              </el-button>
            </div>
            
            <el-table :data="reports" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="报告标题" />
              <el-table-column prop="type" label="报告类型" />
              <el-table-column prop="status" label="状态" />
              <el-table-column prop="created_at" label="创建时间" />
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="viewReport(scope.row)">
                    <el-icon><View /></el-icon>
                    查看
                  </el-button>
                  <el-button type="success" size="small" @click="downloadReport(scope.row)">
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
  </div>
</template>

<script setup lang="ts">
import { DocumentAdd, View, Download, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Report {
  id: number
  title: string
  type: string
  status: string
  created_at: string
}

interface Pagination {
  page: number
  pageSize: number
  total: number
}

const reports = ref<Report[]>([])
const pagination = ref<Pagination>({
  page: 1,
  pageSize: 10,
  total: 0
})

const generateReport = () => {
  ElMessage.success('报告生成功能正在开发中')
}

const viewReport = (report: Report) => {
  ElMessage.success('查看报告功能正在开发中')
}

const downloadReport = (report: Report) => {
  ElMessage.success('下载报告功能正在开发中')
}

const deleteReport = (report: Report) => {
  ElMessage.success('删除报告功能正在开发中')
}

const handleSizeChange = (val: number) => {
  pagination.value.pageSize = val
  fetchReports()
}

const handleCurrentChange = (val: number) => {
  pagination.value.page = val
  fetchReports()
}

const fetchReports = () => {
  // 模拟数据
  reports.value = [
    {
      id: 1,
      title: '2024年第一季度安全威胁报告',
      type: '季度报告',
      status: '已完成',
      created_at: '2024-04-01'
    },
    {
      id: 2,
      title: 'APT组织攻击分析报告',
      type: '专项报告',
      status: '生成中',
      created_at: '2024-04-15'
    }
  ]
  pagination.value.total = reports.value.length
}

fetchReports()
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
</style>