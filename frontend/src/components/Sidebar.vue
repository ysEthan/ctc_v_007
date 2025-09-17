<template>
  <aside class="sidebar">
    <!-- 品牌Logo -->
    <div class="brand">
      <router-link to="/" class="logo">
        <el-icon><Grid /></el-icon>
        <span>CTC</span>BOARD
      </router-link>
    </div>
    
    <nav>
      <ul class="nav">
        <li :class="{ active: $route.path === '/dashboard' }">
          <router-link to="/dashboard" title="仪表盘">
            <el-icon><Odometer /></el-icon>
            仪表盘
          </router-link>
        </li>

        <!-- 数据管理模块 -->
        <li class="nav-dropdown" :class="{ expanded: isMenuExpanded('data'), active: $route.path.startsWith('/icc') || $route.path.startsWith('/subscription') || $route.path.startsWith('/usage') || $route.path.startsWith('/cug') }">
          <a href="#" title="数据管理" @click.prevent="toggleMenu('data')">
            <el-icon><DataBoard /></el-icon>
            数据管理
            <el-icon class="dropdown-arrow" :class="{ rotated: isMenuExpanded('data') }">
              <ArrowDown />
            </el-icon>
          </a>
          <ul class="nav-sub" v-show="isMenuExpanded('data')">
            <li>
              <router-link to="/icc" title="ICC管理">
                ICC管理
              </router-link>
            </li>
            <li>
              <router-link to="/subscription" title="订阅管理">
                订阅管理
              </router-link>
            </li>
             <li>
               <router-link to="/usage" title="用量管理">
                 用量管理
               </router-link>
             </li>
             <li>
               <router-link to="/cug" title="CUG详单">
                 CUG详单
               </router-link>
             </li>
          </ul>
        </li>

        <!-- 文件管理：一级菜单（位于数据管理之后） -->
        <li :class="{ active: $route.path.startsWith('/document') }">
          <router-link to="/document" title="文件管理">
            <el-icon><Folder /></el-icon>
            文件管理
          </router-link>
        </li>

        

         <li class="nav-dropdown" :class="{ expanded: isMenuExpanded('system'), active: $route.path === '/about' || $route.path === '/help' }">
           <a href="#" title="系统" @click.prevent="toggleMenu('system')">
             <el-icon><Setting /></el-icon>
             系统
             <el-icon class="dropdown-arrow" :class="{ rotated: isMenuExpanded('system') }">
               <ArrowDown />
             </el-icon>
           </a>
           <ul class="nav-sub" v-show="isMenuExpanded('system')">
             <li>
               <router-link to="/about" title="关于">
                 关于
               </router-link>
             </li>
             <li>
               <router-link to="/help" title="帮助">
                 帮助
               </router-link>
             </li>
           </ul>
         </li>







      </ul>
    </nav>

    <h5 class="sidebar-header">设置</h5>
    <div class="setting-list">
      <div class="row">
        <div class="col-xs-8">
          <label for="check1" class="control-label">状态</label>
        </div>
        <div class="col-xs-4">
          <el-switch v-model="shareStatus" id="check1" />
        </div>
      </div>
      <div class="row">
        <div class="col-xs-8">
          <label for="check2" class="control-label">通知</label>
        </div>
        <div class="col-xs-4">
          <el-switch v-model="pushNotifications" id="check2" />
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const shareStatus = ref(true)
const pushNotifications = ref(false)

// 控制下拉菜单的展开状态
const expandedMenus = ref<Set<string>>(new Set())

const toggleMenu = (menuName: string) => {
  if (expandedMenus.value.has(menuName)) {
    expandedMenus.value.delete(menuName)
  } else {
    expandedMenus.value.add(menuName)
  }
}

const isMenuExpanded = (menuName: string) => {
  return expandedMenus.value.has(menuName)
}

// 监听路由变化，自动展开包含当前路由的父菜单
watch(() => route.path, (newPath) => {
  if (newPath === '/about' || newPath === '/help') {
    expandedMenus.value.add('system')
  }
  if (newPath.startsWith('/icc') || newPath.startsWith('/subscription') || newPath.startsWith('/usage') || newPath.startsWith('/cug')) {
    expandedMenus.value.add('data')
  }
}, { immediate: true })
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 202px;
  height: 100vh;
  background: #000000;
  color: #ecf0f1;
  z-index: 1000;
  overflow-y: auto;
  transition: all 0.3s ease;
}

.brand {
  padding: 20px 15px;
  border-bottom: 1px solid #333333;
  background: #111111;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #ecf0f1;
  font-size: 18px;
  font-weight: 600;
  transition: color 0.3s ease;
}

.logo:hover {
  color: #3498db;
}

.logo .el-icon {
  margin-right: 10px;
  font-size: 20px;
  color: #3498db;
}

.logo span {
  color: #3498db;
}

.sidebar-header {
  padding: 20px 15px 10px;
  margin: 0;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  color: #95a5a6;
  border-bottom: 1px solid #34495e;
}

.nav {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav li {
  position: relative;
}

.nav li a {
  display: block;
  padding: 12px 20px;
  color: #bdc3c7;
  text-decoration: none;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  font-weight: 500;
}

.nav li a:hover {
  background: #333333;
  color: #ecf0f1;
  border-left-color: #3498db;
}

/* 只对一级菜单的直接子元素应用高亮，不影响二级菜单 */
.nav > li.active > a {
  background: #e3f2fd;
  color: #1976d2;
  border-left-color: #1976d2;
}

.nav li a .el-icon {
  margin-right: 10px;
  width: 16px;
  text-align: center;
}

.nav-sub {
  display: none;
  background: #000000;
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.nav-dropdown.expanded .nav-sub {
  display: block;
  max-height: 500px;
}

.dropdown-arrow {
  float: right;
  transition: transform 0.3s ease;
  font-size: 12px;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.nav-sub li a {
  padding: 10px 20px 10px 50px;
  font-size: 13px;
  border-left: none;
  font-weight: 400;
}

.nav-sub li a:hover {
  background: #333333;
  border-left: none;
}

/* 二级菜单保持与侧边栏背景色一致，不高亮，但选中时显示蓝色字体 */
.nav-sub li a.router-link-active,
.nav-sub li a.router-link-exact-active {
  background: #000000 !important;
  color: #3498db !important;
  border-left: none !important;
}

.nav-sub li a.router-link-active:hover,
.nav-sub li a.router-link-exact-active:hover {
  background: #333333 !important;
}

.label {
  display: inline-block;
  padding: 2px 6px;
  font-size: 11px;
  font-weight: 600;
  line-height: 1;
  color: #fff;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 10px;
  margin-left: 8px;
}

.label-primary {
  background-color: #3498db;
}

.label-circle {
  border-radius: 50%;
  width: 18px;
  height: 18px;
  line-height: 14px;
  text-align: center;
}


.setting-list {
  padding: 20px 15px;
  border-top: 1px solid #34495e;
}

.setting-list .row {
  margin-bottom: 15px;
}

.control-label {
  font-size: 13px;
  color: #bdc3c7;
  margin: 0;
  line-height: 32px;
  font-weight: 500;
}

.col-xs-8 {
  width: 66.66666667%;
  float: left;
}

.col-xs-4 {
  width: 33.33333333%;
  float: left;
  text-align: right;
}
</style>
