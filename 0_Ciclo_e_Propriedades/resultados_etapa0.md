# Etapa 0 — Propriedades dos fluidos, ponto das bombas e balanço do ciclo — turbopump-design

> Script: `etapa0_ciclo.py` (Python + Cantera 3.2). Requisitos: `../docs/requisitos.md`. Data: 2026-11-12.
> **As eficiências desta etapa são provisórias** (0,60 e 0,45). As etapas 2 e 3 calcularam 0,706 e 0,555, e a potência requerida da turbina caiu de 593 para 501 kW. Os valores finais estão em `../docs/parametros_mestres.md`.

## 1. Propriedades dos fluidos a 300 K
| Propriedade | HTP 90 % (em massa) | Jet A | Fonte / nota |
|---|---|---|---|
| ρ (densidade) | 1385 kg/m³ | 795 kg/m³ | HTP: 1386,7 kg/m³ a 25 °C (CRC Handbook), corrigido −0,1 %. Jet A: típico ~804 a 15 °C, faixa de especificação 775–840 (CRC Report 663 / ASTM D1655); usar o ρ medido do lote |
| p_v (pressão de vapor) | ~0,5 kPa (incerto ±50 %) | ~0,4 kPa | HTP: Evonik / Schumb (MIT, 1953). Jet A: CRC 663. Irrelevante para o NPSH, porque a entrada está a 500 kPa |
| μ (viscosidade dinâmica) | ~1,1 mPa·s | ~1,3 mPa·s | HTP: ~1,26 mPa·s a 20 °C (Schumb), corrigido para 27 °C. Jet A: CRC 663 |
| c_p (calor específico do líquido) | ~2,75 kJ/(kg·K) | ~2,0 kJ/(kg·K) | HTP: média em massa de H₂O₂ e H₂O |

Pendência: confirmar ρ e μ do HTP 90 % a 27 °C em Schumb et al. e as propriedades do Jet A com o fornecedor.

## 2. Ponto de projeto das bombas
Equações: H = Δp/(ρg); Q = ṁ/ρ; P_h = Q·Δp; P_eixo = P_h/η (Huzel eq. 6-9 a 6-11; Gülich cap. 3).

H é a altura manométrica (o aumento de pressão expresso em metros de coluna do próprio fluido) e Q é a vazão volumétrica.

| Bomba | Q | H | P_h (hidráulica) | η assumida | P_eixo | NPSH disponível | Aquecimento pelas perdas |
|---|---|---|---|---|---|---|---|
| OP (HTP) | 12,64 L/s | 1693 m | 290,6 kW | 0,60 | 484 kW | 36,8 m | 2,4 K |
| FP (Jet A) | 3,14 L/s | 1667 m | 40,9 kW | 0,45 | 91 kW | 64,1 m | 4,5 K |
| **Total** | | | 331 kW | | **575 kW** | | |

Com eficiência mecânica de 0,97, a turbina precisaria entregar cerca de 593 kW (valor provisório, ver nota no topo).

As duas alturas são quase iguais (~1,7 km), o que favorece um eixo único. As vazões são pequenas, então a velocidade específica n_q = n·√Q / H^0,75 (n em rpm, Q em m³/s, H em m) é baixa, principalmente na FP:

| n [mil rpm] | 40 | 60 | 80 |
|---|---|---|---|
| n_q da OP | 17 | 25 | 34 |
| n_q da FP | 8,6 | 12,9 | 17 |

## 3. Gás de HTP 90 % decomposto
Composição congelada, gás ideal (Cantera, mecanismo gri30).

- Produtos por kg: 0,576 kg de H₂O + 0,424 kg de O₂. Massa molar 22,1 g/mol, fração molar de O₂ 0,29: o gás é **oxidante**.
- A 1150 K: c_p = 1854 J/(kg·K), γ = 1,255.
- Temperatura adiabática de decomposição: **1030 K** partindo de líquido a 298 K (a literatura dá ~1020–1030 K, o que valida o modelo) e **1182 K** partindo de líquido pré-aquecido a 400 K. Os 1150 K do requisito são coerentes (~3 % abaixo do adiabático).
- Hipóteses: entalpias de formação do NIST (H₂O₂ líquido −187,78 kJ/mol; H₂O líquida −285,83 kJ/mol); calor de mistura desprezado.

## 4. Balanço de potência da turbina (150 bar e 1150 K → 130 bar)
| Grandeza | Valor |
|---|---|
| Razão de pressões | 1,154 |
| Queda de entalpia isentrópica | 61,0 kJ/kg (queda de temperatura ideal de 33 K) |
| Velocidade isentrópica c₀ (*spouting velocity*) | 349 m/s |
| Potência ideal (17,5 kg/s) | 1068 kW |
| Queda de entalpia real necessária | 33,9 kJ/kg, ou ΔT ≈ 18 K |
| Eficiência necessária da turbina | 0,56 |

**Queda de 10 K na turbina (valor de referência): não fecha.** 10 K correspondem a 324 kW, menos que a potência *hidráulica* total das bombas (331 kW). Seria preciso bombas com eficiência acima de 100 %.

**Queda de 50 bar no gerador de gás (200 → 150 bar): alta, mas plausível** se incluir o injetor do leito, o leito catalítico e a placa de saída. Cada 10 bar a menos na descarga da OP economizam 21 kW de eixo.

## 5. Riscos e observações
- HTP 90 % a 400 K na saída da refrigeração regenerativa: a taxa de decomposição já é alta nessa temperatura. O tempo de residência curto ajuda, mas a margem térmica é pequena.
- Os dois propelentes têm pressão de vapor desprezível frente aos 5 bar de entrada. A cavitação é governada pela rotação (Etapa 1), não pela pressão de vapor.

## 6. Eixo único e alternativas
| Arranjo | Prós | Contras |
|---|---|---|
| **Eixo único FP – OP – turbina** (adotado) | Menos peças e mancais, uma turbina, compacto, partida simples | Uma rotação para duas bombas muito diferentes (a FP fica ineficiente); selo interpropelente obrigatório; rotor mais longo |
| Eixo único com caixa de engrenagens | FP em rotação maior | Engrenagens, lubrificação, massa |
| Dois eixos, duas turbinas | Cada bomba na rotação ótima; propelentes separados | Dobro de mancais e selos, divisão do gás, controle |
| FP de emissão parcial ou multiestágio | Adequada a n_q muito baixo | Geometria e eficiência próprias |
| FP elétrica | Desacopla totalmente | Bateria e inversor de ~100 kW |

Para uso único e ~0,5 MW, o eixo único é a escolha racional. O custo é o selo interpropelente e a FP com eficiência baixa, que pesa pouco porque ela consome só ~15 % da potência.

## 7. Pendências
1. Queda de temperatura real da turbina no projeto de referência.
2. Divisão dos 50 bar do gerador de gás (injetor, leito, saída).
3. Confirmar as propriedades do HTP a 27 °C e do Jet A do lote.
