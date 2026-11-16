# Parâmetros mestres — turbopump-design

> Arquivo **gerado** por `tools/consolidar_parametros.py` a partir dos JSON das etapas 1–5.
> Não edite à mão: refaça a etapa e rode o script de novo. Versão para scripts: `parametros_mestres.json`.
> Status: dimensionamento meanline (1D, numa linha média do escoamento), preliminar, ainda sem validação no CFTurbo.

## 1. Operação
| Grandeza | Valor |
|---|---|
| Rotação nominal n | 55000 rpm (ω = 5760 rad/s) |
| Potência de eixo, bomba de oxidante (OP) | 411,6 kW (η = 0,706) |
| Potência de eixo, bomba de combustível (FP) | 74,3 kW (η = 0,55) |
| Potência requerida da turbina | 500,9 kW (η mecânica 0,97) |
| Potência disponível da turbina | 774,2 kW (margem +55 %) |
| Torque nominal FP / OP / turbina | 12,9 / 71,5 / 87,0 N·m |
| Torque de projeto no trecho OP → turbina | 134,4 N·m |

## 2. Bomba de oxidante (OP, HTP 90 %)
| Grandeza | Valor |
|---|---|
| Vazão útil Q / altura H | 12,6 L/s / 1693 m |
| Velocidade específica n_q | 23,4 |
| NPSH disponível / admissível | 36,8 / 30,6 m |
| Indutor: Ø ponta entrada → saída / cubo | 46,5 → 42,0 / 28,0 mm |
| Indutor: pás / passo / comprimento axial | 3 / 22,4 mm / 18,5 mm |
| Indutor: ângulo de pá na ponta β1B / número de cavitação K | 8,7° / 0,0256 (limite 0,025) |
| Indutor: altura gerada | 100,4 m |
| Impeller: d2 / b2 / d1 | 63,75 / 4,72 / 42,0 mm |
| Impeller: pás / β1B (shroud, cubo) / β2B | 6 / 15,0°, 23,8° / 25,0° |
| Impeller: u2 / coeficiente de pressão ψ | 183,6 m/s / 0,927 |
| Anéis de desgaste (frente e trás) | Ø47 mm, folga 0,08 mm |
| Voluta | dupla 2x180 deg, secao circular, velocidade constante; garganta Ø10,05 mm cada |
| Empuxo radial nominal / de projeto | 685 / 1699 N |

## 3. Bomba de combustível (FP, Jet A)
| Grandeza | Valor |
|---|---|
| Vazão Q / altura H | 3,1 L/s / 1667 m |
| Velocidade específica n_q | 11,8 |
| NPSH disponível / NPSH3 estimado | 64,1 / 45,6 m (sem indutor) |
| Tipo | radial semiaberto (sem disco frontal), simples estagio, entrada axial, em balanco |
| Impeller: d2 / b2 / d1 | 60,00 / 2,81 / 26,9 mm |
| Impeller: pás + splitters / β1B (cubo, ponta) / β2B | 6 + 6 / 20,0°, 15,6° / 25,0° |
| Furo do eixo / cubo no olho | 14 / 20 mm |
| Anel traseiro de balanceamento | Ø45,2 mm, folga 0,05 mm |
| Voluta | espiral simples, secao circular, 360 graus; garganta Ø5,98 mm |
| Empuxo radial nominal / de projeto | 180 / 586 N |

## 4. Turbina
| Grandeza | Valor |
|---|---|
| Tipo | axial, 1 estagio, admissao total, bocais subsonicos convergentes, rotor com shroud |
| Gás (HTP 90 % decomposto): cp / γ / R | 1854 J/(kg·K) / 1,255 / 376,2 J/(kg·K) |
| Razão de pressões / queda isentrópica | 1,154 / 61,0 kJ/kg |
| Grau de reação / ψ / φ | 0,50 / 1,00 / 0,60 |
| Eficiência total-estática estimada / mínima necessária | 0,725 / 0,469 |
| Diâmetro médio / ponta / raiz | 73,0 / 92,7 / 53,4 mm |
| Altura de pá estator / rotor | 18,4 / 19,6 mm |
| Bocais / pás do rotor | 23 / 29 |
| Ângulos α2 / β3 (medidos do eixo) | 59,0° / 59,0° |
| Velocidade periférica média / na ponta | 210,3 / 266,8 m/s |
| Tensão na raiz da pá (estimada) | 235 MPa |

## 5. Rotor (entrada para a rotodinâmica)
Referência axial: z=0 no nariz da FP, +z para a turbina.

### 5.1 Eixo
Material IN718, E = 200 GPa, ρ = 8190 kg/m³.

| z inicial [mm] | z final [mm] | Ø [mm] |
|---|---|---|
| 0 | 20 | 14 |
| 20 | 28 | 18 |
| 28 | 52 | 20 |
| 52 | 90 | 22 |
| 90 | 136 | 24 |
| 136 | 150 | 22 |
| 150 | 166 | 20 |
| 166 | 180 | 24 |
| 180 | 198 | 20 |

### 5.2 Peças montadas
Ip = momento de inércia polar (em torno do eixo de rotação); Id = diametral (transversal), no centro de massa da própria peça.

| Peça | Material | m [g] | z do CG [mm] | Ip [kg·mm²] | Id [kg·mm²] |
|---|---|---|---|---|---|
| Impeller FP (semiaberto) | 17-4PH H1025 | 83,1 | 11,6 | 32,0 | 17,2 |
| Fluido arrastado FP | Jet A | 5,9 | 11,0 | 3,1 | 1,5 |
| Pistas int. B1 (par) | aço | 48,4 | 40,0 | 6,8 | 5,7 |
| Rotores selos IP | aço | 140,0 | 71,0 | 28,7 | 27,8 |
| Indutor OP | Al 6061-T6 | 16,8 | 101,2 | 4,3 | 2,6 |
| Impeller OP | Al 6061-T6 | 41,7 | 122,8 | 22,9 | 11,7 |
| Fluido arrastado OP | HTP | 13,2 | 122,8 | 9,6 | 4,8 |
| Luva S6 | aço | 18,4 | 143,0 | 2,9 | 1,6 |
| Pista int. B2 | aço | 20,3 | 158,0 | 2,7 | 1,6 |
| Luva S7 | aço | 23,8 | 172,0 | 4,4 | 2,5 |
| Rotor turbina (disco+pás+shroud) | MAR-M-247 | 296,0 | 190,0 | 247,1 | 126,6 |
| Eixo (distribuído) | IN718 | 575,3 | 106,5 | 34,6 | — |
| **Rotor total** | | **1283** | **116,0** | **399** | **5098** (no CG do rotor) |

### 5.3 Mancais
| Mancal | Tipo | Posição z [mm] | Furo [mm] | Refrigeração |
|---|---|---|---|---|
| B1 | par contato angular 25 graus DB, classe 7004, hibrido | 34 e 46 | 20 | Jet A |
| B2 | rolos cilindricos classe NU204, hibrido | 158 | 20 | HTP buffer 155 bar |

DN (furo em mm × rpm) = 1,10·10⁶.

### 5.4 Cargas
| Caso | F radial FP [N] | F radial OP [N] | Reação B1 [N] | Reação B2 [N] |
|---|---|---|---|---|
| nominal (BEP) | 190 | 693 | 470 | 447 |
| projeto kR,tot=0,15 | 596 | 1707 | 1329 | 1007 |

Empuxo axial líquido: **-1638 N** (sinal negativo = em direção à FP), com o escape da turbina saindo para +z. Se o escape sair para −z, o valor passa a -14433 N (ver `pendencias_e_decisoes.md`).

### 5.5 Primeira velocidade crítica
Modelo de viga de Euler-Bernoulli em elementos finitos, com efeito giroscópico dos discos, precessão direta síncrona.

| Rigidez B1 / B2 [MN/m] | 1ª crítica [rpm] | Razão crítica / nominal |
|---|---|---|
| 20 / 40 | 59938 | 1,09 |
| 35 / 70 | 74720 | 1,36 |
| 50 / 100 | 83983 | 1,53 |
| 100 / 200 | 97780 | 1,78 |
| 200 / 400 | 105754 | 1,92 |
| rígidos | 135400 | 2,46 |

Frequências naturais com o rotor parado (mancais 50/100 MN/m): 1183, 1829, 2171 Hz.
