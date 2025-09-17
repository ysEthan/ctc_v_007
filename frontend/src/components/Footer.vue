<template>
  <footer id="footer">
    <div class="footer-content">
      <div class="footer-left">
        <p>&copy; {{ currentYear }} CTC 通用网页系统模板. 保留所有权利.</p>
      </div>
      <div class="footer-right">
        <p>版本 {{ version }} | 技术支持: <a href="mailto:support@ctc.com">support@ctc.com</a></p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
const version = '1.0.0'
</script>

<style scoped>
#footer {
  position: fixed;
  bottom: 0;
  left: 202px;
  right: 0;
  height: 40px;
  background: #f8f9fa;
  border-top: 1px solid #e5e5e5;
  z-index: 998;
  display: flex;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
  transition: left 0.3s ease;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  font-size: 12px;
  color: #666;
}

.footer-left p,
.footer-right p {
  margin: 0;
}

.footer-right a {
  color: #3498db;
  text-decoration: none;
}

.footer-right a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  #footer {
    left: 0;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 5px;
  }
}
</style>
