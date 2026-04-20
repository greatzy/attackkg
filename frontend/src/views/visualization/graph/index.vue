<template>
  <div class="attack-graph-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h2>攻击路径图谱</h2>
          <p>可视化展示威胁行为者的攻击路径和技术关系</p>
        </div>
        <div class="header-right">
          <select 
            v-model="selectedTactic" 
            class="filter-select"
            @change="handleFilterChange"
          >
            <option value="">选择战术</option>
            <option 
              v-for="tactic in tactics" 
              :key="tactic.tactic_id" 
              :value="tactic.tactic_id" 
            >{{ tactic.name }}</option>
          </select>
          <button class="refresh-button" @click="refreshData" :disabled="loading">
            刷新数据
          </button>
        </div>
      </div>
    </div>

    <!-- Graph Container -->
    <div class="graph-container" v-if="!loading">
      <div class="graph-content">
        <div class="graph-header">
          <div class="graph-stats">
            <span class="stat-tag">节点: {{ graphData.total_nodes }}</span>
            <span class="stat-tag">关系: {{ graphData.total_edges }}</span>
            <span class="stat-tag" v-if="debugInfo">{{ debugInfo }}</span>
          </div>
          <div class="graph-controls">
            <button class="control-button" @click="resetZoom">
              重置视图
            </button>
            <button class="control-button" @click="togglePhysics">
              {{ physicsEnabled ? '停止动画' : '开启动画' }}
            </button>
            <button class="control-button" @click="debugGraph">
              调试
            </button>
          </div>
        </div>
        
        <!-- 使用 vue-echarts 组件 -->
        <div class="graph-chart">
          <v-chart 
            ref="chartRef"
            class="chart"
            :option="chartOption"
            @click="handleChartClick"
          />
        </div>
        <div class="debug-info" v-if="debugDetails">
          <h4>调试信息:</h4>
          <pre>{{ debugDetails }}</pre>
        </div>
      </div>
    </div>
    <div class="loading-container" v-else>
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Right Panel -->
    <div class="right-panel">
      <!-- Node Details Panel -->
      <div class="details-panel" v-if="selectedNode">
        <div class="panel-header">
          <span>节点详情</span>
          <button class="close-button" @click="selectedNode = null">
            ×
          </button>
        </div>
        
        <div class="node-details">
          <h3>{{ selectedNode.name }}</h3>
          <p class="node-id">ID: {{ selectedNode.id }}</p>
          <p class="node-type">
            <span class="type-tag" :class="selectedNode.type === 'tactic' ? 'tactic-tag' : 'technique-tag'">
              {{ selectedNode.type === 'tactic' ? '战术' : '技术' }}
            </span>
          </p>
          <p v-if="selectedNode.description" class="node-description">
            {{ selectedNode.description }}
          </p>
          <div v-if="selectedNode.type === 'technique'" class="node-actions">
            <button class="detail-button" @click="showTechniqueDetail(selectedNode)">
              查看详情
            </button>
          </div>
        </div>
      </div>
      
      <!-- Legend Panel -->
      <div class="legend-panel">
        <div class="panel-header">
          <span>图例说明</span>
        </div>
        
        <div class="legend-content">
          <div class="legend-item">
            <div class="legend-color" style="background-color: #409eff;"></div>
            <span>战术 (Tactic)</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background-color: #67c23a;"></div>
            <span>主技术 (Technique)</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background-color: #e6a23c;"></div>
            <span>子技术 (Sub-technique)</span>
          </div>
          <div class="legend-item">
            <div class="legend-line" style="border-top: 2px solid #909399;"></div>
            <span>归属关系</span>
          </div>
          <div class="legend-item">
            <div class="legend-line" style="border-top: 2px dashed #f56c6c;"></div>
            <span>攻击路径</span>
          </div>
        </div>
      </div>
      
      <!-- Attack Path Analysis -->
      <div class="path-panel">
        <div class="panel-header">
          <span>攻击路径分析</span>
        </div>
        
        <div class="path-content">
          <div class="empty-state" v-if="!selectedPath.length">
            <p>点击节点查看攻击路径</p>
          </div>
          <div v-else class="path-list">
            <div class="timeline">
              <div 
                v-for="(node, index) in selectedPath" 
                :key="index"
                class="timeline-item"
                :class="index === 0 ? 'timeline-start' : index === selectedPath.length - 1 ? 'timeline-end' : 'timeline-middle'"
              >
                <div class="path-node">
                  <strong>{{ node.name }}</strong>
                  <p class="path-node-id">{{ node.id }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Technique Detail Dialog -->
    <div class="dialog-overlay" v-if="detailDialogVisible">
      <div class="dialog-content">
        <div class="dialog-header">
          <h3>技术详情</h3>
          <button class="close-button" @click="detailDialogVisible = false">
            ×
          </button>
        </div>
        <div v-if="selectedTechnique" class="technique-detail">
          <h3>{{ selectedTechnique.name }}</h3>
          <p class="technique-id">ID: {{ selectedTechnique.id }}</p>
          <p class="technique-description">{{ selectedTechnique.description || '暂无描述' }}</p>
          <div class="technique-url" v-if="selectedTechnique.url">
            <a :href="selectedTechnique.url" target="_blank" class="tech-link">
              查看 MITRE 官方文档
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import {
  GraphChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { ElMessage } from 'element-plus'
import { getTactics, getAttackPaths } from '@/api/attack'

// Register ECharts components
use([
  GraphChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  CanvasRenderer
])

// State
const loading = ref(false)
const chartRef = ref<any>(null)

const tactics = ref<any[]>([])
const selectedTactic = ref('')
const physicsEnabled = ref(true)

const graphData = ref({
  nodes: [] as any[],
  edges: [] as any[],
  total_nodes: 0,
  total_edges: 0
})

const selectedNode = ref<any>(null)
const selectedPath = ref<any[]>([])
const detailDialogVisible = ref(false)
const selectedTechnique = ref<any>(null)
const debugInfo = ref('')
const debugDetails = ref('')

// Chart option computed property
const chartOption = computed(() => {
  // Create nodes and edges from graph data
  const nodes = graphData.value.nodes.map(node => ({
    id: node.id,
    name: node.name,
    symbolSize: node.type === 'tactic' ? 40 : 25,
    category: node.type === 'tactic' ? 0 : node.is_subtechnique ? 2 : 1,
    itemStyle: {
      color: node.type === 'tactic' ? '#409eff' : node.is_subtechnique ? '#e6a23c' : '#67c23a'
    },
    label: {
      show: true,
      formatter: '{b}',
      fontSize: node.type === 'tactic' ? 12 : 10
    },
    data: node
  }))
  
  const edges = graphData.value.edges.map(edge => ({
    source: edge.source,
    target: edge.target,
    lineStyle: {
      type: edge.type === 'belongs_to' ? 'solid' : 'dashed',
      color: edge.type === 'belongs_to' ? '#909399' : '#f56c6c',
      width: edge.type === 'belongs_to' ? 1 : 2
    }
  }))
  
  return {
    title: {
      text: '攻击路径图谱',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          return `<strong>${params.data.name}</strong><br/>ID: ${params.data.id}`
        }
        return ''
      }
    },
    legend: {
      data: ['战术', '主技术', '子技术'],
      bottom: 10
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: nodes,
        links: edges,
        categories: [
          { name: '战术', itemStyle: { color: '#409eff' } },
          { name: '主技术', itemStyle: { color: '#67c23a' } },
          { name: '子技术', itemStyle: { color: '#e6a23c' } }
        ],
        roam: true,
        draggable: true,
        focusNodeAdjacency: true,
        force: {
          repulsion: 300,
          gravity: 0.1,
          edgeLength: [50, 200],
          layoutAnimation: physicsEnabled.value
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        }
      }
    ]
  }
})

// Load tactics for filter
const loadTactics = async () => {
  try {
    const response = await getTactics()
    if (response && response.items) {
      tactics.value = response.items
    }
  } catch (error) {
    console.error('Error loading tactics:', error)
    ElMessage.error('加载战术数据失败')
  }
}

// Load graph data
const loadGraphData = async () => {
  console.log('Loading graph data...')
  loading.value = true
  
  try {
    const response = await getAttackPaths(selectedTactic.value || undefined)
    console.log('API Response:', response)
    
    if (response && response.nodes && response.edges) {
      graphData.value = {
        nodes: response.nodes,
        edges: response.edges,
        total_nodes: response.total_nodes || response.nodes.length,
        total_edges: response.total_edges || response.edges.length
      }
      loading.value = false
      console.log('Graph data loading completed')
      debugInfo.value = '数据加载成功'
      ElMessage.success('数据加载成功')
    } else {
      ElMessage.error('数据格式错误')
      loading.value = false
    }
  } catch (error) {
    console.error('Error loading graph data:', error)
    ElMessage.error('加载图数据失败')
    loading.value = false
  }
}

// Analyze attack path from selected node
const analyzeAttackPath = (nodeId: string) => {
  // Simple path analysis - find connected nodes
  const path = [graphData.value.nodes.find(n => n.id === nodeId)]
  
  // Find outgoing edges
  const outgoingEdges = graphData.value.edges.filter(e => e.source === nodeId && e.type === 'leads_to')
  
  // Add target nodes to path
  outgoingEdges.forEach(edge => {
    const targetNode = graphData.value.nodes.find(n => n.id === edge.target)
    if (targetNode && !path.find(p => p.id === targetNode.id)) {
      path.push(targetNode)
    }
  })
  
  selectedPath.value = path
}

// Handle chart click event
const handleChartClick = (params: any) => {
  console.log('Node clicked:', params)
  if (params.dataType === 'node') {
    selectedNode.value = params.data.data || params.data
    analyzeAttackPath(params.data.id)
  }
}

// Reset zoom
const resetZoom = () => {
  if (chartRef.value) {
    chartRef.value.chart.dispatchAction({
      type: 'restore'
    })
  }
}

// Toggle physics animation
const togglePhysics = () => {
  physicsEnabled.value = !physicsEnabled.value
  console.log('Physics enabled:', physicsEnabled.value)
}

// Handle filter change
const handleFilterChange = () => {
  loadGraphData()
}

// Refresh data
const refreshData = () => {
  loadGraphData()
}

// Show technique detail
const showTechniqueDetail = (technique: any) => {
  selectedTechnique.value = technique
  detailDialogVisible.value = true
}

// Debug graph
const debugGraph = () => {
  let details = ''
  
  // Check chart instance
  details += `Chart instance: ${chartRef.value ? 'Created' : 'Not created'}\n`
  
  // Check data
  details += `Nodes count: ${graphData.value.nodes.length}\n`
  details += `Edges count: ${graphData.value.edges.length}\n`
  details += `Nodes: ${JSON.stringify(graphData.value.nodes, null, 2)}\n`
  details += `Edges: ${JSON.stringify(graphData.value.edges, null, 2)}\n`
  details += `Chart option: ${JSON.stringify(chartOption.value, null, 2)}\n`
  
  debugDetails.value = details
  debugInfo.value = '调试信息已显示'
  
  console.log('Debug info:', details)
}

// Lifecycle hooks
onMounted(() => {
  console.log('Component mounted, initializing...')
  loadTactics()
  // Wait a bit for DOM to render before loading graph
  setTimeout(() => {
    console.log('Loading graph data after DOM render...')
    loadGraphData()
    // Auto debug after a short delay
    setTimeout(() => {
      console.log('Auto debugging...')
      debugGraph()
    }, 1000)
  }, 500)
})

onUnmounted(() => {
  // Cleanup if needed
})
</script>

<style scoped lang="scss">
.attack-graph-page {
  padding: 20px;
  display: grid;
  grid-template-columns: 1fr 300px;
  grid-gap: 20px;

  .page-header {
    grid-column: 1 / -1;
    margin-bottom: 20px;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

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
        gap: 10px;

        .filter-select {
          padding: 8px 12px;
          border: 1px solid #dcdfe6;
          border-radius: 4px;
          font-size: 14px;
          width: 180px;

          &:focus {
            outline: none;
            border-color: #409eff;
            box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
          }
        }

        .refresh-button {
          padding: 8px 16px;
          background-color: #409eff;
          color: white;
          border: none;
          border-radius: 4px;
          font-size: 14px;
          cursor: pointer;

          &:hover {
            background-color: #66b1ff;
          }

          &:disabled {
            background-color: #c0c4cc;
            cursor: not-allowed;
          }
        }
      }
    }
  }

  .graph-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;

    .graph-content {
      .graph-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #e4e7ed;

        .graph-stats {
          display: flex;
          gap: 10px;

          .stat-tag {
            padding: 4px 12px;
            background-color: #ecf5ff;
            color: #409eff;
            border-radius: 10px;
            font-size: 14px;
          }
        }

        .graph-controls {
          display: flex;
          gap: 10px;

          .control-button {
            padding: 6px 12px;
            background-color: #f5f7fa;
            color: #606266;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;

            &:hover {
              background-color: #ecf5ff;
              border-color: #c6e2ff;
            }
          }
        }
      }

      .graph-chart {
        height: 600px;
        background-color: #f5f7fa;
        border-radius: 8px;
        position: relative;

        .chart {
          width: 100% !important;
          height: 100% !important;
        }
      }

      .debug-info {
        margin-top: 20px;
        padding: 15px;
        background-color: #f0f0f0;
        border-radius: 8px;
        max-height: 300px;
        overflow-y: auto;

        h4 {
          margin: 0 0 10px 0;
          color: #303133;
        }

        pre {
          margin: 0;
          font-family: monospace;
          font-size: 12px;
          white-space: pre-wrap;
          color: #606266;
        }
      }
    }
  }

  .loading-container {
    grid-column: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 600px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    .loading-spinner {
      width: 40px;
      height: 40px;
      border: 4px solid #f3f3f3;
      border-top: 4px solid #409eff;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin-bottom: 10px;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    p {
      color: #606266;
      font-size: 14px;
    }
  }

  .right-panel {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .details-panel,
    .legend-panel,
    .path-panel {
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      padding: 16px;

      .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e4e7ed;

        span {
          font-size: 16px;
          font-weight: 500;
          color: #303133;
        }

        .close-button {
          background: none;
          border: none;
          font-size: 18px;
          color: #909399;
          cursor: pointer;

          &:hover {
            color: #606266;
          }
        }
      }
    }

    .details-panel {
      .node-details {
        h3 {
          margin: 0 0 10px 0;
          color: #303133;
          font-size: 18px;
        }

        .node-id {
          color: #909399;
          font-size: 14px;
          margin-bottom: 10px;
        }

        .node-type {
          margin-bottom: 15px;

          .type-tag {
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 12px;

            &.tactic-tag {
              background-color: #ecf5ff;
              color: #409eff;
            }

            &.technique-tag {
              background-color: #f0f9eb;
              color: #67c23a;
            }
          }
        }

        .node-description {
          color: #606266;
          line-height: 1.6;
          margin-bottom: 15px;
          font-size: 14px;
        }

        .node-actions {
          margin-top: 20px;

          .detail-button {
            padding: 6px 12px;
            background-color: #409eff;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;

            &:hover {
              background-color: #66b1ff;
            }
          }
        }
      }
    }

    .legend-panel {
      .legend-content {
        .legend-item {
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 10px;

          .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
          }

          .legend-line {
            width: 30px;
            height: 0;
          }

          span {
            font-size: 13px;
            color: #606266;
          }
        }
      }
    }

    .path-panel {
      .path-content {
        .empty-state {
          text-align: center;
          padding: 20px 0;
          color: #909399;
          font-size: 14px;
        }

        .path-list {
          .timeline {
            position: relative;
            padding-left: 20px;

            &::before {
              content: '';
              position: absolute;
              left: 8px;
              top: 0;
              bottom: 0;
              width: 2px;
              background-color: #e4e7ed;
            }

            .timeline-item {
              position: relative;
              margin-bottom: 15px;
              padding-left: 20px;

              &::before {
                content: '';
                position: absolute;
                left: -20px;
                top: 6px;
                width: 16px;
                height: 16px;
                border-radius: 50%;
                background-color: #dcdfe6;
              }

              &.timeline-start::before {
                background-color: #409eff;
              }

              &.timeline-end::before {
                background-color: #67c23a;
              }

              &.timeline-middle::before {
                background-color: #909399;
              }

              .path-node {
                strong {
                  color: #303133;
                  font-size: 14px;
                }

                .path-node-id {
                  color: #909399;
                  font-size: 12px;
                  margin: 5px 0 0 0;
                }
              }
            }
          }
        }
      }
    }
  }

  .dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;

    .dialog-content {
      background-color: white;
      border-radius: 8px;
      width: 600px;
      max-width: 90%;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

      .dialog-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px;
        border-bottom: 1px solid #e4e7ed;

        h3 {
          margin: 0;
          color: #303133;
          font-size: 18px;
        }

        .close-button {
          background: none;
          border: none;
          font-size: 18px;
          color: #909399;
          cursor: pointer;

          &:hover {
            color: #606266;
          }
        }
      }

      .technique-detail {
        padding: 20px;

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

        .technique-url {
          margin-top: 20px;

          .tech-link {
            color: #409eff;
            text-decoration: none;

            &:hover {
              text-decoration: underline;
            }
          }
        }
      }
    }
  }
}

@media (max-width: 1200px) {
  .attack-graph-page {
    grid-template-columns: 1fr;

    .right-panel {
      grid-column: 1;
      flex-direction: row;
      flex-wrap: wrap;

      .details-panel,
      .legend-panel,
      .path-panel {
        flex: 1;
        min-width: 250px;
      }
    }
  }
}

@media (max-width: 768px) {
  .attack-graph-page {
    padding: 10px;

    .right-panel {
      flex-direction: column;

      .details-panel,
      .legend-panel,
      .path-panel {
        min-width: auto;
      }
    }
  }
}
</style>
