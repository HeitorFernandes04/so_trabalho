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
- Rodar cada cenário 10 vezes para calcular médias
- Salvar os resultados no arquivo `resultados.csv`

### Passo 2 — Verificar os resultados.

O arquivo `resultados.csv` vai nos entregar as informações contendo:
Abordagem, Workers e Tempo médio.

---

## Estrutura dos arquivos

```
so_trabalho/
├── experimento.py        ← experimento principal
└── resultados.csv        ← gerado após rodar o experimento
```

---

## Observação importante (Windows)

No Windows, o Python possui o **GIL (Global Interpreter Lock)**, que impede que
threads executem código Python puro em paralelo real. Por isso, espera-se que:

- **Threads** tenham desempenho similar ou pior que execução sequencial em tarefas CPU intensivas
- **Processos** consigam paralelismo real, pois cada processo tem seu próprio interpretador

Essa diferença é justamente o ponto central da análise do trabalho.
