# turbopump-design

Preliminary design of a single-shaft rocket turbopump (90 % HTP / Jet A): cycle balance, pump inducer/impeller/volute meanline sizing, axial turbine, shaft, bearings and seals. Didactic project supporting an undergraduate thesis and a master's project on turbopump rotordynamics at Poli-USP.

Projeto didático: dimensionar do zero uma turbobomba de eixo único a partir apenas dos requisitos de pressão e vazão, com todas as contas em Python e cada equação rastreada à sua fonte. O texto dos relatórios está em português.

## O que é dimensionado
```
            Jet A                HTP 90 %
              │                     │
   ┌──────────▼───┐   ┌─────────────▼────────┐   ┌───────────┐
   │ bomba de     │   │ bomba de oxidante    │   │ turbina   │
   │ combustível  ├───┤ (indutor + impeller) ├───┤ axial     │   eixo único, 55 000 rpm
   └──────────────┘   └──────────────────────┘   └─────▲─────┘
                                                       │
                                  gás de HTP decomposto (150 bar, 1150 K)
```
Ciclo de combustão estagiada rica em oxidante: todo o HTP refrigera a câmara, é decomposto num leito catalítico, aciona a turbina e só então entra na câmara. Requisitos completos em [`docs/requisitos.md`](docs/requisitos.md).

## Resultados principais
| | Bomba de oxidante | Bomba de combustível | Turbina |
|---|---|---|---|
| Fluido | HTP 90 % | Jet A | HTP decomposto (H₂O + O₂) |
| Vazão | 17,5 kg/s | 2,5 kg/s | 17,5 kg/s |
| Pressão | 5 → 235 bar | 5 → 135 bar | 150 → 130 bar |
| Tipo | indutor + impeller fechado, voluta dupla | impeller semiaberto, sem indutor | axial, 1 estágio, reação 50 % |
| Diâmetro | 63,8 mm (saída do impeller) | 60,0 mm (saída do impeller) | 73,0 mm (médio) |
| Pás | 3 (indutor) + 6 | 6 + 6 *splitters* | 23 bocais / 29 pás |
| Eficiência | 0,71 | 0,55 | 0,73 (total-estática) |
| Potência de eixo | 412 kW | 74 kW | 501 kW requeridos |

| Rotor | Valor |
|---|---|
| Rotação nominal | 55 000 rpm |
| Massa / comprimento | 1,28 kg / 198 mm |
| Mancais | par de contato angular (lado combustível) + rolos cilíndricos (lado turbina), furo de 20 mm |
| Empuxo axial líquido | −1,6 kN |
| 1ª velocidade crítica | 84 000 rpm (1,53 × nominal) com mancais de 50/100 MN/m |

Todos os parâmetros, incluindo a tabela de massas, inércias e segmentos do eixo para a rotodinâmica: [`docs/parametros_mestres.md`](docs/parametros_mestres.md) (leitura) e [`docs/parametros_mestres.json`](docs/parametros_mestres.json) (scripts).

**Status:** dimensionamento meanline (1D) concluído para as etapas 0 a 5. Falta validar no CFTurbo e fazer o CAD. Há decisões em aberto que mudam números, listadas em [`docs/pendencias_e_decisoes.md`](docs/pendencias_e_decisoes.md).

## Estrutura
| Pasta | Conteúdo | Relatório |
|---|---|---|
| [`0_Ciclo_e_Propriedades/`](0_Ciclo_e_Propriedades) | Propriedades dos fluidos, ponto das bombas, gás da turbina, balanço de potência | [`resultados_etapa0.md`](0_Ciclo_e_Propriedades/resultados_etapa0.md) |
| [`1_Rotacao_e_Arranjo/`](1_Rotacao_e_Arranjo) | Rotação nominal (cavitação, tensões, mancais, crítica) e arranjo do eixo | [`resultados_etapa1.md`](1_Rotacao_e_Arranjo/resultados_etapa1.md) |
| [`2_Bomba_HTP/`](2_Bomba_HTP) | Bomba de oxidante: indutor, impeller, voluta | [`resultados_etapa2.md`](2_Bomba_HTP/resultados_etapa2.md) |
| [`3_Bomba_JetA/`](3_Bomba_JetA) | Bomba de combustível e comparação de conceitos para baixa velocidade específica | [`resultados_etapa3.md`](3_Bomba_JetA/resultados_etapa3.md) |
| [`4_Turbina/`](4_Turbina) | Turbina axial: gás, triângulos de velocidade, perdas, tensões | [`resultados_etapa4.md`](4_Turbina/resultados_etapa4.md) |
| [`5_Eixo_Mancais_Selos/`](5_Eixo_Mancais_Selos) | Eixo, empuxos, mancais, selos, 1ª velocidade crítica, massas e inércias | [`resultados_etapa5.md`](5_Eixo_Mancais_Selos/resultados_etapa5.md) |
| [`docs/`](docs) | Requisitos, parâmetros consolidados, pendências, glossário | — |
| [`tools/`](tools) | Script que consolida os resultados das etapas | — |

Cada pasta de etapa tem o script, a saída dele (`saida_*.txt`), os resultados em JSON/CSV e um `README.md` próprio. Os relatórios citam uns aos outros por um número antigo ("01" a "06"); a correspondência está em [`docs/requisitos.md`](docs/requisitos.md). Símbolos e termos: [`docs/glossario.md`](docs/glossario.md).

## Como rodar
Python 3.10 ou mais novo.

```bash
pip install -r requirements.txt

python 0_Ciclo_e_Propriedades/etapa0_ciclo.py
python 1_Rotacao_e_Arranjo/etapa1_rotacao.py
python 1_Rotacao_e_Arranjo/etapa1_rev_rotacao_arranjo.py
python 2_Bomba_HTP/etapa2_bomba_htp.py
python 3_Bomba_JetA/etapa3_bomba_combustivel.py
python 4_Turbina/etapa4_turbina.py
python 5_Eixo_Mancais_Selos/etapa5_eixo_mancais.py     # lê os JSON das etapas 2, 3 e 4; leva ~1 min

python tools/consolidar_parametros.py                  # regenera docs/parametros_mestres.*
```

A ordem importa: as entradas de cada etapa vêm das anteriores (ficam no topo de cada script, com a fonte comentada). Depois de refazer uma etapa, rode as seguintes e o consolidador.

## Arquivos para as ferramentas seguintes
| Uso | Arquivo |
|---|---|
| Rotodinâmica: segmentos do eixo | `5_Eixo_Mancais_Selos/etapa5_eixo_segmentos.csv` |
| Rotodinâmica: discos (massa, posição, inércias) | `5_Eixo_Mancais_Selos/etapa5_rotor_massas.csv` |
| Rotodinâmica: crítica × rigidez dos mancais | `5_Eixo_Mancais_Selos/etapa5_criticas.csv` |
| CFTurbo: bomba de oxidante | `2_Bomba_HTP/etapa2_cfturbo.csv` |
| CFTurbo: bomba de combustível | `3_Bomba_JetA/cfturbo_fuel_pump_inputs.csv` |
| CFTurbo: turbina | `4_Turbina/etapa4_cfturbo.csv` |
| CAD: geometria de cada componente | `etapa2_bomba_htp.json`, `fuel_pump_geometry.json`, `etapa4_turbina.json`, `etapa5_eixo_mancais.json` |

## Referências
- Gülich, J. F. *Centrifugal Pumps*. Springer.
- Huzel, D. K.; Huang, D. H. *Modern Engineering for Design of Liquid-Propellant Rocket Engines*. AIAA, 1992. Capítulo 6.
- Monografias NASA de critérios de projeto: SP-8052 (indutores), SP-8101 (eixos e acoplamentos), SP-8121 (selos), e as de sistemas de turbobomba e de bombas centrífugas.
- Dixon, S. L.; Hall, C. A. *Fluid Mechanics and Thermodynamics of Turbomachinery*.

## Limitações
Projeto preliminar e didático. Os resultados vêm de correlações 1D e não foram validados por CFD nem por ensaio. Massas e inércias são analíticas, com incerteza de ±20 a 25 %.
