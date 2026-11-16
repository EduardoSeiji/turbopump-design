# Decisões tomadas e pendências abertas

Visão única do que já está decidido, do que ainda depende de decisão e do que os relatórios das etapas dizem de forma diferente entre si. Os números vêm dos relatórios `resultados_etapaX.md` (revisão 2) e de `parametros_mestres.md`.

## 1. Decisões tomadas
| Decisão | Valor | Por quê | Onde |
|---|---|---|---|
| Rotação nominal | 55 000 rpm | Limite ativo: cavitação do indutor da bomba de oxidante (OP) | Etapa 1 §6 |
| Arranjo do rotor | FP em balanço – mancal B1 – selos interpropelentes – OP com eixo passante – mancal B2 – turbina em balanço | O gás da turbina é oxidante, então fica ao lado da OP; o único selo entre propelentes vê só pressão de sucção | Etapa 5 §2 |
| Eixo sob a OP | Inconel 718 maciço, Ø24 mm | O trecho no meio do vão é o que mais pesa na 1ª velocidade crítica | Etapa 1 §5 |
| Rotor empilhado com tirante (*tie-bolt*) e peças de alumínio | Rejeitado | O alumínio tem 1/3 da rigidez do aço e derruba a crítica | Etapa 1 §5 |
| Critério de cavitação da OP | Número de cavitação K ≥ 0,025 e margem de NPSH de 1,2 | 2,5 vezes o K mínimo experimental de pás finas (NASA SP-8052) | Etapa 1 §3 |
| Indutor | Só na OP | A FP tem margem de NPSH de 1,41 sem indutor | Etapas 2 e 3 |
| Impeller da OP | Fechado, 6 pás, anéis de desgaste na frente e atrás, furos de balanceamento | Sem balanceamento o empuxo axial seria de 13 kN | Etapas 2 e 5 |
| Impeller da FP | Semiaberto, 6 pás + 6 *splitters*, anel traseiro e furos de balanceamento | Eficiência 6 pontos acima do fechado; usinável em 5 eixos | Etapa 3 §4 |
| Turbina | Axial, 1 estágio, admissão total, reação de 50 % | Única opção com pá curta (altura/diâmetro médio abaixo de 0,3) | Etapa 4 §4 |
| Mancais | B1: par de contato angular (Jet A). B2: rolos cilíndricos (HTP) | B1 segura o empuxo axial; B2 flutua axialmente para absorver dilatação | Etapa 5 §6 |

## 2. Pendências que mudam o projeto
Em ordem de impacto.

### 2.1 Sentido do escape da turbina
As etapas 4 e 5 discordam do sinal do empuxo axial do rotor da turbina (6,2 a 6,5 kN):

- Etapa 5: o escape sai para fora (+z, longe das bombas). O empuxo líquido no mancal B1 fica em **−1,6 kN**, aceitável.
- Etapa 4: escreve o empuxo apontando para as bombas. Com esse sinal, o líquido seria **−14,4 kN**, inaceitável sem pistão de balanceamento.

É uma decisão de arranjo (de que lado ficam os bocais e o coletor de escape). Precisa ser fechada antes do CAD.

### 2.2 Sobra de 55 % de potência na turbina
Com as bombas dimensionadas, a turbina precisa de 501 kW e consegue entregar 774 kW com as pressões do requisito. Em regime isso não se sustenta: o rotor aceleraria. Opções:

1. Reduzir a queda de pressão na turbina de 20 para ~13 bar, o que permite baixar a pressão de descarga da OP.
2. Válvula de *bypass* da turbina (parte do gás vai direto para a câmara), que também serve de controle.
3. Aceitar rotação acima de 55 000 rpm, o que piora a cavitação.

A Etapa 5 dimensionou o eixo para o torque máximo disponível (134 N·m). Se a opção 1 ou 2 for adotada, o torque de projeto cai para ~105 N·m.

### 2.3 Margem de cavitação do indutor da OP
K de operação = 0,0256 contra limite de 0,025: folga de 2 %, sobre um K mínimo ainda não validado. É o maior risco da OP. Depende do CFTurbo ou de ensaio.

### 2.4 Rigidez real dos mancais
É o parâmetro que mais pesa na 1ª velocidade crítica: 1,53 vezes a rotação nominal com 50/100 MN/m, mas abaixo de ~25/50 MN/m a margem de 20 % some. Depende da pré-carga do par B1 e do suporte.

### 2.5 Voluta dupla ou simples na OP
A dupla foi adotada para segurar o empuxo radial na partida (2,64 → 0,69 kN). No ponto de projeto ela é pior (481 → 685 N) e a garganta cai para Ø10 mm, mais difícil de fabricar.

### 2.6 Mancal B2
- Pouca carga radial (0,45 kN nominal) a 55 000 rpm: risco de os rolos deslizarem em vez de rolar. Opções: pré-carga radial ou trocar por contato angular com mola.
- Opera em HTP, ao lado do disco da turbina a ~1130 K, e o vazamento do selo S7 (48 g/s de HTP) decompõe nessa cavidade. Falta a análise térmica.

### 2.7 Premissa de 5 bar na entrada
É pressão total na entrada das bombas, sem perdas de linha. Cada 1 bar a menos corta ~15 % da rotação máxima por cavitação da OP. A FP precisa de pelo menos 4,3 bar para dispensar o indutor.

## 3. Diferenças entre relatórios (ainda não reconciliadas)
As etapas foram revisadas em sequência (1 → 5), então as primeiras não viram os resultados finais das últimas.

| Assunto | Relatório mais antigo | Valor atual | Efeito |
|---|---|---|---|
| 1ª velocidade crítica | Etapa 1: 1,28 × nominal (rotor estimado) | Etapa 5: 1,53 × nominal (peças reais) | A crítica **deixa de ser argumento** contra 60 000 rpm (daria 1,40). Restam cavitação e pá da turbina |
| Potências | Etapa 1: OP 415 kW, turbina 504 kW | 411,6 e 501 kW | Desprezível |
| Eficiência da FP no meanline | Etapa 1: 0,60 | Etapa 3: 0,555 | Nenhum (o ciclo já usava 0,55) |
| Eficiências e potência da turbina | Etapa 0: 0,60 / 0,45 e 593 kW (provisórias) | 0,706 / 0,555 e 501 kW | Etapa 0 mantida como registro do ponto de partida |
| Sinal do empuxo da turbina | Etapa 4: para as bombas | Etapa 5: para longe das bombas | Ver 2.1 |

## 4. Comparação com o projeto de referência
| Item | Referência | Este projeto | Leitura |
|---|---|---|---|
| Rotação | 60 000 rpm | 55 000 rpm (−8 %) | A 60 000 rpm o indutor da OP operaria com K ≈ 0,022. A referência provavelmente aceita um indutor mais agressivo ou usa um eixo mais fino sob a OP |
| Queda de temperatura na turbina | 10 K | 15,4 K (mínimo do balanço) | 10 K dão 324 kW, menos que a potência hidráulica das bombas (331 kW): o valor de referência não fecha |

## 5. O que falta fazer
1. Validar bombas e turbina no CFTurbo (eficiência, NPSH, carregamento das pás) e atualizar os JSON.
2. Fechar as pendências 2.1 e 2.2 e, se mudarem, refazer as etapas 4 e 5.
3. Etapa 6: CAD paramétrico no Fusion a partir dos JSON, e trocar as massas e inércias analíticas (incerteza de ±20 a 25 %) pelas do CAD. Os rotores dos selos interpropelentes (140 g, estimados) são a prioridade.
4. Rotodinâmica completa (diagrama de Campbell, amortecimento, rigidez dos anéis de desgaste, resposta ao desbalanceamento).
5. Compatibilidade de materiais com HTP nas peças molhadas (o níquel do Inconel catalisa a decomposição).
6. Empuxo axial nos transientes de partida e corte.
7. Conferir a numeração de uma fonte: a Etapa 1 cita "NASA SP-8100" para rigidez do eixo e limites de DN. Verificar no PDF se a monografia correta é essa ou a de sistemas de turbobomba.
