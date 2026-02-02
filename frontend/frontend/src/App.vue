<template>
  <div class="container">
    <h1>Operadoras</h1>
    <SearchBar />
    <ChartButton />
    <Table />
  </div>
</template>

<script lang="ts">
import Table from './components/Table.vue'
import SearchBar from './components/SearchBar.vue'
import GraficoBotao from './components/GraficoBotao.vue'

export default {
  components: { Table, SearchBar, GraficoBotao }
}
</script>
