"""
turbopump-design - Etapa 2 (rev. 2): bomba de oxidante (HTP 90 %) - meanline
Indutor (NASA SP-8052) + impeller radial (Gulich cap. 7, Tab. 7.1) + voluta (Gulich 7.8)

rev. 2: premissas da rev. 1 trocadas pelos resultados reais das etapas 0, 1 (rev. 2) e 5:
  - eixo sob a OP IN718 D24 mm, cubo do indutor 28 mm (nu ~0,61)  [etapa 1 rev. 2 / etapa 5]
  - criterio de cavitacao K_op >= 0,025 alem de F_NPSH = 1,2       [etapa 1 rev. 2]
  - ponta do indutor afunilada na saida p/ d1/d2 <= 0,70            [etapa 1 rev. 2, Huzel p.182]
  - vazamentos do buffer do mancal B2 (S6 recircula p/ succao, S7 p/ turbina) [etapa 5 sec. 7]
  - anel de desgaste traseiro + furos de balanceamento obrigatorios [etapa 5 sec. 5.2]
  - voluta dupla (180 deg) como baseline; simples mantida como alternativa [etapa 5 sec. 5.1]

Unidades SI. Saidas: etapa2_bomba_htp.json (geometria p/ CAD) e etapa2_cfturbo.csv
Uso: python etapa2_bomba_htp.py
"""
import csv, json, math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

g, pi = 9.80665, math.pi

# ============================================================ inputs (etapas anteriores)
rho, pv, mu = 1385.0, 500.0, 1.1e-3            # etapa 0 (HTP 90 % a 300 K)
mdot = 17.5
p_in, p_out = 5e5, 235e5                       # requisitos
n = 55000.0                                    # etapa 1 rev. 2
w = n*pi/30
F_NPSH, K_lim = 1.20, 0.025                    # etapa 1 rev. 2
d_shaft = 0.024                                # etapa 1 rev. 2 (IN718 macico sob a OP)
d_hub_ind = 0.028                              # etapa 1 rev. 2 / etapa 5 sec. 10
m_S6, m_S7 = 0.120, 0.050                      # etapa 5 sec. 7 [kg/s]: buffer alimentado pela descarga

Q = mdot/rho                                   # vazao util entregue ao motor
Q_S6, Q_S7 = m_S6/rho, m_S7/rho
Q_ind = Q + Q_S6                               # S6 volta a succao da OP -> passa pelo indutor
Q_Le = Q + Q_S6 + Q_S7                         # sai pela voluta (buffer tira da descarga)
H = (p_out - p_in)/(rho*g)
NPSHA = (p_in - pv)/(rho*g)
NPSH3_adm = NPSHA/F_NPSH
nq = n*Q**0.5/H**0.75
nss_req = n*Q_ind**0.5/NPSH3_adm**0.75

# ============================================================ 1. INDUTOR (SP-8052 2.1.3 / 3.1.3)
def inducer_state(D, dh, Qi=Q_ind):
    ut = w*D/2
    cm = Qi/(pi/4*(D**2 - dh**2))
    phi = cm/ut
    tau = 2*g*NPSH3_adm/ut**2                  # SP-8052 eq. 2
    K = (tau - phi**2)/(1 + phi**2)
    return dict(D=D, nu=dh/D, ut=ut, cm=cm, phi=phi, tau=tau, K=K)

ind_opt = inducer_state(minimize_scalar(lambda D: -inducer_state(D, d_hub_ind)['K'],
                                        bounds=(0.03, 0.08), method='bounded').x, d_hub_ind)
D_t = math.ceil(ind_opt['D']*2000)/2000        # arredonda p/ cima (0,5 mm), curva plana no otimo
ind = inducer_state(D_t, d_hub_ind)
K_brum = 2*ind['phi']**2/(1 - 2*ind['phi']**2) # SP-8052 eq. 5

z_ind, sol_t = 3, 2.5
t_ind_tip, t_ind_hub, clr_ind = 0.8e-3, 1.6e-3, 0.20e-3
beta1_flow_t = math.degrees(math.atan(ind['phi']))
beta1B_t = beta1_flow_t/(1 - 0.425)            # SP-8052 3.1.9 (alpha/beta = 0,425)
lead = 2*pi*(D_t/2)*math.tan(math.radians(beta1B_t))      # SP-8052 eq. 31
beta1B_hub = math.degrees(math.atan(lead/(pi*d_hub_ind)))
chord_t = sol_t*pi*D_t/z_ind
L_ax_ind = chord_t*math.sin(math.radians(beta1B_t))
L_const_tip = lead/z_ind                       # ponta constante por 1 passo axial (SP-8052 2.1.3)

# ============================================================ 2. IMPELLER (Gulich Tab. 7.1)
eta_h, eta_ind = 0.83, 0.70
z, e_bl, beta2B = 6, 1.5e-3, 25.0
d1 = 0.042                                     # olho = saida afunilada do indutor
dn = d_hub_ind                                 # cubo continuo 28 mm
D_t_exit = d1
b2s = 0.017 + 0.262*(nq/100) - 0.08*(nq/100)**2 + 0.0093*(nq/100)**3   # Gulich eq. 7.1
nss_imp, F_imp = 200.0, 1.30                   # Gulich Tab. D6.1

def leakage(H_th, c2, c1, d2):
    """anel de desgaste (labirinto), Gulich cap. 3.6 simplificado; mesmo anel na frente e atras"""
    s, mu_sp = 0.08e-3, 0.45
    d_sp = d1 + 2*(1.5e-3 + 1.0e-3)
    u_sp, u2 = w*d_sp/2, w*d2/2
    H_p = H_th - (c2**2 - c1**2)/(2*g)
    H_sp = H_p - (u2**2 - u_sp**2)/(8*g)
    return mu_sp*pi*d_sp*s*(2*g*H_sp)**0.5, d_sp, H_sp

def impeller(Q_La, d2, rcu):
    b2, u2 = b2s*d2, w*d2/2
    tau2 = 1/(1 - z*e_bl/(pi*d2*math.sin(math.radians(beta2B))))         # T3.2.3
    eps_lim = math.exp(-8.16*math.sin(math.radians(beta2B))/z)           # T3.2.4
    d1ms = ((d1**2 + dn**2)/2)**0.5/d2
    kw = 1.0 if d1ms <= eps_lim else 1 - ((d1ms - eps_lim)/(1 - eps_lim))**3
    gamma = 0.98*(1 - math.sin(math.radians(beta2B))**0.5/z**0.7)*kw    # T3.2.6
    c2m = Q_La/(pi*d2*b2)
    c2u = u2*(gamma - c2m*tau2/(u2*math.tan(math.radians(beta2B))))     # T3.2.7
    H_th = (u2*c2u - w*rcu)/g                                            # Euler c/ pre-rotacao
    return dict(b2=b2, u2=u2, tau2=tau2, eps_lim=eps_lim, d1ms=d1ms, kw=kw, gamma=gamma,
                c2m=c2m, c2u=c2u, H_th=H_th, H=eta_h*H_th)

# iteracao acoplada: vazamentos (frente + furos de balanceamento) <-> H_ind <-> d2
Q_sp = Q_E = 0.03*Q
for it in range(50):
    Q_La = Q_Le + Q_sp + Q_E
    NPSH3_imp = (n*Q_La**0.5/nss_imp)**(4/3)
    H_ind = F_imp*NPSH3_imp - NPSHA
    rcu = g*H_ind/(eta_ind*w)                  # vortice livre na saida do indutor
    H_imp = H - H_ind
    d2 = brentq(lambda d: impeller(Q_La, d, rcu)['H'] - H_imp, 0.03, 0.15)
    imp = impeller(Q_La, d2, rcu)
    c2 = math.hypot(imp['c2m'], imp['c2u'])
    c1m = Q_La/(pi/4*(d1**2 - dn**2))
    c1u = rcu/(d1/2)
    q_new, d_sp, H_sp = leakage(imp['H_th'], c2, math.hypot(c1m, c1u), d2)
    if abs(q_new - Q_sp) < 1e-9:
        break
    Q_sp = Q_E = q_new
Q_La = Q_Le + Q_sp + Q_E
b2, u2 = imp['b2'], imp['u2']
psi = 2*g*H_imp/u2**2
psi_ref = 1.21*math.exp(-0.77*nq/100)          # Gulich eq. 3.26
eta_v = Q/Q_La

# indutor: saida
cm_ind2 = Q_ind/(pi/4*(D_t_exit**2 - d_hub_ind**2))
u_t2 = w*D_t_exit/2
cu2t = rcu/(D_t_exit/2)
beta2_flow_t = math.degrees(math.atan(cm_ind2/(u_t2 - cu2t)))
beta2B_t = math.degrees(math.atan(lead/(pi*D_t_exit)))  # placa plana, passo constante
dev_ind = beta2B_t - beta2_flow_t
psi_ind = g*H_ind/ind['ut']**2
P_ind = rho*g*Q_ind*H_ind/eta_ind

# impeller: entrada e saida
u1 = w*d1/2
tau1 = 1/(1 - z*e_bl/(pi*d1*math.sin(math.radians(15))))
beta1_flow = math.degrees(math.atan(c1m*tau1/(u1 - c1u)))
i1 = 2.0
beta1B = beta1_flow + i1
beta1B_i = math.degrees(math.atan(c1m*tau1/(w*dn/2 - rcu/(dn/2)))) + i1
w1 = math.hypot(c1m, u1 - c1u)
w2u = u2 - imp['c2u']
w2 = math.hypot(imp['c2m'], w2u)
beta2_flow = math.degrees(math.atan(imp['c2m']/w2u))
alpha2 = math.degrees(math.atan(imp['c2m']/imp['c2u']))
dev = beta2B - beta2_flow

# atrito de disco (Daily & Nece regime IV; Gulich Tab. 3.6), 2 faces
r2 = d2/2
Re = w*r2**2/(mu/rho)
cM = 0.051*0.03**0.1/Re**0.2
P_RR = 2*0.5*cM*rho*w**2*r2**5*w
P_imp = rho*g*Q_La*imp['H_th']
P_shaft = P_imp + P_ind + P_RR
P_h = rho*g*Q*H                                 # potencia util (vazao entregue ao motor)
eta_pump = P_h/P_shaft
T_OP = P_shaft/w

# ============================================================ 3. VOLUTA (Gulich 7.8)
dz = 1.07*d2
e3 = max(0.02*d2, 1.5e-3)
b3 = 2.0*b2
r2c2u = r2*imp['c2u']
rz_ = dz/2 + e3/2
def throat_d(Qpart):
    """secao circular tangente a rz': Q = r2 c2u * 2pi (rc - sqrt(rc^2 - (d/2)^2))  (Gulich eq. 3.15)"""
    f = lambda d: r2c2u*2*pi*((rz_ + d/2) - ((rz_ + d/2)**2 - (d/2)**2)**0.5) - Qpart
    return brentq(f, 1e-4, 0.1)

def volute(z_Le, f_Q):
    eps_sp = 360.0/z_Le
    Qd = f_Q*Q_Le
    d3q = throat_d(Qd/z_Le)                    # Gulich eq. 7.24 (cada voluta parcial)
    A3q = pi*d3q**2/4
    eps = np.arange(0, eps_sp + 1e-9, 30.0)
    d_eps = d3q*np.sqrt(eps/eps_sp)            # velocidade constante: A ~ eps (Gulich eq. 7.26-7.27)
    return dict(z_Le=z_Le, f_Q=f_Q, d3q=d3q, A3q=A3q, c3q=Qd/z_Le/A3q, eps=eps, d=d_eps, r_out=rz_ + d_eps)

vol_single = volute(1, 1.00)
vol_double = volute(2, 1.10)                   # Gulich 7.8.1: duplas a n_q baixo -> Q_Le (1,05-1,25) Q
c3u = imp['c2u']*d2/dz
c3m = Q_Le/(pi*dz*b3)
alpha3B = math.degrees(math.atan(c3m/c3u))    # Gulich eq. 3.16-3.19, i3 = 0
d_dis, half_angle = 0.025, 5.0
d_dis_A = 2*vol_double['A3q']                  # duas gargantas -> soma de areas no bocal
d_eq_double = (4*d_dis_A/pi)**0.5
L_dif = (d_dis - d_eq_double)/(2*math.tan(math.radians(half_angle)))
c_dis = Q_Le/(pi/4*d_dis**2)

# empuxo radial (Gulich eq. 9.6; Fig. 9.27/9.28; 9.3.10 p/ dupla)
b2tot = b2 + 2*1.5e-3
x = nq
kR100 = 4.562e-5*x**2 - 1.894e-3*x + 3.179e-02
kR0 = 3.730e-08*x**4 - 7.274e-06*x**3 + 3.610e-04*x**2 + 2.041e-03*x + 3.944e-02
kR_dyn = 0.03                                  # Gulich Tab. 9.4 (q* = 1: 0,01-0,05)
kR_double = 0.15*kR0                           # Gulich 9.3.10 item 1: 10-20 % do shut-off da simples
F0 = rho*g*H*d2*b2tot
loads = dict(
    single=dict(BEP=(kR100 + kR_dyn)*F0, shutoff=(kR0 + kR_dyn)*F0),
    double=dict(BEP=(kR_double + kR_dyn)*F0, shutoff=(kR_double + kR_dyn)*F0),
    design_kR015=0.15*F0)                      # Gulich 9.3 item 13

# ============================================================ 4. massas e inercias (Al 6061-T6)
rho_al = 2700.0
def ring(ro, ri, L, rho_m=rho_al):
    m = rho_m*pi*(ro**2 - ri**2)*L
    return m, 0.5*m*(ro**2 + ri**2), 0.25*m*(ro**2 + ri**2) + m*L**2/12
t_back, t_front, L_hub = 2.5e-3, 1.5e-3, 0.018
imp_parts = [ring(dn/2, d_shaft/2, L_hub),                 # cubo (bore 24)
             ring(r2, dn/2, t_back),                        # disco traseiro
             ring(r2, d_sp/2, t_front),                     # shroud
             ring(d_sp/2 + 1.0e-3, d_sp/2 - 1.5e-3, 6e-3)]  # anel frontal (labirinto)
L_bl = (r2 - d1/2)/math.sin(math.radians(0.5*(beta1B + beta2B)))
m_bl = rho_al*z*L_bl*0.5*(b2 + (d1 - dn)/2)*e_bl
r_bl = 0.5*(r2 + d1/2)
imp_parts.append((m_bl, m_bl*r_bl**2, 0.5*m_bl*r_bl**2))
ind_parts = [ring(d_hub_ind/2, d_shaft/2, L_ax_ind)]
D_tm = 0.5*(D_t + D_t_exit)
h_bl = (D_tm - d_hub_ind)/2
r_ib = 0.5*(D_tm/2 + d_hub_ind/2)
m_ib = rho_al*z_ind*chord_t*h_bl*0.5*(t_ind_tip + t_ind_hub)*0.9
ind_parts.append((m_ib, m_ib*(r_ib**2 + h_bl**2/12), 0.5*m_ib*r_ib**2 + m_ib*L_ax_ind**2/12))
S = lambda parts, i: sum(p[i] for p in parts)
m_imp, Ip_imp, Id_imp = S(imp_parts, 0), S(imp_parts, 1), S(imp_parts, 2)
m_ind, Ip_ind, Id_ind = S(ind_parts, 0), S(ind_parts, 1), S(ind_parts, 2)
# fluido arrastado nos canais do impeller (aprox.: volume entre discos d1..d2 x b medio)
m_fl = rho*pi*(r2**2 - (d1/2)**2)*0.5*(b2 + (d1 - dn)/2)*0.9
Ip_fl = 0.5*m_fl*(r2**2 + (d1/2)**2)

# ============================================================ saida
R = lambda v, k=3: round(float(v), k)
def vol_json(v):
    return {"z_Le": v['z_Le'], "Q_design_factor": v['f_Q'], "d3q_mm": R(v['d3q']*1e3, 2), "A3q_mm2": R(v['A3q']*1e6, 1),
            "c3q": R(v['c3q'], 2), "c3q_c2": R(v['c3q']/c2, 3),
            "sections": [{"eps_deg": int(e), "d_mm": R(d*1e3, 2), "r_out_mm": R(ro*1e3, 2)}
                         for e, d, ro in zip(v['eps'], v['d'], v['r_out'])]}
out = {
  "meta": {"projeto": "turbopump-design", "etapa": "2 - bomba de oxidante (HTP 90%)", "revisao": 2,
           "unidades": "SI; mm e graus onde indicado"},
  "ponto": {"n_rpm": n, "Q_util_m3s": R(Q, 6), "Q_inducer_m3s": R(Q_ind, 6), "Q_volute_m3s": R(Q_Le, 6),
            "H_m": R(H, 1), "NPSHA_m": R(NPSHA, 2), "NPSH3_adm_m": R(NPSH3_adm, 2),
            "nq": R(nq, 2), "nss_req": R(nss_req, 1), "S_US": R(nss_req/0.0194, 0), "rho": rho},
  "inducer": {"z": z_ind, "D_tip_inlet_mm": R(D_t*1e3, 2), "D_tip_exit_mm": R(D_t_exit*1e3, 2),
              "L_const_tip_mm": R(L_const_tip*1e3, 1), "d_hub_mm": R(d_hub_ind*1e3, 2), "bore_mm": d_shaft*1e3,
              "nu_in": R(ind['nu']), "phi_tip": R(ind['phi'], 4), "u_tip": R(ind['ut'], 1), "cm_in": R(ind['cm'], 2),
              "tau": R(ind['tau'], 4), "K_op": R(ind['K'], 4), "K_lim": K_lim, "K_brumfield": R(K_brum, 4),
              "D_opt_brumfield_mm": R(ind_opt['D']*1e3, 2),
              "beta1_flow_tip_deg": R(beta1_flow_t, 2), "beta1B_tip_deg": R(beta1B_t, 2),
              "incidence_tip_deg": R(beta1B_t - beta1_flow_t, 2), "beta1B_hub_deg": R(beta1B_hub, 2),
              "lead_mm": R(lead*1e3, 2), "beta2B_tip_exit_deg": R(beta2B_t, 2),
              "beta2_flow_tip_exit_deg": R(beta2_flow_t, 2), "deviation_tip_exit_deg": R(dev_ind, 2),
              "solidity_tip": sol_t, "chord_tip_mm": R(chord_t*1e3, 1), "L_axial_mm": R(L_ax_ind*1e3, 1),
              "wrap_deg": R(math.degrees(chord_t*math.cos(math.radians(beta1B_t))/(D_t/2)), 0),
              "t_tip_mm": t_ind_tip*1e3, "t_hub_mm": t_ind_hub*1e3, "tip_clearance_mm": clr_ind*1e3,
              "H_m": R(H_ind, 1), "psi_NASA": R(psi_ind, 4), "eta": eta_ind, "P_kW": R(P_ind/1e3, 1),
              "rcu_exit_m2s": R(rcu, 4)},
  "impeller": {"z": z, "d2_mm": R(d2*1e3, 2), "b2_mm": R(b2*1e3, 2), "b2_star": R(b2s, 4), "d1_mm": R(d1*1e3, 2),
               "dn_mm": R(dn*1e3, 2), "bore_mm": d_shaft*1e3, "d1_d2": R(d1/d2, 3), "e_blade_mm": e_bl*1e3,
               "beta1B_shroud_deg": R(beta1B, 2), "beta1B_hub_deg": R(beta1B_i, 2), "beta1_flow_deg": R(beta1_flow, 2),
               "i1_deg": i1, "beta2B_deg": beta2B, "beta2_flow_deg": R(beta2_flow, 2), "deviation_deg": R(dev, 2),
               "alpha2_deg": R(alpha2, 2), "slip_factor": R(imp['gamma'], 4), "kw": R(imp['kw'], 3), "tau2": R(imp['tau2'], 4),
               "psi": R(psi, 4), "psi_ref_Gulich_3_26": R(psi_ref, 4), "phi2": R(imp['c2m']/u2, 4),
               "u1": R(u1, 1), "u2": R(u2, 1), "c1m": R(c1m, 2), "c1u": R(c1u, 2), "w1": R(w1, 1),
               "c2m": R(imp['c2m'], 2), "c2u": R(imp['c2u'], 2), "c2": R(c2, 1), "w2": R(w2, 1), "w2_w1": R(w2/w1, 3),
               "H_m": R(H_imp, 1), "H_th_m": R(imp['H_th'], 1), "eta_h": eta_h,
               "Q_La_m3s": R(Q_La, 6), "Q_front_ring_m3s": R(Q_sp, 6), "Q_balance_holes_m3s": R(Q_E, 6),
               "eta_v": R(eta_v, 4), "d_wear_ring_mm": R(d_sp*1e3, 2), "wear_ring_clearance_mm": 0.08,
               "rear_wear_ring_mm": R(d_sp*1e3, 2), "NPSH3_imp_m": R(NPSH3_imp, 1), "NPSHA_imp_m": R(NPSHA + H_ind, 1),
               "t_back_mm": t_back*1e3, "t_front_mm": t_front*1e3, "L_hub_mm": L_hub*1e3},
  "volute": {"baseline": "dupla 2x180 deg, secao circular, velocidade constante",
             "d_cutwater_mm": R(dz*1e3, 2), "e3_mm": R(e3*1e3, 2), "b3_mm": R(b3*1e3, 2), "alpha3B_deg": R(alpha3B, 2),
             "double": vol_json(vol_double), "single_alternative": vol_json(vol_single),
             "diffuser": {"d_in_equiv_mm": R(d_eq_double*1e3, 2), "d_out_mm": d_dis*1e3, "half_angle_deg": half_angle,
                          "L_mm": R(L_dif*1e3, 1), "c_out": R(c_dis, 2)}},
  "performance": {"P_h_kW": R(P_h/1e3, 1), "P_imp_kW": R(P_imp/1e3, 1), "P_ind_kW": R(P_ind/1e3, 1),
                  "P_disc_kW": R(P_RR/1e3, 2), "P_shaft_kW": R(P_shaft/1e3, 1), "eta_pump": R(eta_pump, 3),
                  "torque_Nm": R(T_OP, 2),
                  "nota": "sem perdas de mancais/selos; para o ciclo usar eta ~0,70"},
  "loads": {"kR_single_BEP": R(kR100, 4), "kR_single_0": R(kR0, 4), "kR_double": R(kR_double, 4), "kR_dyn": kR_dyn,
            "FR_single_BEP_N": R(loads['single']['BEP'], 0), "FR_single_shutoff_N": R(loads['single']['shutoff'], 0),
            "FR_double_N": R(loads['double']['BEP'], 0), "FR_design_kR015_N": R(loads['design_kR015'], 0),
            "BPF_impeller_Hz": R(z*n/60, 0), "BPF_inducer_Hz": R(z_ind*n/60, 0)},
  "mass_inertia_Al6061": {"m_impeller_kg": R(m_imp, 4), "Ip_impeller_kgm2": float(f"{Ip_imp:.3e}"),
                          "Id_impeller_kgm2": float(f"{Id_imp:.3e}"), "m_inducer_kg": R(m_ind, 4),
                          "Ip_inducer_kgm2": float(f"{Ip_ind:.3e}"), "Id_inducer_kgm2": float(f"{Id_ind:.3e}"),
                          "m_fluid_impeller_kg": R(m_fl, 4), "Ip_fluid_kgm2": float(f"{Ip_fl:.3e}"),
                          "nota": "analitico +-20 %; Id no CG de cada peca; substituir pelo CAD"},
}
with open('etapa2_bomba_htp.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

I, M, V = out['inducer'], out['impeller'], out['volute']
rows = [
 ("Projeto", "Fluido: densidade", rho, "kg/m3", "HTP 90 % a 300 K"),
 ("Projeto", "Fluido: viscosidade dinamica", mu, "Pa.s", ""),
 ("Projeto", "Fluido: pressao de vapor", pv, "Pa", "incerto +-50 %"),
 ("Projeto", "Vazao (voluta)", R(Q_Le*3600, 2), "m3/h", "util + buffer do mancal B2"),
 ("Projeto", "Altura total H", R(H, 1), "m", "dp_tt = 230 bar"),
 ("Projeto", "Rotacao n", n, "rpm", ""),
 ("Projeto", "NPSH disponivel", R(NPSHA, 2), "m", "p_in total 5 bar"),
 ("Indutor", "Vazao no indutor", R(Q_ind*3600, 2), "m3/h", "inclui recirculacao S6"),
 ("Indutor", "Altura do indutor", I['H_m'], "m", ""),
 ("Indutor", "D ponta entrada", I['D_tip_inlet_mm'], "mm", f"constante por {I['L_const_tip_mm']} mm"),
 ("Indutor", "D ponta saida", I['D_tip_exit_mm'], "mm", "afunilada"),
 ("Indutor", "D cubo (constante)", I['d_hub_mm'], "mm", "eixo passante D24"),
 ("Indutor", "Numero de pas", z_ind, "-", ""),
 ("Indutor", "beta1B ponta / cubo", f"{I['beta1B_tip_deg']} / {I['beta1B_hub_deg']}", "deg", "placa plana, r.tan(beta) = cte"),
 ("Indutor", "Passo da helice (lead)", I['lead_mm'], "mm", "constante"),
 ("Indutor", "Comprimento axial", I['L_axial_mm'], "mm", f"solidez ponta {sol_t}"),
 ("Indutor", "Espessura ponta / cubo", f"{t_ind_tip*1e3} / {t_ind_hub*1e3}", "mm", "bordo de ataque em cunha"),
 ("Indutor", "Folga de ponta", clr_ind*1e3, "mm", ""),
 ("Impeller", "Altura do impeller", M['H_m'], "m", f"eta_h = {eta_h}"),
 ("Impeller", "Vazao no impeller Q_La", R(Q_La*3600, 2), "m3/h", f"eta_v = {M['eta_v']}"),
 ("Impeller", "d_H (cubo)", M['dn_mm'], "mm", ""),
 ("Impeller", "d_S (succao = d1)", M['d1_mm'], "mm", "= saida do indutor"),
 ("Impeller", "d2", M['d2_mm'], "mm", ""),
 ("Impeller", "b2", M['b2_mm'], "mm", ""),
 ("Impeller", "Numero de pas", z, "-", "sem splitters"),
 ("Impeller", "beta1B shroud / hub", f"{M['beta1B_shroud_deg']} / {M['beta1B_hub_deg']}", "deg", f"incidencia {i1} deg"),
 ("Impeller", "beta2B", beta2B, "deg", "constante na largura"),
 ("Impeller", "Espessura de pa", e_bl*1e3, "mm", ""),
 ("Impeller", "Pre-rotacao r.cu na entrada", I['rcu_exit_m2s'], "m2/s", f"c1u shroud = {M['c1u']} m/s"),
 ("Impeller", "Tipo", "fechado + aneis frontal e traseiro + furos", "", f"d_anel {M['d_wear_ring_mm']} mm, folga 0,08 mm"),
 ("Voluta", "Tipo", "dupla 2x180 deg, secao circular", "", "velocidade constante (A ~ eps)"),
 ("Voluta", "d_z (lingueta)", V['d_cutwater_mm'], "mm", "d_z/d2 = 1,07"),
 ("Voluta", "b3", V['b3_mm'], "mm", "b3/b2 = 2"),
 ("Voluta", "d3q por voluta parcial", V['double']['d3q_mm'], "mm", f"projeto 1,10 x Q; simples seria {V['single_alternative']['d3q_mm']} mm"),
 ("Voluta", "alpha3B", V['alpha3B_deg'], "deg", ""),
 ("Voluta", "e3 (lingueta e nervura)", V['e3_mm'], "mm", ""),
 ("Voluta", "Difusor: d saida / L", f"{d_dis*1e3} / {V['diffuser']['L_mm']}", "mm", f"semiangulo {half_angle} deg"),
]
with open('etapa2_cfturbo.csv', 'w', newline='', encoding='utf-8') as f:
    wr = csv.writer(f, delimiter=';')
    wr.writerow(["componente", "parametro", "valor", "unidade", "observacao"])
    wr.writerows(rows)
print(json.dumps(out, indent=1, ensure_ascii=False))
