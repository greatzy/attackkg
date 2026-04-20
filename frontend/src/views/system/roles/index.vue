<template>
  <div class="roles-page">
    <el-card class="page-header">
      <div class="header-content">
        <h2>角色管理</h2>
        <p>管理系统角色和权限分配</p>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="roles-container">
          <div class="roles-content">
            <div class="roles-header">
              <el-button type="primary" @click="addRole">
                <el-icon><UserFilled /></el-icon>
                新增角色
              </el-button>
              <el-button type="success" @click="refreshData">
                <el-icon><Refresh /></el-icon>
                刷新数据
              </el-button>
            </div>
            
            <el-table :data="roles" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="角色名称" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="status" label="状态" />
              <el-table-column prop="created_at" label="创建时间" />
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editRole(scope.row)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button type="success" size="small" @click="viewRole(scope.row)">
                    <el-icon><View /></el-icon>
                    查看
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteRole(scope.row)">
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

interface Role {
  id: number
  name: string
  description: string
  status: string
  created_at: string
}

interface Pagination {
  page: number
  pageSize: number
  total: number
}

const roles = ref<Role[]>([])
const pagination = ref<Pagination>({
  page: 1,
  pageSize: 10,
  total: 0
})

const addRole = () => {
  ElMessage.success('新增角色功能正在开发中')
}

const editRole = (role: Role) => {
  ElMessage.success('编辑角色功能正在开发中')
}

const viewRole = (role: Role) => {
  ElMessage.success('查看角色功能正在开发中')
}

const deleteRole = (role: Role) => {
  ElMessage.success('删除角色功能正在开发中')
}

const refreshData = () => {
  ElMessage.success('数据已刷新')
  fetchRoles()
}

const handleSizeChange = (val: number) => {
  pagination.value.pageSize = val
  fetchRoles()
}

const handleCurrentChange = (val: number) => {
  pagination.value.page = val
  fetchRoles()
}

const fetchRoles = () => {
  // 模拟数据
  roles.value = [
    {
      id: 1,
      name: '超级管理员',
      description: '拥有系统所有权限',
      status: '启用',
      created_at: '2024-01-01'
    },
    {
      id: 2,
      name: '普通用户',
      description: '拥有基本的系统权限',
      status: '启用',
      created_at: '2024-01-15'
    }
  ]
  pagination.value.total = roles.value.length
}

fetchRoles()
</script>

<style scoped lang="scss">
.roles-page {
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

  .roles-container {
    .roles-content {
      .roles-header {
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