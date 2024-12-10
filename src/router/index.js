import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/mechanical-settings',
      name: 'MechanicalSettings',
      component: () => import('../views/MechanicalSettings.vue')
    },
    {
      path: '/conveyor-control',
      name: 'ConveyorControl',
      component: () => import('../views/ConveyorControl.vue')
    },
    {
      path: '/phenotype-analysis',
      name: 'PhenotypeAnalysis',
      component: () => import('../views/PhenotypeAnalysis.vue')
    },
    {
      path: '/system-settings',
      name: 'SystemSettings',
      component: () => import('../views/SystemSettings.vue')
    }
  ]
})

export default router 