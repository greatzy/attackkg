<template>
  <div class="software-container">
    <div class="data-card">
      <div class="card-header">
        <h2>软件管理</h2>
        <div class="header-actions">
          <button class="btn btn-primary" @click="refreshData">
            <span class="icon-refresh"></span>
            刷新数据
          </button>
          <button class="btn btn-success" @click="showCreateForm = true">
            <span class="icon-plus"></span>
            添加软件
          </button>
        </div>
      </div>
      
      <!-- 搜索区域 -->
      <div class="search-form">
        <div class="form-row">
          <div class="form-item">
            <label>搜索</label>
            <input 
              type="text" 
              v-model="searchForm.search" 
              placeholder="搜索软件名称或描述"
              class="form-input"
              @input="handleSearch"
            >
          </div>
          <div class="form-item">
            <label>类型</label>
            <select 
              v-model="searchForm.type" 
              class="form-select"
              @change="handleSearch"
            >
              <option value="">全部</option>
              <option value="malware">恶意软件</option>
              <option value="tool">工具</option>
            </select>
          </div>
          <div class="form-item">
            <label>平台</label>
            <select 
              v-model="searchForm.platform" 
              class="form-select"
              @change="handleSearch"
            >
              <option value="">全部</option>
              <option v-for="platform in platformOptions" :key="platform" :value="platform">
                {{ platform }}
              </option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- 软件列表 -->
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th class="checkbox-column">
                <input type="checkbox" v-model="selectAll" @change="handleSelectAll">
              </th>
              <th class="id-column">软件ID</th>
              <th>软件名称</th>
              <th class="type-column">类型</th>
              <th>适用平台</th>
              <th>别名</th>
              <th class="version-column">版本</th>
              <th class="action-column">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="software in paginatedSoftware" :key="software.software_id">
              <td class="checkbox-column">
                <input type="checkbox" v-model="selectedSoftware" :value="software" @change="handleSelectOne">
              </td>
              <td class="id-column">{{ software.software_id }}</td>
              <td class="name-column">{{ software.name }}</td>
              <td class="type-column">{{ software.type === 'malware' ? '恶意软件' : '工具' }}</td>
              <td class="platforms-column">{{ software.platforms ? software.platforms.join(', ') : '-' }}</td>
              <td class="aliases-column">{{ software.aliases ? software.aliases.join(', ') : '-' }}</td>
              <td class="version-column">{{ software.version }}</td>
              <td class="action-column">
                <button class="btn btn-view" @click="viewSoftware(software)">查看</button>
                <button class="btn btn-edit" @click="editSoftware(software)">编辑</button>
                <button class="btn btn-delete" @click="deleteSoftware(software)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- 空状态 -->
        <div v-if="paginatedSoftware.length === 0" class="empty-state">
          <p>暂无软件数据</p>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
      
      <!-- 批量操作 -->
      <div v-if="selectedSoftware.length > 0" class="batch-actions">
        <span>已选择 {{ selectedSoftware.length }} 项</span>
        <button class="btn btn-danger" @click="batchDelete">批量删除</button>
      </div>
      
      <!-- 分页 -->
      <div class="pagination">
        <div class="pagination-info">
          共 {{ pagination.total }} 条记录，每页 {{ pagination.per_page }} 条
        </div>
        <div class="pagination-controls">
          <button class="btn btn-sm" @click="changePage(pagination.page - 1)" :disabled="pagination.page === 1">上一页</button>
          <span class="page-info">{{ pagination.page }} / {{ totalPages }}</span>
          <button class="btn btn-sm" @click="changePage(pagination.page + 1)" :disabled="pagination.page === totalPages">下一页</button>
          <select v-model="pagination.per_page" @change="handlePageSizeChange" class="form-select">
            <option value="10">10条/页</option>
            <option value="20">20条/页</option>
            <option value="50">50条/页</option>
            <option value="100">100条/页</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- 添加/编辑表单 -->
    <div v-if="showCreateForm || showEditForm" class="modal-overlay" @click="closeForm">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ showEditForm ? '编辑软件' : '添加软件' }}</h3>
          <button class="btn-close" @click="closeForm">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>软件ID</label>
            <input type="text" v-model="formData.software_id" class="form-input" required>
          </div>
          <div class="form-group">
            <label>名称</label>
            <input type="text" v-model="formData.name" class="form-input" required>
          </div>
          <div class="form-group">
            <label>类型</label>
            <select v-model="formData.type" class="form-select" required>
              <option value="malware">恶意软件</option>
              <option value="tool">工具</option>
            </select>
          </div>
          <div class="form-group">
            <label>适用平台</label>
            <div class="platform-checkboxes">
              <label v-for="platform in platformOptions" :key="platform" class="checkbox-label">
                <input 
                  type="checkbox" 
                  :value="platform" 
                  v-model="formData.platforms"
                >
                {{ platform }}
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>别名</label>
            <input type="text" v-model="formData.aliasesInput" class="form-input" placeholder="多个别名用逗号分隔">
          </div>
          <div class="form-group">
            <label>版本</label>
            <input type="text" v-model="formData.version" class="form-input" required>
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="formData.description" class="form-textarea" rows="3" required></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeForm">取消</button>
          <button class="btn btn-primary" @click="submitForm">{{ showEditForm ? '更新' : '保存' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { getSoftware } from '@/api/attack'
import type { Software } from '@/types'

// 平台选项
const platformOptions = [
  'Windows', 'Linux', 'macOS', 'iOS', 'Android', 'AWS', 'Azure', 'GCP'
]

// 响应式数据
const loading = ref(false)
const software = ref<Software[]>([])
const selectedSoftware = ref<Software[]>([])
const selectAll = ref(false)
const searchForm = ref({
  search: '',
  type: '',
  platform: ''
})
const pagination = ref({
  page: 1,
  per_page: 10,
  total: 0
})
const showCreateForm = ref(false)
const showEditForm = ref(false)
const formData = ref({
  software_id: '',
  name: '',
  type: 'malware',
  platforms: [] as string[],
  aliases: [] as string[],
  aliasesInput: '',
  version: '',
  description: ''
})

// 监听别名输入
watch(() => formData.value.aliasesInput, (newValue) => {
  if (newValue) {
    formData.value.aliases = newValue.split(',').map(item => item.trim()).filter(item => item)
  } else {
    formData.value.aliases = []
  }
})

// 从API获取软件数据
const fetchSoftware = async () => {
  loading.value = true
  try {
    const response = await getSoftware({
      page: pagination.value.page,
      per_page: pagination.value.per_page,
      search: searchForm.value.search,
      type: searchForm.value.type
    })
    
    // 确保response和response.items存在
    if (response && response.items) {
      software.value = response.items.map((item: any) => ({
        ...item
      }))
      pagination.value.total = response.total || software.value.length
    }
  } catch (error) {
    console.error('获取软件数据失败:', error)
    // 如果API调用失败，使用默认数据
    software.value = []
    pagination.value.total = 0
  } finally {
    loading.value = false
  }
}

// 计算属性
const filteredSoftware = computed(() => {
  return software.value
})

const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.per_page)
})

const paginatedSoftware = computed(() => {
  return software.value
})

// 搜索和刷新
const refreshData = async () => {
  searchForm.value = {
    search: '',
    type: '',
    platform: ''
  }
  pagination.value.page = 1
  await fetchSoftware()
}

const handleSearch = async () => {
  pagination.value.page = 1
  await fetchSoftware()
}

// 选择操作
const handleSelectAll = () => {
  if (selectAll.value) {
    selectedSoftware.value = [...paginatedSoftware.value]
  } else {
    selectedSoftware.value = []
  }
}

const handleSelectOne = () => {
  selectAll.value = selectedSoftware.value.length === paginatedSoftware.value.length
}

// 分页操作
const changePage = async (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    pagination.value.page = page
    await fetchSoftware()
  }
}

const handlePageSizeChange = async () => {
  pagination.value.page = 1
  await fetchSoftware()
}

// 表单操作
const closeForm = () => {
  showCreateForm.value = false
  showEditForm.value = false
  formData.value = {
    software_id: '',
    name: '',
    type: 'malware',
    platforms: [],
    aliases: [],
    aliasesInput: '',
    version: '',
    description: ''
  }
}

const submitForm = () => {
  if (!formData.value.software_id || !formData.value.name || !formData.value.type || formData.value.platforms.length === 0 || !formData.value.version || !formData.value.description) {
    alert('请填写所有必填字段')
    return
  }
  
  if (showEditForm.value) {
    // 编辑操作
    const index = software.value.findIndex(s => s.software_id === formData.value.software_id)
    if (index !== -1) {
      software.value[index] = {
        ...formData.value,
        aliases: formData.value.aliases
      }
    }
  } else {
    // 添加操作
    software.value.push({
      ...formData.value,
      aliases: formData.value.aliases
    })
  }
  
  closeForm()
  pagination.value.total = filteredSoftware.value.length
  alert(showEditForm.value ? '软件更新成功' : '软件添加成功')
}

const editSoftware = (item: any) => {
  formData.value = {
    ...item,
    aliasesInput: item.aliases.join(', ')
  }
  showEditForm.value = true
  showCreateForm.value = false
}

// 查看操作
const viewSoftware = (item: any) => {
  alert(`软件详情：\nID: ${item.software_id}\n名称: ${item.name}\n类型: ${item.type === 'malware' ? '恶意软件' : '工具'}\n平台: ${item.platforms.join(', ')}\n别名: ${item.aliases.join(', ')}\n版本: ${item.version}\n描述: ${item.description}`)
}

// 删除操作
const deleteSoftware = (item: any) => {
  if (confirm(`确定要删除软件 ${item.name} 吗？`)) {
    const index = software.value.findIndex(s => s.software_id === item.software_id)
    if (index !== -1) {
      software.value.splice(index, 1)
      selectedSoftware.value = selectedSoftware.value.filter(s => s.software_id !== item.software_id)
      pagination.value.total = filteredSoftware.value.length
      alert('软件删除成功')
    }
  }
}

const batchDelete = () => {
  if (confirm(`确定要删除选中的 ${selectedSoftware.value.length} 个软件吗？`)) {
    const idsToDelete = selectedSoftware.value.map(s => s.software_id)
    software.value = software.value.filter(s => !idsToDelete.includes(s.software_id))
    selectedSoftware.value = []
    selectAll.value = false
    pagination.value.total = filteredSoftware.value.length
    alert('批量删除成功')
  }
}

// 生命周期
onMounted(async () => {
  await fetchSoftware()
})
</script>
<style lang="scss" scoped>
.software-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
  
  .data-card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px;
      background: #f8f9fa;
      border-bottom: 1px solid #e4e7ed;
      
      h2 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        color: #303133;
      }
      
      .header-actions {
        display: flex;
        gap: 10px;
      }
    }
    
    .search-form {
      padding: 20px;
      background: #fafafa;
      border-bottom: 1px solid #e4e7ed;
      
      .form-row {
        display: flex;
        gap: 20px;
        align-items: flex-end;
        
        .form-item {
          flex: 1;
          min-width: 200px;
          
          label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #606266;
          }
          
          .form-input,
          .form-select {
            width: 100%;
            padding: 10px;
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
    
    .table-container {
      position: relative;
      
      .data-table {
        width: 100%;
        border-collapse: collapse;
        
        th,
        td {
          padding: 12px 16px;
          text-align: left;
          border-bottom: 1px solid #ebeef5;
        }
        
        th {
          background: #f5f7fa;
          font-weight: 600;
          color: #303133;
          font-size: 14px;
        }
        
        tr:hover {
          background: #f5f7fa;
        }
        
        .checkbox-column {
          width: 40px;
          text-align: center;
        }
        
        .id-column {
          width: 100px;
        }
        
        .type-column {
          width: 80px;
        }
        
        .version-column {
          width: 80px;
        }
        
        .action-column {
          width: 180px;
          text-align: center;
          
          .btn {
            margin: 0 4px;
          }
        }
        
        .name-column {
          min-width: 200px;
        }
        
        .platforms-column,
        .aliases-column {
          min-width: 150px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }
      
      .empty-state {
        padding: 60px 0;
        text-align: center;
        color: #909399;
      }
      
      .loading-state {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.8);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        
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
      }
    }
    
    .batch-actions {
      padding: 15px 20px;
      background: #fafafa;
      border-top: 1px solid #e4e7ed;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .pagination {
      padding: 20px;
      background: #f8f9fa;
      border-top: 1px solid #e4e7ed;
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .pagination-info {
        color: #606266;
        font-size: 14px;
      }
      
      .pagination-controls {
        display: flex;
        align-items: center;
        gap: 10px;
        
        .btn-sm {
          padding: 4px 12px;
          font-size: 12px;
        }
        
        .page-info {
          min-width: 80px;
          text-align: center;
          color: #606266;
        }
        
        .form-select {
          padding: 4px 8px;
          border: 1px solid #dcdfe6;
          border-radius: 4px;
          font-size: 12px;
        }
      }
    }
  }
  
  // 按钮样式
  .btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    
    &:hover {
      opacity: 0.9;
    }
    
    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    
    &.btn-primary {
      background: #409eff;
      color: #fff;
    }
    
    &.btn-success {
      background: #67c23a;
      color: #fff;
    }
    
    &.btn-danger {
      background: #f56c6c;
      color: #fff;
    }
    
    &.btn-secondary {
      background: #909399;
      color: #fff;
    }
    
    &.btn-view {
      background: #1890ff;
      color: #fff;
    }
    
    &.btn-edit {
      background: #52c41a;
      color: #fff;
    }
    
    &.btn-delete {
      background: #ff4d4f;
      color: #fff;
    }
    
    .icon-plus::before {
      content: '+';
      font-weight: bold;
      font-size: 16px;
    }
    
    .icon-refresh {
      animation: rotate 2s linear infinite;
      
      &::before {
        content: '⟳';
      }
      
      @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    }
  }
  
  // 模态框
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: #fff;
    border-radius: 8px;
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px;
      border-bottom: 1px solid #e4e7ed;
      
      h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
      }
      
      .btn-close {
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
        color: #909399;
        
        &:hover {
          color: #606266;
        }
      }
    }
    
    .modal-body {
      padding: 20px;
      
      .form-group {
        margin-bottom: 15px;
        
        label {
          display: block;
          margin-bottom: 8px;
          font-weight: 500;
          color: #606266;
        }
        
        .form-input,
        .form-select,
        .form-textarea {
          width: 100%;
          padding: 10px;
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
        
        .platform-checkboxes {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          
          .checkbox-label {
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 5px 10px;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            cursor: pointer;
            
            &:hover {
              background: #f5f7fa;
            }
          }
        }
      }
    }
    
    .modal-footer {
      padding: 20px;
      border-top: 1px solid #e4e7ed;
      display: flex;
      justify-content: flex-end;
      gap: 10px;
    }
  }
}

@media (max-width: 768px) {
  .software-container {
    padding: 10px;
    
    .data-card {
      .card-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
        
        .header-actions {
          width: 100%;
          justify-content: space-between;
        }
      }
      
      .search-form {
        .form-row {
          flex-direction: column;
          align-items: stretch;
          gap: 15px;
        }
      }
      
      .table-container {
        overflow-x: auto;
        
        .data-table {
          min-width: 1000px;
        }
      }
      
      .pagination {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
        
        .pagination-controls {
          justify-content: center;
        }
      }
    }
  }
}
</style>