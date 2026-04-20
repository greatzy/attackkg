<template>
  <div class="attack-matrix-page">
    <!-- Page Header -->
    <el-card class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h2>ATT&CK矩阵</h2>
          <p>可视化展示MITRE ATT&CK框架的战术和技术关系</p>
        </div>
        <div class="header-right">
          <el-select 
            v-model="selectedPlatform" 
            placeholder="选择平台" 
            clearable
            style="width: 150px; margin-right: 10px;"
            @change="handlePlatformChange"
          >
            <el-option label="Windows" value="Windows" />
            <el-option label="Linux" value="Linux" />
            <el-option label="MacOS" value="MacOS" />
            <el-option label="Network" value="Network" />
            <el-option label="Azure AD" value="Azure AD" />
          </el-select>
          <el-button type="primary" @click="refreshData" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新数据
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- Matrix Container -->
    <el-card class="matrix-container" v-loading="loading">
      <div class="matrix-content">
        <!-- Matrix Header -->
        <div class="matrix-header">
          <div class="matrix-stats">
            <el-tag type="info">战术: {{ matrixData.length }}</el-tag>
            <el-tag type="info" style="margin-left: 10px;">技术: {{ totalTechniques }}</el-tag>
          </div>
          <div class="matrix-legend">
            <div class="legend-item">
              <div class="legend-color" style="background-color: #409eff;"></div>
              <span>通用技术</span>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #67c23a;"></div>
              <span>子技术</span>
            </div>
          </div>
        </div>

        <!-- Matrix Grid -->
        <div class="matrix-grid" v-if="matrixData.length > 0">
          <div class="matrix-row header-row">
            <div 
              v-for="tactic in matrixData" 
              :key="tactic.tactic_id"
              class="matrix-cell tactic-header"
            >
              <div class="tactic-name">{{ tactic.name }}</div>
              <div class="tactic-id">{{ tactic.tactic_id }}</div>
            </div>
          </div>
          
          <div class="matrix-body">
            <div 
              v-for="(row, rowIndex) in techniqueRows" 
              :key="rowIndex"
              class="matrix-row"
            >
              <div 
                v-for="tactic in matrixData" 
                :key="tactic.tactic_id"
                class="matrix-cell technique-cell"
              >
                <div v-if="getTechniqueAtRow(tactic, rowIndex)" class="technique-list">
                  <div
                    v-for="technique in getTechniqueAtRow(tactic, rowIndex)"
                    :key="technique.technique_id"
                    class="technique-item"
                    :class="{ 'is-subtechnique': technique.is_subtechnique }"
                    @click="showTechniqueDetail(technique)"
                    @mouseenter="handleTechniqueHover(technique)"
                    @mouseleave="handleTechniqueLeave"
                  >
                    <div class="technique-id">{{ technique.technique_id }}</div>
                    <div class="technique-name">{{ technique.name }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <el-empty v-else description="暂无数据" />
      </div>
    </el-card>

    <!-- Technique Detail Dialog -->
    <el-dialog
      v-model="detailDialogVisible"
      title="技术详情"
      width="600px"
      destroy-on-close
    >
      <div v-if="selectedTechnique" class="technique-detail">
        <h3>{{ selectedTechnique.name }}</h3>
        <p class="technique-id">ID: {{ selectedTechnique.technique_id }}</p>
        <p class="technique-description">{{ selectedTechnique.description }}</p>
        <div class="technique-platforms">
          <strong>适用平台:</strong>
          <el-tag 
            v-for="platform in selectedTechnique.platforms" 
            :key="platform"
            size="small"
            style="margin-left: 5px;"
          >
            {{ platform }}
          </el-tag>
        </div>
        <div class="technique-url" v-if="selectedTechnique.url">
          <el-link :href="selectedTechnique.url" target="_blank" type="primary">
            查看 MITRE 官方文档
          </el-link>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getAttackMatrix } from '@/api/attack'

// 数据类型定义
type MatrixTechnique = {
  technique_id: string
  name: string
  description: string
  platforms: string[]
  is_subtechnique: boolean
  url?: string
}

type MatrixTactic = {
  tactic_id: string
  name: string
  techniques: MatrixTechnique[]
}

const loading = ref(false)
const matrixData = ref<MatrixTactic[]>([])
const totalTechniques = ref(0)
const selectedPlatform = ref('')
const detailDialogVisible = ref(false)
const selectedTechnique = ref<MatrixTechnique | null>(null)

// Calculate the maximum number of technique rows needed
const techniqueRows = computed(() => {
  if (matrixData.value.length === 0) return 0
  const maxTechniques = Math.max(
    ...matrixData.value.map(t => t.techniques.length)
  )
  return Math.ceil(maxTechniques / 3) // Show 3 techniques per row
})

// Get techniques for a specific tactic and row
const getTechniqueAtRow = (tactic: MatrixTactic, rowIndex: number) => {
  const startIdx = rowIndex * 3
  const endIdx = startIdx + 3
  return tactic.techniques.slice(startIdx, endIdx)
}

const loadMatrixData = async () => {
  loading.value = true
  try {
    // 从API获取真实数据
    const response = await getAttackMatrix(selectedPlatform.value || undefined)
    
    console.log('API Response:', response)
    
    if (response && response.matrix) {
      matrixData.value = response.matrix
      totalTechniques.value = response.total_techniques || matrixData.value.reduce((total, tactic) => total + tactic.techniques.length, 0)
      ElMessage.success('数据加载成功')
    } else {
      ElMessage.error('数据格式错误')
    }
  } catch (error) {
    ElMessage.error('加载矩阵数据失败')
    console.error('Error loading matrix data:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  loadMatrixData()
  ElMessage.success('数据已刷新')
}

const handlePlatformChange = () => {
  loadMatrixData()
}

const showTechniqueDetail = (technique: MatrixTechnique) => {
  selectedTechnique.value = technique
  detailDialogVisible.value = true
}

const handleTechniqueHover = (technique: MatrixTechnique) => {
  // Could add hover effects here
}

const handleTechniqueLeave = () => {
  // Could remove hover effects here
}

onMounted(() => {
  loadMatrixData()
})
</script>

<style scoped lang="scss">
.attack-matrix-page {
  padding: 20px;

  .page-header {
    margin-bottom: 20px;

    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .header-left {
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

      .header-right {
        display: flex;
        align-items: center;
      }
    }
  }

  .matrix-container {
    .matrix-content {
      .matrix-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #e4e7ed;

        .matrix-stats {
          display: flex;
          gap: 10px;
        }

        .matrix-legend {
          display: flex;
          gap: 20px;

          .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;

            .legend-color {
              width: 16px;
              height: 16px;
              border-radius: 3px;
            }

            span {
              font-size: 12px;
              color: #606266;
            }
          }
        }
      }

      .matrix-grid {
        overflow-x: auto;

        .matrix-row {
          display: flex;
          min-width: 1200px;

          &.header-row {
            background-color: #f5f7fa;
            border-bottom: 2px solid #409eff;
          }
        }

        .matrix-cell {
          flex: 1;
          min-width: 150px;
          padding: 10px;
          border-right: 1px solid #e4e7ed;
          border-bottom: 1px solid #e4e7ed;

          &:last-child {
            border-right: none;
          }

          &.tactic-header {
            text-align: center;
            background-color: #f5f7fa;

            .tactic-name {
              font-weight: bold;
              color: #303133;
              font-size: 14px;
              margin-bottom: 5px;
            }

            .tactic-id {
              font-size: 12px;
              color: #909399;
            }
          }

          &.technique-cell {
            min-height: 80px;
            background-color: #fff;

            .technique-list {
              display: flex;
              flex-direction: column;
              gap: 5px;

              .technique-item {
                padding: 8px;
                border-radius: 4px;
                background-color: #409eff;
                color: white;
                cursor: pointer;
                transition: all 0.3s;

                &:hover {
                  background-color: #66b1ff;
                  transform: translateY(-2px);
                  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
                }

                &.is-subtechnique {
                  background-color: #67c23a;

                  &:hover {
                    background-color: #85ce61;
                  }
                }

                .technique-id {
                  font-size: 10px;
                  font-weight: bold;
                  margin-bottom: 2px;
                }

                .technique-name {
                  font-size: 11px;
                  line-height: 1.2;
                }
              }
            }
          }
        }
      }
    }
  }
}

.technique-detail {
  h3 {
    margin: 0 0 10px 0;
    color: #303133;
  }

  .technique-id {
    color: #909399;
    font-size: 14px;
    margin-bottom: 15px;
  }

  .technique-description {
    color: #606266;
    line-height: 1.6;
    margin-bottom: 15px;
  }

  .technique-platforms {
    margin-bottom: 15px;
  }

  .technique-url {
    margin-top: 20px;
  }
}
</style>
