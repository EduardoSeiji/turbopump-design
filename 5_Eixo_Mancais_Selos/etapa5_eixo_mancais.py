"""
turbopump-design — Etapa 5: eixo, mancais e selos (preliminar, sem ROSS) — rev. 2
Unidades SI internamente; posições em mm a partir do nariz da FP (z = 0), +z -> turbina.

Inputs lidos dos JSONs das etapas anteriores (com fallback para os valores dos relatórios):
  ../2_Bomba_HTP/etapa2_bomba_htp.json   (OP: indutor, impeller, massas, F_R)
  ../3_Bomba_JetA/fuel_pump_geometry.json (FP: impeller semiaberto, massas, F_R, F_ax)
  ../4_Turbina/etapa4_turbina.json        (turbina: potência, geometria, massas, p2/p3)
Fontes: Gülich cap. 9 (Tab. 9.1, 9.2, 9.4), Huzel cap. 6 (p.206-218, Tab. 6-9),
NASA SP-8101 (eixos/acoplamentos), SP-8121 (selos), SP-8052 (indutor).

Saídas (nesta pasta): etapa5_eixo_mancais.json, etapa5_rotor_massas.csv,
etapa5_eixo_segmentos.csv, etapa5_criticas.csv (+ stdout -> saida_etapa5.txt).
"""
import csv
import json
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def carrega(rel):
    p = os.path.join(RAIZ, rel)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    print(f"[aviso] {rel} não encontrado: usando valores de fallback")
    return None


op_j = carrega("2_Bomba_HTP/etapa2_bomba_htp.json")
fp_j = carrega("3_Bomba_JetA/fuel_pump_geometry.json")
tb_j = carrega("4_Turbina/etapa4_turbina.json")

g = 9.81
mm = 1e-3
# ----------------------------------------------------------------- 1. ponto de operação
n = 55_000.0                                  # rpm (02 rev. 2)
w = n * 2 * np.pi / 60
rho_ox, rho_f = 1385.0, 795.0                 # kg/m3 (01)
mdot_ox, mdot_f = 17.5, 2.5
dp_ox, dp_f = 230e5, 130e5
p_in = 5e5

P_OP = (op_j["performance"]["P_shaft_kW"] if op_j else 411.6) * 1e3
P_FP = (fp_j["design_point"]["P_shaft_cycle_kW"] if fp_j else 74.33) * 1e3
eta_mec = tb_j["inputs"]["eta_mec"] if tb_j else 0.97
P_T = (P_OP + P_FP) / eta_mec                 # = P_req da turbina (05: 500,9 kW)
P_disp = (tb_j["balanco"]["P_disp_kW"] if tb_j else 774.2) * 1e3   # com η_ts de projeto
P_loss = P_T - P_OP - P_FP
T_f, T_o, T_T = P_FP / w, P_OP / w, P_T / w
T_disp = P_disp / w                           # torque que a turbina consegue dar a 55 krpm

# torque de projeto: maior entre overspeed 1,1 (T ∝ n², SP-8101 §3.1.1.1) e o torque disponível da turbina
k_os = 1.1 ** 2
T_des = {"FP-B1": T_f * k_os,
         "B1-OP": (P_FP + 0.5 * P_loss) / w * k_os,
         "OP-T": max(T_T * k_os, T_disp)}

# ----------------------------------------------------------------- 2. geometria das bombas e turbina
ind = op_j["inducer"] if op_j else {}
imp = op_j["impeller"] if op_j else {}
Dt_in = ind.get("D_tip_inlet_mm", 46.5) * mm
d_hub_ind = ind.get("d_hub_mm", 28.0) * mm
H_ind = ind.get("H_m", 100.4)
d2_ox = imp.get("d2_mm", 63.75) * mm
b2_ox = imp.get("b2_mm", 4.72) * mm
u2_ox = imp.get("u2", 183.6)
psi_ox = imp.get("psi", 0.927)
eta_h_ox = imp.get("eta_h", 0.83)
H_imp_ox = imp.get("H_m", 1593.0)
d_ring_ox = imp.get("d_wear_ring_mm", 47.0) * mm      # anel frontal = traseiro (furos de balanceamento)
dn_ox = imp.get("dn_mm", 28.0) * mm
c1m_ox = imp.get("c1m", 18.62)
Q_La_ox = imp.get("Q_La_m3s", 0.014332)
p1_ox = p_in + rho_ox * g * H_ind             # entrada do impeller OP (saída do indutor)

fpi = fp_j["impeller"] if fp_j else {}
d2_f = fpi.get("d2", 60.0) * mm
F_ax_fp = -(fp_j["loads"]["F_axial_N_to_suction"] if fp_j else -13.0)  # 04: + p/ sucção -> aqui +z
F_R_fp_nom = fp_j["loads"]["F_radial_nominal_N"] if fp_j else 180.0
F_R_fp_des = fp_j["loads"]["F_radial_design_N"] if fp_j else 586.0
F_R_op_nom = op_j["loads"]["FR_double_N"] if op_j else 685.0
F_R_op_des = op_j["loads"]["FR_design_kR015_N"] if op_j else 1699.0

geo_t = tb_j["geometria"] if tb_j else {}
d_tip = geo_t.get("d_tip_mm", 92.65) * mm
p2_T = (tb_j["escoamento"]["p2_bar"] if tb_j else 139.7) * 1e5
p3_T = (tb_j["inputs"]["p3_bar"] if tb_j else 130.0) * 1e5
F_ax_T_05 = (tb_j["cargas"]["F_ax_rotor_kN"] if tb_j else 6.25) * 1e3   # módulo (05 §7)

# ----------------------------------------------------------------- 3. peças do rotor (massas e inércias)
AL, SS, IN = 2700.0, 7800.0, 8190.0


class Peca:
    """Peça com (m, z_CG, Ip, Id) dados, ou construída por anéis (r_i, r_o, L, z0)."""

    def __init__(s, nome, mat, fonte, m=None, zc=None, Ip=None, Id=None, rho=None):
        s.nome, s.mat, s.fonte, s.rho, s.aneis = nome, mat, fonte, rho, []
        s._p = (m, zc, Ip, Id) if m is not None else None

    def anel(s, di, do, L, z0, fill=1.0):
        s.aneis.append((di / 2, do / 2, L, z0, fill))
        return s

    def props(s):
        if s._p:
            return s._p
        parts = [(s.rho * f * np.pi * (ro**2 - ri**2) * L, ri, ro, L, z0 + L / 2)
                 for ri, ro, L, z0, f in s.aneis]
        m = sum(p[0] for p in parts)
        zc = sum(p[0] * p[4] for p in parts) / m
        Ip = sum(mi * (ri**2 + ro**2) / 2 for mi, ri, ro, L, z in parts)
        Id = sum(mi * (3 * (ri**2 + ro**2) + L**2) / 12 + mi * (z - zc) ** 2
                 for mi, ri, ro, L, z in parts)
        return m, zc, Ip, Id


rd = fp_j["rotordynamics"] if fp_j else {}
fp_m = rd.get("impeller_17-4PH", {"m_kg": 0.0831, "Ip_kgm2": 3.197e-5, "Id_kgm2": 1.72e-5, "z_cg_mm": 2.36})
fp_fl = rd.get("entrained_fluid", {"m_kg": 0.00593, "Ip_kgm2": 3.08e-6})
mi_op = op_j["mass_inertia_Al6061"] if op_j else {
    "m_impeller_kg": 0.0417, "Ip_impeller_kgm2": 2.288e-5, "Id_impeller_kgm2": 1.168e-5,
    "m_inducer_kg": 0.0168, "Ip_inducer_kgm2": 4.255e-6, "Id_inducer_kgm2": 2.581e-6,
    "m_fluid_impeller_kg": 0.0132, "Ip_fluid_kgm2": 9.614e-6}
rot_t = tb_j["rotor"] if tb_j else {"m_g": 296.0, "Ip_kgmm2": 247.1, "Id_kgmm2": 126.6}

# posições axiais (arranjo da 06 §2, ajustado às peças reais)
z_fp_rear = 14.0 * mm                                 # face traseira do disco da FP
z_ind0, L_ind = 92.0 * mm, ind.get("L_axial_mm", 18.5) * mm
z_imp0, L_imp = 112.0 * mm, imp.get("L_hub_mm", 18.0) * mm
z_tb = 190.0 * mm                                     # CG do rotor da turbina (disco 12 mm em z 184-196)
zB1a, zB1b, zB2 = 34 * mm, 46 * mm, 158 * mm

pecas = [
    Peca("Impeller FP (semiaberto)", "17-4PH H1025", "04 §7", fp_m["m_kg"],
         z_fp_rear - fp_m["z_cg_mm"] * mm, fp_m["Ip_kgm2"], fp_m["Id_kgm2"]),
    Peca("Fluido arrastado FP", "Jet A", "04 §7", fp_fl["m_kg"], z_fp_rear - 3 * mm,
         fp_fl["Ip_kgm2"], fp_fl["Ip_kgm2"] / 2),
    Peca("Pistas int. B1 (par)", "aço", "06 rev.1", rho=SS).anel(20 * mm, 27 * mm, 24 * mm, 28 * mm),
    Peca("Rotores selos IP", "aço", "06 rev.1", rho=SS).anel(22 * mm, 34 * mm, 34 * mm, 54 * mm),
    Peca("Indutor OP", "Al 6061-T6", "03 §4.6", mi_op["m_inducer_kg"], z_ind0 + L_ind / 2,
         mi_op["Ip_inducer_kgm2"], mi_op["Id_inducer_kgm2"]),
    Peca("Impeller OP", "Al 6061-T6", "03 §4.6", mi_op["m_impeller_kg"], z_imp0 + 0.6 * L_imp,
         mi_op["Ip_impeller_kgm2"], mi_op["Id_impeller_kgm2"]),
    Peca("Fluido arrastado OP", "HTP", "03 §4.6", mi_op["m_fluid_impeller_kg"], z_imp0 + 0.6 * L_imp,
         mi_op["Ip_fluid_kgm2"], mi_op["Ip_fluid_kgm2"] / 2),
    Peca("Luva S6", "aço", "06 rev.1", rho=SS).anel(22 * mm, 28 * mm, 10 * mm, 138 * mm),
    Peca("Pista int. B2", "aço", "06 rev.1", rho=SS).anel(20 * mm, 26 * mm, 12 * mm, 152 * mm),
    Peca("Luva S7", "aço", "06 rev.1", rho=SS).anel(24 * mm, 30 * mm, 12 * mm, 166 * mm),
    Peca("Rotor turbina (disco+pás+shroud)", "MAR-M-247", "05 §6", rot_t["m_g"] * 1e-3, z_tb,
         rot_t["Ip_kgmm2"] * 1e-6, rot_t["Id_kgmm2"] * 1e-6),
]

# eixo IN718 maciço: (z_ini, z_fim, d) [mm]; sob a OP = Ø24 (02 rev. 2 §5)
eixo_seg = [(0, 20, 14), (20, 28, 18), (28, 52, 20), (52, 90, 22), (90, 136, 24),
            (136, 150, 22), (150, 166, 20), (166, 180, 24), (180, 198, 20)]
E_sh, rho_sh = 200e9, IN


def eixo_props():
    m = zc = Ip = 0.0
    for z0, z1, d in eixo_seg:
        mi = rho_sh * np.pi * (d * mm) ** 2 / 4 * (z1 - z0) * mm
        m += mi; zc += mi * (z0 + z1) / 2 * mm; Ip += mi * (d * mm) ** 2 / 8
    return m, zc / m, Ip


# ----------------------------------------------------------------- 4. empuxo axial
def F_Hy(da, db, dp_La, k, u2, d2, rho):                 # Gülich Eq. T9.2.7 / T9.2.13
    return np.pi / 4 * (da**2 - db**2) * (dp_La - rho / 2 * k**2 * u2**2 *
                                          (1 - (da**2 + db**2) / (2 * d2**2)))


dpLa_ox = rho_ox * g * H_imp_ox * (1 - psi_ox / (4 * eta_h_ox))  # ~Gülich Eq. T9.2.2
k_rot = 0.5
F_unbal_ox = F_Hy(d_ring_ox, dn_ox, dpLa_ox, k_rot, u2_ox, d2_ox, rho_ox)
FI_ox = rho_ox * Q_La_ox * c1m_ox                               # Eq. T9.2.9 (ε2 = 90°)
f_res = 0.15                                                    # Eq. T9.2.14: 0,1-0,2


def F_res_ox(fr=f_res):
    return fr * F_unbal_ox - FI_ox                              # + p/ sucção (−z)


p_B1, p_drain, p_purge, p_buf = 8e5, 1.5e5, 4e5, 155e5
d_S1, d_IP, d_S6, d_S7 = 20 * mm, 30 * mm, 22 * mm, 26 * mm


def ledger(sinal_turbina=+1, pb=None):
    """F_z = Σ A_j (p_esq − p_dir). Fileiras de pás tratadas como 'vedação'.
    sinal_turbina=+1: escape da turbina para +z (arranjo 06); −1: escape para −z (leitura da 05)."""
    pb = p_buf if pb is None else pb
    seq = [("S1 FP traseira→B1", d_S1, p_in, p_B1),
           ("S2 primário Jet A", d_IP, p_B1, p_drain),
           ("S3 intermediário (He)", d_IP, p_drain, p_purge),
           ("S4 intermediário (He)", d_IP, p_purge, p_drain),
           ("S5 primário HTP", d_IP, p_drain, p_in),
           ("Indutor OP (D_t entrada)", Dt_in, p_in, p1_ox),
           ("S6 traseira OP→buffer B2", d_S6, p1_ox, pb),
           ("S7 buffer→cavidade disco", d_S7, pb, p2_T),
           ("Rotor turbina", d_tip, p2_T, p3_T)]
    termos = []
    for nome, d, pl, pr in seq:
        F = np.pi / 4 * d**2 * (pl - pr)
        if nome == "Rotor turbina" and sinal_turbina < 0:
            F = -F_ax_T_05
        termos.append((nome, d, pl, pr, F))
    return termos


def F_net(fr=f_res, sinal_turbina=+1, pb=None):
    return sum(t[4] for t in ledger(sinal_turbina, pb)) - F_res_ox(fr) + F_ax_fp


F_ax = F_net()
F_ax_faixa = (F_net(0.10), F_net(0.20))
F_ax_pbuf = (F_net(pb=145e5), F_net(pb=165e5))
F_ax_turb_neg = F_net(sinal_turbina=-1)

# ----------------------------------------------------------------- 5. forças radiais e reações
z_fp = pecas[0].props()[1]
z_op = (pecas[4].props()[0] * pecas[4].props()[1] + pecas[5].props()[0] * pecas[5].props()[1]) / (
    pecas[4].props()[0] + pecas[5].props()[0])
m_fp = pecas[0].props()[0] + pecas[1].props()[0]
m_op = sum(pecas[i].props()[0] for i in (4, 5, 6))
m_tb = pecas[-1].props()[0]
G_bal = 2.5e-3                                    # ISO 21940 G2.5 [m/s]
a_lat = 10 * g
zB1 = 0.5 * (zB1a + zB1b)


def reacoes(F_fp, F_op, F_tb):
    loads = [(F_fp, z_fp), (F_op, z_op), (F_tb, z_tb)]
    R2 = sum(F * (z - zB1) for F, z in loads) / (zB2 - zB1)
    return sum(F for F, _ in loads) - R2, R2, loads


def M_em(z, R1, R2, loads):
    M = sum(F * (z - zi) for F, zi in loads if zi < z)
    M -= R1 * (z - zB1) if z > zB1 else 0
    M -= R2 * (z - zB2) if z > zB2 else 0
    return abs(M)


casos = {"nominal (BEP)": (F_R_fp_nom, F_R_op_nom), "projeto kR,tot=0,15": (F_R_fp_des, F_R_op_des)}
res_rad = {}
for nome, (Ff, Fo) in casos.items():
    F_fp = Ff + m_fp * (G_bal * w + a_lat)
    F_op = Fo + m_op * (G_bal * w + a_lat)
    F_tb = m_tb * (G_bal * w + a_lat)
    res_rad[nome] = (F_fp, F_op, F_tb, *reacoes(F_fp, F_op, F_tb))

# ----------------------------------------------------------------- 6. diâmetro mínimo
Se, Sy, Kf, SF, tau_adm = 300e6, 900e6, 2.0, 1.5, 150e6
R1d, R2d, loadsd = res_rad["projeto kR,tot=0,15"][3:]
secoes = [("FP-B1 (z=24)", 24, "FP-B1"), ("B1 centro (z=40)", 40, "FP-B1"),
          ("Sob selos IP (z=70)", 70, "B1-OP"), ("Sob OP (z=110)", 110, "B1-OP"),
          ("S6 (z=143)", 143, "OP-T"), ("B2 (z=158)", 158, "OP-T"),
          ("Montagem turbina (z=181)", 181, "OP-T")]
tab_d = []
for nome, zmm, trecho in secoes:
    M = M_em(zmm * mm, R1d, R2d, loadsd); T = T_des[trecho]
    d_fad = (32 * SF / np.pi * np.sqrt((Kf * M / Se) ** 2 + 0.75 * (T / Sy) ** 2)) ** (1 / 3)
    d_tor = (16 * T / (np.pi * tau_adm)) ** (1 / 3)
    d_real = next(d for z0, z1, d in eixo_seg if z0 <= zmm < z1) * mm
    tab_d.append((nome, M, T, d_tor, d_fad, d_real))

# ----------------------------------------------------------------- 7. mancais (C de catálogo = ordem de grandeza)
C_B1, C_B2 = 1.62 * 10.0e3, 25.0e3        # par DB classe 7004 (25°) ; rolos classe NU204
Fa = abs(F_ax)
mancais = {}
for nome, v in res_rad.items():
    R1, R2 = v[3], v[4]
    P1 = 0.67 * R1 + 0.87 * Fa if Fa / max(R1, 1) > 0.68 else R1   # ISO 281, par DB 25°
    L1 = (C_B1 / P1) ** 3 * 1e6 / n                                 # min
    L2 = (C_B2 / R2) ** (10 / 3) * 1e6 / n
    mancais[nome] = dict(R_B1=R1, R_B2=R2, P_B1=P1, P_B2=R2, L10_B1_min=L1, L10_B2_min=L2)
Pd = 1.0e3                                  # ~1 kW por rolamento a DN 1e6 (premissa)
mcool_B1, mcool_B2 = 2 * Pd / (2000 * 15), Pd / (2750 * 10)


# ----------------------------------------------------------------- 8. selos
def vaz_anular(d, c, dp, rho, Cd=0.6):
    return rho * Cd * np.pi * d * c * np.sqrt(2 * dp / rho)


selos_def = [("S1 FP traseira→B1", "anel flutuante", d_S1, p_B1 - p_in, rho_f),
             ("S2 primário Jet A", "face (carbono × carbeto)", d_IP, p_B1 - p_drain, None),
             ("S3/S4 intermediários", "circunferencial segmentado, purga He", d_IP, p_purge - p_drain, None),
             ("S5 primário HTP", "face (materiais classe HTP)", d_IP, p_in - p_drain, None),
             ("S6 traseira OP↔buffer B2", "anel flutuante multiestágio", d_S6, p_buf - p1_ox, rho_ox),
             ("S7 buffer B2→turbina", "anel flutuante + labirinto", d_S7, p_buf - p2_T, rho_ox)]
tab_selos = [(nm, tp, d, dp, np.pi * d * n / 60, vaz_anular(d, 15e-6, dp, r) if r else None)
             for nm, tp, d, dp, r in selos_def]


# ----------------------------------------------------------------- 9. 1ª crítica (FE Euler-Bernoulli + giroscópico)
def rotor_FE(kb1, kb2, Omega, segs=None):
    segs = segs or eixo_seg
    zs = sorted(set([z for s in segs for z in s[:2]] +
                    [round(p.props()[1] * 1e3) for p in pecas] + [34, 46, 158, 10, 70, 120]))
    zs = np.array(zs, float) * mm
    N = len(zs); nd = 4 * N                       # [u, β, v, γ] por nó
    K = np.zeros((nd, nd)); M = np.zeros((nd, nd)); G = np.zeros((nd, nd))

    def dseg(zm):
        return next(d for z0, z1, d in segs if z0 * mm <= zm < z1 * mm + 1e-9) * mm
    for e in range(N - 1):
        L = zs[e + 1] - zs[e]; d = dseg(0.5 * (zs[e] + zs[e + 1]))
        I = np.pi * d**4 / 64; A = np.pi * d**2 / 4
        ke = E_sh * I / L**3 * np.array([[12, 6 * L, -12, 6 * L], [6 * L, 4 * L * L, -6 * L, 2 * L * L],
                                         [-12, -6 * L, 12, -6 * L], [6 * L, 2 * L * L, -6 * L, 4 * L * L]])
        me = rho_sh * A * L / 420 * np.array([[156, 22 * L, 54, -13 * L], [22 * L, 4 * L * L, 13 * L, -3 * L * L],
                                              [54, 13 * L, 156, -22 * L], [-13 * L, -3 * L * L, -22 * L, 4 * L * L]])
        for off in (0, 2):
            idx = [4 * e + off, 4 * e + off + 1, 4 * (e + 1) + off, 4 * (e + 1) + off + 1]
            K[np.ix_(idx, idx)] += ke; M[np.ix_(idx, idx)] += me

    def near(z):
        return int(np.argmin(abs(zs - z)))
    for p in pecas:
        m, zc, Ip, Id = p.props(); i = near(zc)
        M[4 * i, 4 * i] += m; M[4 * i + 2, 4 * i + 2] += m
        M[4 * i + 1, 4 * i + 1] += Id; M[4 * i + 3, 4 * i + 3] += Id
        G[4 * i + 1, 4 * i + 3] += Ip; G[4 * i + 3, 4 * i + 1] -= Ip
    for zb, kb in ((zB1a, kb1), (zB1b, kb1), (zB2, kb2)):
        i = near(zb); K[4 * i, 4 * i] += kb; K[4 * i + 2, 4 * i + 2] += kb
    Minv = np.linalg.inv(M)
    A = np.block([[np.zeros((nd, nd)), np.eye(nd)], [-Minv @ K, -Minv @ (Omega * G)]])
    lam, vec = np.linalg.eig(A)
    out = []
    for l, v in zip(lam, vec.T):
        if l.imag <= 1e-6:
            continue
        U, V = v[:nd][0::4], v[:nd][2::4]
        j = np.argmax(abs(U) + abs(V))
        out.append((l.imag, np.imag(np.conj(U[j]) * V[j]) < 0))   # True = forward
    return sorted(out)


def critica1(kb1, kb2, segs=None):
    Om = np.linspace(500, 2.6 * w, 160)
    f1 = np.array([[f for f, fw in rotor_FE(kb1, kb2, O, segs) if fw][0] for O in Om])
    s = f1 - Om
    i = np.where(np.sign(s[:-1]) != np.sign(s[1:]))[0]
    if len(i) == 0:
        return float("nan")
    i = i[0]
    return (Om[i] - s[i] * (Om[i + 1] - Om[i]) / (s[i + 1] - s[i])) * 60 / (2 * np.pi)


kb_sweep = [(20e6, 40e6), (35e6, 70e6), (50e6, 100e6), (100e6, 200e6), (200e6, 400e6), (1e11, 1e11)]
crit = [(k1, k2, critica1(k1, k2)) for k1, k2 in kb_sweep]
# sensibilidade: diâmetro sob a OP
crit_dOP = []
for dop in (20, 22, 24):
    segs = [(a, b, (dop if (a, b) == (90, 136) else d)) for a, b, d in eixo_seg]
    crit_dOP.append((dop, critica1(50e6, 100e6, segs)))
f0 = [f / (2 * np.pi) for f, _ in rotor_FE(50e6, 100e6, 0.0)][:6:2]

# ----------------------------------------------------------------- 10. totais e saídas
m_sh, z_sh, Ip_sh = eixo_props()
props = [(p, *p.props()) for p in pecas]
m_tot = sum(x[1] for x in props) + m_sh
z_cg = (sum(x[1] * x[2] for x in props) + m_sh * z_sh) / m_tot
Ip_tot = sum(x[3] for x in props) + Ip_sh
Id_tot = sum(x[4] + x[1] * (x[2] - z_cg) ** 2 for x in props)
Id_tot += sum(rho_sh * np.pi * (d * mm) ** 2 / 4 * (z1 - z0) * mm *
              (((z1 - z0) * mm) ** 2 / 12 + (d * mm / 2) ** 2 / 4 + ((z0 + z1) / 2 * mm - z_cg) ** 2)
              for z0, z1, d in eixo_seg)

if __name__ == "__main__":
    print(f"n = {n:.0f} rpm, ω = {w:.1f} rad/s")
    print(f"Potências: OP {P_OP/1e3:.1f} kW, FP {P_FP/1e3:.1f} kW, turbina req {P_T/1e3:.1f} kW, "
          f"perdas mec {P_loss/1e3:.1f} kW, turbina disponível {P_disp/1e3:.0f} kW")
    print(f"Torques nominais: FP {T_f:.2f}, OP {T_o:.2f}, T {T_T:.2f} N·m; disponível {T_disp:.1f} N·m")
    print("Torques de projeto:", {k: round(v, 1) for k, v in T_des.items()})
    print(f"\nOP: D_t {Dt_in*1e3:.1f} mm, cubo {d_hub_ind*1e3:.0f} mm, p1 impeller {p1_ox/1e5:.2f} bar, "
          f"Δp_La {dpLa_ox/1e5:.1f} bar, anéis Ø{d_ring_ox*1e3:.0f}")
    print("\nMassas/inércias (Ip, Id em kg·mm², Id no CG da peça):")
    for p, m, zc, Ip, Id in props:
        print(f"  {p.nome:34s} {p.mat:14s} m={m*1e3:7.1f} g z={zc*1e3:6.1f} mm Ip={Ip*1e6:7.2f} Id={Id*1e6:7.2f}  [{p.fonte}]")
    print(f"  {'Eixo (maciço)':34s} {'IN718':14s} m={m_sh*1e3:7.1f} g z={z_sh*1e3:6.1f} mm Ip={Ip_sh*1e6:7.2f}")
    print(f"  ROTOR TOTAL m={m_tot*1e3:.0f} g z_CG={z_cg*1e3:.1f} mm Ip={Ip_tot*1e6:.1f} Id(CG rotor)={Id_tot*1e6:.0f} kg·mm²")
    print(f"\nEmpuxo axial OP: sem balanceamento {F_unbal_ox:.0f} N, residual {F_res_ox():.0f} N (F_I {FI_ox:.0f}); FP (04) {F_ax_fp:+.0f} N em z")
    for nome, d, pl, pr, F in ledger():
        print(f"    {nome:28s} d={d*1e3:5.1f} mm {pl/1e5:6.1f}→{pr/1e5:6.1f} bar  F_z={F:+8.0f} N")
    print(f"  F_net = {F_ax:+.0f} N (+z = p/ turbina); resíduo 0,10/0,20: {F_ax_faixa[0]:+.0f}/{F_ax_faixa[1]:+.0f}; "
          f"p_buf 145/165: {F_ax_pbuf[0]:+.0f}/{F_ax_pbuf[1]:+.0f}")
    print(f"  Se o escape da turbina fosse −z (leitura da 05): F_net = {F_ax_turb_neg:+.0f} N")
    print()
    for nome, v in res_rad.items():
        print(f"  {nome}: F_FP {v[0]:.0f} F_OP {v[1]:.0f} F_T {v[2]:.0f} N → R_B1 {v[3]:.0f} R_B2 {v[4]:.0f} N")
    print("\nDiâmetros:")
    for nome, M, T, dt, df, dr in tab_d:
        print(f"  {nome:26s} M={M:6.1f} T={T:6.1f} N·m d_tor={dt*1e3:5.1f} d_fad={df*1e3:5.1f} adotado={dr*1e3:4.0f} mm")
    print("\nMancais:")
    for nome, v in mancais.items():
        print(f"  {nome}: " + ", ".join(f"{k} {x:.0f}" for k, x in v.items()))
    print(f"  DN = {20*n:.2e}; refrig. B1 {mcool_B1*1e3:.0f} g/s Jet A, B2 {mcool_B2*1e3:.0f} g/s HTP")
    print("\nSelos:")
    for nm, tp, d, dp, u, mv in tab_selos:
        vz = f"{mv*1e3:6.0f} g/s" if mv else "     —"
        print(f"  {nm:28s} {tp:38s} d={d*1e3:4.0f} Δp={dp/1e5:6.1f} bar u={u:5.1f} m/s vaz={vz}")
    print("\n1ª crítica forward (c/ giroscópico):")
    for k1, k2, c in crit:
        print(f"  k_B1={k1/1e6:5.0f} k_B2={k2/1e6:5.0f} MN/m → {c:7.0f} rpm ({c/n:.2f}·n)")
    print("  Sensib. d sob OP (k 50/100):", [(d, round(c), round(c / n, 2)) for d, c in crit_dOP])
    print("  f naturais não girando (50/100) [Hz]:", [round(f) for f in f0])

    # --- arquivos
    with open(os.path.join(AQUI, "etapa5_rotor_massas.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(["peca", "material", "m_kg", "z_cg_mm", "Ip_kgm2", "Id_kgm2_no_cg", "fonte"])
        for p, m, zc, Ip, Id in props:
            wr.writerow([p.nome, p.mat, f"{m:.5f}", f"{zc*1e3:.1f}", f"{Ip:.4e}", f"{Id:.4e}", p.fonte])
        wr.writerow(["Eixo (maciço, distribuído)", "IN718", f"{m_sh:.5f}", f"{z_sh*1e3:.1f}", f"{Ip_sh:.4e}", "", "este"])
        wr.writerow(["ROTOR TOTAL", "", f"{m_tot:.5f}", f"{z_cg*1e3:.1f}", f"{Ip_tot:.4e}", f"{Id_tot:.4e}", "Id no CG do rotor"])
    with open(os.path.join(AQUI, "etapa5_eixo_segmentos.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(["z_ini_mm", "z_fim_mm", "d_mm", "material", "E_Pa", "rho_kgm3"])
        for z0, z1, d in eixo_seg:
            wr.writerow([z0, z1, d, "IN718", E_sh, rho_sh])
    with open(os.path.join(AQUI, "etapa5_criticas.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(["k_B1_N_m", "k_B2_N_m", "n_crit1_rpm", "n_crit1_sobre_n"])
        for k1, k2, c in crit:
            wr.writerow([f"{k1:.3e}", f"{k2:.3e}", f"{c:.0f}", f"{c/n:.3f}"])
    out = {
        "meta": {"projeto": "turbopump-design", "etapa": "5 - eixo, mancais, selos", "revisao": 2,
                 "z_ref": "z=0 no nariz da FP, +z para a turbina", "unidades": "SI (z em mm)"},
        "operacao": {"n_rpm": n, "P_OP_W": P_OP, "P_FP_W": P_FP, "P_turbina_req_W": P_T,
                     "P_turbina_disp_W": P_disp, "torques_nominais_Nm": {"FP": T_f, "OP": T_o, "turbina": T_T},
                     "torques_projeto_Nm": T_des},
        "eixo": {"segmentos_mm": eixo_seg, "material": "IN718", "E_Pa": E_sh, "rho": rho_sh,
                 "secoes": [dict(secao=a, M_Nm=b, T_Nm=c, d_tor_mm=d * 1e3, d_fad_mm=e * 1e3, d_adot_mm=f * 1e3)
                            for a, b, c, d, e, f in tab_d]},
        "mancais": {"B1": {"tipo": "par contato angular 25 graus DB, classe 7004, hibrido", "z_fileiras_mm": [34, 46],
                           "bore_mm": 20, "refrigeracao": "Jet A", "vazao_kg_s": mcool_B1},
                    "B2": {"tipo": "rolos cilindricos classe NU204, hibrido", "z_mm": 158, "bore_mm": 20,
                           "refrigeracao": "HTP buffer 155 bar", "vazao_kg_s": mcool_B2},
                    "DN": 20 * n, "cargas": mancais},
        "empuxo_axial_N": {"liquido": F_ax, "faixa_residuo": F_ax_faixa, "faixa_pbuf": F_ax_pbuf,
                           "se_escape_turbina_menos_z": F_ax_turb_neg,
                           "termos": [dict(item=a, d_mm=b * 1e3, p_esq_bar=c / 1e5, p_dir_bar=d / 1e5, F_z_N=e)
                                      for a, b, c, d, e in ledger()],
                           "OP_sem_balanceamento": F_unbal_ox, "OP_residual": F_res_ox(), "FP_04": F_ax_fp},
        "empuxo_radial": {k: dict(F_FP=v[0], F_OP=v[1], F_T=v[2], R_B1=v[3], R_B2=v[4]) for k, v in res_rad.items()},
        "selos": [dict(selo=a, tipo=b, d_mm=c * 1e3, dp_bar=d / 1e5, u_ms=e, vazamento_kg_s=f)
                  for a, b, c, d, e, f in tab_selos],
        "rotor": {"pecas": [dict(nome=p.nome, material=p.mat, m_kg=m, z_cg_mm=zc * 1e3, Ip_kgm2=Ip, Id_kgm2=Id, fonte=p.fonte)
                            for p, m, zc, Ip, Id in props],
                  "eixo": dict(m_kg=m_sh, z_cg_mm=z_sh * 1e3, Ip_kgm2=Ip_sh),
                  "total": dict(m_kg=m_tot, z_cg_mm=z_cg * 1e3, Ip_kgm2=Ip_tot, Id_cg_kgm2=Id_tot),
                  "mancais_z_mm": {"B1": [34, 46], "B2": 158}},
        "critica": {"k_sweep": [dict(k_B1=a, k_B2=b, n_c_rpm=c) for a, b, c in crit],
                    "sens_d_sob_OP_k50_100": crit_dOP, "f_nao_girando_Hz": f0},
    }
    with open(os.path.join(AQUI, "etapa5_eixo_mancais.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=float)
