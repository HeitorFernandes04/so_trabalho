"""
Trabalho de Sistemas Operacionais
Tema 8: Comparação prática entre Processos e Threads

Tarefa: Cálculo de números primos (CPU intensivo)
Linguagem: Python 3
"""

import multiprocessing
import threading
import time
import csv


# ─────────────────────────────────────────────
# TAREFA: verificar se um número é primo
# ─────────────────────────────────────────────
def eh_primo(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


# ─────────────────────────────────────────────
# WORKERS — precisam estar no escopo GLOBAL
# (obrigatório no Windows com multiprocessing)
# ─────────────────────────────────────────────
def worker_processo(inicio, fim, fila):
    """Worker para processos — retorna resultado via Queue."""
    count = sum(1 for n in range(inicio, fim) if eh_primo(n))
    fila.put(count)


def worker_thread(inicio, fim, resultados, indice):
    """Worker para threads — salva resultado em lista compartilhada."""
    resultados[indice] = sum(1 for n in range(inicio, fim) if eh_primo(n))


# ─────────────────────────────────────────────
# EXPERIMENTO COM PROCESSOS
# ─────────────────────────────────────────────
def rodar_com_processos(limite, num_workers):
    tamanho_bloco = limite // num_workers
    intervalos = [
        (
            i * tamanho_bloco,
            (i + 1) * tamanho_bloco if i < num_workers - 1 else limite
        )
        for i in range(num_workers)
    ]

    fila = multiprocessing.Queue()

    processos = [
        multiprocessing.Process(target=worker_processo, args=(ini, fim, fila))
        for ini, fim in intervalos
    ]

    inicio_tempo = time.perf_counter()
    for p in processos:
        p.start()
    for p in processos:
        p.join()
    fim_tempo = time.perf_counter()

    total = sum(fila.get() for _ in range(num_workers))
    return fim_tempo - inicio_tempo, total


# ─────────────────────────────────────────────
# EXPERIMENTO COM THREADS
# ─────────────────────────────────────────────
def rodar_com_threads(limite, num_workers):
    tamanho_bloco = limite // num_workers
    intervalos = [
        (
            i * tamanho_bloco,
            (i + 1) * tamanho_bloco if i < num_workers - 1 else limite
        )
        for i in range(num_workers)
    ]

    resultados = [0] * num_workers

    threads = [
        threading.Thread(target=worker_thread, args=(ini, fim, resultados, i))
        for i, (ini, fim) in enumerate(intervalos)
    ]

    inicio_tempo = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fim_tempo = time.perf_counter()

    total = sum(resultados)
    return fim_tempo - inicio_tempo, total


# ─────────────────────────────────────────────
# EXECUÇÃO PRINCIPAL
# ─────────────────────────────────────────────
def executar_experimentos():
    LIMITE       = 500_000
    REPETICOES   = 10
    WORKERS_LIST = [1, 2, 4]

    print("=" * 60)
    print("  EXPERIMENTO: Processos vs Threads — Números Primos")
    print(f"  Limite: {LIMITE:,}  |  Repetições: {REPETICOES}")
    print("=" * 60)

    registros = []

    for num_workers in WORKERS_LIST:
        print(f"\n--- {num_workers} worker(s) ---")
        for abordagem, funcao in [("Processos", rodar_com_processos),
                                   ("Threads",   rodar_com_threads)]:
            tempos = []
            for rep in range(1, REPETICOES + 1):
                tempo, total_primos = funcao(LIMITE, num_workers)
                tempos.append(tempo)
                print(f"  [{abordagem:10s}] rep={rep} | "
                      f"tempo={tempo:.3f}s | primos={total_primos:,}")

            tempo_medio = sum(tempos) / REPETICOES
            print(f"  [{abordagem:10s}] MÉDIA = {tempo_medio:.3f}s")

            registros.append({
                "abordagem":          abordagem,
                "workers":            num_workers,
                "tempo_medio":        round(tempo_medio, 4),
                "primos_encontrados": total_primos,
            })

    # Salva CSV
    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        campos = ["abordagem", "workers", "tempo_medio", "primos_encontrados"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros)

    print("\n" + "=" * 60)
    print("  RESUMO FINAL")
    print("=" * 60)
    print(f"{'Abordagem':<12} {'Workers':<10} {'Tempo médio (s)'}")
    print("-" * 35)
    for r in registros:
        print(f"{r['abordagem']:<12} {r['workers']:<10} {r['tempo_medio']}")

    print("\n✔ Resultados salvos em: resultados.csv")


# ─────────────────────────────────────────────
# ENTRY POINT — obrigatório no Windows
# ─────────────────────────────────────────────
if __name__ == "__main__":
    multiprocessing.freeze_support()
    executar_experimentos()
