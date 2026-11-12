# Etapa 0 — Propriedades dos fluidos e balanço do ciclo

Primeira etapa do projeto didático `turbopump-design` (TCC/Mestrado, Poli-USP): turbobomba de eixo único
(bomba de HTP 90 % + bomba de Jet A + turbina a gás de HTP decomposto).

## Conteúdo
| Arquivo | Descrição |
|---|---|
| `etapa0_ciclo.py` | Propriedades a 300 K, H/Q/potências das bombas, gás de decomposição do HTP (Cantera) e balanço da turbina |
| `saida_etapa0.txt` | Saída do script |
| `requirements.txt` | Dependências |

## Como rodar
```bash
pip install -r requirements.txt
python etapa0_ciclo.py
```

## Resultados principais
| Grandeza | Bomba HTP | Bomba Jet A |
|---|---|---|
| Q | 12,6 L/s | 3,1 L/s |
| H | 1693 m | 1667 m |
| P hidráulica | 291 kW | 41 kW |
| η assumida | 0,60 | 0,45 |
| P de eixo | 484 kW | 91 kW |

- Potência requerida da turbina ≈ 593 kW (η_mec = 0,97).
- Gás de HTP 90 %: T adiabática 1030 K (líquido a 298 K) / 1182 K (líquido a 400 K); M = 22,1 g/mol, γ = 1,255.
- Turbina 150 → 130 bar, 1150 K: Δh_s = 61 kJ/kg; necessário ΔT ≈ 18 K com η_T ≈ 0,56
  (ΔT = 10 K não fecha o balanço).

Hipóteses: composição congelada, gás ideal, calor de mistura do HTP desprezado, η provisórias (revisar na Etapa 1).
