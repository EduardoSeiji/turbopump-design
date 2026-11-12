# Etapa 5 — Eixo, mancais e selos (preliminar, sem ROSS)

Projeto didático `turbopump-design` (TCC/Mestrado, Poli-USP). Rev. 2.

**Resultado:** n = 55 000 rpm; arranjo FP (balanço) – B1 (par DB, Jet A) – pacote interpropelente com purga de He – OP (eixo passante Ø24) – B2 (rolos, buffer HTP) – turbina (balanço); rotor 1,28 kg, z_CG 116 mm, Ip 399 / Id 5098 kg·mm²; empuxo axial líquido −1,6 kN; 1ª crítica 84 000 rpm (1,53·n) com mancais de 50/100 MN/m.
Detalhes, o que mudou na rev. 2, discordâncias e pendências: `resultados_etapa5.md`.

## Conteúdo
| Arquivo | Descrição |
|---|---|
| `etapa5_eixo_mancais.py` | Torques, diâmetro mínimo (torção + fadiga), empuxos axial e radial, mancais, selos, 1ª crítica (FE de viga + giroscópico), massas e inércias |
| `etapa5_eixo_mancais.json` | Todos os resultados (entrada do CAD e do ROSS) |
| `etapa5_rotor_massas.csv` | Peças do rotor: m, z_CG, Ip, Id (separador `;`) |
| `etapa5_eixo_segmentos.csv` | Segmentos do eixo (z, Ø, material) |
| `etapa5_criticas.csv` | 1ª crítica × rigidez dos mancais |
| `saida_etapa5.txt` | Saída do script |
| `resultados_etapa5.md` | Relatório da etapa |

## Como rodar
```bash
pip install -r requirements.txt
python etapa5_eixo_mancais.py > saida_etapa5.txt   # também grava .json e .csv nesta pasta
```
O script lê `../2_Bomba_HTP/etapa2_bomba_htp.json`, `../3_Bomba_JetA/fuel_pump_geometry.json` e `../4_Turbina/etapa4_turbina.json`. Se algum não existir, usa os valores dos relatórios (fallback) e avisa. Rode a partir de qualquer pasta. A varredura da crítica leva ~1 min.
