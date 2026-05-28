# Trabalho de SO — Tema 8: Processos vs Threads

## Pré-requisitos

- Python 3.8 ou superior
- Instalar dependências:

```bash
pip install psutil matplotlib
```

---

## Como executar

### Passo 1 — Rodar os experimentos

```bash
python experimento.py
```

O script vai:
- Testar com 1, 2 e 4 workers
- Rodar cada cenário 3 vezes para calcular médias
- Salvar os resultados no arquivo `resultados.csv`

### Passo 2 — Gerar os gráficos

```bash
python gerar_graficos.py
```

Vai gerar o arquivo `graficos_comparativos.png` com 3 gráficos:
1. Tempo de execução
2. Uso de CPU
3. Uso de memória

---

## Estrutura dos arquivos

```
so_trabalho/
├── experimento.py        ← experimento principal
├── gerar_graficos.py     ← gerador de gráficos
├── resultados.csv        ← gerado após rodar o experimento
└── graficos_comparativos.png  ← gerado pelo script de gráficos
```

---

## Observação importante (Windows)

No Windows, o Python possui o **GIL (Global Interpreter Lock)**, que impede que
threads executem código Python puro em paralelo real. Por isso, espera-se que:

- **Threads** tenham desempenho similar ou pior que execução sequencial em tarefas CPU intensivas
- **Processos** consigam paralelismo real, pois cada processo tem seu próprio interpretador

Essa diferença é justamente o ponto central da análise do trabalho.
