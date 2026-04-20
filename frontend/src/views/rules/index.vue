<template>
  <div class="rules-container">
    <div class="card">
      <div class="card-header">
        <h2>检测规则管理</h2>
        <div class="header-buttons">
          <button class="btn primary" @click="refreshData">
            刷新数据
          </button>
          <button class="btn success" @click="createRule">
            创建规则
          </button>
        </div>
      </div>
      
      <!-- 搜索区域 -->
      <div class="search-form">
        <input 
          v-model="searchForm.search" 
          placeholder="搜索规则名称或描述"
          class="search-input"
        />
      </div>
      
      <!-- 规则列表 -->
      <div class="rules-table">
        <div class="table-header">
          <div class="header-cell">规则ID</div>
          <div class="header-cell">规则名称</div>
          <div class="header-cell">类型</div>
          <div class="header-cell">严重程度</div>
          <div class="header-cell">状态</div>
          <div class="header-cell">操作</div>
        </div>
        <div class="table-body">
          <div v-for="rule in rules" :key="rule.id" class="table-row">
            <div class="table-cell">{{ rule.id }}</div>
            <div class="table-cell">{{ rule.name }}</div>
            <div class="table-cell">{{ rule.rule_type }}</div>
            <div class="table-cell">{{ rule.severity }}</div>
            <div class="table-cell">{{ rule.status }}</div>
            <div class="table-cell">
              <button class="btn small primary" @click="viewRule(rule)">
                查看
              </button>
              <button class="btn small warning" @click="editRule(rule)">
                编辑
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 规则表单对话框 -->
    <div v-if="dialogVisible" class="dialog-overlay" @click="dialogVisible = false">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>{{ dialogTitle }}</h3>
          <button class="dialog-close" @click="dialogVisible = false">×</button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label>规则名称</label>
            <input v-model="ruleForm.name" placeholder="请输入规则名称" class="form-input" />
          </div>
          <div class="form-group">
            <label>规则类型</label>
            <select v-model="ruleForm.rule_type" class="form-select">
              <option value="">请选择规则类型</option>
              <option value="sigma">Sigma</option>
              <option value="yara">YARA</option>
              <option value="snort">Snort</option>
            </select>
          </div>
          <div class="form-group">
            <label>严重程度</label>
            <select v-model="ruleForm.severity" class="form-select">
              <option value="low">低</option>
              <option value="medium">中</option>
              <option value="high">高</option>
            </select>
          </div>
          <div class="form-group">
            <label>状态</label>
            <select v-model="ruleForm.status" class="form-select">
              <option value="active">活跃</option>
              <option value="draft">草稿</option>
            </select>
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="ruleForm.description" placeholder="请输入规则描述" class="form-textarea" rows="3" />
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn" @click="dialogVisible = false">取消</button>
          <button class="btn primary" @click="saveRule">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 响应式数据
const loading = ref(false)
const rules = ref<any[]>([])
const searchForm = ref({
  search: ''
})

// 对话框数据
const dialogVisible = ref(false)
const dialogTitle = ref('')
const ruleForm = ref({
  id: '',
  name: '',
  rule_type: '',
  severity: 'medium',
  status: 'active',
  description: ''
})

// 搜索和刷新
const refreshData = () => {
  searchForm.value = {
    search: ''
  }
  loadRules()
}

// 加载规则数据
const loadRules = async () => {
  loading.value = true
  try {
    // 使用模拟数据
    const mockRules = [
      {
        id: 1,
        name: '检测PowerShell异常执行',
        rule_type: 'sigma',
        severity: 'high',
        status: 'active',
        description: '检测PowerShell执行异常命令'
      },
      {
        id: 2,
        name: '检测SQL注入攻击',
        rule_type: 'snort',
        severity: 'medium',
        status: 'active',
        description: '检测SQL注入攻击尝试'
      },
      {
        id: 3,
        name: '检测暴力破解攻击',
        rule_type: 'suricata',
        severity: 'high',
        status: 'active',
        description: '检测SSH暴力破解攻击'
      }
    ]
    
    rules.value = mockRules
    console.log('数据加载成功')
  } catch (error: any) {
    console.error('加载规则数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 查看规则
const viewRule = (row: any) => {
  alert(`规则名称: ${row.name}\n类型: ${row.rule_type}\n严重程度: ${row.severity}\n状态: ${row.status}\n描述: ${row.description}`)
}

// 创建规则
const createRule = () => {
  dialogTitle.value = '创建规则'
  ruleForm.value = {
    id: '',
    name: '',
    rule_type: '',
    severity: 'medium',
    status: 'active',
    description: ''
  }
  dialogVisible.value = true
}

// 编辑规则
const editRule = (row: any) => {
  dialogTitle.value = '编辑规则'
  ruleForm.value = { ...row }
  dialogVisible.value = true
}

// 保存规则
const saveRule = () => {
  alert('规则保存成功')
  dialogVisible.value = false
  loadRules()
}

// 生命周期
onMounted(() => {
  loadRules()
})
</script>

<style lang="scss" scoped>
.rules-container {
  padding: 20px;
  
  .card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px;
      border-bottom: 1px solid #e4e7ed;
      
      h2 {
        margin: 0;
        font-size: 18px;
        color: #303133;
      }
      
      .header-buttons {
        display: flex;
        gap: 10px;
      }
    }
    
    .search-form {
      padding: 15px 20px;
      background: #f5f7fa;
      border-bottom: 1px solid #e4e7ed;
      
      .search-input {
        width: 300px;
        padding: 8px 12px;
        border: 1px solid #dcdfe6;
        border-radius: 4px;
        font-size: 14px;
      }
    }
    
    .rules-table {
      .table-header {
        display: flex;
        background: #f8f9fa;
        border-bottom: 1px solid #e4e7ed;
        
        .header-cell {
          padding: 12px 15px;
          font-weight: 600;
          font-size: 14px;
          color: #606266;
          border-right: 1px solid #e4e7ed;
          
          &:last-child {
            border-right: none;
          }
        }
      }
      
      .table-body {
        .table-row {
          display: flex;
          border-bottom: 1px solid #e4e7ed;
          
          &:hover {
            background: #f5f7fa;
          }
          
          .table-cell {
            padding: 12px 15px;
            font-size: 14px;
            color: #303133;
            border-right: 1px solid #e4e7ed;
            
            &:last-child {
              border-right: none;
              display: flex;
              gap: 8px;
            }
          }
        }
      }
    }
  }
  
  .btn {
    padding: 6px 12px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background: white;
    color: #606266;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      color: #409eff;
      border-color: #c6e2ff;
      background: #ecf5ff;
    }
    
    &.primary {
      background: #409eff;
      border-color: #409eff;
      color: white;
      
      &:hover {
        background: #66b1ff;
        border-color: #66b1ff;
      }
    }
    
    &.success {
      background: #67c23a;
      border-color: #67c23a;
      color: white;
      
      &:hover {
        background: #85ce61;
        border-color: #85ce61;
      }
    }
    
    &.warning {
      background: #e6a23c;
      border-color: #e6a23c;
      color: white;
      
      &:hover {
        background: #ebb563;
        border-color: #ebb563;
      }
    }
    
    &.small {
      padding: 4px 8px;
      font-size: 12px;
    }
  }
  
  .dialog-overlay {
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
  
  .dialog {
    background: white;
    border-radius: 8px;
    width: 600px;
    max-width: 90%;
    
    .dialog-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px;
      border-bottom: 1px solid #e4e7ed;
      
      h3 {
        margin: 0;
        font-size: 16px;
        color: #303133;
      }
      
      .dialog-close {
        background: none;
        border: none;
        font-size: 20px;
        color: #909399;
        cursor: pointer;
        
        &:hover {
          color: #606266;
        }
      }
    }
    
    .dialog-body {
      padding: 20px;
      
      .form-group {
        margin-bottom: 15px;
        
        label {
          display: block;
          margin-bottom: 5px;
          font-size: 14px;
          color: #606266;
        }
        
        .form-input,
        .form-select,
        .form-textarea {
          width: 100%;
          padding: 8px 12px;
          border: 1px solid #dcdfe6;
          border-radius: 4px;
          font-size: 14px;
        }
        
        .form-textarea {
          resize: vertical;
        }
      }
    }
    
    .dialog-footer {
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      padding: 20px;
      border-top: 1px solid #e4e7ed;
    }
  }
}
</style>
