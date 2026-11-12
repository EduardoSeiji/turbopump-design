# Etapa 2 — Bomba de oxidante (HTP 90 %): indutor + impeller + voluta

Projeto didático `turbopump-design` (TCC/Mestrado, Poli-USP). Dimensionamento meanline (1D), rev. 2.

**Resultado:** n = 55 000 rpm; indutor D_t 46,5 → 42 mm, cubo 28 mm; impeller d2 = 63,8 mm, b2 = 4,7 mm, 6 pás, β2B = 25°; voluta dupla 2×180°; P_eixo ≈ 412 kW, η ≈ 0,71.
Detalhes, equações (com fonte), o que mudou na rev. 2 e pendências: `resultados_etapa2.md`.

## Conteúdo
| Arquivo | Descrição |
|---|---|
| `etapa2_bomba_htp.py` | Contas: indutor (NASA SP-8052), impeller (Gülich Tab. 7.1), voluta (Gülich 7.8), vazamentos, potência, empuxo radial, massas/inércias |
| `etapa2_bomba_htp.json` | Geometria e resultados (entrada dos scripts de CAD e da etapa de eixo/mancais) |
| `etapa2_cfturbo.csv` | Parâmetros para digitar no CFTurbo (separador `;`) |
| `saida_etapa2.txt` | Saída do script |
| `resultados_etapa2.md` | Relatório da etapa |

## Como rodar
```bash
pip install -r requirements.txt
python etapa2_bomba_htp.py      # grava o .json e o .csv nesta pasta
```
Os inputs das etapas anteriores (rotação, eixo, cubo, vazamentos do buffer) estão no topo do script, com a fonte comentada.
