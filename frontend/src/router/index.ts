import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// Configure NProgress
NProgress.configure({ showSpinner: false })

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { public: true, title: '登录' }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '首页', icon: 'HomeFilled' }
      },
      {
        path: 'attack',
        name: 'AttackKnowledge',
        meta: { title: 'ATT&CK知识库', icon: 'Collection' },
        children: [
          {
            path: 'tactics',
            name: 'Tactics',
            component: () => import('@/views/attack/tactics/index.vue'),
            meta: { title: '战术管理' }
          },
          {
            path: 'techniques',
            name: 'Techniques',
            component: () => import('@/views/attack/techniques/index.vue'),
            meta: { title: '技术管理' }
          },
          {
            path: 'mitigations',
            name: 'Mitigations',
            component: () => import('@/views/attack/mitigations/index.vue'),
            meta: { title: '缓解措施' }
          },
          {
            path: 'software',
            name: 'Software',
            component: () => import('@/views/attack/software/index.vue'),
            meta: { title: '软件管理' }
          }
        ]
      },
      {
        path: 'actors',
        name: 'ThreatActors',
        component: () => import('@/views/actors/index.vue'),
        meta: { title: '威胁行为者', icon: 'UserFilled' }
      },
      {
        path: 'rules',
        name: 'DetectionRules',
        component: () => import('@/views/rules/index.vue'),
        meta: { title: '检测规则', icon: 'DocumentChecked' }
      },
      {
        path: 'visualization',
        name: 'Visualization',
        meta: { title: '可视化分析', icon: 'DataAnalysis' },
        children: [
          {
            path: 'matrix',
            name: 'AttackMatrix',
            component: () => import('@/views/visualization/matrix/index.vue'),
            meta: { title: 'ATT&CK矩阵' }
          },
          {
            path: 'graph',
            name: 'AttackGraph',
            component: () => import('@/views/visualization/graph/index.vue'),
            meta: { title: '攻击路径图谱' }
          }
        ]
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/reports/index.vue'),
        meta: { title: '安全报告', icon: 'Document' }
      },
      {
        path: 'intelligence',
        name: 'Intelligence',
        component: () => import('@/views/intelligence/index.vue'),
        meta: { title: '威胁情报', icon: 'WarningFilled' }
      },
      {
        path: 'system',
        name: 'System',
        meta: { title: '系统管理', icon: 'Setting' },
        children: [
          {
            path: 'users',
            name: 'Users',
            component: () => import('@/views/system/users/index.vue'),
            meta: { title: '用户管理' }
          },
          {
            path: 'roles',
            name: 'Roles',
            component: () => import('@/views/system/roles/index.vue'),
            meta: { title: '角色管理' }
          },
          {
            path: 'logs',
            name: 'Logs',
            component: () => import('@/views/system/logs/index.vue'),
            meta: { title: '日志审计' }
          }
        ]
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  NProgress.start()
  
  // Set page title
  document.title = to.meta.title ? `${to.meta.title} - 网络安全攻击知识库系统` : '网络安全攻击知识库系统'
  
  // For testing purposes, skip authentication check
  // This will allow access to all routes without login
  next()
  
  /*
  const userStore = useUserStore()
  
  // Check if route requires authentication
  if (!to.meta.public) {
    if (!userStore.token) {
      next('/login')
      return
    }
    
    // Get user info if not loaded
    if (!userStore.userInfo) {
      try {
        await userStore.getUserInfo()
      } catch {
        userStore.logout()
        next('/login')
        return
      }
    }
  }
  
  // Redirect to home if already logged in
  if (to.path === '/login' && userStore.token) {
    next('/')
    return
  }
  
  next()
  */
})

router.afterEach(() => {
  NProgress.done()
})

export default router
