<template>
  <div>
    <!-- Tabela de operadoras -->
    <table class="table" v-if="operadoras.length > 0">
      <thead>
        <tr>
          <th>Nome da Operadora</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(op, index) in operadoras" :key="index">
          <td>{{ op }}</td>
          <td>
            <button
              class="btn btn-details"
              @click="verDetalhes(op)"
            >
              Detalhes
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Carregando operadoras...</p>

    <!-- Paginação -->
    <div class="pagination">
      <button class="btn" @click="prevPage" :disabled="!prevCursor">
        Anterior
      </button>
      <button class="btn" @click="nextPage" :disabled="!nextCursor">
        Próximo
      </button>
    </div>

    <!-- MODAL -->
    <div
      v-if="showModal"
      class="modal-overlay"
      @click.self="fecharModal"
    >
      <div class="modal">
        <div class="modal-header">
          <h3>Despesas — {{ operadoraSelecionada }}</h3>
          <button class="close-btn" @click="fecharModal">×</button>
        </div>

        <div class="modal-body">
          <ul v-if="despesas && despesas.length > 0">
            <li v-for="(item, index) in despesas" :key="index">
              R$ {{ item.valor.toFixed(2) }}
            </li>
          </ul>

          <p v-else>Nenhuma despesa encontrada.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'

interface Despesa {
  valor: number
}

export default defineComponent({
  name: 'Table',
  setup() {
    // Lista de operadoras
    const operadoras = ref<string[]>([])

    // Paginação
    const limit = 5
    const nextCursor = ref<number | null>(null)
    const prevCursor = ref<number | null>(null)

    // Modal / detalhes
    const showModal = ref(false)
    const despesas = ref<Despesa[] | null>(null)
    const operadoraSelecionada = ref<string | null>(null)

    // Buscar operadoras
    const fetchOperadoras = async (cursor: number | null = null) => {
      try {
        const params: any = { limit }
        if (cursor !== null) params.cursor = cursor

        const response = await axios.get(
          'http://127.0.0.1:8000/api/operadoras/',
          { params }
        )

        operadoras.value = response.data.items
        nextCursor.value = response.data.next_cursor || null
        prevCursor.value = response.data.prev_cursor || null
      } catch (error) {
        console.error('Erro ao buscar operadoras:', error)
      }
    }

    // Buscar despesas da operadora
    const verDetalhes = async (razaoSocial: string) => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/operadoras/${encodeURIComponent(
            razaoSocial
          )}/despesas`
        )

        operadoraSelecionada.value = response.data.razao_social
        despesas.value = response.data.despesas
        showModal.value = true
      } catch (error) {
        console.error('Erro ao buscar despesas:', error)
      }
    }

    const fecharModal = () => {
      showModal.value = false
    }

    onMounted(() => fetchOperadoras())

    const nextPage = () => {
      if (nextCursor.value !== null) {
        fetchOperadoras(nextCursor.value)
      }
    }

    const prevPage = () => {
      if (prevCursor.value !== null) {
        fetchOperadoras(prevCursor.value)
      }
    }

    return {
      operadoras,
      nextPage,
      prevPage,
      nextCursor,
      prevCursor,
      verDetalhes,
      despesas,
      operadoraSelecionada,
      showModal,
      fecharModal
    }
  }
})
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  margin-bottom: 15px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.table th:nth-child(1),
.table td:nth-child(1) {
  width: 300px;
}

.table th:nth-child(2),
.table td:nth-child(2) {
  width: 120px;
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
  gap: 10px;
  margin-top: 10px;
}

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  width: 420px;
  max-height: 80vh;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 8px;
}

.modal-body {
  margin-top: 10px;
  overflow-y: auto;
}

.close-btn {
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
}
</style>
