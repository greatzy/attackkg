<template>
  <div class="tactics-container">
    <div class="data-card">
      <div class="card-header">
        <span>战术管理</span>
        <button class="refresh-button" @click="refreshData">
          刷新数据
        </button>
      </div>
      
      <!-- 搜索区域 -->
      <div class="search-form">
        <div class="form-item">
          <label>搜索</label>
          <input 
            v-model="searchForm.search" 
            placeholder="搜索战术名称或描述"
            class="search-input"
            @input="handleSearch"
          />
        </div>
      </div>
      
      <!-- 战术列表 -->
      <div class="table-container" v-if="!loading">
        <table class="data-table">
          <thead>
            <tr>
              <th class="checkbox-column"><input type="checkbox" @change="selectAll" :checked="allSelected" /></th>
              <th class="id-column">战术ID</th>
              <th class="name-column">战术名称</th>
              <th class="short-name-column">简写</th>
              <th class="description-column">描述</th>
              <th class="count-column">技术数量</th>
              <th class="version-column">版本</th>
              <th class="action-column">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tactic in filteredTactics" :key="tactic.tactic_id">
              <td class="checkbox-column"><input type="checkbox" v-model="tactic.selected" @change="handleSelectionChange" /></td>
              <td class="id-column">{{ tactic.tactic_id }}</td>
              <td class="name-column">{{ formatTacticName(tactic) }}</td>
              <td class="short-name-column">{{ tactic.short_name }}</td>
              <td class="description-column">{{ tactic.description }}</td>
              <td class="count-column">{{ tactic.technique_count }}</td>
              <td class="version-column">{{ tactic.version }}</td>
              <td class="action-column">
                <button class="view-button" @click="viewTactic(tactic)">
                  查看
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- 无数据状态 -->
        <div class="empty-state" v-if="filteredTactics.length === 0">
          <p>暂无战术数据</p>
        </div>
      </div>
      
      <!-- 加载状态 -->
      <div class="loading-state" v-else>
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <!-- 分页 -->
      <div class="pagination" v-if="!loading && filteredTactics.length > 0">
        <span class="total">共 {{ filteredTactics.length }} 条数据</span>
        <div class="page-controls">
          <button 
            class="page-button" 
            @click="prevPage" 
            :disabled="pagination.page === 1"
          >
            上一页
          </button>
          <span class="page-info">
            第 {{ pagination.page }} 页，共 {{ totalPages }} 页
          </span>
          <button 
            class="page-button" 
            @click="nextPage" 
            :disabled="pagination.page === totalPages"
          >
            下一页
          </button>
          <select v-model="pagination.per_page" @change="handleSizeChange" class="page-size-select">
            <option value="10">10条/页</option>
            <option value="20">20条/页</option>
            <option value="50">50条/页</option>
            <option value="100">100条/页</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Tactic } from '@/types'
import { getTactics } from '@/api/attack'

// 响应式数据
const loading = ref(false)
const tactics = ref<Tactic[]>([])
const selectedTactics = ref<Tactic[]>([])
const searchForm = ref({
  search: '',
  version: ''
})
const pagination = ref({
  page: 1,
  per_page: 20,
  total: 0
})

// 计算属性
const filteredTactics = computed(() => {
  return tactics.value
})

const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.per_page)
})

const allSelected = computed({
  get: () => tactics.value.length > 0 && tactics.value.every(tactic => tactic.selected),
  set: (value) => {
    tactics.value.forEach(tactic => tactic.selected = value)
    handleSelectionChange()
  }
})

// 搜索和刷新
const refreshData = async () => {
  searchForm.value = {
    search: '',
    version: ''
  }
  pagination.value.page = 1
  await fetchTactics()
}

const handleSearch = async () => {
  pagination.value.page = 1
  await fetchTactics()
}

// 从API获取战术数据
const fetchTactics = async () => {
  loading.value = true
  try {
    const response = await getTactics({
      page: pagination.value.page,
      per_page: pagination.value.per_page,
      search: searchForm.value.search
    })
    
    // 确保response和response.items存在
    if (response && response.items) {
      tactics.value = response.items.map((tactic: any) => ({
        ...tactic,
        selected: false
      }))
      pagination.value.total = response.total || tactics.value.length
    }
  } catch (error) {
    console.error('获取战术数据失败:', error)
    // 如果API调用失败，使用默认数据
    tactics.value = [
      {
        tactic_id: 'TA0001',
        name: '初始访问',
        short_name: 'Initial Access',
        description: '获取对网络的初始访问权限',
        technique_count: 12,
        version: '1.0',
        selected: false
      },
      {
        tactic_id: 'TA0002',
        name: '执行',
        short_name: 'Execution',
        description: '在目标系统上执行代码',
        technique_count: 8,
        version: '1.0',
        selected: false
      }
    ]
    pagination.value.total = tactics.value.length
  } finally {
    loading.value = false
  }
}

// 格式化战术名称
const formatTacticName = (row: Tactic) => {
  return `${row.name || row.tactic_id}`
}

// 表格操作
const handleSelectionChange = () => {
  selectedTactics.value = tactics.value.filter(tactic => tactic.selected)
}

const selectAll = () => {
  // 由allSelected的setter处理
}

const viewTactic = (row: Tactic) => {
  console.log('查看战术:', row)
  alert(`战术详情: ${row.name}\n\n战术ID: ${row.tactic_id}\n名称: ${row.name}\n描述: ${row.description}\n简写: ${row.short_name}\n版本: ${row.version}\n技术数量: ${row.technique_count}`)
}

// 分页操作
const handleSizeChange = async () => {
  pagination.value.page = 1
  await fetchTactics()
}

const prevPage = async () => {
  if (pagination.value.page > 1) {
    pagination.value.page--
    await fetchTactics()
  }
}

const nextPage = async () => {
  if (pagination.value.page < totalPages.value) {
    pagination.value.page++
    await fetchTactics()
  }
}

// 生命周期
onMounted(async () => {
  await fetchTactics()
})
</script>

<style lang="scss" scoped>
.tactics-container {
  padding: 20px;
  
  .data-card {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 1px solid #e4e7ed;
      
      span {
        font-size: 18px;
        font-weight: 500;
        color: #303133;
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
      }
    }
    
    .search-form {
      margin-bottom: 20px;
      padding: 15px;
      background: #f5f7fa;
      border-radius: 6px;
      
      .form-item {
        display: flex;
        align-items: center;
        gap: 10px;
        
        label {
          font-size: 14px;
          color: #606266;
          white-space: nowrap;
        }
        
        .search-input {
          flex: 1;
          max-width: 300px;
          padding: 8px 12px;
          border: 1px solid #dcdfe6;
          border-radius: 4px;
          font-size: 14px;
          
          &:focus {
            outline: none;
            border-color: #409eff;
            box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
          }
        }
      }
    }
    
    .table-container {
      margin-bottom: 20px;
      
      .data-table {
        width: 100%;
        border-collapse: collapse;
        
        th, td {
          padding: 12px;
          text-align: left;
          border-bottom: 1px solid #e4e7ed;
        }
        
        th {
          background-color: #f8f9fa;
          font-weight: 500;
          color: #303133;
          font-size: 14px;
        }
        
        td {
          color: #606266;
          font-size: 14px;
        }
        
        .checkbox-column {
          width: 50px;
          text-align: center;
        }
        
        .id-column {
          width: 120px;
        }
        
        .name-column {
          min-width: 180px;
        }
        
        .short-name-column {
          width: 100px;
        }
        
        .description-column {
          min-width: 200px;
        }
        
        .count-column {
          width: 100px;
          text-align: center;
        }
        
        .version-column {
          width: 80px;
          text-align: center;
        }
        
        .action-column {
          width: 100px;
          text-align: center;
          
          .view-button {
            padding: 4px 12px;
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
      
      .empty-state {
        text-align: center;
        padding: 40px 0;
        color: #909399;
        font-size: 14px;
      }
    }
    
    .loading-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px 0;
      
      .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #409eff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 10px;
      }
      
      p {
        color: #606266;
        font-size: 14px;
      }
      
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    }
    
    .pagination {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 15px;
      border-top: 1px solid #e4e7ed;
      
      .total {
        color: #606266;
        font-size: 14px;
      }
      
      .page-controls {
        display: flex;
        align-items: center;
        gap: 10px;
        
        .page-button {
          padding: 4px 12px;
          background-color: #f5f7fa;
          color: #606266;
          border: 1px solid #dcdfe6;
          border-radius: 4px;
          font-size: 14px;
          cursor: pointer;
          
          &:hover:not(:disabled) {
            background-color: #ecf5ff;
            border-color: #c6e2ff;
            color: #409eff;
          }
          
          &:disabled {
            opacity: 0.6;
            cursor: not-allowed;
          }
        }
        
        .page-info {
          color: #606266;
          font-size: 14px;
        }
        
        .page-size-select {
          padding: 4px 8px;
          border: 1px solid #dcdfe6;
          border-radius: 4px;
          font-size: 14px;
          
          &:focus {
            outline: none;
            border-color: #409eff;
            box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .tactics-container {
    padding: 10px;
    
    .data-card {
      padding: 15px;
      
      .search-form {
        .form-item {
          flex-direction: column;
          align-items: stretch;
          gap: 5px;
          
          .search-input {
            max-width: none;
          }
        }
      }
      
      .table-container {
        overflow-x: auto;
        
        .data-table {
          font-size: 12px;
          
          th, td {
            padding: 8px;
          }
          
          .action-column {
            .view-button {
              padding: 2px 8px;
              font-size: 11px;
            }
          }
        }
      }
      
      .pagination {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
        
        .page-controls {
          justify-content: center;
          flex-wrap: wrap;
        }
      }
    }
  }
}
</style>
