# Referencial Teórico — Tema 8: Comparação entre Processos e Threads

**Disciplina:** Sistemas Operacionais
**Tema:** Comparação prática entre processos e threads

---

## 1. Processos

Um **processo** é a unidade básica de execução em um sistema operacional. Ele representa
um programa em execução, com seu próprio espaço de endereçamento, recursos de memória,
descritores de arquivo e estado de CPU.

### 1.1 Estrutura de um processo

Cada processo possui:
- **PCB (Process Control Block):** estrutura mantida pelo SO com PID, estado, registradores,
  prioridade, informações de memória e arquivos abertos.
- **Espaço de endereçamento próprio:** regiões de código (text), dados (data/BSS),
  heap (dinâmico) e pilha (stack).
- **Isolamento total:** processos não compartilham memória por padrão; a comunicação
  exige mecanismos explícitos (pipes, sockets, memória compartilhada).

### 1.2 Criação de processos

No UNIX/Linux, processos são criados via `fork()`, que gera uma cópia exata do processo
pai. No Python, a biblioteca `multiprocessing` abstrai esse mecanismo, funcionando também
no Windows através de `spawn` (inicializa novo interpretador Python).

### 1.3 Custo dos processos

A criação de processos é **cara** em termos de recursos:
- Cópia do espaço de endereçamento (ou tabelas de páginas em COW — Copy-on-Write)
- Troca de contexto exige salvar/restaurar todo o estado do processo
- Comunicação entre processos (IPC) tem overhead significativo

> **Referência:** TANENBAUM, A. S.; BOS, H. *Modern Operating Systems*. 4. ed. Pearson, 2015. Cap. 2.

---

## 2. Threads

Uma **thread** (ou processo leve) é uma unidade de execução dentro de um processo. Múltiplas
threads de um mesmo processo **compartilham** o mesmo espaço de endereçamento, arquivos
abertos e outros recursos do processo pai.

### 2.1 Estrutura de uma thread

Cada thread possui individualmente:
- Contador de programa (PC)
- Conjunto de registradores
- Pilha de execução (stack)

Compartilhado entre todas as threads do processo:
- Segmentos de código e dados
- Heap
- Descritores de arquivo

### 2.2 Vantagens das threads

- **Criação mais rápida** que processos (sem cópia de espaço de endereçamento)
- **Comunicação direta** via variáveis compartilhadas (sem IPC)
- **Menor consumo de memória** (sem duplicação de dados)
- **Troca de contexto mais leve**

### 2.3 Desvantagens das threads

- **Risco de condições de corrida:** acesso simultâneo a dados compartilhados pode
  causar inconsistências.
- **Depuração mais difícil:** problemas de concorrência são não-determinísticos.
- **Falha em uma thread pode comprometer o processo inteiro.**

> **Referência:** SILBERSCHATZ, A.; GALVIN, P. B.; GAGNE, G. *Operating System Concepts*. 10. ed. Wiley, 2018. Cap. 4.

---

## 3. O GIL do Python — ponto central desta análise

O **GIL (Global Interpreter Lock)** é um mecanismo interno do CPython (implementação
padrão do Python) que garante que apenas **uma thread execute bytecode Python por vez**,
mesmo em sistemas com múltiplos núcleos.

### 3.1 Por que o GIL existe?

O GIL foi criado para proteger as estruturas internas do interpretador Python (como o
gerenciamento de referências para coleta de lixo) de condições de corrida. Ele simplifica
enormemente a implementação do interpretador.

### 3.2 Impacto no paralelismo

| Tipo de tarefa | Threads (CPython) | Processos |
|---|---|---|
| CPU-intensiva (primos, cálculos) | **Sem ganho real** — GIL impede paralelismo | **Ganho real** — cada processo tem seu GIL |
| I/O-intensiva (rede, disco) | **Ganho real** — GIL é liberado durante I/O | Ganho, mas overhead maior |

> "O GIL é frequentemente apontado como a principal limitação do Python para aplicações
> de alto desempenho em processamento paralelo." — BEAZLEY, D. *Python Essential Reference*. 4. ed. Addison-Wesley, 2009.

### 3.3 Consequência prática esperada nos experimentos

Para a tarefa de **cálculo de números primos** (CPU-intensiva):
- **Threads:** sem ganho com mais workers — o GIL serializa a execução.
- **Processos:** ganho real de desempenho com mais workers, pois cada processo tem
  seu próprio interpretador e seu próprio GIL.

---

## 4. Escalonamento e troca de contexto

O **escalonador (scheduler)** do SO decide qual processo ou thread ocupa a CPU em cada
momento. A **troca de contexto** é a operação de salvar o estado da tarefa atual e
restaurar o estado da próxima.

- Troca de contexto entre **threads** do mesmo processo: mais rápida (compartilham memória).
- Troca de contexto entre **processos**: mais lenta (exige troca de espaço de endereçamento,
  invalidação de cache TLB).

> **Referência:** STALLINGS, W. *Operating Systems: Internals and Design Principles*. 9. ed. Pearson, 2018. Cap. 4.

---

## 5. Tabela comparativa resumida

| Característica | Processo | Thread |
|---|---|---|
| Espaço de endereçamento | Próprio (isolado) | Compartilhado |
| Custo de criação | Alto | Baixo |
| Comunicação | IPC (pipes, sockets) | Variáveis compartilhadas |
| Isolamento de falha | Total | Parcial (afeta o processo) |
| Paralelismo real (Python) | Sim (multiprocessing) | Não (GIL) |
| Overhead de memória | Alto | Baixo |
| Troca de contexto | Pesada | Leve |

---

## 6. Referências

TANENBAUM, A. S.; BOS, H. **Modern Operating Systems**. 4. ed. Pearson, 2015.

SILBERSCHATZ, A.; GALVIN, P. B.; GAGNE, G. **Operating System Concepts**. 10. ed. Wiley, 2018.

STALLINGS, W. **Operating Systems: Internals and Design Principles**. 9. ed. Pearson, 2018.

BEAZLEY, D. **Python Essential Reference**. 4. ed. Addison-Wesley, 2009.
