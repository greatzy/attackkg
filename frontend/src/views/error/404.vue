<template>
  <div class="error-container">
    <div class="error-content">
      <!-- 404 Icon -->
      <div class="error-icon">
        <el-icon class="big-icon">
          <DocumentRemove />
        </el-icon>
      </div>

      <!-- Error Title -->
      <h1 class="error-title">404</h1>
      <h2 class="error-subtitle">页面未找到</h2>
      <p class="error-description">
        很抱歉，您访问的页面不存在或已被移动。
      </p>

      <!-- Error Details -->
      <div class="error-details">
        <el-alert
          :title="getErrorDetails()"
          type="warning"
          :closable="false"
          class="error-alert"
        />
      </div>

      <!-- Action Buttons -->
      <div class="error-actions">
        <el-button
          type="primary"
          size="large"
          @click="goHome"
          class="home-button"
        >
          <el-icon><House /></el-icon>
          返回首页
        </el-button>

        <el-button
          type="default"
          size="large"
          @click="goBack"
          class="back-button"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回上一页
        </el-button>
      </div>

      <!-- Quick Links -->
      <div class="quick-links">
        <h3>快速访问</h3>
        <el-row :gutter="10">
          <el-col :span="8" v-for="(link, index) in quickLinks" :key="index">
            <el-card class="link-card" @click="navigateTo(link.url)">
              <div class="link-content">
                <el-icon class="link-icon">
                  <component :is="link.icon" />
                </el-icon>
                <span class="link-text">{{ link.text }}</span>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- Animated Background -->
    <div class="error-background">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const errorInfo = ref<string | null>(null)

const getErrorDetails = () => {
  return '您可能输入了错误的网址，或者该页面已被移除。'
}

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    goHome()
  }
}

const navigateTo = (url: string) => {
  router.push(url)
  ElMessage.success('正在跳转...')
}

const quickLinks = ref([
  {
    icon: 'Collection',
    text: 'ATT&CK知识库',
    url: '/attack/tactics'
  },
  {
    icon: 'User',
    text: '威胁行为者',
    url: '/actors'
  },
  {
    icon: 'DataAnalysis',
    text: '可视化分析',
    url: '/visualization/matrix'
  },
  {
    icon: 'DocumentChecked',
    text: '检测规则',
    url: '/rules'
  },
  {
    icon: 'WarningFilled',
    text: '威胁情报',
    url: '/intelligence'
  },
  {
    icon: 'Document',
    text: '安全报告',
    url: '/reports'
  }
])

onMounted(() => {
  // Track 404 error
  console.error('404 Error: Page not found')
})
</script>

<style lang="scss" scoped>
.error-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
  position: relative;
  overflow: hidden;
}

.error-content {
  text-align: center;
  z-index: 10;
  position: relative;
  animation: fadeIn 1s ease-out;
}

/* Error Icon */
.error-icon {
  margin-bottom: 30px;
  
  .big-icon {
    font-size: 120px;
    color: rgba(255, 255, 255, 0.8);
    animation: rotate 6s linear infinite;
  }
}

/* Error Text */
.error-title {
  font-size: 80px;
  font-weight: 900;
  color: white;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.error-subtitle {
  font-size: 32px;
  font-weight: 600;
  color: white;
  margin-bottom: 15px;
}

.error-description {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 30px;
  line-height: 1.6;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

/* Error Details */
.error-details {
  margin-bottom: 30px;
  
  .error-alert {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    
    :deep(.el-alert__title) {
      color: white;
    }
    
    :deep(.el-alert__icon) {
      color: white;
    }
  }
}

/* Action Buttons */
.error-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 40px;
  
  .home-button {
    background: white;
    color: #667eea;
    border: none;
    padding: 12px 30px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.3s;
    
    &:hover {
      background: #f0f0f0;
      transform: translateY(-2px);
    }
  }
  
  .back-button {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 12px 30px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    backdrop-filter: blur(10px);
    transition: all 0.3s;
    
    &:hover {
      background: rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
    }
  }
}

/* Quick Links */
.quick-links {
  max-width: 800px;
  margin: 0 auto;
  
  h3 {
    font-size: 20px;
    font-weight: 600;
    color: white;
    margin-bottom: 20px;
  }
  
  .link-card {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      background: rgba(255, 255, 255, 0.2);
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    .link-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      
      .link-icon {
        font-size: 24px;
        color: white;
      }
      
      .link-text {
        font-size: 14px;
        color: white;
        font-weight: 500;
      }
    }
  }
}

/* Animated Background */
.error-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  
  .floating-shape {
    position: absolute;
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
    
    &.shape-1 {
      width: 100px;
      height: 100px;
      background: rgba(255, 255, 255, 0.1);
      top: 20%;
      left: 20%;
      animation-delay: 0s;
    }
    
    &.shape-2 {
      width: 150px;
      height: 150px;
      background: rgba(255, 255, 255, 0.05);
      top: 60%;
      right: 20%;
      animation-delay: 2s;
    }
    
    &.shape-3 {
      width: 80px;
      height: 80px;
      background: rgba(255, 255, 255, 0.15);
      bottom: 30%;
      left: 60%;
      animation-delay: 4s;
    }
  }
}

/* Responsive */
@media (max-width: 768px) {
  .error-content {
    padding: 20px;
  }
  
  .error-title {
    font-size: 60px;
  }
  
  .error-subtitle {
    font-size: 24px;
  }
  
  .error-description {
    font-size: 14px;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
    
    .home-button,
    .back-button {
      width: 100%;
      max-width: 300px;
    }
  }
  
  .quick-links {
    h3 {
      font-size: 18px;
    }
  }
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

/* Loading Effect */
.error-container {
  animation: backgroundShift 10s ease-in-out infinite;
}

@keyframes backgroundShift {
  0%, 100% {
    background: linear-gradient(135deg, #667eea, #764ba2);
  }
  50% {
    background: linear-gradient(135deg, #764ba2, #667eea);
  }
}
</style>
