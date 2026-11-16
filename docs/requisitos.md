# Requisitos e premissas

Entrada de todo o projeto. Nos relatórios das etapas este documento é citado como **"00"**.

## Requisitos das bombas
| Item | Bomba de combustível (FP, *fuel pump*) | Bomba de oxidante (OP, *oxidizer pump*) |
|---|---|---|
| Fluido | Jet A | HTP (*high-test peroxide*, peróxido de hidrogênio concentrado) a 90 % |
| Vazão mássica | 2,5 kg/s | 17,5 kg/s |
| Pressão de entrada | 5 bar | 5 bar |
| Pressão de saída | 135 bar | 235 bar |
| Aumento de pressão Δp | 130 bar | 230 bar |
| Temperatura de entrada | 300 K | 300 K |

A pressão de entrada é a pressão de tanque, sem perdas de linha (premissa).

## Ciclo
Combustão estagiada rica em oxidante, com eixo único (FP – OP – turbina):

```
Jet A:  tanque 5 bar → FP → 135 bar → válvula principal → 130 bar → câmara
HTP:    tanque 5 bar → OP → 235 bar → válvula principal → 230 bar
        → refrigeração regenerativa da câmara → 200 bar / 400 K
        → gerador de gás catalítico (decompõe o HTP) → 150 bar / 1150 K
        → turbina → 130 bar → câmara
```

- Todo o HTP passa pela turbina e depois entra na câmara. Razão de mistura O/F = 17,5 / 2,5 = 7,0.
- Pressão de câmara: 100 bar.
- Uso único (não reutilizável).
- Faixa de *throttle* (variação de empuxo): fora do escopo.

## Valores de referência (só para comparação, nunca como entrada)
O projeto de referência indica 60 000 rpm e uma queda de 10 K na turbina. Cada etapa compara o seu resultado com esses valores apenas no fim.

## Sequência de etapas
| Etapa | Pasta | Citada nos relatórios como |
|---|---|---|
| 0. Propriedades dos fluidos e balanço do ciclo | `0_Ciclo_e_Propriedades/` | 01 |
| 1. Rotação e arranjo do eixo | `1_Rotacao_e_Arranjo/` | 02 |
| 2. Bomba de oxidante (indutor, impeller, voluta) | `2_Bomba_HTP/` | 03 |
| 3. Bomba de combustível | `3_Bomba_JetA/` | 04 |
| 4. Turbina | `4_Turbina/` | 05 |
| 5. Eixo, mancais e selos | `5_Eixo_Mancais_Selos/` | 06 |
| 6. CAD paramétrico (Fusion) | a fazer | — |
