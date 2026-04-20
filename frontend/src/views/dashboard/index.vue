<template>
  <div class="dashboard-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <span class="icon-house"></span>
            仪表板
          </h1>
          <p class="page-description">
            欢迎使用网络安全攻击知识库系统，基于MITRE ATT&CK框架的智能防御平台
          </p>
        </div>
        <div class="header-right">
          <div class="welcome-card">
            <div class="welcome-content">
              <div class="user-avatar">
                {{ userStore.username.charAt(0) }}
              </div>
              <div class="welcome-text">
                <p class="welcome-message">
                  {{ getGreeting() }}，{{ userStore.username }}
                </p>
                <p class="welcome-time">
                  <span class="icon-clock"></span>
                  {{ currentTime }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="statistics-section">
      <div class="stat-grid">
        <div class="stat-card tactic-card">
          <div class="stat-content">
            <div class="stat-icon">
              <span class="icon-collection"></span>
            </div>
            <div class="stat-info">
              <p class="stat-number">{{ stats.tactics }}</p>
              <p class="stat-label">战术 (Tactics)</p>
              <p class="stat-change positive">
                <span class="icon-arrow-up"></span>
                完整覆盖
              </p>
            </div>
          </div>
        </div>

        <div class="stat-card technique-card">
          <div class="stat-content">
            <div class="stat-icon">
              <span class="icon-folder-opened"></span>
            </div>
            <div class="stat-info">
              <p class="stat-number">{{ stats.techniques }}</p>
              <p class="stat-label">技术 (Techniques)</p>
              <p class="stat-change positive">
                <span class="icon-arrow-up"></span>
                {{ (stats.techniques / 300 * 100).toFixed(0) }}% 覆盖率
              </p>
            </div>
          </div>
        </div>

        <div class="stat-card actor-card">
          <div class="stat-content">
            <div class="stat-icon">
              <span class="icon-user"></span>
            </div>
            <div class="stat-info">
              <p class="stat-number">{{ actorStats.total }}</p>
              <p class="stat-label">威胁行为者</p>
              <p class="stat-change positive">
                <span class="icon-arrow-up"></span>
                包含 {{ actorStats.malware }} 种恶意软件
              </p>
            </div>
          </div>
        </div>

        <div class="stat-card rule-card">
          <div class="stat-content">
            <div class="stat-icon">
              <span class="icon-document-checked"></span>
            </div>
            <div class="stat-info">
              <p class="stat-number">{{ ruleStats.active }}</p>
              <p class="stat-label">检测规则</p>
              <p class="stat-change positive">
                <span class="icon-arrow-up"></span>
                {{ ruleStats.active }} 条活跃规则
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ATT&CK Matrix Chart -->
    <div class="chart-section">
      <div class="chart-card">
        <div class="card-header">
          <span>ATT&CK 框架矩阵分布</span>
          <button class="btn-text" @click="viewMatrix">
            <span class="icon-data-analysis"></span>
            查看详情
          </button>
        </div>
        <div class="matrix-chart">
          <div class="empty-state">
            <div class="empty-icon">
              <span class="icon-data-analysis"></span>
            </div>
            <p class="empty-description">攻击矩阵可视化图表</p>
            <button class="btn-primary" @click="viewMatrix">
              <span class="icon-eye"></span>
              点击查看完整矩阵
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity and Quick Actions -->
    <div class="content-section">
      <div class="content-grid">
        <!-- Recent Activity -->
        <div class="activity-card">
          <div class="card-header">
            <span>最新活动</span>
            <button class="btn-text">
              <span class="icon-more"></span>
              更多
            </button>
          </div>
          <div v-if="recentActivity.length > 0" class="activity-timeline">
            <div 
              v-for="(item, index) in recentActivity" 
              :key="index"
              class="timeline-item"
              :class="getActivityType(item.type)"
            >
              <div class="timeline-marker" :style="{ backgroundColor: getActivityColor(item.type) }"></div>
              <div class="timeline-content">
                <div class="timeline-title">{{ item.title }}</div>
                <div class="timeline-meta">
                  <span class="timeline-tag" :class="getMetaType(item.type)">{{ item.meta }}</span>
                  <span class="timeline-time">
                    <span class="icon-clock"></span>
                    {{ formatTime(item.time) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <p class="empty-description">暂无活动记录</p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="quick-actions-card">
          <div class="card-header">
            <span>快速操作</span>
            <button class="btn-text">
              <span class="icon-setting"></span>
              管理
            </button>
          </div>
          <div class="action-grid">
            <div 
              v-for="(action, index) in quickActions" 
              :key="index"
              class="action-card" 
              :class="action.color"
              @click="handleQuickAction(action)"
            >
              <div class="action-content">
                <div class="action-icon">
                  <span :class="'icon-' + action.icon.toLowerCase()"></span>
                </div>
                <div class="action-info">
                  <p class="action-title">{{ action.title }}</p>
                  <p class="action-description">{{ action.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- System Status -->
    <div class="system-status-section">
      <div class="status-card">
        <div class="card-header">
          <span>系统状态</span>
          <span class="status-tag success">运行正常</span>
        </div>
        <div class="status-grid">
          <div class="stat-item">
            <div class="stat-prefix">
              <span class="icon-connection success-icon"></span>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ systemStatus.database.connection }}ms</div>
              <div class="stat-label">数据库响应时间</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-prefix">
              <span class="icon-clock success-icon"></span>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ systemStatus.cache.hits }}ms</div>
              <div class="stat-label">缓存响应时间</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-prefix">
              <span class="icon-info warning-icon"></span>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ systemStatus.api.responseTime }}ms</div>
              <div class="stat-label">API响应时间</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-prefix">
              <span class="icon-timer success-icon"></span>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ systemStatus.sync.last }}</div>
              <div class="stat-label">数据同步时间</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// Data
const currentTime = ref('')
const stats = ref({
  tactics: 14,
  techniques: 250,
  subtechniques: 500,
  mitigations: 100,
  software: {
    total: 300,
    malware: 200,
    tools: 100
  },
  platforms: 8
})

const actorStats = ref({
  total: 100,
  malware: 85,
  tools: 45
})

const ruleStats = ref({
  active: 250,
  draft: 15,
  inactive: 10
})

const recentActivity = ref([
  {
    type: 'login',
    title: '系统登录成功',
    meta: '安全事件',
    time: '2026-01-15 09:30:00'
  },
  {
    type: 'sync',
    title: 'ATT&CK数据库同步',
    meta: '数据更新',
    time: '2026-01-14 23:00:00'
  },
  {
    type: 'rule',
    title: '新增检测规则',
    meta: '规则管理',
    time: '2026-01-14 16:45:00'
  }
])

const quickActions = ref([
  {
    title: 'ATT&CK矩阵',
    description: '查看完整ATT&CK攻击矩阵',
    icon: 'Collection',
    color: 'primary',
    action: 'visualization/matrix'
  },
  {
    title: '威胁行为者',
    description: '查看威胁行为者详情',
    icon: 'User',
    color: 'warning',
    action: 'actors'
  },
  {
    title: '检测规则',
    description: '管理检测规则库',
    icon: 'DocumentChecked',
    color: 'success',
    action: 'rules'
  },
  {
    title: '威胁情报',
    description: '查看最新威胁情报',
    icon: 'WarningFilled',
    color: 'danger',
    action: 'intelligence'
  }
])

const systemStatus = ref({
  database: {
    connection: 150
  },
  cache: {
    hits: 120
  },
  api: {
    responseTime: 80
  },
  sync: {
    last: '2026-01-14 23:00:00'
  }
})

// Methods
const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return '早上好'
  if (hour < 18) return '下午好'
  return '晚上好'
}

const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

const getActivityType = (type: string) => {
  const types = {
    login: 'primary',
    sync: 'success',
    rule: 'warning',
    report: 'info',
    actor: 'danger'
  }
  return types[type as keyof typeof types] || 'info'
}

const getActivityColor = (type: string) => {
  const colors = {
    login: '#409EFF',
    sync: '#67C23A',
    rule: '#E6A23C',
    report: '#909399',
    actor: '#F56C6C'
  }
  return colors[type as keyof typeof colors] || '#909399'
}

const getMetaType = (type: string) => {
  const types = {
    login: 'primary',
    sync: 'success',
    rule: 'warning',
    report: 'info',
    actor: 'danger'
  }
  return types[type as keyof typeof types] || 'info'
}

const viewMatrix = () => {
  router.push('/visualization/matrix')
}

const handleQuickAction = (action: any) => {
  router.push(`/${action.action}`)
}

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN')
}

let timer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 0;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* Page Header */
.page-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 30px;
  margin-bottom: 30px;
  
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
    
    .header-left {
      .page-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        
        .icon-house::before {
          content: '🏠';
          font-size: 24px;
        }
      }
      
      .page-description {
        font-size: 14px;
        opacity: 0.9;
        line-height: 1.5;
      }
    }
    
    .header-right {
      .welcome-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 20px;
        
        .welcome-content {
          display: flex;
          align-items: center;
          gap: 15px;
          
          .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #409EFF, #67C23A);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 600;
          }
          
          .welcome-text {
            .welcome-message {
              font-size: 16px;
              font-weight: 600;
              margin-bottom: 5px;
            }
            
            .welcome-time {
              font-size: 12px;
              opacity: 0.8;
              display: flex;
              align-items: center;
              gap: 5px;
              
              .icon-clock::before {
                content: '🕒';
              }
            }
          }
        }
      }
    }
  }
}

/* Statistics Cards */
.statistics-section {
  margin-bottom: 30px;
  
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .stat-card {
    background: #fff;
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 20px;
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .stat-content {
      display: flex;
      align-items: center;
      gap: 20px;
      
      .stat-icon {
        font-size: 48px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        
        .icon-collection::before {
          content: '📚';
        }
        
        .icon-folder-opened::before {
          content: '📁';
        }
        
        .icon-user::before {
          content: '👤';
        }
        
        .icon-document-checked::before {
          content: '✓';
          font-weight: bold;
        }
      }
      
      .stat-info {
        flex: 1;
        
        .stat-number {
          font-size: 32px;
          font-weight: 700;
          color: #303133;
          margin-bottom: 5px;
        }
        
        .stat-label {
          font-size: 14px;
          color: #606266;
          margin-bottom: 3px;
        }
        
        .stat-change {
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 5px;
          
          &.positive {
            color: #67C23A;
          }
          
          &.negative {
            color: #F56C6C;
          }
          
          .icon-arrow-up::before {
            content: '↑';
          }
        }
      }
    }
  }
  
  .tactic-card {
    border-left: 4px solid #667eea;
  }
  
  .technique-card {
    border-left: 4px solid #764ba2;
  }
  
  .actor-card {
    border-left: 4px solid #F56C6C;
  }
  
  .rule-card {
    border-left: 4px solid #67C23A;
  }
}

/* Matrix Chart */
.chart-section {
  margin-bottom: 30px;
  
  .chart-card {
    background: #fff;
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 1px solid #e4e7ed;
      
      .btn-text {
        background: none;
        border: none;
        color: #409EFF;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 14px;
        
        &:hover {
          text-decoration: underline;
        }
        
        .icon-data-analysis::before {
          content: '📊';
        }
      }
    }
    
    .matrix-chart {
      height: 400px;
      display: flex;
      align-items: center;
      justify-content: center;
      
      .empty-state {
        text-align: center;
        
        .empty-icon {
          font-size: 64px;
          margin-bottom: 15px;
          
          .icon-data-analysis::before {
            content: '📊';
          }
        }
        
        .empty-description {
          color: #909399;
          margin-bottom: 20px;
        }
        
        .btn-primary {
          background: #409EFF;
          color: #fff;
          border: none;
          border-radius: 4px;
          padding: 10px 20px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 5px;
          margin: 0 auto;
          
          &:hover {
            background: #66b1ff;
          }
          
          .icon-eye::before {
            content: '👁️';
          }
        }
      }
    }
  }
}

/* Content Section */
.content-section {
  margin-bottom: 30px;
  
  .content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 20px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .activity-card,
  .quick-actions-card {
    background: #fff;
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 1px solid #e4e7ed;
      
      .btn-text {
        background: none;
        border: none;
        color: #409EFF;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 14px;
        
        &:hover {
          text-decoration: underline;
        }
        
        .icon-more::before {
          content: '•••';
        }
        
        .icon-setting::before {
          content: '⚙️';
        }
      }
    }
  }
  
  .activity-timeline {
    .timeline-item {
      position: relative;
      padding-left: 30px;
      margin-bottom: 20px;
      
      &::before {
        content: '';
        position: absolute;
        left: 8px;
        top: 0;
        bottom: -20px;
        width: 2px;
        background: #e4e7ed;
      }
      
      &:last-child::before {
        display: none;
      }
      
      .timeline-marker {
        position: absolute;
        left: 0;
        top: 6px;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        z-index: 1;
      }
      
      .timeline-content {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        
        .timeline-title {
          font-size: 14px;
          color: #303133;
          margin-bottom: 10px;
        }
        
        .timeline-meta {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 12px;
          
          .timeline-tag {
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 12px;
            
            &.primary {
              background: #ecf5ff;
              color: #409EFF;
            }
            
            &.success {
              background: #f0f9eb;
              color: #67C23A;
            }
            
            &.warning {
              background: #fdf6ec;
              color: #E6A23C;
            }
            
            &.danger {
              background: #fef0f0;
              color: #F56C6C;
            }
            
            &.info {
              background: #f4f4f5;
              color: #909399;
            }
          }
          
          .timeline-time {
            display: flex;
            align-items: center;
            gap: 3px;
            color: #909399;
            
            .icon-clock::before {
              content: '🕒';
            }
          }
        }
      }
    }
  }
  
  .quick-actions-card {
    .action-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
    }
    
    .action-card {
      border: 1px solid #f0f0f0;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.3s;
      padding: 20px;
      
      &:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
      }
      
      .action-content {
        display: flex;
        align-items: center;
        gap: 15px;
        
        .action-icon {
          font-size: 32px;
          color: #667eea;
          
          .icon-collection::before {
            content: '📚';
          }
          
          .icon-user::before {
            content: '👤';
          }
          
          .icon-documentchecked::before {
            content: '✓';
            font-weight: bold;
          }
          
          .icon-warningfilled::before {
            content: '⚠️';
          }
        }
        
        .action-info {
          flex: 1;
          
          .action-title {
            font-size: 16px;
            font-weight: 600;
            color: #303133;
            margin-bottom: 3px;
          }
          
          .action-description {
            font-size: 12px;
            color: #909399;
            line-height: 1.4;
          }
        }
      }
      
      &.primary {
        border-left: 4px solid #667eea;
      }
      
      &.warning {
        border-left: 4px solid #E6A23C;
      }
      
      &.success {
        border-left: 4px solid #67C23A;
      }
      
      &.danger {
        border-left: 4px solid #F56C6C;
      }
    }
  }
}

/* System Status */
.system-status-section {
  .status-card {
    background: #fff;
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    margin-bottom: 30px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 1px solid #e4e7ed;
      
      .status-tag {
        padding: 4px 12px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 500;
        
        &.success {
          background: #f0f9eb;
          color: #67C23A;
        }
      }
    }
    
    .status-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
    }
    
    .stat-item {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      padding: 10px;
      
      .stat-prefix {
        .success-icon {
          color: #67C23A;
          font-size: 24px;
        }
        
        .warning-icon {
          color: #E6A23C;
          font-size: 24px;
        }
        
        .icon-connection::before {
          content: '🔗';
        }
        
        .icon-clock::before {
          content: '🕒';
        }
        
        .icon-info::before {
          content: 'ℹ️';
        }
        
        .icon-timer::before {
          content: '⏱️';
        }
      }
      
      .stat-content {
        text-align: left;
        
        .stat-value {
          font-size: 20px;
          font-weight: 600;
          color: #303133;
          margin-bottom: 4px;
        }
        
        .stat-label {
          font-size: 12px;
          color: #909399;
        }
      }
    }
  }
}

/* Responsive */
@media (max-width: 1200px) {
  .page-header {
    padding: 20px;
    
    .header-content {
      flex-direction: column;
      gap: 20px;
      align-items: center;
      text-align: center;
    }
  }
  
  .content-section {
    .content-grid {
      grid-template-columns: 1fr;
    }
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 15px;
    
    .page-title {
      font-size: 24px;
    }
  }
  
  .statistics-section {
    .stat-grid {
      padding: 0 10px;
    }
    
    .stat-card {
      .stat-content {
        flex-direction: column;
        text-align: center;
        
        .stat-icon {
          font-size: 36px;
        }
        
        .stat-info {
          .stat-number {
            font-size: 24px;
          }
        }
      }
    }
  }
  
  .chart-section {
    .chart-card {
      margin: 0 10px;
      
      .matrix-chart {
        height: 300px;
      }
    }
  }
  
  .content-section {
    .content-grid {
      padding: 0 10px;
    }
    
    .quick-actions-card {
      .action-grid {
        grid-template-columns: 1fr;
      }
    }
  }
  
  .system-status-section {
    .status-card {
      margin: 0 10px 30px;
      
      .status-grid {
        grid-template-columns: 1fr;
      }
    }
  }
}
</style>