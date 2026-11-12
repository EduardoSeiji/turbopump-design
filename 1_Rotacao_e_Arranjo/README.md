# Etapa 1 — Rotação do eixo único e arranjo sob a bomba de oxidante

Projeto didático `turbopump-design` (TCC/Mestrado, Poli-USP).

**Decisão:** n = 55 000 rpm. Eixo monolítico IN718 Ø24 mm sob a bomba de oxidante (OP). Cubo do indutor de 28 mm (ν = 0,61), D_t ≈ 46 mm.
Detalhes, equações (com fonte) e pendências em `resultados_etapa1.md`.

## Conteúdo
| Arquivo | Descrição |
|---|---|
| `etapa1_rotacao.py` | v1: varredura em n (cavitação por n_ss, n_q, u2, DN, η de Gülich T3.9.1) |
| `etapa1_rev_rotacao_arranjo.py` | rev. 2: cavitação do indutor pelo número de cavitação K (NASA SP-8052) + 1ª crítica (viga FE + discos) para opções de eixo sob a OP |
| `indutor_OP_K.csv` | K_op, D_t, u_t, φ, β_B vs cubo e rotação |
| `critica_rotor.csv` | 1ª crítica forward síncrona por caso (k mancais 50/100 e 100/200 MN/m) |
| `resultados_etapa1.json` | Resumo numérico da decisão (entrada das etapas seguintes) |
| `saida_etapa1_*.txt` | Saída dos scripts |
| `resultados_etapa1.md` | Relatório da etapa |

## Como rodar
```bash
pip install -r requirements.txt
python etapa1_rotacao.py
python etapa1_rev_rotacao_arranjo.py   # grava os .csv e o .json nesta pasta
```
O modelo do rotor dá a 1ª crítica cerca de 2,4 % abaixo do modelo da etapa de eixo/mancais. Use os números para comparar casos entre si, não como valor absoluto.
