import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { requiresAuth: false } // 首页允许未登录访问
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue'),
      meta: { requiresAuth: true } // 关于页面需要登录
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('../views/Help.vue'),
      meta: { requiresAuth: true } // 帮助页面需要登录
    },
    // 认证相关路由
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/Register.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/email-verification',
      name: 'EmailVerification',
      component: () => import('../views/EmailVerification.vue'),
      meta: { requiresGuest: true }
    },
    // ICC管理路由
    {
      path: '/icc',
      name: 'ICCList',
      component: () => import('../views/ICC/ICCList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/icc/:id',
      name: 'ICCDetail',
      component: () => import('../views/ICC/ICCDetail.vue'),
      meta: { requiresAuth: true }
    },
    // 订阅管理路由
    {
      path: '/subscription',
      name: 'SubscriptionList',
      component: () => import('../views/Subscription/SubscriptionList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/subscription/:id',
      name: 'SubscriptionDetail',
      component: () => import('../views/Subscription/SubscriptionDetail.vue'),
      meta: { requiresAuth: true }
    },
    // 用量管理路由
    {
      path: '/usage',
      name: 'UsageList',
      component: () => import('../views/Usage/UsageList.vue'),
      meta: { requiresAuth: true }
    },
    // CUG详单路由
    {
      path: '/cug',
      name: 'CUGList',
      component: () => import('../views/CUG/CUGList.vue'),
      meta: { requiresAuth: true }
    },
    // 文档管理路由
    {
      path: '/document',
      name: 'DocumentList',
      component: () => import('../views/Document/DocumentList.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 检查是否需要游客状态（已登录用户不能访问）
  if (to.meta.requiresGuest) {
    if (userStore.isLoggedIn) {
      // 已登录用户跳转到首页
      next('/')
    } else {
      next()
    }
  }
  // 检查是否需要认证
  else if (to.meta.requiresAuth) {
    if (!userStore.isLoggedIn) {
      // 检查是否有token
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          // 尝试获取用户信息
          await userStore.fetchUserInfo()
          next()
        } catch (error) {
          // token无效，清除并跳转到登录页
          userStore.clearUser()
          next({
            path: '/login',
            query: { redirect: to.fullPath }
          })
        }
      } else {
        // 没有token，跳转到登录页
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
      }
    } else {
      next()
    }
  }
  // 其他页面（如首页）允许访问
  else {
    next()
  }
})

export default router
