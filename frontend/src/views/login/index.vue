<template>
  <div class="login-container">
    <div class="login-wrapper">
      <!-- Logo and title -->
      <div class="login-header">
        <div class="logo">
          <el-icon class="logo-icon"><Shield /></el-icon>
        </div>
        <h2 class="title">网络安全攻击知识库系统</h2>
        <p class="subtitle">基于MITRE ATT&CK框架的智能防御平台</p>
      </div>

      <!-- Login form -->
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            size="large"
            :prefix-icon="User"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            size="large"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item prop="remember">
          <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
        </el-form-item>

        <el-form-item class="form-actions">
          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <!-- Footer -->
      <div class="login-footer">
        <p>© 2026 网络安全攻击知识库系统. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import type { FormInstance } from 'element-plus'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  try {
    const valid = await loginFormRef.value?.validate()
    if (!valid) return

    loading.value = true
    await userStore.loginAction(loginForm)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.login-wrapper {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 40px 30px;
  width: 100%;
  max-width: 420px;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    animation: gradient 3s ease infinite;
  }
}

@keyframes gradient {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(20px); }
}

.login-header {
  text-align: center;
  margin-bottom: 30px;

  .logo {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;

    .logo-icon {
      font-size: 60px;
      color: #667eea;
      background: linear-gradient(135deg, #667eea, #764ba2);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
  }

  .title {
    font-size: 24px;
    font-weight: 700;
    color: #303133;
    margin-bottom: 8px;
  }

  .subtitle {
    font-size: 14px;
    color: #909399;
  }
}

.login-form {
  .el-form-item {
    margin-bottom: 24px;
  }

  .form-actions {
    margin-bottom: 0;
  }
}

.login-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  font-size: 16px;
  height: 44px;

  &:hover {
    background: linear-gradient(135deg, #764ba2, #667eea);
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }
}

.login-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;

  p {
    font-size: 12px;
    color: #909399;
    margin: 0;
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .login-container {
    padding: 10px;
  }

  .login-wrapper {
    padding: 30px 20px;
    margin: 10px;
  }

  .login-header {
    .logo {
      .logo-icon {
        font-size: 50px;
      }
    }

    .title {
      font-size: 20px;
    }

    .subtitle {
      font-size: 12px;
    }
  }
}

/* Animation */
.login-wrapper {
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
