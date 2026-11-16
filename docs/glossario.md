# Glossário de símbolos e termos

Os relatórios usam a notação do Gülich (*Centrifugal Pumps*), do Huzel & Huang e das monografias NASA de critérios de projeto (série SP-8000).

## Componentes
| Termo | Significado |
|---|---|
| OP (*oxidizer pump*) | Bomba de oxidante (HTP) |
| FP (*fuel pump*) | Bomba de combustível (Jet A) |
| Impeller | Rotor da bomba centrífuga: acelera o fluido para fora e é quem gera a pressão |
| Indutor | Hélice axial antes do impeller. Dá um primeiro aumento de pressão para o impeller não cavitar |
| Voluta | Carcaça em caracol que coleta o fluido na saída do impeller e converte velocidade em pressão |
| Lingueta (*cutwater*) | Ponto onde a voluta começa, logo depois da saída |
| Shroud | Disco de cobertura das pás. Impeller fechado tem; semiaberto não tem |
| Splitter | Pá curta intercalada entre as pás principais, só na parte de fora do impeller |
| Anel de desgaste | Folga anular estreita que limita o vazamento da saída de volta para a entrada |
| Furos de balanceamento | Furos no disco que igualam a pressão atrás do impeller à da sucção e reduzem o empuxo axial |
| B1, B2 | Mancais: B1 do lado da FP, B2 do lado da turbina |
| S1 a S7 | Selos do eixo, numerados da FP para a turbina |
| Selo interpropelente | Conjunto de selos que impede combustível e oxidante de se encontrarem ao longo do eixo |

## Ponto de operação
| Símbolo | Significado | Unidade |
|---|---|---|
| ṁ | Vazão mássica | kg/s |
| Q | Vazão volumétrica (ṁ/ρ) | m³/s ou L/s |
| H | Altura manométrica: aumento de pressão expresso em metros de coluna do fluido, H = Δp/(ρg) | m |
| n, ω | Rotação | rpm, rad/s |
| P_h | Potência hidráulica (útil), Q·Δp | W |
| η | Eficiência. η_h hidráulica, η_v volumétrica (vazamentos), η_mec mecânica | — |
| BEP (*best efficiency point*) | Ponto de máxima eficiência, onde a bomba é projetada | — |

## Cavitação
| Símbolo | Significado |
|---|---|
| NPSH (*net positive suction head*) | Margem de pressão na entrada acima da pressão de vapor, em metros |
| NPSHA / NPSH3 | Disponível na instalação / exigido pela bomba (critério de 3 % de queda de altura) |
| F_NPSH | Margem de segurança NPSHA/NPSH3 |
| n_ss, S | Velocidade específica de sucção (métrica, em unidades americanas). Quanto maior, mais a bomba aguenta girar com pouca pressão na entrada |
| K | Número de cavitação da pá do indutor: quanto de pressão sobra sobre a pá, em relação à pressão dinâmica. K* é o mínimo em que a pá ainda funciona |
| τ | Parâmetro de cavitação do indutor, 2g·NPSH/u_t² |

## Geometria e escoamento na bomba
Índice 1 = entrada do impeller; 2 = saída do impeller; 3 = voluta.

| Símbolo | Significado |
|---|---|
| d1, d2 | Diâmetro de entrada (olho) e de saída do impeller |
| b2 | Largura do canal na saída do impeller |
| D_t, ν | Diâmetro da ponta do indutor; razão cubo/ponta |
| z | Número de pás |
| u | Velocidade periférica da pá (ω·r) |
| c | Velocidade absoluta do fluido. c_m componente meridional (carrega a vazão); c_u componente tangencial (carrega a energia) |
| w | Velocidade do fluido vista pela pá (relativa) |
| α | Ângulo da velocidade absoluta |
| β | Ângulo da velocidade relativa. β_B (ou β1B, β2B) é o ângulo da pá |
| i, δ | Incidência (diferença entre pá e escoamento na entrada) e desvio (na saída) |
| γ (*slip factor*) | Quanto o fluido "escorrega" e sai menos tangencial que a pá |
| ψ | Coeficiente de pressão, 2gH/u2². Liga a altura à velocidade da ponta |
| φ | Coeficiente de vazão, c_m/u |
| n_q | Velocidade específica, n·√Q/H^0,75. Diz que formato de rotor serve: baixa = muita pressão e pouca vazão (rotor radial estreito) |
| k_R, F_R | Coeficiente e força de empuxo radial (a voluta empurra o impeller de lado) |

## Turbina
| Símbolo | Significado |
|---|---|
| PR | Razão de pressões entrada/saída |
| c0 (*spouting velocity*) | Velocidade que o gás atingiria numa expansão ideal |
| u/c0 | Razão de velocidades. Cada tipo de turbina tem um valor ótimo |
| R (grau de reação) | Fração da expansão que acontece no rotor. R = 0 é impulso |
| η_ts, η_tt | Eficiência total-estática (a energia cinética de saída é perda) e total-total |
| Dm, h | Diâmetro médio e altura da pá |
| AN² | Área anular × rotação². Mede a tensão centrífuga nas pás |

## Eixo e rotodinâmica
| Símbolo | Significado |
|---|---|
| DN | Furo do rolamento (mm) × rotação (rpm). Limite de velocidade de rolamentos |
| Ip, Id | Momento de inércia polar (em torno do eixo de rotação) e diametral (transversal) |
| Velocidade crítica | Rotação que coincide com uma frequência natural de flexão do rotor |
| Precessão direta (*forward whirl*) | Órbita do eixo no mesmo sentido da rotação. É a que o desbalanceamento excita |
| Efeito giroscópico | Discos girando resistem a inclinar. Enrijece a precessão direta e sobe a crítica |
| Efeito Lomakin | Anéis de desgaste e selos anulares com alta diferença de pressão funcionam como mancais adicionais |
| L10 | Vida de rolamento que 90 % das peças atingem |
