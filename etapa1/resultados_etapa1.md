# Etapa 1 — Rotação do eixo único e arranjo sob a OP (turbopump-design) — **rev. 2**

> Scripts: `etapa1_rotacao.py` (v1, varredura; coeficiente de η corrigido) e `etapa1_rev_rotacao_arranjo.py` (rev. 2: cavitação por K + 1ª crítica).
> Unidades SI; n em rpm; n_q e n_ss métricos do Gülich [rpm, m³/s, m]; S em US (S = n_ss/0,0194, Gülich Eq. T3.4.18). Data: 2026-11-12.
> Rev. 2 substitui as premissas da v1 pelos resultados de 01 (Etapa 0), 03 (OP), 04 (FP), 05 (turbina) e 06 (eixo/mancais).

## 0. Decisão (resumo)
- **n_nominal = 55 000 rpm** (mantida; 60 000 rpm rejeitada nesta revisão — §6).
- **Arranjo mantido (06 §2):** FP em balanço – B1 (par contato angular, Jet A) – pacote interpropelente – **OP com eixo passante** – B2 (rolos, HTP) – turbina em balanço.
- **Sob a OP: eixo monolítico IN718 Ø24 mm** (maciço ou oco Ø12), luva/revestimento compatível com HTP; indutor + impeller de Al 6061 montados sobre ele. **Cubo do indutor na entrada = 28 mm (ν = 0,61).** Indutor reotimizado para esse cubo: **D_t ≈ 46 mm**.
- **Rotor empilhado com tie-bolt e peças de Al: rejeitado** (perde rigidez — §5).
- Critério de cavitação da OP passa a ser **K_op ≥ 0,025** (número de cavitação de pá, 2,5 × K* experimental), além de F_NPSH = 1,2 no NPSH.

## 1. O que mudou (v1 → rev. 2)
| Item | v1 (premissa) | rev. 2 (resultado real) | Fonte |
|---|---|---|---|
| ρ HTP / Jet A | 1385 / 795 kg/m³ | igual | 01 §1 |
| p_v Jet A | 1000 Pa | 400 Pa (irrelevante) | 01 §1 |
| NPSHA OP / FP | 36,8 / 64,0 m | 36,8 / 64,1 m | 01 §2 |
| η correlação Gülich T3.9.1 | 0,76 / 0,53 (**errado**: expoente m com 0,08) | 0,73 / 0,42 (m com 0,1; FP fora da faixa Q ≥ 5 L/s) | Gülich Tab. 3.9 |
| η_OP | 0,76 | 0,752 meanline; **0,70 p/ ciclo** (c/ perdas mec./traseira) | 03 §4.4 |
| η_FP | 0,53 | 0,60 meanline semiaberto; **0,55 adotado** | 04 §4 |
| P_OP / P_FP (eixo) | 382 / 77 kW | 415 / 74 kW (η 0,70 / 0,55) | 03, 04 |
| P turbina (η_mec 0,97) | 458 kW (sem η_mec) | **504 kW** | — |
| Torque turbina → OP | 80 N·m | **87,5 N·m** (nominal) | — |
| FP indutor | "talvez" | **sem indutor** (NPSH3 35,7 m, F_NPSH 1,80) | 04 §5 |
| Cubo do indutor OP (ν) | 0,30 (premissa) | **0,61** (cubo 28 mm, eixo passante) | 06 §10 |
| Critério de cavitação OP | n_ss = 500 @ ν 0,3 (equivale a K ≥ 0,034) | **K_op ≥ 0,025** + F_NPSH 1,2 | SP-8052 §2.1.3 |
| n_max cavitação OP | 57,9 krpm | **55,8 krpm** (cubo 28) · 61,8 (cubo 20) | §3 |
| D_t / u_t indutor @55k | 39,4 mm / 114 m/s | **46,2 mm / 133 m/s** | §3 |
| d mancal / DN | 20,9 mm / 1,15·10⁶ (estimado) | 20 mm / 1,10·10⁶ | 06 §6 |
| 1ª crítica | não avaliada | 1,28·n (eixo Ø24 sob OP, k 50/100 MN/m) | §5 |
| Restrição da turbina | não avaliada | h/Dm 0,27 @55k vs 0,32 @60k | 05 §6 |

## 2. Inputs e hipóteses
- Ponto de projeto: OP Q = 12,64 L/s, H = 1693 m; FP Q = 3,145 L/s, H = 1667 m (01 §2).
- NPSH de projeto do indutor = NPSHA/F_NPSH = 36,8/1,2 = 30,6 m (F_NPSH mantido de v1).
- Modelo do rotor: viga Euler-Bernoulli FE + discos com (Id − Ip) (forward síncrona), segmentos/massas/inércias do 06 §9, mancais B1 (z 34/46, k_B1 total do par) e B2 (z 158). Calibração: 65 700 rpm vs 67 300 rpm do 06 (−2,4 %; diferença vem da interpretação de k_B1 e da discretização). **Usar como comparação relativa.**

## 3. Cavitação da OP pelo número de cavitação K (NASA SP-8052)
Mecanismo: K = (p − p_v)/(½ρw²) na ponta da pá mede quanto "sobra" de pressão sobre a pá no bordo de ataque. A pá só funciona até um K* mínimo, que depende da espessura e do ângulo dela.
Equações: τ = 2g·NPSH/u_t² = K + Kφ² + φ² (SP-8052 eq. 2); D_t que maximiza K (Brumfield, eq. 5–6); S'_max = 5055/[(1+K)^¼·K^½] (eq. 7); S = S'·√(1−ν²) (eq. 4). K* experimental = 0,006–0,01 para pás muito finas (§2.1.3).

| Cubo [mm] | n [krpm] | D_t [mm] | ν | u_t [m/s] | φ | β_B ponta | **K_op** | K_op/K*(0,01) | S req [US] |
|---|---|---|---|---|---|---|---|---|---|
| 20 (03) | 55 | 40,9 | 0,49 | 118 | 0,108 | 10,7° | 0,0315 | 3,2 | 24 450 |
| **28 (06)** | **55** | **46,2** | **0,61** | **133** | **0,089** | **8,9°** | **0,0258** | **2,6** | 24 450 |
| 28 | 60 | 46,2 | 0,61 | 145 | 0,082 | 8,1° | 0,0217 | 2,2 | 26 700 |

n_max para K_op = K_lim:
| Cubo [mm] | K_lim 0,034 (= critério v1) | **K_lim 0,025** | K_lim 0,020 |
|---|---|---|---|
| 14 | 56,5 | 66,1 | 73,9 |
| 20 | 52,9 | 61,8 | 69,2 |
| 24 | 50,4 | 58,8 | 65,8 |
| 28 | 47,8 | **55,8** | 62,5 |

Leituras:
- Cubo maior não muda o S requerido (S usa a vazão real); muda o S **corrigido** S' = S/√(1−ν²) e, portanto, o K em que a pá opera. A otimização de Brumfield compensa parte disso aumentando D_t.
- O critério físico "K real ≈ 2–3 × K_min de supercavitação" (SP-8052 eq. 29–30) dá K_op/K_cr ≈ 1,2–1,4 **em qualquer n** (os dois escalam com φ²). Ele valida a pá, mas não limita a rotação. Quem limita é o K* empírico.
- O n_max = 47,6 krpm do 06 §10 vem de manter o K implícito da minha v1 (0,034 ≈ 3,4 × K*), que somado ao F_NPSH 1,2 era margem dupla. **Com K_lim = 0,025, 55 krpm passa mesmo com cubo de 28 mm (folga de ~1,5 % em n). 60 krpm exigiria aceitar K_op ≈ 0,022.**
- Custos do cubo 28: u_t 118 → 133 m/s (mais risco de erosão; aceitável para uso único com Al anodizado, SP-8052 §3.5.2.1); olho maior. Com d1 = D_t = 46 mm, d1/d2 = 0,73 > 0,70 (Huzel p.182), então o indutor deve **afunilar a ponta na saída** (~41–42 mm) para o impeller.

## 4. Demais limites a 55 krpm (atualizados)
| Limite | Valor | Admissível | Status | Fonte |
|---|---|---|---|---|
| u2 OP (Al 6061) | 182 m/s | 286 m/s (disco furado, SF 1,5) | ✔ | 03 §4.2; v1 §4.4 |
| u2 FP (17-4PH ou Al 7075) | 172 m/s | 323 / 352 m/s | ✔ | 04 §6 |
| DN B1 / B2 (bore 20) | 1,10·10⁶ | 2,1·10⁶ / 1,6·10⁶ | ✔ | 06 §6; Huzel p.209 |
| n_q OP / FP | 23,4 / 11,8 | — | FP no limite inferior econômico (Gülich §2.2) | 03, 04 |
| Turbina h/Dm / σ_raiz | 0,27 / ~195 MPa | ≲ 0,25 p/ pá curta sem torção | ⚠ leve | 05 §6 |
| 1ª crítica / n | 1,28 (Ø24 sob OP) | ≥ 1,20 | ✔ (depende da rigidez de mancal) | §5; Huzel p.206 |

## 5. Arranjo do eixo sob a OP (decisão)
Seção equivalente de aço (mesmo EI, E = 200 GPa):
| Construção sob a OP | d_eq [mm] |
|---|---|
| 06: IN718 Ø20 maciço + luva/cubo não estrutural | 20,0 |
| Tie-bolt IN718 Ø12 + cubos Al 6061 Ø22 (junta perfeita) | **17,5** |
| Tie-bolt IN718 Ø12 + cubos 316L Ø22 | 21,8 |
| **IN718 Ø24 maciço** | **24,0** |
| IN718 Ø24 oco Ø12 | 23,6 |

1ª crítica (modelo rev. 2):
| Caso | k 50/100 MN/m [rpm] | k 100/200 [rpm] | n_c/55k | n_c/60k |
|---|---|---|---|---|
| 06 base (Ø20 sob OP) | 65 700 | 73 700 | 1,19 | 1,10 |
| Tie-bolt + Al (d_eq 18) | 61 300 | 66 900 | 1,11 ❌ | 1,02 ❌ |
| Ø22 | 68 700 | 78 700 | 1,25 | 1,14 |
| **Ø24 (escolhido)** | **70 500** | **82 400** | **1,28** | 1,18 |
| Ø24 + pacote IP −10 mm | 70 800 | 84 500 | 1,29 | 1,18 |

Por que Ø24 maciço e cubo 28:
- O trecho sob a OP manda na 1ª crítica (06 §8). Ir de 20 para 24 mm dá +7 % em n_c.
- O preço é o cubo do indutor maior (ν 0,61). O §3 mostra que esse custo cabe em 55 krpm.
- Tie-bolt só ajudaria com peças de aço. Peças de Al têm E ≈ ⅓ do aço e derrubam o EI. Com 316L, a massa sobe ~3× (03 §4.5) e a tensão a 182 m/s fica perto do escoamento do 316L.
- Encurtar o pacote interpropelente rende só +0,3–1,7 % → vale fazer se for barato, mas não resolve sozinho.
- **A rigidez dos mancais pesa mais que a geometria do eixo:** 50/100 → 100/200 MN/m dá +17 %. Isso é a pendência nº 1.
- Torção e fadiga sob a OP estão folgadas: T ≈ 21 N·m (só o torque da FP passa por ali), M ≈ 36 N·m → σ ≈ 27 MPa em Ø24.

## 6. Rotação final: 55 vs 60 krpm
| Critério | 55 krpm | 60 krpm | Vence |
|---|---|---|---|
| Cavitação OP (cubo 28) | K 0,026 (2,6 × K*) | K 0,022 (2,2 × K*) | 55 |
| 1ª crítica (k 50/100) | 1,28·n ✔ | 1,18·n ❌ (precisa k ≥ ~70/140 MN/m) | 55 |
| Turbina (h/Dm, σ_raiz) | 0,27 / ~195 MPa | 0,32 / 232 MPa | 55 |
| η FP | 0,60 | 0,61 | ≈ |
| Massa OP | — | d2 58 mm, ~−20 % | 60 |
| DN | 1,10·10⁶ | 1,20·10⁶ | ≈ |
→ **55 000 rpm.** Os 60 krpm só passam se três coisas forem confirmadas ao mesmo tempo: rigidez de mancal ≥ ~70/140 MN/m, K* ≤ 0,01 do indutor real (CFTurbo/teste) e pá de turbina torcida/afilada.

## 7. Comparação com a referência (só no fim)
Referência: 60 000 rpm. Proposta: 55 000 rpm (−8 %).
A diferença agora tem causa identificada:
- a referência deve ter mancais mais rígidos (ou um vão B1–B2 menor);
- e/ou aceita indutor com K ≈ 0,022.

A cavitação deixou de ser a explicação única: com cubo de 20 mm (eixo fino), 60 krpm cabe em K_lim 0,025, mas aí a crítica cai para 1,10·n. Pendência: obter da referência posição/tipo dos mancais e cubo do indutor.

## 8. Discordâncias com etapas anteriores (sinalizadas, não alteradas)
1. **06 §10 (n_max 47,6 krpm com ν 0,62):** decorre do critério implícito K ≥ 0,034 da minha v1, que somado ao F_NPSH 1,2 era margem dupla. Com K_lim 0,025, o cubo 28 funciona a 55 krpm. **O conflito de 06 §10 se resolve sem baixar a rotação.**
2. **06 §10, recomendação "2 (tie-bolt) + 4":** discordo do item 2 com peças de Al (d_eq 17,5 mm → n_c 1,11·n). O item 4 tem efeito pequeno (≤ 1,7 %).
3. **03 §2 (cubo 20 mm, eixo ~16 mm):** incompatível com a rigidez do 06 e com este arranjo. **A Etapa 2 precisa refazer o indutor com cubo 28** (D_t ≈ 46 mm, u_t 133 m/s, β_B ponta ≈ 9°, afunilar ponta na saída p/ d1/d2 ≤ 0,70).
4. **06 §1 usou η 0,76/0,53 da minha v1** (correlação com coeficiente errado). Os valores reais (03/04) dão potência total parecida (+6 %), então o impacto é pequeno, mas o torque de projeto deve ser atualizado para 87,5 N·m nominal.
5. **05 §3** usou ρ_HTP = 1390 e η assumidos → refazer com P_T = 504 kW (η_T mínimo = 0,47; ΔT ≈ 15,5 K com c_p 1854).

## 9. Pendências
1. **Rigidez real de B1 (pré-carga) e B2** — é o parâmetro que mais pesa na 1ª crítica e no veredito 55 vs 60 krpm.
2. Etapa 2: refazer o indutor da OP com cubo 28 mm e validar K* no CFTurbo (pá mais fina/afiada ajuda).
3. Etapa 5: eixo Ø24 sob a OP, compatibilidade com HTP (IN718 molhado → luva 316L ou revestimento; Ni catalisa a decomposição), refazer massas/crítica no modelo do 06 e depois no ROSS.
4. Confirmar a premissa "5 bar = pressão total na entrada" (cada −1 bar no NPSHA corta ~15 % em n_max).
5. Etapa 4: refazer a turbina para 55 krpm e 504 kW; avaliar afilamento/torção da pá.
