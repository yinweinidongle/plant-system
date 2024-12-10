<template>
  <div class="home">
    <header class="header">
      <div class="header-content">
        <h1>作物表型分析系统</h1>
        <p class="subtitle">智能化 · 高效率 · 精准化</p>
      </div>
    </header>
    
    <main class="main-content">
      <div class="button-grid">
        <el-button 
          v-for="button in buttons" 
          :key="button.route"
          type="primary"
          size="large"
          class="feature-button"
          @click="navigateTo(button.route)"
          target="_blank"
        >
          <div class="button-content">
            <el-icon class="button-icon">
              <component :is="button.icon" />
            </el-icon>
            <span class="button-text">{{ button.text }}</span>
          </div>
        </el-button>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Setting, Van, DataAnalysis, Tools,Promotion } from '@element-plus/icons-vue'
import Footer from '../components/Footer.vue'

const router = useRouter()

const buttons = [
  {
    text: '机械臂设置',
    route: '/mechanical-settings',
    icon: Tools
  },
  {
    text: '表型流水线控制',
    route: '/conveyor-control',
    icon: Promotion
  },
  {
    text: '作物表型分析',
    route: '/phenotype-analysis',
    icon: DataAnalysis
  },
  {
    text: '系统设置',
    route: '/#',
    icon: Setting
  }
]

const navigateTo = (route) => {
  window.open(route, '_blank')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #409EFF 0%, #2c3e50 100%);
  color: white;
  padding: 40px 20px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.header h1 {
  margin: 0;
  font-size: 2.5em;
  font-weight: 600;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
  margin-top: 10px;
  font-size: 1.2em;
  opacity: 0.9;
  letter-spacing: 2px;
}

.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
  max-width: 1000px;
  width: 100%;
}

.feature-button {
  height: 220px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 1.6em;
  border-radius: 12px;
  transition: all 0.3s ease;
  border: none;
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  box-shadow: 5px 5px 15px #d1d1d1,
              -5px -5px 15px #ffffff;
  padding: 20px;
}

.feature-button:hover {
  transform: translateY(-5px);
  box-shadow: 8px 8px 20px #d1d1d1,
              -8px -8px 20px #ffffff;
}

.button-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.button-icon {
  font-size: 2.5em;
  margin-bottom: 25px;
  color: #409EFF;
}

.button-text {
  font-weight: 600;
  text-shadow: 0 0.5px 0.5px rgba(0, 0, 0, 0.4);
  color: #2c3e50;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .button-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 0 20px;
  }

  .feature-button {
    height: 180px;
    font-size: 1.4em;
  }

  .button-icon {
    margin-bottom: 20px;
  }

  .header h1 {
    font-size: 2em;
  }

  .subtitle {
    font-size: 1em;
  }
}
</style> 