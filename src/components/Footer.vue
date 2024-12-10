<template>
  <footer class="footer">
    <div class="footer-content">
      <p>© {{ currentYear }} 作物表型分析系统</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'

const currentYear = ref(new Date().getFullYear())
</script>

<style scoped>
.footer {
  background-color: #2c3e50;
  color: #ffffff;
  padding: 20px 0;
  text-align: center;
  width: 100%;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer p {
  margin: 5px 0;
  font-size: 14px;
  opacity: 0.8;
}

.company {
  font-weight: 500;
}
</style> 