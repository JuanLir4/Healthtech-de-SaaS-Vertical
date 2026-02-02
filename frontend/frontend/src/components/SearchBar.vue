<template>
  <div class="search-filter">
    <input
      type="text"
      placeholder="Buscar CNPJ..."
      v-model="cnpj"
    />
    <button class="btn" @click="buscarOperadora">Filtrar</button>
    <button class="btn-secundario" @click="mostrarGrafico">
      Ver despesas por UF
    </button>
  </div>

  <div v-if="operadora" class="resultado">
    <p><strong>Nome:</strong> {{ operadora.razao_social }}</p>
    <p><strong>CNPJ:</strong> {{ operadora.cnpj }}</p>
  </div>

  <div v-else-if="erro" class="erro">
    {{ erro }}
  </div>

<div v-if="graficoVisivel" class="modal-overlay" @click.self="fecharGrafico">
  <div class="modal">
    <div class="modal-header">
      <h3>Despesas por UF</h3>
      <button class="close-btn" @click="fecharGrafico">×</button>
    </div>

    <canvas ref="chartRef" class="grafico"></canvas>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, nextTick } from 'vue'
import axios from 'axios'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
)

interface Operadora {
  razao_social: string
  cnpj: string
}

interface DespesaUFResponse {
  uf: string
  despesas: number
}

export default defineComponent({
  name: 'SearchBar',
  setup() {
    const cnpj = ref('')
    const operadora = ref<Operadora | null>(null)
    const erro = ref('')

    const chartRef = ref<HTMLCanvasElement | null>(null)
    const graficoVisivel = ref(false)
    let chartInstance: Chart | null = null

    const fecharGrafico = () => {
      graficoVisivel.value = false

      if (chartInstance) {
        chartInstance.destroy()
        chartInstance = null
        }
    }

    const buscarOperadora = async () => {
      erro.value = ''
      operadora.value = null

      if (!cnpj.value) {
        erro.value = 'Digite um CNPJ válido.'
        return
      }

      try {
        const response = await axios.get<Operadora>(
          `http://127.0.0.1:8000/api/operadoras/${cnpj.value}`
        )
        operadora.value = response.data
      } catch (e: any) {
        erro.value =
          e.response?.status === 404
            ? 'Operadora não encontrada.'
            : 'Erro ao buscar operadora.'
      }
    }

    const mostrarGrafico = async () => {
      erro.value = ''
      graficoVisivel.value = false

      try {
        const ufs = ['SP', 'RJ', 'PE', 'MG']

        const respostas = await Promise.all(
          ufs.map(uf =>
            axios.get<DespesaUFResponse>(
              `http://127.0.0.1:8000/api/operadoras/uf/${uf}/despesas`
            )
          )
        )

        const labels = respostas.map(r => r.data.uf)
        const valores = respostas.map(r => r.data.despesas)

        graficoVisivel.value = true
        await nextTick()

        if (chartInstance) chartInstance.destroy()

        chartInstance = new Chart(chartRef.value!, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              {
                label: 'Soma das despesas por UF',
                data: valores
              }
            ]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  callback: value =>
                    `R$ ${Number(value).toLocaleString('pt-BR')}`
                }
              }
            }
          }
        })
      } catch (e) {
        erro.value = 'Erro ao carregar gráfico de despesas por UF.'
        console.error(e)
      }
    }

    return {
      cnpj,
      operadora,
      erro,
      buscarOperadora,
      mostrarGrafico,
      chartRef,
      graficoVisivel,
      fecharGrafico
    }
  }
})
</script>

<style scoped>

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  max-width: 800px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  line-height: 1;
}

.close-btn:hover {
  color: red;
}

.search-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-filter input {
  flex: 1;
  padding: 8px 12px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background: #0056b3;
}

.btn-secundario {
  padding: 8px 16px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-secundario:hover {
  background: #1e7e34;
}

.resultado {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #007bff;
  border-radius: 5px;
  background: #f0f8ff;
}

.erro {
  margin-top: 10px;
  color: red;
  font-weight: bold;
}

.grafico {
  margin-top: 30px;
  max-width: 700px;
}
</style>
