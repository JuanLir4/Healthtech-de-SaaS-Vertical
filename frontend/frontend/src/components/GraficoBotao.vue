<template>
  <div class="chart-button">
    <button class="btn">Mostrar Gráfico</button>
  </div>
</template>

<script lang="ts">
export default {
  name: 'GraficoBotao'
}
</script>


<style scoped>
.chart-button {
  text-align: right;
  margin-bottom: 10px;
}

.btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn:hover {
  background: #0056b3;
}
</style>