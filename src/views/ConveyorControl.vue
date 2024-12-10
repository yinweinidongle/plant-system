<template>
  <PageLayout>
    <template #title>表型流水线控制</template>
    <div class="mechanical-settings">
      <div class="left-panel">
        <div class="control-panel">
          <TransportControl />
        </div>
        <div class="conveyor-diagram">
          <ConveyorDiagram />
        </div>
      </div>
      <div class="right-panel">
        <YsView title="表型舱摄像头" />
        <CameraView title="机械臂摄像头" />
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import PageLayout from '../components/PageLayout.vue'
import CameraView from '../components/CameraView.vue'
import TransportControl from '../components/TransportControl.vue'
import ConveyorDiagram from '../components/ConveyorDiagram.vue'
import YsView from '../components/YsView.vue'
</script>

<style scoped>
.mechanical-settings {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  height: calc(100vh - 140px);
  overflow: hidden;
}

.left-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.control-panel {
  height: 60%;
  overflow: auto;
}

.robot-diagram {
  height: 40%;
  background:url('../assets/robot.png') no-repeat center center / 100% 100%;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.robot-diagram img {
  width: 100%;
  height: calc(100% - 30px);
  object-fit: contain;
}

.right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
  overflow: hidden;
}

.right-panel > * {
  height: calc(50% - 10px);
}

h3 {
  margin: 0 0 15px 0;
  color: #2c3e50;
}

@media (max-width: 1200px) {
  .mechanical-settings {
    grid-template-columns: 1fr;
  }
}
</style> 