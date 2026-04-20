<template>
  <div class="users-page">
    <el-card class="page-header">
      <div class="header-content">
        <h2>用户管理</h2>
        <p>管理系统用户信息和权限设置</p>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="users-container">
          <div class="users-content">
            <div class="users-header">
              <el-button type="primary" @click="addUser">
                <el-icon><UserFilled /></el-icon>
                新增用户
              </el-button>
              <el-button type="success" @click="refreshData">
                <el-icon><Refresh /></el-icon>
                刷新数据
              </el-button>
            </div>
            
            <el-table :data="users" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="username" label="用户名" />
              <el-table-column prop="email" label="邮箱" />
              <el-table-column prop="role" label="角色" />
              <el-table-column prop="status" label="状态" />
              <el-table-column prop="created_at" label="创建时间" />
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editUser(scope.row)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button type="success" size="small" @click="viewUser(scope.row)">
                    <el-icon><View /></el-icon>
                    查看
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteUser(scope.row)">
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="pagination">
              <el-pagination
                v-model:current-page="pagination.page"
                v-model:page-size="pagination.pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="pagination.total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { UserFilled, Refresh, Edit, View, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface User {
  id: number
  username: string
  email: string
  role: string
  status: string
  created_at: string
}

interface Pagination {
  page: number
  pageSize: number
  total: number
}

const users = ref<User[]>([])
const pagination = ref<Pagination>({
  page: 1,
  pageSize: 10,
  total: 0
})

const addUser = () => {
  ElMessage.success('新增用户功能正在开发中')
}

const editUser = (user: User) => {
  ElMessage.success('编辑用户功能正在开发中')
}

const viewUser = (user: User) => {
  ElMessage.success('查看用户功能正在开发中')
}

const deleteUser = (user: User) => {
  ElMessage.success('删除用户功能正在开发中')
}

const refreshData = () => {
  ElMessage.success('数据已刷新')
  fetchUsers()
}

const handleSizeChange = (val: number) => {
  pagination.value.pageSize = val
  fetchUsers()
}

const handleCurrentChange = (val: number) => {
  pagination.value.page = val
  fetchUsers()
}

const fetchUsers = () => {
  // 模拟数据
  users.value = [
    {
      id: 1,
      username: 'admin',
      email: 'admin@example.com',
      role: '超级管理员',
      status: '活跃',
      created_at: '2024-01-01'
    },
    {
      id: 2,
      username: 'user1',
      email: 'user1@example.com',
      role: '普通用户',
      status: '活跃',
      created_at: '2024-01-15'
    }
  ]
  pagination.value.total = users.value.length
}

fetchUsers()
</script>

<style scoped lang="scss">
.users-page {
  padding: 20px;

  .page-header {
    margin-bottom: 20px;

    .header-content {
      h2 {
        margin: 0 0 10px 0;
        color: #303133;
        font-size: 24px;
      }

      p {
        margin: 0;
        color: #606266;
        font-size: 14px;
      }
    }
  }

  .users-container {
    .users-content {
      .users-header {
        margin-bottom: 20px;
        display: flex;
        justify-content: flex-end;
        gap: 10px;
      }

      .pagination {
        margin-top: 20px;
        display: flex;
        justify-content: flex-end;
      }
    }
  }
}
</style>