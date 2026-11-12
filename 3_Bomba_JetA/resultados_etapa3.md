# Etapa 3 — Bomba de combustível (FP, Jet A) — turbopump-design — **rev. 2**

> Script: `etapa3_bomba_combustivel.py` → `fuel_pump_geometry.json`, `cfturbo_fuel_pump_inputs.csv/.md`, `etapa3_raw.json`, `saida_etapa3.txt`.
> SI; n_q métrico do Gülich [rpm, m³/s, m]. Data: 2026-11-12. Status: meanline 1D, a validar no CFTurbo.
> Rev. 2 troca as premissas da rev. 1 pelos resultados de 01, 02 rev. 2, 03 rev. 2 e 06.

## 0. Resumo
n = 55 000 rpm · n_q 11,8 · impeller radial **semiaberto**, sem indutor, 6 + 6 splitters · d2 = 60,0 mm, b2 = 2,81 mm, d1 = 26,9 mm, cubo 20 / furo 14 mm · anel traseiro Ø45,2 + furos de balanceamento → **F_ax ≈ 0** · voluta simples, garganta Ø6,0 mm · **η = 0,555 (meanline) ≈ 0,55 (ciclo), P_eixo = 74 kW, T = 12,9 N·m** · F_NPSH = 1,41 · impeller 83 g (17-4PH) ou 30 g (Al 7075).

## 1. O que mudou (rev. 1 → rev. 2)
| Item | rev. 1 (premissa) | rev. 2 (resultado real) | Fonte / causa |
|---|---|---|---|
| Furo (eixo) / cubo no olho | 10 / 13 mm | **14 / 20 mm** | 06 §9: eixo 0–20 mm = Ø14; cubo = furo + parede/porca |
| Comprimento do cubo | 20 mm | 18 mm | 06 §2: FP em z 0–18 |
| β1a ponta (escoamento) | 12° | **10°** | recupera margem de cavitação perdida com o cubo maior |
| d1 / u1 | 21,7 mm / 62,5 m/s | **26,9 mm / 77,4 m/s** | cubo maior → olho maior |
| NPSH3 / n_ss / F_NPSH | 35,7 m / 211 / 1,80 | **45,6 m / 176 / 1,41** | idem |
| p_in mínima (F 1,2) | 3,3 bar | 4,3 bar | margem de linha cai de 1,7 para 0,7 bar |
| Indutor | não | **não** (margem menor) | — |
| Lado traseiro | sem compensação (8,8 kN); aletas sugeridas | **anel traseiro Ø45,2 mm + furos** → F_ax ≈ 0 | 06 §2/§5.2: S1 pressupõe câmara traseira a ~p1 |
| Vazamento interno Q_E/Q | 0 | 9,8 % (η_v 0,91) | anel traseiro, folga 0,05 mm, 5 dentes |
| β1B hub/mean/tip | 28,3 / 21,6 / 18,3° | **20,0 / 17,3 / 15,6°** | — |
| d2 / b2 / u2 | 59,7 / 2,80 mm / 172 m/s | **60,0 / 2,81 mm / 173 m/s** | — |
| η meanline / η ciclo | 0,602 / 0,55 | **0,555 / 0,55** (agora coincidem) | 02 rev. 2 já usava 0,55 → sem impacto na turbina |
| P_eixo meanline / ciclo | 67,9 / 74 kW | **73,6 / 74,3 kW** | — |
| Torque | 11,8 N·m | **12,8 (ciclo 12,9) N·m** | 06 §3 usa 13,4 ✔ |
| k_R (empuxo radial) BEP / shut-off | 0,05 / 0,40 (a conferir) | **0,016 / 0,10 (+0,03 dinâmico); projeto 0,15** | 06 §5.1 (Gülich Fig. 9.27/9.28, Tab. 9.4) |
| F_R nominal / shut-off / projeto | 194 / 1553 / — N | **180 / 508 / 586 N** | — |
| Massa 17-4PH / Al 7075 | 66 / 24 g | **83 / 30 g** | cubo maior + anel traseiro |
| Ip / Id (17-4PH) | 2,7 / 1,4·10⁻⁵ kg·m² | **3,20 / 1,72·10⁻⁵ kg·m²** | — |
| ΔT do Jet A | 5,4 K | 6,5 K | — |
| A 60 krpm: F_NPSH / η | 1,57 / 0,61 | 1,22 / 0,56 | — |

## 2. O desafio do n_q baixo (mecanismo)
Vazão pequena com altura grande dá canais estreitos (b2/d2 = 0,047). P_u ∝ Q·H, mas o atrito de disco ∝ ρω³r2⁵ (Gülich T3.6.2) e o vazamento ∝ folga·√Δp. Nenhum dos dois cai com Q, então as perdas secundárias chegam a 30–50 % de P_u (Gülich §3.6.1). Alavancas: ψ alto, menos superfície de disco, folgas apertadas.

## 3. Premissas
| Premissa | Valor | Justificativa |
|---|---|---|
| η_h | 0,75 (0,72 efetivo c/ folga de topo) | T3.9.6 industrial = 0,70 (extrapolado, Q < 5 L/s); usinado, Re ≈ 3·10⁶ |
| b2* | 0,047 | Gülich Eq. 7.1 |
| Pás | 6 + 6 splitters (0,6) | Gülich §7.3.3 |
| β2B | 25° (δ2 = 15°) | Gülich §7.2 (20–27° típico); 22° dá δ2 12,6° com η igual |
| β1a ponta / incidência | 10° / 3° | Fig. 6.20/6.21; T7.1.7 |
| λc / λw,3 | 1,1 / 0,3·tan β1a^0,57 = 0,112 | Gülich Eq. 6.10, Fig. 6.20 |
| Folga de topo | 0,10 mm, perda η_h ≈ s/b2 | ordem de grandeza; validar |
| Anel traseiro | labirinto 5 dentes, s 0,05 mm; câmara a p_in | igual ao frontal do fechado; furos ventilam |
| k (rotação na câmara) | 0,5 | Gülich §9.1 |
| Perdas mecânicas | fora (η_mec 0,97 global) | 01 |

## 4. Conceitos (n = 55 krpm)
| Conceito | d2 [mm] | η | P_eixo [kW] | Comentário |
|---|---|---|---|---|
| A1 Fechado + anéis frente/trás + furos (como 03) | 59,2 | 0,495 | 82,6 | disco frontal (10,5 kW) + 2 anéis (12 % de Q); canal 2,8 mm sob disco → AM/brasado |
| **A2 Semiaberto + anel traseiro + furos (baseline)** | **60,0** | **0,555** | **73,6** | sem disco frontal; usinável em 5 eixos; empuxo ≈ 0; S1 vê ~p1 |
| A2b Semiaberto sem compensação | 59,7 | 0,603 | 67,8 | 8,5 kN de empuxo → inaceitável para B1 |
| A2c Semiaberto + aletas traseiras (k 0,85) | 59,7 | ~0,57–0,59 (custo das aletas não modelado) | ~70 | 2,4 kN residual; câmara no cubo a ~16 bar (vs ~8 bar de S1 na 06) |
| B Barske / emissão parcial | 54,0 | 0,38–0,45 | 91–108 | vence só abaixo de n_q ≈ 8 (n < ~37 krpm) |
| C 2 estágios | 43,6 | 0,46 (T3.9.2) | 89 | crossover + rotor mais longo |
Balanço do baseline: P_u 40,9 + hidráulica 15,6 + vazamento 5,6 + disco traseiro 11,6 = 73,6 kW. Incerteza estatística: ±0,2(1−η) ≈ ±0,09 (T3.9.10).

## 5. Indutor
| Item | Valor |
|---|---|
| NPSH3 impeller | 45,6 m (λw,3 0,112) |
| n_ss | 176 (Gülich: 160–250) |
| F_NPSH | **1,41** (meta 1,2) |
| p_in mínima | 4,3 bar |
**Decisão: sem indutor**, com margem mais fina que na rev. 1. Gatilho para incluir: NPSH3 (CFTurbo/teste) > 53 m, p_in real < 4,3 bar, ou cubo > ~22 mm (com cubo 24 e β1a 12°, F = 1,02). Indutor de reserva: D_t 24,8 mm, D_h 7,4 mm, u_t 71 m/s (SP-8052 Eq. 65, φ 0,10). A 60 krpm, F = 1,22: no limite.

## 6. Geometria (baseline rev. 2)
| Impeller | Valor | | Voluta | Valor |
|---|---|---|---|---|
| d2 / b2 | 60,0 / 2,81 mm | | Tipo | espiral simples 360°, seção circular |
| d1 / d1m / cubo / furo | 26,9 / 23,7 / 20 / 14 mm | | d_lingueta / b3 | 64,2 / 5,6 mm |
| u2 / u1 | 172,8 / 77,4 m/s | | Garganta | 28,1 mm² (Ø 5,98), c3q/c2 0,86 |
| z | 6 + 6 splitters | | Difusor | cônico 8°, Ø 6 → 22,4, L 117 mm |
| β1B hub/mean/tip | 20,0 / 17,3 / 15,6° | | Sucção | Ø 28,3 mm |
| β2B / β2 / δ2 | 25 / 10,0 / 15,0° | | | |
| c2u / c2m / α2 | 130,8 / 7,4 m/s / 3,2° | | | |
| ψ / γ (slip) / w2/w1 | 1,096 / 0,85 / 0,54 | | | |
| e1 / e2 / folga de topo | 0,8 / 0,8 / 0,10 mm | | | |
| Anel traseiro | Ø45,2, s 0,05 mm, 5 dentes, L 5 mm | | | |
Seções da voluta a cada 30° no JSON.

## 7. Cargas e rotodinâmica
| Grandeza | Valor | Nota |
|---|---|---|
| Torque | 12,8 N·m (ciclo 12,9) | |
| F_R nominal / shut-off / projeto | 180 / 508 / 586 N | Gülich Eq. 9.6, k_R da 06 |
| F_ax (→ sucção) | ≈ 0 | sensibilidade: +127 N por bar de pressão na câmara acima de p_in; ±0,5 kN para η_h 0,70–0,80 |
| Massa 17-4PH / Al 7075-T73 | 83 / 30 g | ±20 % |
| Ip / Id 17-4PH | 3,20·10⁻⁵ / 1,72·10⁻⁵ kg·m² | Id no CG da peça; Ip/Id = 1,86 |
| Ip / Id Al | 1,15·10⁻⁵ / 6,2·10⁻⁶ kg·m² | |
| CG (local) | 2,4 mm à frente da face traseira do disco | |
| Fluido arrastado | 5,9 g, Ip 3,1·10⁻⁶ kg·m² | somar como massa adicional |
| Freq. de passagem de pás | 5,5 kHz (6 pás) / 11 kHz (12 bordos de fuga) | |
| Anel traseiro Ø45 | rigidez de Lomakin (anel funcionando como mancal hidrostático) | entrar no ROSS |

## 8. Discordâncias com etapas anteriores (sinalizadas, não alteradas)
1. **06 §5.2/§9 modela a FP como fechada** (d_sp 32,4 mm, cubo 24, 111 g, Ip 38,4 / Id 20,8 kg·mm²). Esta etapa mantém **semiaberto** (η +6 pontos e usinável) com anel traseiro Ø45,2 + furos. A 06 deve atualizar: massa 83 g, Ip 32,0 / Id 17,2 kg·mm², F_ax da FP ≈ 0 (± resíduo) e F_R nominal 0,18 kN / projeto 0,59 kN (06: 0,22 / 0,69). Como a câmara traseira continua a ~p1, a premissa de S1 (5 → 8 bar) se mantém.
2. **06 §5.2 usa cubo 24 mm para a FP; aqui adotei 20** (furo 14 + parede/porca). Com cubo 24, F_NPSH cai para ~1,0–1,1 e a FP **passaria a precisar de indutor**. Se a 06 exigir eixo > 14 mm na ponta, esta etapa precisa ser refeita.
3. **02 rev. 2 §1 registra "η_FP 0,60 meanline semiaberto"**: com o anel traseiro, o meanline é 0,555. O 0,55 adotado para o ciclo não muda, então não há impacto na turbina.
4. **Aletas traseiras (alternativa da rev. 1) descartadas como baseline**: deixam a câmara no cubo a ~16 bar, contra os ~8 bar que a 06 assume em S1. Continuam como opção se o anel traseiro (folga de 0,05 mm em Ø45) for difícil de fabricar.

## 9. Comparação com a referência
Só a rotação: 60 krpm. Nela, a FP fica com d2 55,4 mm, η 0,56 e F_NPSH 1,22, ou seja, no limite sem indutor. A FP não decide a rotação (02 rev. 2). Se a referência roda a 60 krpm com cubo ≥ 20 mm na FP, é provável que tenha indutor também na FP, ou olho/β1a mais agressivos.

## 10. Pendências
1. CFTurbo: η, NPSH3, δ2, carga de pá, pressão no canal (define d_E); exportar meridional/pás → JSON.
2. Validar a perda por folga de topo (k_tip = 1) e o modelo de pressão na face frontal do disco (linear em r²).
3. Dimensionar os furos de balanceamento (Q_E ≈ 0,31 L/s com Δp pequeno) e verificar a fabricação da folga de 0,05 mm em Ø45.
4. 06: atualizar massa/inércias/F_R/F_ax da FP (§8.1) e confirmar furo Ø14 / cubo Ø20 na ponta.
5. Conferir no PDF: coeficientes de T3.9.1/T3.9.6 e a Fig. 6.20 (λw a β1a ≈ 10–13°).
