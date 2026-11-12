# Etapa 4 — Turbina axial (meanline 1D) — turbopump-design — **rev. 2**

> Script: `4_Turbina/etapa4_turbina.py` (Python + Cantera 3.2, gri30/NASA 7-coef.) → `etapa4_turbina.json`, `etapa4_varredura_phi.csv`, `etapa4_cfturbo.csv`, `saida_etapa4.txt`.
> SI. Data: 2026-11-12. **Status: meanline 1D, a validar no CFTurbo.**
> A rev. 2 troca as premissas da rev. 1 pelos resultados de 01 (Etapa 0), 02 (Etapa 1 rev. 2), 03 (OP rev. 2), 04 (FP rev. 2) e 06 (eixo/mancais).

## 0. Resumo
n = 55 000 rpm · axial, 1 estágio, admissão total, reação 50 %, rotor com shroud · Dm = 73,0 mm, h_rotor = 19,6 mm (ponta Ø92,7 / raiz Ø53,4) · 23 bocais / 29 pás · **η_ts ≈ 0,73** contra 0,47 necessária → **+55 % de potência disponível** · P_req = 501 kW, T = 87,0 N·m · rotor MAR-M-247: 296 g, Ip 247 / Id 127 kg·mm² · F_ax no rotor 6,2 kN (→ bombas).

## 1. O que mudou (rev. 1 → rev. 2)
| Item | rev. 1 (premissa) | rev. 2 (resultado real) | Fonte |
|---|---|---|---|
| Rotação | indefinida (tabela 30–70 krpm) | **55 000 rpm** | 02 §0 |
| P_OP / P_FP (eixo) | 445,5 / 73,9 kW (η 0,65 / 0,55, ρ 1390) | **411,6 / 74,3 kW** | 03 §4.5; 04 §0 |
| Perdas mecânicas | +3 % | η_mec = 0,97 (≈ +3,1 %) | 01 |
| **P_req turbina** | 534,9 kW | **500,9 kW** | — |
| η_T mínimo / ΔT de balanço | 0,50 / 16,5 K | **0,469 / 15,4 K** (T3 ≈ 1135 K) | — |
| Vazão nos bocais | 17,5 kg/s | 17,45 kg/s (S7, 50 g/s, entra a jusante do estator) | 06 §7 |
| Margem de potência | +44 % | **+55 %** | — |
| PR mínimo (com η de projeto) | 1,104 | 1,096 (queda de 13,2 bar em vez de 20) | — |
| Razão de aspecto no Soderberg | b/h fixo 0,67 | iterada com a corda real (0,60 / 0,46) | — |
| η_ts / η_tt | 0,723 / ~0,85 | 0,725 / 0,834 (η_tt agora calculado direito) | — |
| Dm / h_rotor / h/Dm | f(N) | **73,0 / 19,6 mm / 0,27** | — |
| Número de pás | não definido | **23 bocais / 29 pás** (Zweifel 0,8, primos entre si) | Huzel p. 201 |
| σ na raiz | 161–232 MPa (sem afilamento, IN718) | **136 (afilada) + 99 (shroud) ≈ 235 MPa**, MAR-M-247 | 06 §9 |
| Massa / Ip / Id do rotor | não calculado (06 estimou 402 g / 299 / 156) | **296 g / 247 / 127 kg·mm²** | §6 |
| Empuxo axial | 4,4 kN (só pás) | 4,4 kN nas pás; **6,2 kN no rotor** (disco: frente p2, trás p3) | §7 |
| Alternativa impulso | \"Dm 38 % maior\" — **errado** | Dm **28 % menor** (52,9 mm), mas h 37 mm (h/Dm 0,71) | §4 |

## 2. Gás de HTP 90 % decomposto (composição congelada, gás ideal)
| Propriedade | Valor |
|---|---|
| x_H2O / x_O2 (molar) | 0,708 / 0,292 (gás oxidante) |
| M / R | 22,10 kg/kmol / 376,2 J/(kg·K) |
| cp / γ (1150 K) | 1854 J/(kg·K) / 1,255 |
| T_ad de 298 K / de 400 K | 1030 K (literatura ~1020 ✔) / 1182 K → 1150 K coerente |
| μ (estimada) | 4,3·10⁻⁵ Pa·s |
Bate com 01 §3. Gás ideal OK (Z ≈ 0,98).

## 3. Balanço de potência
| Grandeza | Valor |
|---|---|
| PR (p01/p3) | 1,154 |
| Δh_is total-estática / T3s | 61,0 kJ/kg / 1117 K |
| c0 (spouting velocity) | 349 m/s |
| P_ideal (17,5 kg/s) | 1068 kW |
| P_req = (411,6 + 74,3)/0,97 | **500,9 kW** |
| η_T mínimo | **0,469** |
| P disponível com η_ts 0,725 | 774 kW (**+55 %**) |
| Potência implícita no ΔT = 10 K do fluxograma | 324 kW < P_hidráulica 331 kW ❌ (01 já sinalizou) |
| PR mínimo com η 0,725 | 1,096 (Δp = 13,2 bar) |
**O ciclo fecha com folga grande.** Em regime, a turbina não pode entregar 774 kW contra 501 kW de carga: o rotor aceleraria até as bombas absorverem o excesso. Então uma das premissas do ciclo precisa ceder (ver §8.1).

## 4. Escolha do tipo (mantida)
- PR baixo e vazão alta → **axial, 1 estágio, admissão total, bocais subsônicos convergentes** (Huzel p. 195–199 e 205: staged-combustion usa baixa reação). u/c0 ótimo (0,60) sai com u = 210 m/s → não precisa compounding.
- Modelo: ψ = Δh/u², φ = cx/u, c_θ2 = u(ψ/2 + 1 − R), c_θ3 = u(1 − R − ψ/2) (Dixon, cap. 4). Perdas de Soderberg com correção de razão de aspecto, c3²/2 perdida (total-estática) e fator 0,92 (shroud, disco, otimismo da correlação). Triângulos: Huzel eq. 6-77 a 6-84.

| φ | η_ts R 0,5 | Dm [mm] | h [mm] | η_ts impulso | Dm [mm] | h [mm] |
|---|---|---|---|---|---|---|
| 0,4 | 0,793 | 76,4 | 26,9 | 0,793 | 54,0 | 53,9 |
| 0,5 | 0,761 | 74,8 | 22,4 | 0,779 | 53,5 | 43,9 |
| **0,6** | **0,725** | **73,0** | **19,6** | 0,761 | 52,9 | 37,4 |
| 0,8 | 0,647 | 69,0 | 16,5 | 0,718 | 51,4 | 29,7 |

| Tipo (φ 0,6) | η_ts | u/c0 | Dm | h | h/Dm | p2 | F_ax rotor |
|---|---|---|---|---|---|---|---|
| **Reação 50 % (baseline)** | 0,725 | 0,60 | 73,0 | 19,6 | **0,27** | 139,7 bar | 6,2 kN |
| Baixa reação 25 % | 0,751 | 0,50 | 60,7 | 28,4 | 0,47 | 134,8 bar | 2,8 kN |
| Impulso | 0,761 | 0,44 | 52,9 | 37,4 | 0,71 | 130 bar | ≈ 0 |
Correção da rev. 1: u menor dá Dm **menor** (Dm = 2u/ω). O impulso fica mais leve, mas a pá vira \"bandeira\" (h/Dm 0,71, hub/tip 0,17), com torção extrema e tensão alta. **Reação 50 % fica**, porque é a única com h/Dm < 0,3. O empuxo axial maior vai para B1, e a 06 já o contabiliza.

## 5. Triângulos, estado e geometria (baseline, 55 krpm)
| Grandeza | Valor | | Grandeza | Valor |
|---|---|---|---|---|
| u (raio médio) | 210,3 m/s | | Dm | **73,0 mm** |
| cx = c3 | 126,2 m/s | | d_tip / d_root | **92,7 / 53,4 mm** |
| c2 = w3 / w2 | 245,3 / 126,2 m/s | | h estator / rotor | 18,4 / **19,6 mm** |
| α2 / β2 / β3 / α3 (do eixo) | 59,0° / 0° / 59,0° / 0° | | hub/tip | 0,58 |
| M2 / M_w3 | 0,34 / 0,34 (subsônico) | | b axial estator / rotor | 11 / 9 mm |
| p2 / T2 | 139,7 bar / 1134 K | | z estator / rotor | **23 / 29** (Zweifel 23,0 / 28,1) |
| ρ2 / ρ3 | 32,8 / 30,8 kg/m³ | | Garganta do bocal o / h/o | 5,13 mm / 3,6 (Huzel p. 199: 3,5–8 ✔) |
| A2 / A3 | 42,2 / 45,0 cm² | | Shroud (integral) | 1,5 mm radial × 10 mm |
| T03 (com η de projeto) | 1126 K | | Disco | 12 mm, furo Ø20 |
| Re corda estator | 2,4·10⁶ (alto; perdas de Re desprezíveis) | | Nº de bocais | 23 (Huzel p. 199: 25–61 típico, ok) |
| ζ_N / ζ_R (Soderberg) | 0,067 / 0,064 | | η_ts / η_tt | 0,725 / 0,834 |

## 6. Tensões, massa e inércias (MAR-M-247, ρ 8540 kg/m³)
| Grandeza | Valor |
|---|---|
| u_tip / u_root | 267 / 154 m/s |
| AN² | 1,36·10⁷ m²·rpm² (≈ 2,1·10¹⁰ in²·rpm²; faixa usual 2–5·10¹⁰) |
| σ raiz sem afilamento / afilada (×0,67) | 203 / 136 MPa |
| + shroud (área de raiz estimada) | +99 MPa → **≈ 235 MPa** |
| Atrito de disco (gás 31 kg/m³) | 0,4 kW (desprezível) |

| Peça | m [g] | Ip [kg·mm²] | Id [kg·mm²] |
|---|---|---|---|
| Disco (r 10 → 26,7 mm, 12 mm) | 197,5 | 80,3 | 42,5 |
| Pás (29) | 60,6 | 82,7 | 41,8 |
| Shroud | 37,9 | 84,0 | 42,3 |
| **Rotor da turbina** | **296** | **247** | **127** |
Id no CG da peça, com componentes considerados coplanares. Incerteza ±25 % (espessuras de disco e de pá estimadas). Ip/Id = 1,95, o que confirma o efeito giroscópico forte (06 §9).

## 7. Cargas (input da 06)
| Carga | Valor |
|---|---|
| Torque nominal | 87,0 N·m (02: 87,5 ✔) |
| Força tangencial total nas pás | 3,7 kN |
| F_ax nas pás (Δp rotor × coroa) | 4,4 kN → bombas (−z) |
| F_ax no rotor (frente p2, trás p3, até o furo Ø20) | **6,2 kN → bombas** (06 usou 6,5 kN ✔) |
| Frequência de passagem rotor / estator | 26,6 / 21,1 kHz (≫ modos do eixo) |

## 8. Discordâncias e pontos para o chat de planejamento (sinalizados, não alterados)
1. **Excesso de potência de 55 % (decisão de ciclo, não desta etapa).** As pressões do 00 sobram para as bombas reais. Opções: (a) **reduzir a queda na turbina** de 20 para ~13 bar → a OP pode descarregar ~7 bar a menos (01 §4: −21 kW por −10 bar, o que realimenta e reduz ainda mais); (b) **válvula de bypass da turbina** (gás vai direto para a câmara), útil também como controle e margem para η reais piores; (c) manter e aceitar n > 55 krpm, ruim para crítica e cavitação (02). Recomendo (b) no projeto preliminar e (a) depois do teste. **Também é forte indício de que a referência tem ΔT/PR ou η diferentes dos do fluxograma.**
2. **06 §9 (rotor da turbina 401,8 g, Ip 298,8, Id 156,3 kg·mm²)** → atualizar para **296 g / 247 / 127**. Isso reduz massa no balanço da turbina, o que melhora a crítica.
3. **03 §5.5 (\"η_OP ≈ 0,68 para o ciclo\")**: a própria 03 diz que o mecânico já está no η_mec 0,97. Usei P_OP = 411,6 kW + η_mec, sem dupla contagem.
4. **06 §7, S7 (50 g/s de HTP líquido entra na cavidade do disco a ~1130 K):** decompõe ali, gerando calor e pressão locais ao lado de B2. Isso precisa entrar na térmica da 06 (pendência 4 dela). Na turbina o efeito é desprezível (−0,3 % de vazão no estator).
5. **Correção minha:** a rev. 1 dizia que o impulso teria Dm maior. Está errado; corrigido no §4.

## 9. Comparação com o gabarito (só a rotação e ΔT disponíveis)
- Rotação: 55 krpm (proposta) vs 60 krpm. A 60 krpm esta turbina teria Dm 67 mm e h/Dm 0,32 (rev. 1); não é ela que limita.
- ΔT = 10 K do fluxograma vs 15,4 K de balanço (η_min) e 24 K com η de projeto: incoerente (§3, §8.1).

## 10. Pendências
1. Planejamento: decidir bypass vs redução de PR (§8.1) e refazer P_req se a descarga da OP mudar.
2. CFTurbo (axial turbine): η, perfis, distribuição de carga, garganta; trocar Soderberg por Kacker-Okapuu.
3. Tensão da pá com área de raiz real (perfil) e creep/ruptura do MAR-M-247 a ~1135 K para a duração da queima; vibração de pá (Campbell vs 2,6 / 21 kHz e harmônicos de 23 bocais).
4. Compatibilidade com gás oxidante a 150 bar (29 % molar de O2): folgas de shroud e risco de ignição por atrito.
5. Etapa 5: atualizar massa/inércias e térmica do lado da turbina (S7, escudo térmico).
6. Etapa 6 (CAD): perfis de pá a partir de α2/β3, cordas e z deste arquivo (`etapa4_turbina.json`).
