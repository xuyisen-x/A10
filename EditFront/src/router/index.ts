import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

// createRouter 创建路由实例，===> new VueRouter()
// history 是路由模式，hash模式，history模式
// createWebHistory() 是开启history模块
// createWebHashHistory() 是开启hash模式

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/HomePage/index.vue'),
        meta: { title: '首页' }
    },
    {
        path: '/main',
        name: 'Edit',
        component: () => import('../views/Edit/index.vue'),
        meta: { title: '编辑器' }
    }
] as RouteRecordRaw[]
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

router.beforeEach((to, _, next) => {
    document.title = to.meta.title as string || '默认标题';
    next();
});

export default router