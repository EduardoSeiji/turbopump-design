# Etapa 4 — Turbina axial (meanline 1D)

Projeto didático `turbopump-design` (TCC/Mestrado, Poli-USP). Rev. 2.

**Resultado:** n = 55 000 rpm; turbina axial de 1 estágio, admissão total, reação 50 %; Dm = 73,0 mm, h = 19,6 mm, 23 bocais / 29 pás; η_ts ≈ 0,73 (mínimo necessário 0,47); P = 501 kW, T = 87 N·m; rotor 296 g, Ip 247 / Id 127 kg·mm².
Detalhes, equações, o que mudou na rev. 2 e pendências: `resultados_etapa4.md`.

## Conteúdo
| Arquivo | Descrição |
|---|---|
| `etapa4_turbina.py` | Gás de HTP 90 % (Cantera), balanço de potência, triângulos, perdas de Soderberg, geometria, tensões, massa/inércias, cargas |
| `etapa4_turbina.json` | Resultados e geometria (entrada da etapa de eixo e do CAD) |
| `etapa4_varredura_phi.csv` | Varredura do coeficiente de vazão φ (reação 50 % e impulso) |
| `etapa4_cfturbo.csv` | Parâmetros para o CFTurbo (separador `;`) |
| `saida_etapa4.txt` | Saída do script |
| `resultados_etapa4.md` | Relatório da etapa |

## Como rodar
```bash
pip install -r requirements.txt
python etapa4_turbina.py > saida_etapa4.txt   # também grava .json e .csv nesta pasta
```
Os inputs das etapas anteriores (rotação, potências das bombas, vazamento S7, furo do disco) ficam no topo do script, com a fonte comentada.
