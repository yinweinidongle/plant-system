<template>
  <div class="page-layout">
    <header class="page-header">
      <div class="header-content">
        <!-- <el-button icon="Back" @click="router.push('/')" class="back-button">
          返回首页
        </el-button> -->
        <h2><slot name="title"></slot></h2>
      </div>
    </header>
    
    <main class="page-content">
      <slot></slot>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Footer from './Footer.vue'

const router = useRouter()
</script>

<style scoped>
.page-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.page-header {
  background: linear-gradient(135deg, #409EFF 0%, #2c3e50 100%);
  color: white;
  padding: 20px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-button {
  background-color: transparent;
  border-color: white;
  color: white;
}

.back-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
}

.page-content {
  flex: 1;
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

h2 {
  margin: 0;
  font-size: 1.8em;
}
</style> 