<template>
  <div class="intelligence-page">
    <el-card class="page-header">
      <div class="header-content">
        <h2>威胁情报</h2>
        <p>收集、分析和展示最新的网络安全威胁情报</p>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="intelligence-container">
          <div class="intelligence-content">
            <div class="intelligence-header">
              <el-button type="primary" @click="refreshData">
                <el-icon><Refresh /></el-icon>
                刷新数据
              </el-button>
            </div>
            
            <el-table :data="intelligenceData" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" />
              <el-table-column prop="type" label="类型" />
              <el-table-column prop="severity" label="严重程度" />
              <el-table-column prop="source" label="来源" />
              <el-table-column prop="published_at" label="发布时间" />
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="viewDetail(scope.row)">
                    <el-icon><View /></el-icon>
                    查看详情
                  </el-button>
                  <el-button type="success" size="small" @click="shareIntelligence(scope.row)">
                    <el-icon><Share /></el-icon>
                    分享
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
import { Refresh, View, Share } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Intelligence {
  id: number
  title: string
  type: string
  severity: string
  source: string
  published_at: string
}

interface Pagination {
  page: number
  pageSize: number
  total: number
}

const intelligenceData = ref<Intelligence[]>([])
const pagination = ref<Pagination>({
  page: 1,
  pageSize: 10,
  total: 0
})

const refreshData = () => {
  ElMessage.success('数据已刷新')
  fetchIntelligence()
}

const viewDetail = (item: Intelligence) => {
  ElMessage.success('查看详情功能正在开发中')
}

const shareIntelligence = (item: Intelligence) => {
  ElMessage.success('分享功能正在开发中')
}

const handleSizeChange = (val: number) => {
  pagination.value.pageSize = val
  fetchIntelligence()
}

const handleCurrentChange = (val: number) => {
  pagination.value.page = val
  fetchIntelligence()
}

const fetchIntelligence = () => {
  // 模拟数据
  intelligenceData.value = [
    {
      id: 1,
      title: '新型勒索软件攻击趋势分析',
      type: '威胁分析',
      severity: '高',
      source: 'MITRE ATT&CK',
      published_at: '2024-04-18'
    },
    {
      id: 2,
      title: 'APT组织最新攻击手法',
      type: '威胁情报',
      severity: '中',
      source: 'FireEye',
      published_at: '2024-04-17'
    }
  ]
  pagination.value.total = intelligenceData.value.length
}

fetchIntelligence()
</script>

<style scoped lang="scss">
.intelligence-page {
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

  .intelligence-container {
    .intelligence-content {
      .intelligence-header {
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