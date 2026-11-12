# Etapa 3 — Bomba de combustível (Jet A): impeller semiaberto + voluta

Projeto didático `turbopump-design` (TCC/Mestrado, Poli-USP). Dimensionamento meanline (1D), rev. 2.

**Resultado:** n = 55 000 rpm, n_q 11,8; impeller radial semiaberto sem indutor, 6 pás + 6 splitters, d2 = 60,0 mm, b2 = 2,81 mm, β2B = 25°; anel traseiro Ø45,2 mm + furos de balanceamento (empuxo axial ≈ 0); voluta simples, garganta Ø6,0 mm; P_eixo ≈ 74 kW, η ≈ 0,55; F_NPSH 1,41.
Detalhes, equações (com fonte), o que mudou na rev. 2, comparação de conceitos (fechado, Barske/emissão parcial, 2 estágios) e pendências: `resultados_etapa3.md`.

## Conteúdo
| Arquivo | Descrição |
|---|---|
| `etapa3_bomba_combustivel.py` | Contas: η estatística (Gülich Tab. 3.9), NPSH3 (Eq. 6.10/Fig. 6.20), impeller (Tab. 7.1), voluta (Eq. 3.14), vazamentos, atrito de disco, empuxos, massas/inércias, alternativas |
| `fuel_pump_geometry.json` | Geometria e cargas em mm/° (entrada dos scripts de CAD e da etapa de eixo/mancais) |
| `cfturbo_fuel_pump_inputs.csv` / `.md` | Parâmetros para digitar no CFTurbo |
| `etapa3_raw.json` | Todos os resultados intermediários (baseline, semiaberto sem anel, fechado, alternativas) |
| `saida_etapa3.txt` | Saída do script (inclui sensibilidades) |
| `resultados_etapa3.md` | Relatório da etapa |

## Como rodar
```bash
pip install -r requirements.txt
python etapa3_bomba_combustivel.py > saida_etapa3.txt   # grava .json e .csv nesta pasta
```
Inputs das etapas anteriores (vazão, pressões, propriedades, rotação, furo/cubo do eixo, k_R) ficam no topo do script (`FL`, `BASE`), com a fonte comentada. O diâmetro do anel traseiro é resolvido automaticamente para empuxo axial nulo.
