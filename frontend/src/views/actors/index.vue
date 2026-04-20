<template>
  <div class="actors-container">
    <div class="card">
      <div class="card-header">
        <h2>威胁行为者管理</h2>
        <div class="header-buttons">
          <button class="btn primary" @click="refreshData">
            刷新数据
          </button>
          <button class="btn success" @click="createActor">
            创建行为者
          </button>
        </div>
      </div>
      
      <!-- 搜索区域 -->
      <div class="search-form">
        <input 
          v-model="searchForm.search" 
          placeholder="搜索行为者名称或别名"
          class="search-input"
        />
        <input 
          v-model="searchForm.origin" 
          placeholder="来源地"
          class="search-input small"
        />
        <input 
          v-model="searchForm.motivation" 
          placeholder="动机"
          class="search-input small"
        />
      </div>
      
      <!-- 行为者列表 -->
      <div class="actors-table">
        <div class="table-header">
          <div class="header-cell">行为者ID</div>
          <div class="header-cell">行为者名称</div>
          <div class="header-cell">来源地</div>
          <div class="header-cell">动机</div>
          <div class="header-cell">首次发现</div>
          <div class="header-cell">最近活动</div>
          <div class="header-cell">使用技术</div>
          <div class="header-cell">使用软件</div>
          <div class="header-cell">操作</div>
        </div>
        <div class="table-body">
          <div v-for="actor in actors" :key="actor.actor_id" class="table-row">
            <div class="table-cell">{{ actor.actor_id }}</div>
            <div class="table-cell">{{ actor.name }}</div>
            <div class="table-cell">{{ actor.origin || '-' }}</div>
            <div class="table-cell">{{ actor.motivation || '-' }}</div>
            <div class="table-cell">{{ actor.first_seen || '-' }}</div>
            <div class="table-cell">{{ actor.last_seen || '-' }}</div>
            <div class="table-cell">{{ actor.technique_count || 0 }}</div>
            <div class="table-cell">{{ actor.software_count || 0 }}</div>
            <div class="table-cell">
              <button class="btn small primary" @click="viewActor(actor)">
                查看
              </button>
              <button class="btn small warning" @click="editActor(actor)">
                编辑
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 行为者表单对话框 -->
    <div v-if="dialogVisible" class="dialog-overlay" @click="dialogVisible = false">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>{{ dialogTitle }}</h3>
          <button class="dialog-close" @click="dialogVisible = false">×</button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label>行为者ID</label>
            <input v-model="actorForm.actor_id" placeholder="请输入行为者ID" class="form-input" />
          </div>
          <div class="form-group">
            <label>行为者名称</label>
            <input v-model="actorForm.name" placeholder="请输入行为者名称" class="form-input" />
          </div>
          <div class="form-group">
            <label>来源地</label>
            <input v-model="actorForm.origin" placeholder="请输入来源地" class="form-input" />
          </div>
          <div class="form-group">
            <label>动机</label>
            <input v-model="actorForm.motivation" placeholder="请输入动机" class="form-input" />
          </div>
          <div class="form-group">
            <label>首次发现</label>
            <input v-model="actorForm.first_seen" placeholder="请输入首次发现时间" class="form-input" />
          </div>
          <div class="form-group">
            <label>最近活动</label>
            <input v-model="actorForm.last_seen" placeholder="请输入最近活动时间" class="form-input" />
          </div>
          <div class="form-group">
            <label>别名</label>
            <textarea v-model="actorForm.aliases" placeholder="请输入别名，多个别名用逗号分隔" class="form-textarea" rows="3" />
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="actorForm.description" placeholder="请输入行为者描述" class="form-textarea" rows="5" />
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn" @click="dialogVisible = false">取消</button>
          <button class="btn primary" @click="saveActor">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 响应式数据
const loading = ref(false)
const actors = ref<any[]>([])
const searchForm = ref({
  search: '',
  origin: '',
  motivation: ''
})

// 对话框数据
const dialogVisible = ref(false)
const dialogTitle = ref('')
const actorForm = ref({
  actor_id: '',
  name: '',
  origin: '',
  motivation: '',
  first_seen: '',
  last_seen: '',
  aliases: '',
  description: ''
})

// 搜索和刷新
const refreshData = () => {
  searchForm.value = {
    search: '',
    origin: '',
    motivation: ''
  }
  loadActors()
}

// 加载行为者数据
const loadActors = async () => {
  loading.value = true
  try {
    // 使用模拟数据
    const mockActors = [
      {
        actor_id: 'APT1',
        name: 'APT1',
        origin: 'China',
        motivation: 'Espionage',
        first_seen: '2006',
        last_seen: '2014',
        technique_count: 25,
        software_count: 10,
        aliases: 'Comment Crew, Shanghai Group',
        description: 'APT1是一个来自中国的高级持续性威胁组织，主要针对政府、军事和企业目标进行网络间谍活动。'
      },
      {
        actor_id: 'Lazarus',
        name: 'Lazarus Group',
        origin: 'North Korea',
        motivation: 'Financial Gain, Espionage',
        first_seen: '2009',
        last_seen: '2024',
        technique_count: 30,
        software_count: 15,
        aliases: 'Hidden Cobra, Guardians of Peace',
        description: 'Lazarus Group是来自朝鲜的黑客组织，以网络攻击和金融诈骗活动而闻名。'
      },
      {
        actor_id: 'APT29',
        name: 'APT29',
        origin: 'Russia',
        motivation: 'Espionage',
        first_seen: '2014',
        last_seen: '2024',
        technique_count: 40,
        software_count: 20,
        aliases: 'Cozy Bear, The Dukes',
        description: 'APT29是来自俄罗斯的高级持续性威胁组织，主要针对政府和外交机构进行网络间谍活动。'
      }
    ]
    
    actors.value = mockActors
    console.log('数据加载成功')
  } catch (error: any) {
    console.error('加载行为者数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 查看行为者
const viewActor = (row: any) => {
  alert(`行为者ID: ${row.actor_id}\n名称: ${row.name}\n来源地: ${row.origin || '-'}\n动机: ${row.motivation || '-'}\n首次发现: ${row.first_seen || '-'}\n最近活动: ${row.last_seen || '-'}\n使用技术: ${row.technique_count || 0}\n使用软件: ${row.software_count || 0}\n别名: ${row.aliases || '-'}\n描述: ${row.description}`)
}

// 创建行为者
const createActor = () => {
  dialogTitle.value = '创建威胁行为者'
  actorForm.value = {
    actor_id: '',
    name: '',
    origin: '',
    motivation: '',
    first_seen: '',
    last_seen: '',
    aliases: '',
    description: ''
  }
  dialogVisible.value = true
}

// 编辑行为者
const editActor = (row: any) => {
  dialogTitle.value = '编辑威胁行为者'
  actorForm.value = { ...row }
  dialogVisible.value = true
}

// 保存行为者
const saveActor = () => {
  alert('行为者保存成功')
  dialogVisible.value = false
  loadActors()
}

// 生命周期
onMounted(() => {
  loadActors()
})
</script>

<style lang="scss" scoped>
.actors-container {
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
      display: flex;
      gap: 10px;
      padding: 15px 20px;
      background: #f5f7fa;
      border-bottom: 1px solid #e4e7ed;
      
      .search-input {
        padding: 8px 12px;
        border: 1px solid #dcdfe6;
        border-radius: 4px;
        font-size: 14px;
        
        &.small {
          width: 150px;
        }
        
        &:first-child {
          flex: 1;
          max-width: 300px;
        }
      }
    }
    
    .actors-table {
      .table-header {
        display: flex;
        background: #f8f9fa;
        border-bottom: 1px solid #e4e7ed;
        
        .header-cell {
          padding: 12px 10px;
          font-weight: 600;
          font-size: 14px;
          color: #606266;
          border-right: 1px solid #e4e7ed;
          text-align: center;
          
          &:first-child {
            width: 120px;
          }
          
          &:nth-child(2) {
            flex: 1;
            min-width: 200px;
            text-align: left;
          }
          
          &:nth-child(3),
          &:nth-child(4) {
            width: 150px;
          }
          
          &:nth-child(5),
          &:nth-child(6) {
            width: 120px;
          }
          
          &:nth-child(7),
          &:nth-child(8) {
            width: 100px;
          }
          
          &:last-child {
            width: 150px;
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
            padding: 12px 10px;
            font-size: 14px;
            color: #303133;
            border-right: 1px solid #e4e7ed;
            text-align: center;
            
            &:first-child {
              width: 120px;
            }
            
            &:nth-child(2) {
              flex: 1;
              min-width: 200px;
              text-align: left;
            }
            
            &:nth-child(3),
            &:nth-child(4) {
              width: 150px;
            }
            
            &:nth-child(5),
            &:nth-child(6) {
              width: 120px;
            }
            
            &:nth-child(7),
            &:nth-child(8) {
              width: 100px;
            }
            
            &:last-child {
              width: 150px;
              border-right: none;
              display: flex;
              gap: 8px;
              justify-content: center;
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
    width: 800px;
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

@media (max-width: 768px) {
  .actors-container {
    padding: 10px;
    
    .card {
      .search-form {
        flex-direction: column;
        align-items: stretch;
        
        .search-input {
          &.small {
            width: 100%;
          }
        }
      }
      
      .actors-table {
        .table-header {
          display: none;
        }
        
        .table-body {
          .table-row {
            flex-direction: column;
            padding: 10px;
            
            .table-cell {
              border-right: none;
              border-bottom: 1px solid #e4e7ed;
              text-align: left;
              width: 100% !important;
              
              &:last-child {
                border-bottom: none;
                justify-content: flex-start;
              }
            }
          }
        }
      }
    }
    
    .dialog {
      width: 95%;
    }
  }
}
</style>