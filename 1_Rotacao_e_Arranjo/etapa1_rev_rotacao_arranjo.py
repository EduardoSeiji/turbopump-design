"""
turbopump-design — Etapa 1 (rev. 2): rotação final e arranjo do eixo sob a OP,
usando os resultados reais das etapas 0, 2, 3, 4 e 5.

Parte A — cavitação do indutor da OP pelo número de cavitação de pá K (NASA SP-8052):
   tau = 2g·NPSH/u_t² = K + K·phi² + phi²   (eq. 2)
   D_t escolhido para maximizar K (Brumfield, eq. 5–6)
   K crítico real ≈ (2–3)·tan²(beta_B/2)    (eq. 29–30 + texto §2.1.5)
   beta_B = beta_flow/(1 − 0,425)            (§2.1.9, mesmo valor da Etapa 2)
Parte B — 1ª crítica (forward síncrona) com viga Euler-Bernoulli + discos (Id − Ip),
   calibrada no modelo do 06 (segmentos, massas e inércias do §9).
"""
import numpy as np
from scipy.linalg import eig

g = 9.81
# ------------------------------------------------------------------ dados reais
rho_ox, Q_ox = 1385.0, 17.5 / 1385.0          # 01
NPSHA_ox = 36.8                                # 01
F_NPSH = 1.20                                  # 02 (mantido)
NPSH_d = NPSHA_ox / F_NPSH                     # 30,6 m
D_t_fixed_ratio = None

def inducer_opt(n, d_hub):
    """Varre D_t e devolve o ponto de K máximo para (Q, n, NPSH_d, d_hub)."""
    best = None
    for Dt in np.linspace(d_hub * 1.25, 0.08, 4000):
        nu = d_hub / Dt
        ut = np.pi * n * Dt / 60
        cm = Q_ox / (np.pi / 4 * Dt**2 * (1 - nu**2))
        phi = cm / ut
        tau = 2 * g * NPSH_d / ut**2
        K = (tau - phi**2) / (1 + phi**2)
        if best is None or K > best["K"]:
            beta_f = np.degrees(np.arctan(phi))
            beta_B = beta_f / (1 - 0.425)
            Kmm = np.tan(np.radians(beta_B) / 2) ** 2          # SP-8052 eq. 30
            Ss = n * np.sqrt(Q_ox) / NPSH_d**0.75              # métrico (Gülich 6.7)
            best = dict(Dt=Dt, nu=nu, ut=ut, phi=phi, tau=tau, K=K, beta_B=beta_B,
                        Kcrit25=2.5 * Kmm, Kcrit3=3.0 * Kmm, nss=Ss, S_US=Ss / 0.0194)
    return best

print("=" * 90)
print("A) INDUTOR DA OP — K máximo (Brumfield) vs K crítico, NPSH de projeto = %.1f m" % NPSH_d)
print(" d_hub  n[krpm]  D_t[mm]  nu    u_t   phi    beta_B   K_op   K_cr(3x)  K_op/K_cr  S[US]")
res = {}
for d_hub in [0.014, 0.020, 0.022, 0.024, 0.028]:
    for n in [50e3, 55e3, 60e3]:
        r = inducer_opt(n, d_hub)
        res[(d_hub, n)] = r
        print(f" {d_hub*1e3:4.0f}   {n/1e3:5.0f}   {r['Dt']*1e3:6.1f}  {r['nu']:.2f}  {r['ut']:5.0f}  "
              f"{r['phi']:.3f}  {r['beta_B']:5.1f}°  {r['K']:.4f}  {r['Kcrit3']:.4f}   "
              f"{r['K']/r['Kcrit3']:5.2f}   {r['S_US']:6.0f}")

# rotação máxima: K_op / K_cr(3x) = 1,0 (já com F_NPSH = 1,2 no NPSH)
def n_max(d_hub, ratio=1.0, which="Kcrit3"):
    lo, hi = 20e3, 120e3
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        r = inducer_opt(mid, d_hub)
        if r["K"] / r[which] >= ratio: lo = mid
        else: hi = mid
    return lo
print("\n Obs.: K_op/K_cr quase não varia com n (Brumfield: K≈2φ², K_cr∝tan²β∝φ²) → esse critério não limita n.")
print(" Limite empírico: K_op ≥ K_lim, K* exp. = 0,006–0,01 (SP-8052 §2.1.3). n_max para K_lim:")
def n_max_K(d_hub, Klim):
    lo, hi = 20e3, 150e3
    for _ in range(50):
        mid = 0.5*(lo+hi)
        if inducer_opt(mid, d_hub)["K"] >= Klim: lo = mid
        else: hi = mid
    return lo
for d_hub in [0.014, 0.020, 0.024, 0.028]:
    print(f"  d_hub {d_hub*1e3:4.0f} mm: K_lim 0,034 (crit. antigo n_ss 500 @ν0,3) → {n_max_K(d_hub,0.034)/1e3:5.1f} | "
          f"0,025 (2,5·K*) → {n_max_K(d_hub,0.025)/1e3:5.1f} | 0,020 (2·K*) → {n_max_K(d_hub,0.020)/1e3:5.1f} krpm")

# ------------------------------------------------------------------ Parte B: rotor
E, rho_s = 200e9, 8190.0
seg06 = [(0, 20, 14), (20, 28, 18), (28, 52, 20), (52, 90, 22), (90, 138, 20),
         (138, 150, 22), (150, 166, 20), (166, 180, 24), (180, 200, 20)]   # 06 §9, mm
parts06 = [  # nome, m[g], z_CG[mm], Ip, Id [kg·mm²]   (06 §9, sem o eixo)
    ("FP", 111.0, 9.6, 38.4, 20.8), ("B1 pistas", 48.4, 40.0, 6.8, 5.7),
    ("selos IP", 140.0, 71.0, 28.7, 27.8), ("indutor OP", 26.6, 103.0, 5.7, 3.9),
    ("impeller OP", 57.9, 127.7, 26.8, 15.3), ("luva S6", 19.8, 143.0, 3.7, 2.0),
    ("B2 pista", 20.3, 158.0, 2.7, 1.6), ("luva S7", 23.8, 172.0, 4.4, 2.5),
    ("turbina", 401.8, 191.0, 298.8, 156.3)]

def critical(seg, parts, bearings, EI_override=None, dz=2.0):
    """1ª forward síncrona [rpm]. bearings: lista (z_mm, k N/m). EI_override: {(z0,z1): EI}."""
    z_end = seg[-1][1]
    nodes = np.arange(0, z_end + 1e-9, dz)
    for p in parts: nodes = np.append(nodes, p[2])
    for z, _ in bearings: nodes = np.append(nodes, z)
    nodes = np.unique(np.round(nodes, 3))
    N = len(nodes); K = np.zeros((2*N, 2*N)); M = np.zeros_like(K)
    for e in range(N - 1):
        z0, z1 = nodes[e], nodes[e+1]; L = (z1 - z0) / 1e3; zm = 0.5 * (z0 + z1)
        d = [s[2] for s in seg if s[0] <= zm < s[1]][0] / 1e3
        A = np.pi * d**2 / 4; EI = E * np.pi * d**4 / 64
        if EI_override:
            for (a, b), v in EI_override.items():
                if a <= zm < b: EI = v
        k = EI / L**3 * np.array([[12, 6*L, -12, 6*L], [6*L, 4*L*L, -6*L, 2*L*L],
                                  [-12, -6*L, 12, -6*L], [6*L, 2*L*L, -6*L, 4*L*L]])
        m = rho_s * A * L / 420 * np.array([[156, 22*L, 54, -13*L], [22*L, 4*L*L, 13*L, -3*L*L],
                                            [54, 13*L, 156, -22*L], [-13*L, -3*L*L, -22*L, 4*L*L]])
        idx = [2*e, 2*e+1, 2*e+2, 2*e+3]
        K[np.ix_(idx, idx)] += k; M[np.ix_(idx, idx)] += m
    for _, mg, z, Ip, Id in parts:
        i = int(np.argmin(abs(nodes - z)))
        M[2*i, 2*i] += mg / 1e3
        M[2*i+1, 2*i+1] += (Id - Ip) * 1e-6          # forward síncrona: Id − Ip
    for z, kb in bearings:
        i = int(np.argmin(abs(nodes - z))); K[2*i, 2*i] += kb
    w2, _ = eig(K, M)
    w2 = np.real(w2[np.isfinite(w2)]); w2 = np.sort(w2[w2 > 1.0])
    return np.sqrt(w2[0]) * 60 / (2*np.pi)

def bearings(kB1, kB2, zB1=(34, 46), zB2=158):
    return [(zB1[0], kB1/2), (zB1[1], kB1/2), (zB2, kB2)]

print("=" * 90)
print("B) 1ª CRÍTICA — calibração com o 06 §8 (50/100 MN/m → 67 300 rpm)")
for tag, b in [("kB1 = total do par (2×25)", bearings(50e6, 100e6)),
               ("kB1 = por fileira (2×50)", bearings(100e6, 100e6))]:
    print(f"  {tag}: {critical(seg06, parts06, b):7.0f} rpm")

b_base = bearings(50e6, 100e6)
print(f"  base 06 (kB1 total do par): {critical(seg06, parts06, b_base):7.0f} rpm")

def seg_mod(d_OP=20, shrink_IP=0.0, d_IP=22):
    """d_OP: diâmetro equivalente aço sob a OP (z 90–138); shrink_IP: encurta pacote IP [mm]."""
    out = []
    for z0, z1, d in seg06:
        if (z0, z1) == (90, 138): d = d_OP
        if (z0, z1) == (52, 90): d = d_IP
        out.append([z0, z1, d])
    # encurtar o pacote IP: desloca tudo a jusante de z=52 por -shrink
    res = []
    for z0, z1, d in out:
        if z0 >= 52 and (z0, z1) != (52, 90): z0, z1 = z0 - shrink_IP, z1 - shrink_IP
        elif (z0, z1) == (52, 90): z1 = z1 - shrink_IP
        res.append((z0, z1, d))
    return res
def parts_mod(shrink_IP=0.0, f_IP=1.0, f_OP=1.0):
    out = []
    for nm, m, z, Ip, Id in parts06:
        if nm == "selos IP": m, Ip, Id, z = m*f_IP, Ip*f_IP, Id*f_IP, z - shrink_IP/2
        elif z > 60: z = z - shrink_IP
        if nm in ("indutor OP", "impeller OP"): m, Ip, Id = m*f_OP, Ip*f_OP, Id*f_OP
        out.append((nm, m, z, Ip, Id))
    return out
def brg(kB1, kB2, shrink=0.0): return bearings(kB1, kB2, zB2=158 - shrink)

def eq_d(parts_EI):
    """diâmetro equivalente de aço (E=200 GPa) de uma seção composta [(E, d_out, d_in)]."""
    EI = sum(Ei*np.pi*(do**4 - di**4)/64 for Ei, do, di in parts_EI)
    return (EI*64/(np.pi*200e9))**0.25

print("\n Seção equivalente sob a OP (diâmetro de aço com mesmo EI):")
cases_EI = {
  "06: eixo IN718 20 maciço + luva/cubo (não estrutural)": eq_d([(200e9,0.020,0)]),
  "tie-bolt IN718 12 + cubo Al 6061 22 (junta perfeita)": eq_d([(200e9,0.012,0),(69e9,0.022,0.012)]),
  "tie-bolt IN718 12 + cubo 316L 22": eq_d([(200e9,0.012,0),(193e9,0.022,0.012)]),
  "eixo IN718 24 maciço + cubo Al fino (ν→0,61 c/ 28)": eq_d([(200e9,0.024,0)]),
  "eixo IN718 24 oco 12 (cubo 28)": eq_d([(200e9,0.024,0.012)]),
}
for k,v in cases_EI.items(): print(f"   {k:55s} d_eq = {v*1e3:5.1f} mm")

print("\n 1ª crítica [rpm] e razão p/ 55 e 60 krpm (critério ≥ 1,20, Huzel p.206):")
print("  caso                                              k 50/100   k 100/200   | n_c/55k  n_c/60k (k 50/100)")
cases = [
  ("06 base (d_OP 20, IP 38 mm)",                      dict(d_OP=20), dict()),
  ("d_OP 18 (tie-bolt + Al)",                          dict(d_OP=18), dict()),
  ("d_OP 22",                                          dict(d_OP=22), dict()),
  ("d_OP 24 (eixo 24, cubo Al 28)",                    dict(d_OP=24), dict()),
  ("d_OP 20 + IP −10 mm",                              dict(d_OP=20, shrink_IP=10), dict(shrink_IP=10, f_IP=0.75)),
  ("d_OP 22 + IP −10 mm",                              dict(d_OP=22, shrink_IP=10), dict(shrink_IP=10, f_IP=0.75)),
  ("d_OP 24 + IP −10 mm",                              dict(d_OP=24, shrink_IP=10), dict(shrink_IP=10, f_IP=0.75)),
  ("d_OP 24 + IP −10 mm + d_IP 24",                    dict(d_OP=24, shrink_IP=10, d_IP=24), dict(shrink_IP=10, f_IP=0.75)),
]
crit_table = []
for nm, sk, pk in cases:
    sh = sk.get("shrink_IP", 0.0)
    c1 = critical(seg_mod(**sk), parts_mod(**pk), brg(50e6, 100e6, sh))
    c2 = critical(seg_mod(**sk), parts_mod(**pk), brg(100e6, 200e6, sh))
    crit_table.append((nm, c1, c2))
    print(f"  {nm:48s}  {c1:8.0f}   {c2:8.0f}    |  {c1/55e3:5.2f}    {c1/60e3:5.2f}")

# ------------------------------------------------------------------ exportação
import csv, json, os
out_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(out_dir, "indutor_OP_K.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["d_hub_mm", "n_rpm", "D_t_mm", "nu", "u_t_m_s", "phi", "beta_B_deg", "K_op",
                "K_cr_3x", "K_op_sobre_Kstar_0p01", "S_US"])
    for (dh, n), r in sorted(res.items()):
        w.writerow([round(dh*1e3, 1), int(n), round(r["Dt"]*1e3, 2), round(r["nu"], 3), round(r["ut"], 1),
                    round(r["phi"], 4), round(r["beta_B"], 2), round(r["K"], 4), round(r["Kcrit3"], 4),
                    round(r["K"]/0.01, 2), round(r["S_US"])])
with open(os.path.join(out_dir, "critica_rotor.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["caso", "nc_k50_100_rpm", "nc_k100_200_rpm", "nc_sobre_55k", "nc_sobre_60k"])
    for nm, c1, c2 in crit_table:
        w.writerow([nm, round(c1), round(c2), round(c1/55e3, 3), round(c1/60e3, 3)])
r55 = res[(0.028, 55e3)]
summary = {
    "decisao": {"n_nominal_rpm": 55000,
                "arranjo": "FP balanco - B1 (par contato angular) - pacote interpropelente - OP eixo passante - B2 (rolos) - turbina balanco",
                "eixo_sob_OP": "IN718 macico D24 mm, luva/revestimento compativel com HTP",
                "cubo_indutor_OP_mm": 28, "criterio_cavitacao": "K_op >= 0.025 (2.5 x K* 0.01) com F_NPSH 1.2"},
    "indutor_OP_55k_cubo28": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r55.items()},
    "potencias_kW": {"OP_eixo": 415, "FP_eixo": 74, "turbina_eta_mec_0p97": 504},
    "torque_turbina_Nm": 87.5,
    "DN_mancais": 1.10e6,
    "primeira_critica_rpm": {nm: round(c1) for nm, c1, _ in crit_table},
    "nota_modelo_rotor": "Euler-Bernoulli FE + discos (Id-Ip); 2.4 % abaixo do modelo da etapa de eixo/mancais; usar como comparacao relativa",
}
with open(os.path.join(out_dir, "resultados_etapa1.json"), "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print("\nArquivos gravados: indutor_OP_K.csv, critica_rotor.csv, resultados_etapa1.json")
