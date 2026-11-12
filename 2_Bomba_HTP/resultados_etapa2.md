# Etapa 2 — Bomba de oxidante (OP, HTP 90 %): indutor + impeller + voluta (meanline) — **rev. 2**

> Script: `etapa2_bomba_htp.py` → `etapa2_bomba_htp.json` (geometria p/ CAD), `etapa2_cfturbo.csv` (entrada CFTurbo), `saida_etapa2.txt`.
> SI; n em rpm; n_q e n_ss métricos do Gülich [rpm, m³/s, m]. Data: 2026-11-12. **Status: meanline 1D, a validar no CFTurbo.**
> Rev. 2 troca as premissas da rev. 1 pelos resultados de 01 (Etapa 0), 02 (Etapa 1 rev. 2), 04 (FP) e 06 (eixo/mancais/selos).

## 0. Resumo
n = 55 000 rpm · indutor D_t 46,5 → 42 mm, cubo 28 mm, K_op = 0,0256 (≥ 0,025 ✔) · impeller d2 = 63,8 mm, b2 = 4,7 mm, 6 pás, β2B = 25° · voluta **dupla** 2×180°, garganta Ø10,0 mm cada · **P_eixo = 412 kW, η = 0,706, T = 71,5 N·m** · impeller 42 g + indutor 17 g (Al 6061).

## 1. O que mudou (rev. 1 → rev. 2)
| Item | rev. 1 (premissa) | rev. 2 (resultado real) | Fonte |
|---|---|---|---|
| Eixo sob a OP / furo | ~16 mm (premissa) | **24 mm IN718 maciço** | 02 §0, §5 |
| Cubo do indutor (ν) | 20 → 24 mm (0,49) | **28 mm constante (0,60)** | 02 §0; 06 §10 |
| Critério de cavitação | só F_NPSH 1,2 | F_NPSH 1,2 **e K_op ≥ 0,025** | 02 §3 |
| D_t indutor / u_t | 41,0 mm / 118 m/s | **46,5 mm (entrada) → 42 mm (saída)** / 134 m/s | 02 §3 |
| φ / β1B ponta / K_op | 0,106 / 10,6° / 0,031 | 0,088 / **8,7°** / **0,0256** | SP-8052 |
| Indutor: comprimento / H | 19,7 mm / 94,7 m | 18,5 mm / 100,4 m | — |
| Olho d1 / d1/d2 | 41 mm (= D_t) / 0,65 | 42 mm (ponta afunilada) / 0,66 (≤ 0,70 ✔) | 02 §3; Huzel p.182 |
| Cubo do impeller dn | 24 mm | 28 mm | — |
| Vazões internas | só anel frontal | + furos de balanceamento (anel traseiro) + S6 (120 g/s → sucção) + S7 (50 g/s → turbina) | 06 §5.2, §7 |
| η_v | 0,943 | **0,882** | — |
| d2 / b2 / u2 | 63,3 / 4,69 mm / 182 m/s | **63,8 / 4,72 mm / 184 m/s** | — |
| δ (desvio) | 13,6° | 13,3° | — |
| Voluta | simples, garganta Ø14,2 mm | **dupla 2×180°**, Ø10,0 mm cada (simples: Ø13,9) | 06 §5.1 |
| P_eixo / η_OP / torque | 387 kW / 0,752 / 67,1 N·m | **412 kW / 0,706 / 71,5 N·m** | — |
| F_R BEP / shut-off | 475 N / 2,6 kN (simples) | 685 N **constante** (dupla) | Gülich 9.3.10 |
| Massa impeller / indutor | 45 / 18 g | **42 / 17 g** (+ 13 g de fluido no impeller) | — |
| Ip impeller / indutor | 2,05e-5 / 3,2e-6 kg·m² | 2,29e-5 / 4,3e-6 kg·m² | — |

## 2. Hipóteses / decisões
1. Arranjo da 06/02: OP no meio do eixo, entrada por cotovelo lateral, eixo passante Ø24. Indutor e impeller em Al 6061-T6, montados sobre luva/revestimento compatível com HTP (02 §0).
2. Indutor de **placa plana, passo constante** (r·tanβ = cte), 3 pás, solidez 2,5, folga 0,2 mm, η_ind = 0,70. A ponta fica constante por 1 passo axial (7,5 mm, SP-8052 §2.1.3) e depois afunila de 46,5 para 42 mm até o olho.
3. H_ind: NPSHA_imp ≥ 1,3·NPSH3_imp, com n_ss do impeller = 200 (Gülich Tab. D6.1). Saída do indutor em vórtice livre (r·c_u = cte), o que dá pré-rotação no olho do impeller.
4. Impeller fechado. Anéis de desgaste frontal e traseiro iguais (Ø47, folga 0,08 mm, labirinto μ ≈ 0,45) + furos de balanceamento: vazamento traseiro ≈ frontal (06 §5.2: obrigatório).
5. η_h = 0,83 (Gülich Fig. 3.27, conservador). z = 6, e = 1,5 mm, β2B = 25° fixo, d2 resolvido.
6. Voluta dupla 2×180°: cada parcial dimensionada para 1,10·Q/2 (Gülich 7.8.1: duplas com n_q baixo → Q_Le = 1,05–1,25·Q). Seção circular, velocidade constante (n_q < 25–35), d_z/d2 = 1,07, b3/b2 = 2.

## 3. Equações (fonte)
| Grandeza | Equação | Fonte |
|---|---|---|
| Cavitação do indutor | τ = 2g·NPSH/u_t² = K + Kφ² + φ²; D_t que maximiza K | NASA SP-8052 eq. 2, §3.1.3.1(A) |
| Brumfield | K = 2φ²/(1 − 2φ²) | SP-8052 eq. 5 |
| β_B indutor | β_B = β_flow/(1 − α/β), α/β = 0,425 | SP-8052 §3.1.9 |
| Passo | λ = 2πr·tanβ = cte | SP-8052 eq. 31 |
| Placa plana | ψ = gH/u_t² ≲ 0,075 | SP-8052 §2.1.12 |
| n_q, n_ss | n√Q/H^0,75 ; n√Q/NPSH3^0,75 | Gülich eq. 2.5, 6.7 |
| Q_La | Q_La = Q_Le + Q_sp + Q_E | Gülich T7.1.1 |
| b2 | b2* = 0,017 + 0,262x − 0,08x² + 0,0093x³ | Gülich eq. 7.1 |
| β1B | arctan[c1m·τ1/(u1 − c1u)] + i1 | Gülich T7.1.7 |
| Slip | γ = 0,98·(1 − √sinβ2B/z^0,7)·k_w | Gülich T3.2.6 |
| c2u / Euler | c2u = u2[γ − c2m·τ2/(u2 tanβ2B)]; H = η_h(u2c2u − u1c1u)/g | Gülich T3.2.7, T7.1.9 |
| Vazamento do anel | Q = μπd_sp·s·√(2gH_sp), H_sp = H_p − (u2² − u_sp²)/8g | Gülich cap. 3.6 (simplif.) |
| Atrito de disco | M = 2·½·c_M·ρω²r2⁵, c_M = 0,051(s/r)^0,1/Re^0,2 | Gülich Tab. 3.6 |
| Garganta | Q_Le·ε_sp/2π = r2c2u·∫(b/r)dr | Gülich eq. 3.15, 7.24 |
| Seções | A(ε) = A3q·ε/ε_sp | Gülich eq. 7.26–7.27 |
| Lingueta | α3B = arctan[(Q/πd3b3)/(c2u·d2/d3)] | Gülich eq. 3.16–3.19 |
| Empuxo radial | F_R = k_R·ρgH·d2·b2tot; dupla ≈ 0,15·k_R0 | Gülich eq. 9.6, Fig. 9.27/9.28, §9.3.10 |

## 4. Resultados
### 4.1 Vazões
| Q útil | Q indutor (+S6) | Q voluta (+S6+S7) | Q_sp frontal | Q_E furos | Q_La impeller | η_v |
|---|---|---|---|---|---|---|
| 12,64 L/s | 12,72 | 12,76 | 0,79 | 0,79 | **14,33 L/s** | 0,882 |

### 4.2 Indutor
| Grandeza | Valor |
|---|---|
| D_t entrada / saída | **46,5 / 42,0 mm** (ótimo de Brumfield 46,3 mm); ponta constante por 7,5 mm |
| Cubo / furo | 28 / 24 mm (ν = 0,60) |
| u_t / c_m / φ | 133,9 / 11,8 m/s / 0,088 |
| τ / K_op / K_Brumfield | 0,0335 / **0,0256** (≥ 0,025 ✔; 2,6 × K* 0,01) / 0,0156 |
| β1 escoam. / β1B ponta / incidência / β1B cubo | 5,0° / **8,7°** / 3,7° / 14,3° |
| Passo / β2B ponta saída / desvio | 22,4 mm / 9,6° / 1,0° |
| z / solidez / corda / L axial / wrap | 3 / 2,5 / 122 mm / **18,5 mm** / ≈ 300° |
| Espessuras ponta/cubo / folga | 0,8 / 1,6 / 0,2 mm |
| H / ψ_NASA / P | **100,4 m** / 0,055 / 24,8 kW |
| NPSHA no olho / NPSH3_imp | 137,2 / 105,5 m (1,30 ✔) |

### 4.3 Impeller
| Grandeza | Valor |
|---|---|
| d2 / b2 / b2* | **63,75 / 4,72 mm** / 0,074 |
| d1 / dn / furo / d1/d2 | 42 / 28 / 24 mm / 0,66 |
| u1 / u2 | 121,0 / **183,6 m/s** |
| c1m / c1u / w1 | 18,6 / 11,6 / 110,9 m/s |
| β1B shroud / hub (i = 2°) | 15,0° / 23,8° |
| β2B / β2 / δ | 25° / 11,7° / 13,3° (≤ 14 ✔) |
| γ / τ2 / ψ / φ2 | 0,798 / 1,12 / 0,927 / 0,083 |
| c2m / c2u / c2 / α2 | 15,2 / 110,2 / 111,2 m/s / 7,8° |
| w2 / w2/w1 | 74,9 m/s / 0,68 |
| H / H_th | 1593 / 1919 m |
| Anéis de desgaste frente/trás | Ø47 mm, folga radial 0,08 mm |

### 4.4 Voluta dupla e difusor
| Grandeza | Valor |
|---|---|
| d_z / e3 (lingueta e nervura) / α3B / b3 | 68,2 / 1,5 mm / 3,5° / 9,45 mm |
| Garganta de cada voluta parcial | **Ø10,05 mm** (79 mm²), c3q = 88 m/s, c3q/c2 = 0,80 |
| Seções (cada parcial, 0–180°) | d = d3q·√(ε/180°) (passo de 30° no JSON) |
| Alternativa simples | Ø13,85 mm, c3q/c2 = 0,76 |
| Difusor | Ø eq. 14,2 → 25 mm, semiângulo 5°, L = 62 mm, c_saída = 26 m/s |

### 4.5 Desempenho
| P_h | P_impeller | P_indutor | P_disco | **P_eixo** | **η_OP** | **Torque** |
|---|---|---|---|---|---|---|
| 290,6 kW | 373,6 kW | 24,8 kW | 13,2 kW | **411,6 kW** | **0,706** | **71,5 N·m** |
Sem mancais/selos. A furação de balanceamento custou ~4,5 pontos de η.

### 4.6 Dados para rotodinâmica (06 / TCC)
| Grandeza | Valor | Nota |
|---|---|---|
| Impeller Al 6061: m / Ip / Id | 41,7 g / 2,29e-5 / 1,17e-5 kg·m² | ±20 %; Id no CG da peça |
| Indutor: m / Ip / Id | 16,8 g / 4,26e-6 / 2,58e-6 kg·m² | |
| Fluido nos canais do impeller | 13,2 g / Ip 9,6e-6 kg·m² | somar como massa adicional |
| F_R voluta dupla (estática 0,031 + dinâmica 0,03) | **685 N** em toda a faixa | |
| F_R simples (comparação) | 481 N BEP / 2,64 kN shut-off | |
| F_R de projeto (k_R,tot 0,15) | 1,70 kN | Gülich 9.3 item 13 |
| Freq. de passagem de pás | 5,5 kHz (impeller) / 2,75 kHz (indutor) | RSI (interação rotor-estator) |
| Anéis Ø47, folga 0,08 mm | 2 anéis | rigidez de Lomakin (efeito de mancal do anel) → ROSS |
| Torque OP | 71,5 N·m | turbina → OP: (412 + 74)/0,97/ω ≈ 87 N·m ✔ (02) |

## 5. Discordâncias com etapas anteriores (sinalizadas, não alteradas)
1. **06 §5.1 diz que a voluta dupla reduz F_R em 50–70 %.** Isso só vale **fora do ponto de projeto**. No BEP (Best Efficiency Point, ponto de máxima eficiência) a simples já tem k_R ≈ 0,013, e a dupla fica em ~0,03 (481 → 685 N). O ganho real é no transitório de partida e em carga parcial (2,64 → 0,69 kN). Adotei a dupla por isso, mas é escolha discutível: a garganta cai para Ø10 mm, há nervura extra e o CAD fica mais complexo.
2. **06 §9 usa impeller OP 57,9 g e indutor 26,6 g**; aqui saem 41,7 g e 16,8 g (+13 g de fluido). A 06 deve atualizar massas e inércias.
3. **06 §5.2 usa d_sp = 51 mm** para o empuxo axial da OP; aqui o anel é **Ø47 mm**, frontal e traseiro → refazer o empuxo.
4. **06 §4/§9 ainda tem o eixo sob a OP com Ø20**; a 02 rev. 2 decidiu Ø24, e esta etapa já usa 24. A 06 precisa atualizar a crítica.
5. **02 §1: "η_OP 0,70 com perdas mecânicas"**: o meanline já dá 0,706 *sem* perdas mecânicas, por causa dos furos de balanceamento. Para o ciclo, η_OP ≈ 0,68. O impacto na turbina é pequeno (P_OP 412 vs 415 kW, porque o mecânico já está no η_mec 0,97).
6. **05 (turbina)** ainda usa ρ = 1390 kg/m³ e η assumidos; não é desta etapa.

## 6. Comparação com a referência
Referência: 60 000 rpm. Com cubo 28, o indutor a 60 krpm teria K ≈ 0,022 < 0,025 (02 §3). Esta etapa confirma os 55 krpm da 02: K_op = 0,0256 deixa ~2 % de folga. A geometria da bomba de referência não está disponível.

## 7. Pendências
1. CFTurbo: H, η_h, δ, carga de pá, NPSH3 do indutor (λ_w e K* reais). Se K* ≤ 0,01 for confirmado, a margem existe.
2. Voluta dupla vs simples: decidir com a 06 (cargas de partida nos mancais) e com a fabricação da garganta de Ø10.
3. Tensões nas pás do indutor (0,8 mm Al a 134 m/s) e modos de pá.
4. Furos de balanceamento: diâmetro e número (dimensionar para Q_E ≈ 0,8 L/s com Δp pequeno).
5. Alternativa δ: 7 pás e β2B 22° (δ ≈ 11°).
6. Conferir no PDF: solidez típica (SP-8052 §2.1.5), d_z/d2 para alta pressão (Gülich Tab. 10.2), c_M de Daily & Nece, curva F_Dsp (Fig. 9.29).
