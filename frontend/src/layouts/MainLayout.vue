<template>
  <div class="main-layout">
    <!-- Header -->
    <header class="layout-header">
      <div class="header-content">
        <div class="header-left">
          <button 
            class="menu-toggle" 
            @click="toggleSidebar"
          >
            <span class="icon-menu"></span>
          </button>
          <div class="logo">
            <h1>网络安全攻击知识库系统</h1>
          </div>
        </div>
        <div class="header-right">
          <div class="user-dropdown" @click="toggleUserDropdown">
            <div class="user-avatar">
              🛡️
            </div>
            <span class="username">{{ userStore.username }}</span>
            <span class="dropdown-arrow"></span>
            <div v-if="isUserDropdownOpen" class="dropdown-menu">
              <div class="dropdown-item" @click="handleDropdownCommand('profile')">
                <span class="icon-user"></span>
                个人信息
              </div>
              <div class="dropdown-item" @click="handleDropdownCommand('settings')">
                <span class="icon-setting"></span>
                系统设置
              </div>
              <div class="dropdown-divider"></div>
              <div class="dropdown-item" @click="handleDropdownCommand('logout')">
                <span class="icon-logout"></span>
                退出登录
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="layout-body">
      <!-- Sidebar -->
      <aside 
        :style="{ width: sidebarWidth }" 
        class="layout-sidebar"
        :class="{ collapsed: isSidebarCollapsed }"
      >
        <nav class="sidebar-menu">
          <template v-for="route in menuRoutes" :key="route.name">
            <!-- Single level menu -->
            <a 
              v-if="!route.children" 
              :href="'/' + route.path"
              class="menu-item"
              :class="{ active: activeMenu === '/' + route.path }"
            >
              <span v-if="route.meta?.icon" class="menu-icon">
                {{ getIcon(route.meta.icon) }}
              </span>
              <span class="menu-title">{{ route.meta?.title }}</span>
            </a>

            <!-- Multi level menu -->
            <div v-else class="sub-menu">
              <div 
                class="sub-menu-title"
                :class="{ active: isSubMenuActive(route) }"
                @click="toggleSubMenu(route.name)"
              >
                <span v-if="route.meta?.icon" class="menu-icon">
                  {{ getIcon(route.meta.icon) }}
                </span>
                <span class="menu-title">{{ route.meta?.title }}</span>
                <span class="sub-menu-arrow" :class="{ rotated: openSubMenus.includes(route.name) }"></span>
              </div>
              <div 
                class="sub-menu-content"
                :class="{ open: openSubMenus.includes(route.name) }"
              >
                <a 
                  v-for="child in route.children" 
                  :key="child.name"
                  :href="'/' + route.path + '/' + child.path"
                  class="sub-menu-item"
                  :class="{ active: activeMenu === '/' + route.path + '/' + child.path }"
                >
                  {{ child.meta?.title }}
                </a>
              </div>
            </div>
          </template>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="layout-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const isSidebarCollapsed = ref(false)
const isUserDropdownOpen = ref(false)
const openSubMenus = ref<string[]>([])

const sidebarWidth = computed(() => isSidebarCollapsed.value ? '64px' : '220px')

const menuRoutes = computed(() => {
  // Get routes from router config directly
  const layoutRoute = router.getRoutes().find(r => r.path === '/')
  return (layoutRoute?.children || []).filter(r => !r.meta?.hidden)
})

const activeMenu = computed(() => {
  return route.path
})

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const toggleUserDropdown = () => {
  isUserDropdownOpen.value = !isUserDropdownOpen.value
}

const toggleSubMenu = (menuName: string) => {
  const index = openSubMenus.value.indexOf(menuName)
  if (index > -1) {
    openSubMenus.value.splice(index, 1)
  } else {
    openSubMenus.value.push(menuName)
  }
}

const isSubMenuActive = (route: any) => {
  return route.children.some((child: any) => 
    activeMenu.value === '/' + route.path + '/' + child.path
  )
}

const getIcon = (iconName: string) => {
  const iconMap: Record<string, string> = {
    HomeFilled: '🏠',
    Collection: '📚',
    UserFilled: '👤',
    DocumentChecked: '✓',
    DataAnalysis: '📊',
    Document: '📄',
    WarningFilled: '⚠️',
    Setting: '⚙️'
  }
  return iconMap[iconName] || '📄'
}

const handleDropdownCommand = (command: string) => {
  isUserDropdownOpen.value = false
  switch (command) {
    case 'profile':
      // Handle profile
      console.log('Profile')
      break
    case 'settings':
      // Handle settings
      console.log('Settings')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const handleLogout = async () => {
  try {
    await userStore.logout()
    router.push('/login')
  } catch (error) {
    userStore.logout()
    router.push('/login')
  }
}

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.user-dropdown')) {
    isUserDropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  // Initialize open submenus based on current route
  initOpenSubMenus()
  
  // Watch for route changes to update open submenus
  router.afterEach(() => {
    updateOpenSubMenus()
  })
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Update open submenus based on current route
const updateOpenSubMenus = () => {
  const currentPath = route.path
  const newOpenSubMenus: string[] = []
  
  menuRoutes.value.forEach(menuRoute => {
    if (menuRoute.children) {
      const hasActiveChild = menuRoute.children.some(child => {
        const childPath = '/' + menuRoute.path + '/' + child.path
        return currentPath === childPath
      })
      
      if (hasActiveChild) {
        newOpenSubMenus.push(menuRoute.name)
      }
    }
  })
  
  // Only update if there are changes
  if (JSON.stringify(newOpenSubMenus) !== JSON.stringify(openSubMenus.value)) {
    openSubMenus.value = newOpenSubMenus
  }
}

// Initialize open submenus based on current route
const initOpenSubMenus = () => {
  const currentPath = route.path
  
  menuRoutes.value.forEach(menuRoute => {
    if (menuRoute.children) {
      const hasActiveChild = menuRoute.children.some(child => {
        const childPath = '/' + menuRoute.path + '/' + child.path
        return currentPath === childPath
      })
      
      if (hasActiveChild) {
        openSubMenus.value.push(menuRoute.name)
      }
    }
  })
}
</script>

<style lang="scss">
.main-layout {
  height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;

  .layout-header {
    background-color: #ffffff;
    border-bottom: 1px solid #e4e7ed;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    height: 60px;

    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      height: 100%;
      padding: 0 20px;

      .header-left {
        display: flex;
        align-items: center;
        gap: 16px;

        .menu-toggle {
          background: none;
          border: none;
          font-size: 20px;
          color: #606266;
          padding: 8px;
          cursor: pointer;
          border-radius: 4px;
          transition: all 0.2s;

          &:hover {
            color: #409eff;
            background-color: #ecf5ff;
          }

          .icon-menu::before {
            content: '☰';
          }
        }

        .logo {
          h1 {
            font-size: 18px;
            color: #303133;
            margin: 0;
            white-space: nowrap;
          }
        }
      }

      .header-right {
        .user-dropdown {
          position: relative;
          display: flex;
          align-items: center;
          gap: 10px;
          cursor: pointer;
          padding: 8px 12px;
          border-radius: 4px;
          transition: background-color 0.2s;

          &:hover {
            background-color: #f5f7fa;
          }

          .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #409eff, #67c23a);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 600;
          }

          .username {
            color: #606266;
            font-size: 14px;
          }

          .dropdown-arrow {
            width: 0;
            height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #606266;
            transition: transform 0.2s;
          }

          &:hover .dropdown-arrow {
            border-top-color: #409eff;
          }

          .dropdown-menu {
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 8px;
            background: white;
            border: 1px solid #e4e7ed;
            border-radius: 4px;
            box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
            min-width: 180px;
            z-index: 1000;

            .dropdown-item {
              display: flex;
              align-items: center;
              gap: 8px;
              padding: 10px 16px;
              color: #606266;
              font-size: 14px;
              cursor: pointer;
              transition: background-color 0.2s;

              &:hover {
                background-color: #ecf5ff;
                color: #409eff;
              }

              .icon-user::before {
                content: '👤';
              }

              .icon-setting::before {
                content: '⚙️';
              }

              .icon-logout::before {
                content: '🚪';
              }
            }

            .dropdown-divider {
              height: 1px;
              background-color: #e4e7ed;
              margin: 5px 0;
            }
          }
        }
      }
    }
  }

  .layout-body {
    display: flex;
    flex: 1;
    overflow: hidden;

    .layout-sidebar {
      background-color: #304156;
      box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
      transition: width 0.3s;
      overflow: hidden;

      &.collapsed {
        width: 64px;
      }

      .sidebar-menu {
        padding: 16px 0;

        .menu-item {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px 20px;
          color: #bfcbd9;
          text-decoration: none;
          transition: all 0.3s;
          border-left: 3px solid transparent;

          &:hover {
            color: #ffffff;
            background-color: rgba(64, 158, 255, 0.2);
          }

          &.active {
            color: #ffffff;
            background-color: rgba(64, 158, 255, 0.3);
            border-left-color: #409eff;

            &:hover {
              background-color: rgba(64, 158, 255, 0.4);
            }
          }

          .menu-icon {
            font-size: 18px;
            width: 24px;
            text-align: center;
          }

          .menu-title {
            font-size: 14px;
          }
        }

        .sub-menu {
          .sub-menu-title {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 20px;
            color: #bfcbd9;
            cursor: pointer;
            transition: all 0.3s;
            border-left: 3px solid transparent;

            &:hover {
              color: #ffffff;
              background-color: rgba(64, 158, 255, 0.2);
            }

            &.active {
              color: #ffffff;
              background-color: rgba(64, 158, 255, 0.3);
              border-left-color: #409eff;
            }

            .menu-icon {
              font-size: 18px;
              width: 24px;
              text-align: center;
            }

            .menu-title {
              font-size: 14px;
              flex: 1;
            }

            .sub-menu-arrow {
              width: 0;
              height: 0;
              border-left: 4px solid #bfcbd9;
              border-top: 4px solid transparent;
              border-bottom: 4px solid transparent;
              transition: transform 0.3s;

              &.rotated {
                transform: rotate(90deg);
              }
            }
          }

          .sub-menu-content {
            overflow: hidden;
            max-height: 0;
            transition: max-height 0.3s ease-out;

            &.open {
              max-height: 500px;
              transition: max-height 0.3s ease-in;
            }

            .sub-menu-item {
              display: block;
              padding: 10px 20px 10px 56px;
              color: #bfcbd9;
              text-decoration: none;
              font-size: 14px;
              transition: all 0.3s;
              background-color: #263445;
              border-left: 3px solid transparent;

              &:hover {
                color: #ffffff;
                background-color: rgba(64, 158, 255, 0.2);
              }

              &.active {
                color: #ffffff;
                background-color: rgba(64, 158, 255, 0.3);
                border-left-color: #409eff;

                &:hover {
                  background-color: rgba(64, 158, 255, 0.4);
                }
              }
            }
          }
        }
      }
    }

    .layout-content {
      flex: 1;
      padding: 20px;
      background-color: #f5f7fa;
      overflow-y: auto;
    }
  }
}

// Responsive design
@media (max-width: 768px) {
  .main-layout {
    .layout-header {
      .header-content {
        .header-left {
          .logo h1 {
            display: none;
          }
        }

        .header-right {
          .user-dropdown .username {
            display: none;
          }
        }
      }
    }

    .layout-body {
      .layout-sidebar {
        position: fixed;
        left: 0;
        top: 60px;
        height: calc(100vh - 60px);
        z-index: 1000;
      }
    }
  }
}

// Fade transition
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
