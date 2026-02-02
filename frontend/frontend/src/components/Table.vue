<template>
  <div>
    <!-- v-if e v-else operadores condicionais -->
     <!-- caso nao tenha elementos mostra umas msg -->
    <table class="table" v-if="operadoras.length > 0">
      <thead>
        <tr>
          <th>Nome da Operadora</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <!-- usando um for aqui -->
        <tr v-for="(op, index) in operadoras" :key="index">
          <td>{{ op }}</td>
          <td>
            <button class="btn btn-details">Detalhes</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Carregando operadoras...</p>

    <div class="pagination">
      <button class="btn" @click="prevPage" :disabled="!prevCursor">Anterior</button>
      <button class="btn" @click="nextPage" :disabled="!nextCursor">Próximo</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'Table',
  setup() {
    const operadoras = ref<{ nome: string }[]>([])
    const limit = 5

    // Keyset pagination
    const nextCursor = ref<number | null>(null)
    const prevCursor = ref<number | null>(null)
    const lastCursor = ref<number | null>(null) // guarda o último cursor da página atual

    const fetchOperadoras = async (cursor: number | null = null) => {
      try {
        const params: any = { limit }
        if (cursor !== null) params.cursor = cursor

        const response = await axios.get('http://127.0.0.1:8000/api/operadoras/', { params })

        operadoras.value = response.data.items 
        
        nextCursor.value = response.data.next_cursor || null
        prevCursor.value = response.data.prev_cursor || null
        lastCursor.value = cursor
      } catch (error) {
        console.error('Erro ao buscar operadoras:', error)
      }
    }

    // feito para carregar a primeira pagina
    onMounted(() => fetchOperadoras())
    

    const nextPage = () => {
      if (nextCursor.value !== null) fetchOperadoras(nextCursor.value)
    }

    const prevPage = () => {
      if (prevCursor.value !== null) fetchOperadoras(prevCursor.value)
    }

    return { operadoras, nextPage, prevPage, nextCursor, prevCursor }
  }
})
</script>

<style scoped>
/* mesmo estilo de antes */
.table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed; /* força largura fixa das colunas */
  margin-bottom: 15px;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  overflow: hidden;      /* esconde texto que ultrapassa */
  text-overflow: ellipsis; /* mostra "..." quando o texto é maior */
  white-space: nowrap;    /* evita quebra de linha */
}

/* opcional: você pode definir largura mínima para cada coluna */
.table th:nth-child(1), .table td:nth-child(1) {
  width: 300px; /* coluna do nome da operadora */
}

.table th:nth-child(2), .table td:nth-child(2) {
  width: 100px; /* coluna dos botões */
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

.btn-details {
  background: #28a745;
}

.btn-details:hover {
  background: #1e7e34;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}
</style>
