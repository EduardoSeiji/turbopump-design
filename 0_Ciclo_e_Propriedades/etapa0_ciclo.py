"""
turbopump-design — Etapa 0: propriedades, ponto das bombas e balanço de potência da turbina.
Requer: numpy, cantera (pip install cantera). Unidades SI em todo o código.
"""
import numpy as np
import cantera as ct

g = 9.80665          # m/s²
T0 = 300.0           # K, temperatura de entrada das bombas

# ---------------------------------------------------------------- (a) propriedades a 300 K
# Fontes (ver 01-resultados-etapa0.md):
#  HTP 90%: rho = 1386.7 kg/m³ @25 °C (CRC Handbook) corrigido p/ 27 °C com beta ~ 0.6e-3 1/K
#           mu ~ 1.26 mPa·s @20 °C -> ~1.1 mPa·s @27 °C (Schumb/MIT 1953, tendência tipo água)
#           p_v total ~ 0.5 kPa @27 °C (Evonik/Schumb: poucos mbar a 30 °C) -> incerto, mas irrelevante p/ NPSH
#           cp_l ~ 2.75 kJ/kgK (mistura 0.9*2.62 + 0.1*4.18)
#  Jet A:   rho ~ 795 kg/m³ @27 °C (típico 804 @15 °C, drho/dT ~ -0.72 kg/m³K; spec 775–840 @15 °C)
#           mu ~ 1.3 mPa·s (nu ~ 1.6 mm²/s), p_v (TVP) ~ 0.4 kPa (CRC Report 663)
props = {
    "HTP90": dict(rho=1386.7*(1-0.6e-3*2), pv=0.5e3, mu=1.1e-3, cp=2750.0),
    "JetA":  dict(rho=795.0,               pv=0.4e3, mu=1.3e-3, cp=2000.0),
}

# ---------------------------------------------------------------- (b) ponto das bombas
pumps = {  # mdot [kg/s], p_in [Pa], p_out [Pa], eta assumida
    "OP (HTP)":  dict(fl="HTP90", mdot=17.5, pin=5e5, pout=235e5, eta=0.60),
    "FP (Jet A)": dict(fl="JetA", mdot=2.5,  pin=5e5, pout=135e5, eta=0.45),
}
eta_mec = 0.97   # mancais + selos (perdas mecânicas ~3 %)

print("== (a)+(b)+(c) Bombas ==")
P_shaft_tot = 0.0
for name, p in pumps.items():
    f = props[p["fl"]]
    dp = p["pout"] - p["pin"]
    Q = p["mdot"]/f["rho"]                      # vazão volumétrica
    H = dp/(f["rho"]*g)                          # altura manométrica (head)
    P_h = Q*dp                                   # potência hidráulica = rho g H Q
    P_s = P_h/p["eta"]                           # potência de eixo
    NPSHa = (p["pin"] - f["pv"])/(f["rho"]*g)    # NPSH disponível (sem perdas na linha)
    dT = (1-p["eta"])*g*H/f["cp"]                # aquecimento do fluido pelas perdas
    p.update(Q=Q, H=H, P_h=P_h, P_s=P_s)
    P_shaft_tot += P_s
    print(f"{name:11s} Q={Q*1e3:6.2f} L/s  H={H:6.0f} m  P_h={P_h/1e3:6.1f} kW  "
          f"P_eixo={P_s/1e3:6.1f} kW  NPSHa={NPSHa:5.1f} m  dT_perdas={dT:4.1f} K")
    for n in (40e3, 60e3, 80e3):                 # só p/ contexto: n_q em função de n (Etapa 1 escolhe n)
        nq = n*np.sqrt(Q)/H**0.75
        print(f"      n={n/1e3:3.0f} krpm -> n_q={nq:5.1f}")
P_turb_req = P_shaft_tot/eta_mec
print(f"Potência de eixo bombas = {P_shaft_tot/1e3:.0f} kW ; turbina deve entregar ≈ {P_turb_req/1e3:.0f} kW")

# ---------------------------------------------------------------- gás de HTP 90% decomposto
# 1 kg HTP90: 0.9 kg H2O2 -> H2O + 1/2 O2 ; 0.1 kg H2O. Decomposição completa, gás ideal.
M_H2O2, M_H2O, M_O2 = 34.0147e-3, 18.0153e-3, 31.9988e-3
n_H2O2 = 0.9/M_H2O2
n_H2O = n_H2O2 + 0.1/M_H2O
n_O2 = 0.5*n_H2O2
gas = ct.Solution("gri30.yaml")
X = {"H2O": n_H2O, "O2": n_O2}

# Entalpia do líquido (formação, 298.15 K): H2O2(l) -187.78 kJ/mol, H2O(l) -285.83 kJ/mol (NIST)
# Calor de mistura desprezado (consistente com 620 kcal/kg de Bretschger & Shanley p/ água líquida).
h_liq298 = (n_H2O2*(-187.78e3) + 0.1/M_H2O*(-285.83e3))     # J/kg
cp_l = props["HTP90"]["cp"]

def T_decomp(T_liq, p):
    h = h_liq298 + cp_l*(T_liq - 298.15)                    # J/kg de HTP líquido
    gas.HPX = h, p, X                                       # composição congelada (sem equilíbrio)
    return gas.T

print("\n== Gás de decomposição ==")
for Tl in (298.15, 400.0):
    print(f"T_liq={Tl:6.1f} K -> T_adiabática={T_decomp(Tl, 200e5):7.1f} K")
gas.TPX = 1150.0, 150e5, X
cp, cv = gas.cp_mass, gas.cv_mass
print(f"@1150 K: M={gas.mean_molecular_weight:.2f} g/mol  cp={cp:.0f} J/kgK  gamma={cp/cv:.3f}  "
      f"x_O2={gas['O2'].X[0]:.3f}  Y_O2={gas['O2'].Y[0]:.3f}")

# ---------------------------------------------------------------- balanço da turbina
mdot_T = 17.5                     # todo o HTP passa pela turbina
p1, T1, p2 = 150e5, 1150.0, 130e5
gas.TPX = T1, p1, X
h1, s1 = gas.h, gas.s
gas.SPX = s1, p2, X
h2s, T2s = gas.h, gas.T
dh_s = h1 - h2s                    # queda isentrópica de entalpia
c0 = np.sqrt(2*dh_s)               # spouting velocity (velocidade isentrópica do jato)
print("\n== Turbina ==")
print(f"PR={p1/p2:.3f}  dh_s={dh_s/1e3:.1f} kJ/kg  dT_s={T1-T2s:.1f} K  c0={c0:.0f} m/s")
print(f"Potência ideal (eta_T=1) = {mdot_T*dh_s/1e3:.0f} kW")
dh_req = P_turb_req/mdot_T
print(f"dh real necessário = {dh_req/1e3:.1f} kJ/kg -> dT real ≈ {dh_req/cp:.1f} K ; eta_T necessária = {dh_req/dh_s:.2f}")
P_10K = mdot_T*cp*10.0
print(f"Com dT=10 K: P_T = {P_10K/1e3:.0f} kW  (< potência hidráulica total "
      f"{(pumps['OP (HTP)']['P_h']+pumps['FP (Jet A)']['P_h'])/1e3:.0f} kW !)")

# ---------------------------------------------------------------- sensibilidade: queda no CGG
print("\n== Sensibilidade: cada 10 bar a menos na descarga da OP ==")
f = props["HTP90"]
dP = pumps["OP (HTP)"]["Q"]*10e5/pumps["OP (HTP)"]["eta"]
print(f"-10 bar -> -{dP/1e3:.1f} kW de eixo ({dP/P_shaft_tot*100:.1f} % do total)")
