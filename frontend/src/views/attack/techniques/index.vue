<template>
  <div class="techniques-container">
    <div class="data-card">
      <div class="card-header">
        <span>技术管理</span>
        <div class="header-buttons">
          <button class="refresh-button" @click="refreshData">
            刷新数据
          </button>
          <button class="create-button" @click="createTechnique">
            创建技术
          </button>
          <button class="delete-button" @click="deleteSelectedTechniques" :disabled="selectedTechniques.length === 0">
            批量删除
          </button>
        </div>
      </div>
      
      <!-- 搜索区域 -->
      <div class="search-form">
        <div class="form-item">
          <label>搜索</label>
          <input 
            v-model="searchForm.search" 
            placeholder="搜索技术名称或描述"
            class="search-input"
            @input="handleSearch"
          />
        </div>
        <div class="form-item">
          <label>战术</label>
          <select 
            v-model="searchForm.tactic_id" 
            class="select-input"
            @change="handleSearch"
          >
            <option value="">选择战术</option>
            <option 
              v-for="tactic in tacticOptions" 
              :key="tactic.tactic_id" 
              :value="tactic.tactic_id"
            >{{ tactic.tactic_id }} - {{ tactic.name }}</option>
          </select>
        </div>
        <div class="form-item">
          <label>平台</label>
          <select 
            v-model="searchForm.platform" 
            class="select-input"
            @change="handleSearch"
          >
            <option value="">选择平台</option>
            <option 
              v-for="platform in platformOptions" 
              :key="platform" 
              :value="platform"
            >{{ platform }}</option>
          </select>
        </div>
      </div>
      
      <!-- 技术列表 -->
      <div class="table-container" v-if="!loading">
        <table class="data-table">
          <thead>
            <tr>
              <th class="checkbox-column"><input type="checkbox" @change="selectAll" :checked="allSelected" /></th>
              <th class="id-column">技术ID</th>
              <th class="name-column">技术名称</th>
              <th class="tactic-column">所属战术</th>
              <th class="platform-column">适用平台</th>
              <th class="detection-column">检测方法</th>
              <th class="subtech-column">子技术数量</th>
              <th class="action-column">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="technique in filteredTechniques" :key="technique.technique_id">
              <td class="checkbox-column"><input type="checkbox" v-model="technique.selected" @change="handleSelectionChange" /></td>
              <td class="id-column">{{ technique.technique_id }}</td>
              <td class="name-column">{{ formatTechniqueName(technique) }}</td>
              <td class="tactic-column">{{ technique.tactic_name }}</td>
              <td class="platform-column">{{ formatPlatforms(technique) }}</td>
              <td class="detection-column">{{ technique.detection || '-' }}</td>
              <td class="subtech-column">{{ technique.subtechnique_count || 0 }}</td>
              <td class="action-column">
                <button class="view-button" @click="viewTechnique(technique)">
                  查看
                </button>
                <button class="edit-button" @click="editTechnique(technique)">
                  编辑
                </button>
                <button class="delete-button" @click="deleteTechnique(technique)">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- 无数据状态 -->
        <div class="empty-state" v-if="filteredTechniques.length === 0">
          <p>暂无技术数据</p>
        </div>
      </div>
      
      <!-- 加载状态 -->
      <div class="loading-state" v-else>
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <!-- 分页 -->
      <div class="pagination" v-if="!loading && filteredTechniques.length > 0">
        <span class="total">共 {{ filteredTechniques.length }} 条数据</span>
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
    
    <!-- 技术表单对话框 -->
    <div class="dialog-overlay" v-if="dialogVisible">
      <div class="dialog-content">
        <div class="dialog-header">
          <h3>{{ dialogTitle }}</h3>
          <button class="close-button" @click="dialogVisible = false">
            ×
          </button>
        </div>
        <form @submit.prevent="saveTechnique" class="technique-form">
          <div class="form-group">
            <label for="technique_id">技术ID *</label>
            <input 
              id="technique_id"
              v-model="techniqueForm.technique_id" 
              placeholder="请输入技术ID"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="name">技术名称 *</label>
            <input 
              id="name"
              v-model="techniqueForm.name" 
              placeholder="请输入技术名称"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="tactic_id">所属战术 *</label>
            <select 
              id="tactic_id"
              v-model="techniqueForm.tactic_id" 
              class="form-select"
              required
            >
              <option value="">请选择战术</option>
              <option 
                v-for="tactic in tacticOptions" 
                :key="tactic.tactic_id" 
                :value="tactic.tactic_id"
              >{{ tactic.tactic_id }} - {{ tactic.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="platforms">适用平台 *</label>
            <select 
              id="platforms"
              v-model="techniqueForm.platforms" 
              class="form-select"
              multiple
              required
            >
              <option 
                v-for="platform in platformOptions" 
                :key="platform" 
                :value="platform"
              >{{ platform }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="detection">检测方法</label>
            <textarea 
              id="detection"
              v-model="techniqueForm.detection" 
              placeholder="请输入检测方法"
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="description">描述 *</label>
            <textarea 
              id="description"
              v-model="techniqueForm.description" 
              placeholder="请输入技术描述"
              class="form-textarea"
              rows="5"
              required
            ></textarea>
          </div>
          <div class="dialog-footer">
            <button type="button" class="cancel-button" @click="dialogVisible = false">取消</button>
            <button type="submit" class="save-button">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Technique, Tactic } from '@/types'
import { getTechniques, getTactics } from '@/api/attack'

// 响应式数据
const loading = ref(false)
const techniques = ref<Technique[]>([])
const selectedTechniques = ref<Technique[]>([])
const tacticOptions = ref<Tactic[]>([])

const searchForm = ref({
  search: '',
  tactic_id: '',
  platform: ''
})

const pagination = ref({
  page: 1,
  per_page: 20,
  total: 0
})

// 平台选项
const platformOptions = ref([
  'Windows', 'Linux', 'macOS', 'iOS', 'Android', 'AWS', 'Azure', 'GCP'
])

// 对话框数据
const dialogVisible = ref(false)
const dialogTitle = ref('')
const techniqueForm = ref<Partial<Technique>>({
  technique_id: '',
  name: '',
  tactic_id: '',
  platforms: [] as string[],
  detection: '',
  description: ''
})
const currentTechniqueId = ref('')

// 计算属性
const filteredTechniques = computed(() => {
  return techniques.value
})

const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.per_page)
})

const allSelected = computed({
  get: () => techniques.value.length > 0 && techniques.value.every(technique => technique.selected),
  set: (value) => {
    techniques.value.forEach(technique => technique.selected = value)
    handleSelectionChange()
  }
})

// 从API获取技术数据
const fetchTechniques = async () => {
  loading.value = true
  try {
    const response = await getTechniques({
      page: pagination.value.page,
      per_page: pagination.value.per_page,
      search: searchForm.value.search,
      tactic_id: searchForm.value.tactic_id,
      platform: searchForm.value.platform
    })
    
    // 确保response和response.items存在
    if (response && response.items) {
      techniques.value = response.items.map((technique: any) => ({
        ...technique,
        selected: false
      }))
      pagination.value.total = response.total || techniques.value.length
    }
  } catch (error) {
    console.error('获取技术数据失败:', error)
    // 如果API调用失败，使用默认数据
    techniques.value = []
    pagination.value.total = 0
  } finally {
    loading.value = false
  }
}

// 从API获取战术数据用于下拉选择
const fetchTactics = async () => {
  try {
    const response = await getTactics()
    if (response && response.items) {
      tacticOptions.value = response.items
    }
  } catch (error) {
    console.error('获取战术数据失败:', error)
  }
}

// 搜索和刷新
const refreshData = async () => {
  searchForm.value = {
    search: '',
    tactic_id: '',
    platform: ''
  }
  pagination.value.page = 1
  await fetchTechniques()
}

const handleSearch = async () => {
  pagination.value.page = 1
  await fetchTechniques()
}

// 格式化显示
const formatTechniqueName = (row: Technique) => {
  return `${row.technique_id} - ${row.name}`
}

const formatPlatforms = (row: Technique) => {
  if (!row.platforms || row.platforms.length === 0) {
    return '-'
  }
  return row.platforms.join(', ')
}

// 表格操作
const handleSelectionChange = () => {
  selectedTechniques.value = techniques.value.filter(technique => technique.selected)
}

const selectAll = () => {
  // 由allSelected的setter处理
}

const viewTechnique = (row: Technique) => {
  console.log('查看技术:', row)
  alert(`技术详情: ${row.name}\n\n技术ID: ${row.technique_id}\n名称: ${row.name}\n战术: ${row.tactic_id} - ${row.tactic_name}\n平台: ${row.platforms?.join(', ') || '-'}\n子技术数量: ${row.subtechnique_count || 0}\n描述: ${row.description}`)
}

// 创建技术
const createTechnique = () => {
  dialogTitle.value = '创建技术'
  techniqueForm.value = {
    technique_id: '',
    name: '',
    tactic_id: '',
    platforms: [],
    detection: '',
    description: ''
  }
  currentTechniqueId.value = ''
  dialogVisible.value = true
}

// 编辑技术
const editTechnique = (row: Technique) => {
  dialogTitle.value = '编辑技术'
  techniqueForm.value = {
    ...row,
    platforms: row.platforms || []
  }
  currentTechniqueId.value = row.technique_id
  dialogVisible.value = true
}

// 保存技术
const saveTechnique = () => {
  if (!techniqueForm.value.technique_id || !techniqueForm.value.name || !techniqueForm.value.tactic_id || !techniqueForm.value.platforms || techniqueForm.value.platforms.length === 0 || !techniqueForm.value.description) {
    alert('请填写所有必填字段')
    return
  }
  
  if (currentTechniqueId.value) {
    // 更新技术
    const index = techniques.value.findIndex(t => t.technique_id === currentTechniqueId.value)
    if (index !== -1) {
      techniques.value[index] = {
        ...techniques.value[index],
        ...techniqueForm.value,
        selected: techniques.value[index].selected
      }
      alert('技术更新成功')
    }
  } else {
    // 创建技术
    const newTechnique: Technique = {
      ...techniqueForm.value as Technique,
      tactic_name: tacticOptions.value.find(t => t.tactic_id === techniqueForm.value.tactic_id)?.name || '',
      subtechnique_count: 0,
      selected: false
    }
    techniques.value.push(newTechnique)
    alert('技术创建成功')
  }
  
  dialogVisible.value = false
}

// 删除技术
const deleteTechnique = (row: Technique) => {
  if (confirm(`确定要删除技术 "${row.name}" 吗？`)) {
    const index = techniques.value.findIndex(t => t.technique_id === row.technique_id)
    if (index !== -1) {
      techniques.value.splice(index, 1)
      alert('技术删除成功')
    }
  }
}

// 批量删除技术
const deleteSelectedTechniques = () => {
  if (selectedTechniques.value.length === 0) return
  
  if (confirm(`确定要删除选中的 ${selectedTechniques.value.length} 个技术吗？`)) {
    const selectedIds = selectedTechniques.value.map(t => t.technique_id)
    techniques.value = techniques.value.filter(t => !selectedIds.includes(t.technique_id))
    selectedTechniques.value = []
    alert('技术删除成功')
  }
}

// 分页操作
const handleSizeChange = async () => {
  pagination.value.page = 1
  await fetchTechniques()
}

const prevPage = async () => {
  if (pagination.value.page > 1) {
    pagination.value.page--
    await fetchTechniques()
  }
}

const nextPage = async () => {
  if (pagination.value.page < totalPages.value) {
    pagination.value.page++
    await fetchTechniques()
  }
}

// 生命周期
onMounted(async () => {
  // 加载战术数据用于下拉选择
  await fetchTactics()
  // 加载技术数据
  await fetchTechniques()
})
</script>

<style lang="scss" scoped>
.techniques-container {
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
      
      .header-buttons {
        display: flex;
        gap: 10px;
        
        button {
          padding: 8px 16px;
          border: none;
          border-radius: 4px;
          font-size: 14px;
          cursor: pointer;
          
          &.refresh-button {
            background-color: #409eff;
            color: white;
            
            &:hover {
              background-color: #66b1ff;
            }
          }
          
          &.create-button {
            background-color: #67c23a;
            color: white;
            
            &:hover {
              background-color: #85ce61;
            }
          }
          
          &.delete-button {
            background-color: #f56c6c;
            color: white;
            
            &:hover:not(:disabled) {
              background-color: #f78989;
            }
            
            &:disabled {
              opacity: 0.6;
              cursor: not-allowed;
            }
          }
        }
      }
    }
    
    .search-form {
      display: flex;
      gap: 15px;
      margin-bottom: 20px;
      padding: 15px;
      background: #f5f7fa;
      border-radius: 6px;
      flex-wrap: wrap;
      
      .form-item {
        display: flex;
        align-items: center;
        gap: 10px;
        
        label {
          font-size: 14px;
          color: #606266;
          white-space: nowrap;
        }
        
        .search-input,
        .select-input {
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
        
        .search-input {
          width: 300px;
        }
        
        .select-input {
          width: 200px;
        }
      }
    }
    
    .table-container {
      margin-bottom: 20px;
      overflow-x: auto;
      
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
          min-width: 200px;
        }
        
        .tactic-column {
          width: 150px;
        }
        
        .platform-column {
          width: 200px;
        }
        
        .detection-column {
          min-width: 200px;
        }
        
        .subtech-column {
          width: 100px;
          text-align: center;
        }
        
        .action-column {
          width: 200px;
          text-align: center;
          
          button {
            padding: 4px 10px;
            border: none;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;
            margin-right: 5px;
            
            &.view-button {
              background-color: #409eff;
              color: white;
              
              &:hover {
                background-color: #66b1ff;
              }
            }
            
            &.edit-button {
              background-color: #e6a23c;
              color: white;
              
              &:hover {
                background-color: #ebb563;
              }
            }
            
            &.delete-button {
              background-color: #f56c6c;
              color: white;
              
              &:hover {
                background-color: #f78989;
              }
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
      width: 800px;
      max-width: 90%;
      max-height: 90vh;
      overflow-y: auto;
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
      
      .technique-form {
        padding: 20px;
        
        .form-group {
          margin-bottom: 16px;
          
          label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            color: #606266;
            font-weight: 500;
          }
          
          .form-input,
          .form-select,
          .form-textarea {
            width: 100%;
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
          
          .form-textarea {
            resize: vertical;
          }
        }
        
        .dialog-footer {
          display: flex;
          justify-content: flex-end;
          gap: 10px;
          margin-top: 20px;
          
          button {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            
            &.cancel-button {
              background-color: #f5f7fa;
              color: #606266;
              
              &:hover {
                background-color: #ecf5ff;
                color: #409eff;
              }
            }
            
            &.save-button {
              background-color: #409eff;
              color: white;
              
              &:hover {
                background-color: #66b1ff;
              }
            }
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .techniques-container {
    padding: 10px;
    
    .data-card {
      padding: 15px;
      
      .card-header {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
        
        .header-buttons {
          justify-content: center;
          flex-wrap: wrap;
        }
      }
      
      .search-form {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
        
        .form-item {
          flex-direction: column;
          align-items: stretch;
          gap: 5px;
          
          .search-input,
          .select-input {
            width: 100%;
          }
        }
      }
      
      .table-container {
        .data-table {
          font-size: 12px;
          
          th, td {
            padding: 8px;
          }
          
          .action-column {
            button {
              padding: 2px 6px;
              font-size: 11px;
              margin-right: 3px;
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
    
    .dialog-overlay {
      .dialog-content {
        width: 95%;
        max-height: 95vh;
        
        .technique-form {
          padding: 15px;
        }
      }
    }
  }
}
</style>