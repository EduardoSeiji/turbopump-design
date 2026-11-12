# CFTurbo — entradas da bomba de combustível (turbopump-design, Etapa 3, rev. 2)

Gerado por `etapa3_bomba_combustivel.py` (mesmos valores em `cfturbo_fuel_pump_inputs.csv`).
Baseline: impeller radial **semiaberto**, sem indutor, anel traseiro + furos de balanceamento, voluta simples.

## 1. Design point
| Campo CFTurbo | Valor | Unidade | Nota |
|---|---|---|---|
| Flow rate Q | 3,145 (11,32 m³/h) | L/s | ṁ = 2,5 kg/s |
| Head H | 1667 | m | Δp = 130 bar |
| Speed n | 55 000 | rpm | Etapa 1 rev. 2 |
| Density ρ | 795 | kg/m³ | Jet A 300 K |
| Kinematic viscosity ν | 1,64·10⁻⁶ | m²/s | μ = 1,3 mPa·s |
| Vapor pressure | 0,4 | kPa | |
| NPSH available | 64,1 | m | |
| Inlet swirl | 0 | — | |
| η_h / η_v (chute) | 0,72 / 0,91 | — | η_v inclui o anel traseiro |

## 2. Main dimensions
| Campo | Valor | Unidade |
|---|---|---|
| Shaft (furo) d_S | 14,0 | mm |
| Hub d_H | 20,0 | mm |
| Suction (eye) d_1 | 26,9 | mm |
| Outlet d_2 | 60,0 | mm |
| Outlet width b_2 | 2,81 | mm |
| ψ | 1,096 | — |
| Shroud | open, tip clearance 0,10 mm | — |

## 3. Blades
| Campo | Valor | Unidade |
|---|---|---|
| Number | 6 + 6 splitters (L_split/L = 0,6) | — |
| Thickness LE / TE | 0,8 / 0,8 | mm |
| β1B hub / mean / shroud | 20,0 / 17,3 / 15,6 | ° |
| Incidence | 3 | ° |
| β2B | 25 | ° |

## 4. Volute
| Campo | Valor | Unidade |
|---|---|---|
| Type | single spiral 360°, circular, r·c_u = cte | — |
| Cutwater diameter | 64,2 | mm |
| b_3 | 5,6 | mm |
| Throat | 28,1 mm² (Ø 5,98) | — |
| Diffuser | conical 8°, saída Ø 22,4 mm, L ≈ 117 mm | — |
| Suction nozzle | Ø 28,3 mm | — |

## 5. Lado traseiro (não é entrada do CFTurbo, mas afeta η)
Anel traseiro labirinto Ø 45,2 mm, folga radial 0,05 mm, 5 dentes; furos de balanceamento ventilam a câmara interna para ~p_in. Q_E ≈ 9,8 % de Q.

## 6. Conferir no CFTurbo
η, H, NPSH3 (script: 45,6 m), δ2 (15°), carga de pá, sensibilidade à folga de topo; distribuição de pressão no canal (define d_E do anel traseiro).
