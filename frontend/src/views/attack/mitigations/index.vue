<template>
  <div class="mitigations-container">
    <div class="data-card">
      <div class="card-header">
        <h2>缓解措施管理</h2>
        <div class="header-actions">
          <button class="btn btn-primary" @click="refreshData">
            <span class="icon-refresh"></span>
            刷新数据
          </button>
          <button class="btn btn-success" @click="showCreateForm = true">
            <span class="icon-plus"></span>
            添加缓解措施
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
              placeholder="搜索缓解措施名称或描述"
              class="form-input"
              @input="handleSearch"
            >
          </div>
          <div class="form-item">
            <label>版本</label>
            <input 
              type="text" 
              v-model="searchForm.version" 
              placeholder="版本"
              class="form-input"
              @input="handleSearch"
            >
          </div>
        </div>
      </div>
      
      <!-- 缓解措施列表 -->
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th class="checkbox-column">
                <input type="checkbox" v-model="selectAll" @change="handleSelectAll">
              </th>
              <th class="id-column">缓解ID</th>
              <th>缓解措施</th>
              <th>描述</th>
              <th class="number-column">关联技术</th>
              <th class="version-column">版本</th>
              <th class="action-column">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mitigation in paginatedMitigations" :key="mitigation.mitigation_id">
              <td class="checkbox-column">
                <input type="checkbox" v-model="selectedMitigations" :value="mitigation" @change="handleSelectOne">
              </td>
              <td class="id-column">{{ mitigation.mitigation_id }}</td>
              <td class="name-column">{{ mitigation.name }}</td>
              <td class="description-column">{{ mitigation.description }}</td>
              <td class="number-column">{{ mitigation.technique_count }}</td>
              <td class="version-column">{{ mitigation.version }}</td>
              <td class="action-column">
                <button class="btn btn-view" @click="viewMitigation(mitigation)">查看</button>
                <button class="btn btn-edit" @click="editMitigation(mitigation)">编辑</button>
                <button class="btn btn-delete" @click="deleteMitigation(mitigation)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- 空状态 -->
        <div v-if="paginatedMitigations.length === 0" class="empty-state">
          <p>暂无缓解措施数据</p>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
      
      <!-- 批量操作 -->
      <div v-if="selectedMitigations.length > 0" class="batch-actions">
        <span>已选择 {{ selectedMitigations.length }} 项</span>
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
          <h3>{{ showEditForm ? '编辑缓解措施' : '添加缓解措施' }}</h3>
          <button class="btn-close" @click="closeForm">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>缓解ID</label>
            <input type="text" v-model="formData.mitigation_id" class="form-input" required>
          </div>
          <div class="form-group">
            <label>名称</label>
            <input type="text" v-model="formData.name" class="form-input" required>
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="formData.description" class="form-textarea" rows="3" required></textarea>
          </div>
          <div class="form-group">
            <label>版本</label>
            <input type="text" v-model="formData.version" class="form-input" required>
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
import { ref, computed, onMounted } from 'vue'
import { getMitigations } from '@/api/attack'
import type { Mitigation } from '@/types'

// 响应式数据
const loading = ref(false)
const mitigations = ref<Mitigation[]>([])
const selectedMitigations = ref<Mitigation[]>([])
const selectAll = ref(false)
const searchForm = ref({
  search: '',
  version: ''
})
const pagination = ref({
  page: 1,
  per_page: 10,
  total: 0
})
const showCreateForm = ref(false)
const showEditForm = ref(false)
const formData = ref({
  mitigation_id: '',
  name: '',
  description: '',
  version: ''
})

// 从API获取缓解措施数据
const fetchMitigations = async () => {
  loading.value = true
  try {
    const response = await getMitigations({
      page: pagination.value.page,
      per_page: pagination.value.per_page,
      search: searchForm.value.search
    })
    
    // 确保response和response.items存在
    if (response && response.items) {
      mitigations.value = response.items.map((mitigation: any) => ({
        ...mitigation
      }))
      pagination.value.total = response.total || mitigations.value.length
    }
  } catch (error) {
    console.error('获取缓解措施数据失败:', error)
    // 如果API调用失败，使用默认数据
    mitigations.value = []
    pagination.value.total = 0
  } finally {
    loading.value = false
  }
}

// 计算属性
const filteredMitigations = computed(() => {
  return mitigations.value
})

const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.per_page)
})

const paginatedMitigations = computed(() => {
  return mitigations.value
})

// 搜索和刷新
const refreshData = async () => {
  searchForm.value = {
    search: '',
    version: ''
  }
  pagination.value.page = 1
  await fetchMitigations()
}

const handleSearch = async () => {
  pagination.value.page = 1
  await fetchMitigations()
}

// 选择操作
const handleSelectAll = () => {
  if (selectAll.value) {
    selectedMitigations.value = [...paginatedMitigations.value]
  } else {
    selectedMitigations.value = []
  }
}

const handleSelectOne = () => {
  selectAll.value = selectedMitigations.value.length === paginatedMitigations.value.length
}

// 分页操作
const changePage = async (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    pagination.value.page = page
    await fetchMitigations()
  }
}

const handlePageSizeChange = async () => {
  pagination.value.page = 1
  await fetchMitigations()
}

// 表单操作
const closeForm = () => {
  showCreateForm.value = false
  showEditForm.value = false
  formData.value = {
    mitigation_id: '',
    name: '',
    description: '',
    version: ''
  }
}

const submitForm = () => {
  if (!formData.value.mitigation_id || !formData.value.name || !formData.value.description || !formData.value.version) {
    alert('请填写所有必填字段')
    return
  }
  
  if (showEditForm.value) {
    // 编辑操作
    const index = mitigations.value.findIndex(m => m.mitigation_id === formData.value.mitigation_id)
    if (index !== -1) {
      mitigations.value[index] = {
        ...formData.value,
        technique_count: mitigations.value[index].technique_count
      }
    }
  } else {
    // 添加操作
    mitigations.value.push({
      ...formData.value,
      technique_count: Math.floor(Math.random() * 10) + 1
    })
  }
  
  closeForm()
  pagination.value.total = filteredMitigations.value.length
  alert(showEditForm.value ? '缓解措施更新成功' : '缓解措施添加成功')
}

const editMitigation = (mitigation: any) => {
  formData.value = { ...mitigation }
  showEditForm.value = true
  showCreateForm.value = false
}

// 查看操作
const viewMitigation = (mitigation: any) => {
  alert(`缓解措施详情：\nID: ${mitigation.mitigation_id}\n名称: ${mitigation.name}\n描述: ${mitigation.description}\n版本: ${mitigation.version}\n关联技术数: ${mitigation.technique_count}`)
}

// 删除操作
const deleteMitigation = (mitigation: any) => {
  if (confirm(`确定要删除缓解措施 ${mitigation.name} 吗？`)) {
    const index = mitigations.value.findIndex(m => m.mitigation_id === mitigation.mitigation_id)
    if (index !== -1) {
      mitigations.value.splice(index, 1)
      selectedMitigations.value = selectedMitigations.value.filter(m => m.mitigation_id !== mitigation.mitigation_id)
      pagination.value.total = filteredMitigations.value.length
      alert('缓解措施删除成功')
    }
  }
}

const batchDelete = () => {
  if (confirm(`确定要删除选中的 ${selectedMitigations.value.length} 个缓解措施吗？`)) {
    const idsToDelete = selectedMitigations.value.map(m => m.mitigation_id)
    mitigations.value = mitigations.value.filter(m => !idsToDelete.includes(m.mitigation_id))
    selectedMitigations.value = []
    selectAll.value = false
    pagination.value.total = filteredMitigations.value.length
    alert('批量删除成功')
  }
}

// 生命周期
onMounted(async () => {
  await fetchMitigations()
})
</script>
<style lang="scss" scoped>
.mitigations-container {
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
          
          .form-input {
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
        
        .number-column {
          width: 100px;
          text-align: center;
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
        
        .description-column {
          min-width: 300px;
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
  .mitigations-container {
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
          min-width: 800px;
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