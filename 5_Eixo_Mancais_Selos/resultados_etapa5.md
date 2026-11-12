# Etapa 5 — Eixo, mancais e selos (preliminar, sem ROSS) — turbopump-design — **rev. 2**

> Script: `5_Eixo_Mancais_Selos/etapa5_eixo_mancais.py` → `etapa5_eixo_mancais.json`, `etapa5_rotor_massas.csv`, `etapa5_eixo_segmentos.csv`, `etapa5_criticas.csv`, `saida_etapa5.txt`.
> SI; z em mm a partir do nariz da FP (z = 0), +z → turbina. Data: 2026-11-12.
> A rev. 2 lê os JSONs de 2_Bomba_HTP, 3_Bomba_JetA e 4_Turbina e troca as premissas da rev. 1 pelos resultados reais de 01, 02 rev. 2, 03 rev. 2, 04 rev. 2 e 05 rev. 2.

## 0. Resumo
n = 55 000 rpm · arranjo FP(balanço)–B1–pacote interpropelente–OP(eixo passante Ø24)–B2–turbina(balanço), mantido · **rotor 1,28 kg, z_CG 116 mm, Ip 399 / Id 5098 kg·mm²** · torque de projeto 134 N·m (= torque disponível da turbina) · empuxo axial líquido **−1,6 kN** (para a FP; faixa −1,0 a −2,3) · **1ª crítica 84 000 rpm = 1,53·n** com mancais 50/100 MN/m (≥ 1,2 ✔; < 1,2 só abaixo de ~25/50 MN/m) · DN 1,10·10⁶.

## 1. O que mudou (rev. 1 → rev. 2)
| Item | rev. 1 (premissa) | rev. 2 (resultado real) | Fonte / causa |
|---|---|---|---|
| P_OP / P_FP / P_turbina | 382 / 77 / 474 kW (η 0,76/0,53, correlação errada) | **411,6 / 74,3 / 501,0 kW** | 03 §4.5, 04 §0, 05 §3 |
| Torque nominal FP / OP / turbina | 13,4 / 66,4 / 82,3 N·m | **12,9 / 71,5 / 87,0 N·m** | idem |
| Torque de projeto OP→T | 124,6 N·m (η Etapa 0 × 1,1²) | **134,4 N·m** = P_disp/ω (turbina entrega até 774 kW) | 05 §3, §8.1 |
| Eixo sob a OP | Ø20 | **Ø24** IN718 maciço (+ revestimento p/ HTP) | 02 rev. 2 §5 |
| Indutor OP | D_t 45, cubo 28, H 80 m (estimado) | **D_t 46,5→42, cubo 28, L 18,5, H 100,4 m** | 03 §4.2 |
| p1 impeller OP | 15,9 bar | **18,6 bar** | 03 |
| Anéis de desgaste OP | d_sp 51 mm (estimado) | **Ø47 frente = trás + furos** | 03 §4.3 |
| Empuxo OP sem balanceamento / residual | 18,5 / 2,55 kN | **13,3 / 1,63 kN** | Gülich T9.2.7/T9.2.14 com ψ 0,927, η_h 0,83, H_imp 1593 m |
| FP | fechada, 111 g, residual 0,31 kN | **semiaberta, 83 g + 6 g fluido, F_ax ≈ +13 N** (anel traseiro Ø45,2 + furos) | 04 §7 |
| Impeller OP / indutor | 57,9 / 26,6 g (anéis estimados) | **41,7 / 16,8 g + 13,2 g de fluido** | 03 §4.6 |
| Rotor da turbina | 401,8 g, Ip 299, Id 156 kg·mm² | **296 g, Ip 247, Id 127 kg·mm²** | 05 §6 |
| Rotor total m / z_CG / Ip / Id | 1377 g / 120,7 / 444 / 6055 | **1283 g / 116,0 / 399 / 5098** | — |
| F_R OP nominal / projeto | 0,57 / 2,0 kN (voluta simples) | **0,69 (voluta dupla, constante) / 1,70 kN** | 03 §4.6 |
| F_R FP nominal / projeto | 0,22 / 0,69 kN | **0,18 / 0,59 kN** | 04 §7 |
| Reações B1 / B2 (projeto) | 1,50 / 1,24 kN | **1,33 / 1,01 kN** | — |
| Empuxo axial líquido | −2,4 kN | **−1,6 kN** (−1,0 a −2,3) | — |
| P_eq B1 / L10 B1 (projeto) | 3,1 kN / 43 h | **2,3 kN / 104 h** | — |
| S6 Δp | 139 bar | 136 bar (vazamento ~121 g/s, = 03) | — |
| 1ª crítica (50/100 MN/m) | 67 300 rpm (1,22·n) | **84 000 rpm (1,53·n)** | Ø24 (+7 %) + turbina 26 % mais leve no balanço (+15 %) |
| Conflito cubo × cavitação (06 §10) | n_max 47,6 krpm → "perde margem" | **resolvido na 02 rev. 2**: K_op = 0,0256 ≥ 0,025 a 55 krpm | 02 §3, 03 §4.2 |
| Recomendação "tie-bolt + pacote curto" | recomendada | **retirada** (tie-bolt com Al derruba EI → 1,11·n) | 02 §5, §8.2 |
| Voluta dupla "reduz F_R 50–70 %" | afirmado | **corrigido**: só fora do BEP; no BEP a dupla tem F_R maior (481 → 685 N) | 03 §5.1 |
Verificação do modelo: turbina antiga (402 g) + Ø24 dá 72 700 rpm, contra 70 500 da 02 rev. 2 (+3 %, coerente).

## 2. Arranjo axial (mantido da rev. 1, posições ajustadas às peças reais)
```
z[mm]: 0──FP──14│S1 20-26│B1 28-52 (34,46)│S2|dr|S3|He|S4|dr|S5 54-88│ind 92-110,5│OP 112-130│S6 138-148│B2 152-164│S7 166-180│T 184-196│198
```
| Elemento | z [mm] | Nota |
|---|---|---|
| Impeller FP semiaberto (furo Ø14, cubo Ø20) | face traseira 14, CG 11,6 | em balanço, entrada axial (04) |
| B1 par DB contato angular 25° (classe 7004, híbrido) | fileiras 34 e 46 | axial + radial, Jet A |
| Pacote interpropelente S2–S5 | 54–88 | NASA SP-8121 Fig. 6; faces veem só 5–8 bar |
| Indutor OP / impeller OP (furo Ø24) | 92–110,5 / 112–130 (CG 101 / 123) | entrada por cotovelo lateral |
| B2 rolos (classe NU204, híbrido) | 152–164 (158) | só radial, buffer HTP 155 bar |
| Rotor da turbina (disco 12 mm + shroud) | 184–196 (CG 190) | escape axial para **+z** |
Vão B1–B2 118 mm; balanços FP ≈ 28 mm e turbina ≈ 32 mm.

## 3. Torque por trecho
| Trecho | T nominal [N·m] | T projeto [N·m] |
|---|---|---|
| FP → B1 | 12,9 | 15,6 (×1,1²) |
| B1 → OP (selos IP, sob o indutor) | 14,2 | 17,2 (×1,1²) |
| OP → B2 → turbina | 87,0 | **134,4** = máx(1,1²·87,0 = 105; P_disp/ω = 134) |
Por que P_disp: a turbina tem 55 % de potência sobrando (05 §3). Na partida ou num bypass mal ajustado ela consegue aplicar esse torque ao eixo antes de a rotação subir.

## 4. Diâmetro do eixo (IN718; Se 300 MPa corrigido, Sy 900 MPa, Kf 2, SF 1,5)
d_fad = [32·SF/π·√((Kf·M/Se)² + 0,75(T/Sy)²)]^⅓ (SP-8101 §3.1.3); d_tor = (16T/(π·150 MPa))^⅓ (Huzel Eq. 6-33).
| Seção | M [N·m] | T [N·m] | d_tor | d_fad | **adotado** |
|---|---|---|---|---|---|
| FP–B1 (z 24) | 7,4 | 15,6 | 8,1 | 9,2 | 18 |
| B1 (z 40) | 16,9 | 15,6 | 8,1 | 12,0 | 20 |
| Selos IP (z 70) | 5,1 | 17,2 | 8,4 | 8,3 | 22 |
| Sob OP (z 110) | 34,4 | 17,2 | 8,4 | 15,2 | **24** |
| S6 (z 143) | 13,5 | 134,4 | 16,6 | 13,4 | 22 |
| B2 (z 158) | 1,1 | 134,4 | 16,6 | 12,6 | 20 |
| Montagem turbina (z 181) | 0,3 | 134,4 | 16,6 | 12,5 | 20 |
Segmentos (z_ini–z_fim: Ø) [mm]: 0–20: 14 · 20–28: 18 · 28–52: 20 · 52–90: 22 · 90–136: 24 · 136–150: 22 · 150–166: 20 · 166–180: 24 · 180–198: 20. A resistência continua folgada; o menor fator é a torção em B2/turbina (d_tor 16,6 vs 20 → τ = 86 MPa no torque máximo).

## 5. Empuxos
### 5.1 Radial (Gülich Eq. 9.6 + desbalanceamento G2.5 14,4 N/kg + 10 g lateral)
| Caso | F_FP | F_OP | F_T | R_B1 | R_B2 |
|---|---|---|---|---|---|
| Nominal (BEP; OP voluta dupla 0,69 kN) | 190 N | 693 N | 33 N | 470 N | 447 N |
| Projeto (k_R,tot = 0,15, Gülich Tab. 9.4 item 13) | 596 N | 1707 N | 33 N | 1329 N | 1007 N |

### 5.2 Axial: F_z = Σ (π/4)d_j²(p_esq − p_dir) + resíduos das bombas (+z = para a turbina)
| Termo | d [mm] | p [bar] | F_z [N] |
|---|---|---|---|
| S1 | 20 | 5 → 8 | −94 |
| S2…S5 (pacote IP) | 30 | 8 → 1,5 → 4 → 1,5 → 5 | +212 |
| Indutor OP (D_t entrada) | 46,5 | 5 → 18,6 | −2317 |
| **S6** | 22 | 18,6 → 155 | **−5183** |
| S7 | 26 | 155 → 139,7 | +812 |
| Rotor turbina (escape +z) | 92,7 | 139,7 → 130 | **+6550** |
| OP residual (0,15 × 13,3 kN − F_I 370 N) | | | −1630 |
| FP (04) | | | +13 |
| **Líquido** | | | **−1638 N** |
Faixa: −971 / −2304 N (resíduo 0,10 / 0,20, Eq. T9.2.14); −1788 / −1487 N (p_buf 145 / 165 bar). O sinal não inverte → B1 trabalha sempre carregado num sentido só (bom contra derrapagem das esferas).

## 6. Mancais
| | B1 (Jet A) | B2 (HTP) |
|---|---|---|
| Tipo | par DB 25°, classe 7004, esferas Si3N4 | rolos cilíndricos classe NU204, híbrido |
| Bore / DN | 20 mm / 1,10·10⁶ (limite 2,1·10⁶) | 20 mm / 1,10·10⁶ (limite 1,6·10⁶) (Huzel p. 209) |
| P_eq nominal / projeto | 1,74 / 2,32 kN | 0,45 / 1,01 kN |
| L10 projeto (C de catálogo, só ordem de grandeza) | ~6200 min | ≫ |
| Refrigeração | ~70 g/s Jet A (descarga FP → sucção FP) | ~40 g/s HTP (buffer alimentado da descarga OP) |
Riscos (mantidos): **B2 com pouca carga (0,45 kN nominal) → derrapagem dos rolos** (pré-carga radial ou contato angular com mola); rolamento em HTP (compatibilidade, decomposição, calor do disco + **decomposição do vazamento S7 na cavidade do disco, ao lado de B2**, 05 §8.4); rolamentos especiais de foguete (catálogo comercial ~0,6–0,8·10⁶).

## 7. Selos
| Selo | Tipo | d [mm] | Δp [bar] | u [m/s] | Vazamento (folga 15 µm) |
|---|---|---|---|---|---|
| S1 FP traseira → B1 | anel flutuante | 20 | 3,0 | 58 | 12 g/s Jet A |
| S2 primário Jet A | face (carbono × carbeto) | 30 | 6,5 | 86 | dreno |
| S3/S4 intermediários | circunferencial segmentado + purga He | 30 | 2,5 | 86 | consumo de He a dimensionar |
| S5 primário HTP | face (materiais classe HTP) | 30 | 3,5 | 86 | dreno |
| S6 traseira OP ↔ buffer | anel flutuante multiestágio | 22 | 136 | 63 | 121 g/s HTP → sucção OP (= 03) |
| S7 buffer → turbina | anel flutuante + labirinto | 26 | 15,3 | 75 | 48 g/s HTP → cavidade do disco (= 05) |
Limites de selo de face: 500 psi / 500 ft/s (SP-8121 §2.2) → S2/S5 folgados. p_purga > p_drenos sempre (SP-8121 §2.1.7–2.1.8).

## 8. 1ª velocidade crítica (FE Euler-Bernoulli + giroscópico dos discos, forward síncrona)
| k_B1 / k_B2 [MN/m] | 1ª crítica [rpm] | n_c / n |
|---|---|---|
| 20 / 40 | 59 900 | 1,09 ❌ |
| 35 / 70 | 74 700 | 1,36 ✔ |
| **50 / 100** | **84 000** | **1,53** ✔ |
| 100 / 200 | 97 800 | 1,78 |
| 200 / 400 | 105 800 | 1,92 |
| rígidos | 135 400 | 2,46 |
Critério: 20 % (Huzel p. 206). Sensibilidade ao eixo sob a OP (50/100): Ø20 1,43 · Ø22 1,49 · Ø24 1,53. Frequências não girando (50/100): 1183, 1829, 2171 Hz.
**Leitura:** com as peças reais a margem ficou confortável. A 60 krpm daria 1,40·n, ou seja, **a crítica deixa de ser o argumento contra 60 krpm** (02 §6 usava 1,18·n). Restam cavitação (K 0,022) e turbina (h/Dm 0,32). A rigidez dos mancais continua sendo a maior incerteza: abaixo de ~25/50 MN/m a margem some.

## 9. Massas e inércias (input do TCC; também em `etapa5_rotor_massas.csv`)
Ip = polar; Id = diametral no CG da própria peça.
| Peça | Material | m [g] | z_CG [mm] | Ip [kg·mm²] | Id [kg·mm²] | Fonte |
|---|---|---|---|---|---|---|
| Impeller FP (semiaberto) | 17-4PH H1025 | 83,1 | 11,6 | 32,0 | 17,2 | 04 |
| Fluido arrastado FP | Jet A | 5,9 | 11,0 | 3,1 | 1,5 | 04 |
| Pistas int. B1 (par) | aço | 48,4 | 40,0 | 6,8 | 5,7 | estimado |
| Rotores selos IP | aço | 140,0 | 71,0 | 28,7 | 27,8 | estimado |
| Indutor OP | Al 6061-T6 | 16,8 | 101,2 | 4,3 | 2,6 | 03 |
| Impeller OP | Al 6061-T6 | 41,7 | 122,8 | 22,9 | 11,7 | 03 |
| Fluido arrastado OP | HTP | 13,2 | 122,8 | 9,6 | 4,8 | 03 |
| Luva S6 | aço | 18,4 | 143,0 | 2,9 | 1,6 | estimado |
| Pista int. B2 | aço | 20,3 | 158,0 | 2,7 | 1,6 | estimado |
| Luva S7 | aço | 23,8 | 172,0 | 4,4 | 2,5 | estimado |
| Rotor turbina (disco+pás+shroud) | MAR-M-247 | 296,0 | 190,0 | 247,1 | 126,6 | 05 |
| Eixo (maciço, distribuído) | IN718 | 575,3 | 106,5 | 34,6 | — | este |
| **Rotor total** | | **1283** | **116,0** | **399** | **5098 (CG do rotor)** | |
Mancais no modelo: B1 = duas molas em z 34 e 46; B2 = mola em z 158. E = 200 GPa, ρ = 8190 kg/m³. Incerteza das peças: ±20–25 % (até o CAD). Os rotores de selo IP (140 g) agora são a 2ª maior massa e são estimativa → prioridade no CAD.

## 10. Discordâncias com etapas anteriores (sinalizadas, não alteradas)
1. **05 §7: "F_ax no rotor 6,2 kN → bombas (−z)".** No arranjo da 06, o escape da turbina sai para fora (+z), então o empuxo do rotor aponta **para +z (para longe das bombas)**: o rotor é empurrado no sentido do escoamento, de p2 = 139,7 para p3 = 130 bar. Com o sinal da 05, o líquido seria **−14,4 kN** em B1, o que é inaceitável sem pistão de balanceamento. A magnitude bate (6,2 vs 6,55 kN; a diferença é o furo Ø20 vs S7 Ø26). **Ação:** a 05 e a 6_CAD precisam confirmar escape para +z (bocais no lado de dentro, coletor de escape para fora). Se o planejamento quiser o escape para dentro, esta etapa tem que ganhar um pistão de balanceamento.
2. **05 §8.1 (55 % de potência sobrando):** não mudei o ciclo, mas dimensionei o trecho OP→T para o torque disponível (134 N·m). Se o planejamento adotar bypass ou PR menor, esse torque cai para ~105 N·m.
3. **02 §3 (K_lim 0,025):** aceito, e isso resolve o conflito da rev. 1. Ressalva: a folga é de 2 % (K_op 0,0256) sobre um K* ainda não validado. É o risco nº 1 da OP e depende do CFTurbo/teste.
4. **04 §8.2 (cubo 20 / furo 14 na FP):** compatível; o eixo na ponta continua Ø14 (d_fad 9,2 mm). Não há pedido desta etapa para engrossar a ponta.
5. Auto-correções da rev. 1: a recomendação "tie-bolt + pacote curto" foi retirada (02 §8.2), e a frase "voluta dupla reduz F_R 50–70 %" passa a valer só fora do BEP (03 §5.1).

## 11. Comparação com o gabarito
A 60 krpm (referência), este rotor teria 1ª crítica de 1,40·n com 50/100 MN/m. Ou seja, a rotodinâmica não impede os 60 krpm. A diferença 55 vs 60 krpm passa a ser explicada só pela cavitação da OP (K 0,022 vs 0,025) e pela pá da turbina, o que reforça a hipótese da 02 de que a referência aceita um indutor mais agressivo.

## 12. Pendências
1. Confirmar o sentido do escape da turbina (§10.1). Isso decide se o empuxo é −1,6 ou −14 kN.
2. Rigidez real de B1 (pré-carga do par DB) e de B2; a margem some abaixo de ~25/50 MN/m.
3. CAD: massas das peças estimadas (rotores de selo IP 140 g, pistas, luvas) e posições finais.
4. Compatibilidade com HTP: B2, faces de S5, S6/S7, eixo IN718 molhado por HTP sob a OP (revestimento).
5. Térmica de B2/S7: disco a ~1130 K + decomposição dos 48 g/s de S7 na cavidade (05 §8.4).
6. B2 levemente carregado: pré-carga radial ou troca por contato angular com mola.
7. Empuxo em transientes (pressões ∝ n²) e com o bypass da turbina.
8. ROSS: rotor completo, amortecimento, rigidez de Lomakin dos anéis Ø47 (OP), Ø45 (FP) e S6, e resposta a desbalanceamento.
