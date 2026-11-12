"""turbopump-design - Etapa 4: turbina axial (meanline 1D), rev. 2.

Gas de HTP 90 % decomposto (Cantera, gri30 / NASA 7-coef.), balanco de potencia,
triangulos de velocidade, perdas de Soderberg, geometria a n = 55 000 rpm,
tensoes de pa, empuxo axial e massa/inercias do rotor da turbina (input da etapa 5).
Unidades SI. Saidas: etapa4_turbina.json, etapa4_varredura_phi.csv,
etapa4_cfturbo.csv e o texto impresso (redirecionar para saida_etapa4.txt).
"""
import csv
import json
import os

import numpy as np
import cantera as ct

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- inputs
# Requisitos/ciclo (00): 150 bar / 1150 K -> 130 bar, todo o HTP passa pela turbina
p01, T01, p3 = 150e5, 1150.0, 130e5
T3_fluxograma = 1140.0                 # so comparacao
m_HTP = 17.5                           # kg/s
m_S7 = 0.050                           # kg/s, vazamento S7 (etapa 5 sec. 7) entra a jusante do estator
m_N = m_HTP - m_S7                     # vazao pelos bocais
m_R = m_HTP                            # vazao pelo rotor
n = 55_000.0                           # rpm (etapa 1 rev. 2)
P_OP = 411.6e3                         # W, eixo da OP (etapa 2 rev. 2, sec. 4.5)
P_FP = 74.3e3                          # W, eixo da FP (etapa 3 rev. 2, ciclo)
eta_mec = 0.97                         # mancais + selos (etapa 0)
d_bore = 20e-3                         # m, eixo na montagem da turbina (etapa 5 sec. 9)

# Escolhas desta etapa
R_DES, PHI_DES = 0.5, 0.6              # grau de reacao, coef. de vazao cx/u
ZWEIFEL = 0.80                         # carregamento de pa (passo otimo)
B_STATOR, B_ROTOR = 11e-3, 9e-3        # m, corda axial
ETA_EXTRA = 0.92                       # folga/vazamento de shroud, disco, otimismo do Soderberg
RHO_BLADE = 8540.0                     # kg/m3, MAR-M-247 (fundida)
TAPER = 0.67                           # fator de tensao p/ pa afilada (A_topo/A_raiz ~ 0,5)
T_SHROUD, W_SHROUD = 1.5e-3, 10e-3     # m, shroud integral: espessura radial, largura
T_DISK = 12e-3                         # m, espessura do disco (estimativa)
T_BLADE_MEAN = 1.2e-3                  # m, espessura media do perfil

# ---------------------------------------------------------------- 1. gas
MW = {'H2O2': 34.0147, 'H2O': 18.0153}
n_h2o2 = 0.90 / MW['H2O2'] * 1e3                      # mol/kg
n_h2o_sol = 0.10 / MW['H2O'] * 1e3
X = {'H2O': n_h2o2 + n_h2o_sol, 'O2': 0.5 * n_h2o2}
g = ct.Solution('gri30.yaml')
g.TPX = T01, p01, X
M_gas = g.mean_molecular_weight
R = ct.gas_constant / M_gas
cp = g.cp_mass
gam = cp / g.cv_mass
mu = 4.3e-5   # Pa.s, estimativa (vapor ~1150 K ~4,1e-5; O2 ~4,8e-5)

def T_ad(T_liq, cp_liq=2.75e3):
    """Temperatura adiabatica de decomposicao (liquido a T_liq -> gas)."""
    h_reac = n_h2o2 * (-187.78e3) + n_h2o_sol * (-285.83e3) + cp_liq * (T_liq - 298.15)
    lo, hi = 600.0, 1600.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        g.TPX = mid, p01, X
        lo, hi = (mid, hi) if g.enthalpy_mass < h_reac else (lo, mid)
    return mid

# ---------------------------------------------------------------- 2. energia disponivel
g.TPX = T01, p01, X
h01, s01 = g.enthalpy_mass, g.entropy_mass
g.SPX = s01, p3, X
dh_is = h01 - g.enthalpy_mass          # total-estatica
T3s = g.T
c0 = np.sqrt(2 * dh_is)
P_req = (P_OP + P_FP) / eta_mec
P_ideal = m_R * dh_is
eta_min = P_req / P_ideal
dT_bal = P_req / (m_R * cp)

def PR_for(dh_target):
    lo, hi = 1.0001, p01 / p3
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        g.SPX = s01, p01 / mid, X
        lo, hi = (mid, hi) if (h01 - g.enthalpy_mass) < dh_target else (lo, mid)
    return mid

# ---------------------------------------------------------------- 3. modelo de estagio
def soderberg(eps_deg, b_over_h):
    z = 0.04 * (1 + 1.5 * (eps_deg / 100) ** 2)
    return (1 + z) * (0.993 + 0.021 * b_over_h) - 1

def stage(psi, phi, Rx, bh_N=0.6, bh_R=0.5):
    """Estagio axial, cx constante. Angulos medidos do eixo axial.
    c_theta2 = u(psi/2 + 1 - R), c_theta3 = u(1 - R - psi/2) (Dixon cap. 4)."""
    ct2 = psi / 2 + 1 - Rx
    ct3 = 1 - Rx - psi / 2
    a2 = np.degrees(np.arctan(ct2 / phi))
    b2 = np.degrees(np.arctan((ct2 - 1) / phi))
    b3 = np.degrees(np.arctan((1 - ct3) / phi))      # relativo, sentido contrario a rotacao
    a3 = np.degrees(np.arctan(ct3 / phi))
    c2 = np.hypot(phi, ct2)
    w2 = np.hypot(phi, ct2 - 1)
    w3 = np.hypot(phi, 1 - ct3)
    c3 = np.hypot(phi, ct3)
    zN, zR = soderberg(a2, bh_N), soderberg(abs(b2) + b3, bh_R)
    loss = zN * c2 ** 2 / 2 + zR * w3 ** 2 / 2 + c3 ** 2 / 2
    eta = psi / (psi + loss) * ETA_EXTRA
    return dict(psi=psi, phi=phi, R=Rx, a2=a2, b2=b2, b3=b3, a3=a3,
                c2=c2, w2=w2, w3=w3, c3=c3, zN=zN, zR=zR,
                eta_ts=eta, nu=np.sqrt(eta / (2 * psi)))

omega = n * np.pi / 30

def design(psi, phi, Rx):
    """Itera razao de aspecto (b/h) com a geometria real."""
    bhN, bhR = 0.6, 0.5
    for _ in range(10):
        s = stage(psi, phi, Rx, bhN, bhR)
        u = s['nu'] * c0
        Dm = 2 * u / omega
        cx = phi * u
        c2 = s['c2'] * u
        # estado 2 (entre estator e rotor): queda isentropica no estator = (1-R)*dh_is
        g.SPX = s01, p01, X
        dhN = (1 - Rx) * dh_is
        lo, hi = p3, p01
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            g.SPX = s01, mid, X
            lo, hi = (lo, mid) if (h01 - g.enthalpy_mass) < dhN else (mid, hi)
        p2 = mid
        T2 = T01 - c2 ** 2 / (2 * cp)
        rho2 = p2 / (R * T2)
        dh = s['eta_ts'] * dh_is
        T03 = T01 - dh / cp
        T3 = T03 - (s['c3'] * u) ** 2 / (2 * cp)
        rho3 = p3 / (R * T3)
        A2 = m_N / (rho2 * cx)
        A3 = m_R / (rho3 * cx)
        h2, h3 = A2 / (np.pi * Dm), A3 / (np.pi * Dm)
        bhN, bhR = B_STATOR / h2, B_ROTOR / h3
    return s, dict(u=u, Dm=Dm, cx=cx, c2=c2, w2=s['w2'] * u, w3=s['w3'] * u, c3=s['c3'] * u,
                   p2=p2, T2=T2, rho2=rho2, rho3=rho3, A2=A2, A3=A3, h2=h2, h3=h3,
                   dh=dh, T03=T03, T3=T3, M2=c2 / np.sqrt(gam * R * T2),
                   Mw3=s['w3'] * u / np.sqrt(gam * R * T3), bhN=bhN, bhR=bhR)

S, G = design(1.0, PHI_DES, R_DES)
P_avail = m_R * G['dh']
PR_min = PR_for(P_req / (m_R * S['eta_ts']))

# ---------------------------------------------------------------- 4. pas (Zweifel), bocais
def pitch(b, a_in, a_out):
    """Zweifel: Z = 2 (s/b) cos^2(a_out) (tan a_in + tan a_out)."""
    ai, ao = np.radians(a_in), np.radians(a_out)
    return ZWEIFEL * b / (2 * np.cos(ao) ** 2 * (np.tan(ai) + np.tan(ao)))

sN = pitch(B_STATOR, 0.0, S['a2'])
sR = pitch(B_ROTOR, abs(S['b2']), S['b3'])
zN_raw, zR_raw = np.pi * G['Dm'] / sN, np.pi * G['Dm'] / sR
zN, zR = 23, 29                        # primos entre si (Huzel p. 201: sem fator comum)
o_N = np.pi * G['Dm'] / zN * np.cos(np.radians(S['a2']))   # garganta do bocal
Re_N = G['rho2'] * G['c2'] * B_STATOR / np.cos(np.radians(S['a2'] / 2)) / mu

# ---------------------------------------------------------------- 5. tensoes
r_m = G['Dm'] / 2
r_tip, r_root = r_m + G['h3'] / 2, r_m - G['h3'] / 2
sig_untap = RHO_BLADE * omega ** 2 * G['A3'] / (2 * np.pi)
sig_tap = TAPER * sig_untap
A_root_blade = (B_ROTOR / np.cos(np.radians(30))) * T_BLADE_MEAN * 1.6   # area da raiz ~1,6x media
m_shroud_blade = RHO_BLADE * 2 * np.pi * r_tip * T_SHROUD * W_SHROUD / zR
sig_shroud = m_shroud_blade * r_tip * omega ** 2 / A_root_blade
AN2 = G['A3'] * n ** 2
u_tip, u_root = omega * r_tip, omega * r_root

# ---------------------------------------------------------------- 6. massa e inercias (rotor)
def ring(ri, ro, L, rho):
    m = rho * np.pi * (ro ** 2 - ri ** 2) * L
    Ip = 0.5 * m * (ri ** 2 + ro ** 2)
    Id = 0.25 * m * (ri ** 2 + ro ** 2) + m * L ** 2 / 12
    return m, Ip, Id

r_b = d_bore / 2
parts = {
    'disco': ring(r_b, r_root, T_DISK, RHO_BLADE),
    'shroud': ring(r_tip, r_tip + T_SHROUD, W_SHROUD, RHO_BLADE),
}
chord = B_ROTOR / np.cos(np.radians(30))
m_bl = zR * RHO_BLADE * G['h3'] * chord * T_BLADE_MEAN
parts['pas'] = (m_bl, m_bl * (r_m ** 2 + G['h3'] ** 2 / 12),
                0.5 * m_bl * (r_m ** 2 + G['h3'] ** 2 / 12) + m_bl * B_ROTOR ** 2 / 12)
m_rot = sum(p[0] for p in parts.values())
Ip_rot = sum(p[1] for p in parts.values())
Id_rot = sum(p[2] for p in parts.values())   # aprox.: componentes centrados no mesmo plano

# ---------------------------------------------------------------- 7. cargas
F_ax_blade = (G['p2'] - p3) * np.pi * (r_tip ** 2 - r_root ** 2)
F_ax_rotor = (G['p2'] - p3) * np.pi * (r_tip ** 2 - r_b ** 2)    # disco: frente a p2, tras a p3
F_tang = P_avail / (omega * r_m)                                 # forca tangencial total nas pas
T_turb = P_req / omega
Re_disk = omega * r_tip ** 2 * G['rho3'] / mu
cM = 0.0102 * (0.05) ** 0.1 / Re_disk ** 0.2                     # Daily & Nece regime IV (Gulich Tab. 3.6)
P_disk = cM * G['rho3'] * omega ** 3 * r_tip ** 5               # 2 faces: 2*0,5*cM*rho*w^3*r^5

# ---------------------------------------------------------------- 8. variantes
alts = {}
for lab, psi, Rx in [('impulso', 2.0, 0.0), ('baixa_reacao_25', 1.5, 0.25)]:
    s_, g_ = design(psi, PHI_DES, Rx)
    alts[lab] = dict(eta_ts=s_['eta_ts'], u_c0=s_['nu'], Dm_mm=g_['Dm'] * 1e3,
                     h3_mm=g_['h3'] * 1e3, h_Dm=g_['h3'] / g_['Dm'], p2_bar=g_['p2'] / 1e5,
                     F_ax_rotor_kN=(g_['p2'] - p3) * np.pi * ((g_['Dm'] + g_['h3']) ** 2 / 4 - r_b ** 2) / 1e3)
sweep = []
for phi in [0.4, 0.5, 0.6, 0.7, 0.8]:
    a, ga = design(1.0, phi, 0.5)
    b, gb = design(2.0, phi, 0.0)
    sweep.append(dict(phi=phi, eta_R50=a['eta_ts'], u_c0_R50=a['nu'], Dm_R50_mm=ga['Dm'] * 1e3,
                      h_R50_mm=ga['h3'] * 1e3, eta_imp=b['eta_ts'], u_c0_imp=b['nu'],
                      Dm_imp_mm=gb['Dm'] * 1e3, h_imp_mm=gb['h3'] * 1e3))

# ---------------------------------------------------------------- saidas
res = dict(
    inputs=dict(p01_bar=p01 / 1e5, T01_K=T01, p3_bar=p3 / 1e5, m_nozzle=m_N, m_rotor=m_R, n_rpm=n,
                P_OP_kW=P_OP / 1e3, P_FP_kW=P_FP / 1e3, eta_mec=eta_mec),
    gas=dict(M=M_gas, R=R, cp=cp, gamma=gam, x_H2O=X['H2O'] / sum(X.values()),
             T_ad_298=T_ad(298.15), T_ad_400=T_ad(400.0), mu_est=mu),
    balanco=dict(PR=p01 / p3, dh_is_kJkg=dh_is / 1e3, T3s=T3s, c0=c0, P_req_kW=P_req / 1e3,
                 P_ideal_kW=P_ideal / 1e3, eta_min=eta_min, dT_balanco=dT_bal,
                 T3_balanco=T01 - dT_bal, P_disp_kW=P_avail / 1e3, margem=P_avail / P_req - 1,
                 PR_min=PR_min, dp_turbina_min_bar=p01 * (1 - 1 / PR_min) / 1e5,
                 P_fluxograma_dT10_kW=m_R * cp * (T01 - T3_fluxograma) / 1e3),
    estagio=dict(tipo='axial, 1 estagio, admissao total, bocais subsonicos convergentes, rotor com shroud',
                 R=R_DES, psi=S['psi'], phi=PHI_DES, alpha2=S['a2'], beta2=S['b2'], beta3=S['b3'],
                 alpha3=S['a3'], eta_ts=S['eta_ts'],
                 eta_tt=G['dh'] / (dh_is - G['c3'] ** 2 / 2),   # aprox.: recupera c3^2/2
                 u_c0=S['nu'], zeta_N=S['zN'], zeta_R=S['zR']),
    geometria=dict(u=G['u'], Dm_mm=G['Dm'] * 1e3, d_tip_mm=2 * r_tip * 1e3, d_root_mm=2 * r_root * 1e3,
                   h_stator_mm=G['h2'] * 1e3, h_rotor_mm=G['h3'] * 1e3, h_Dm=G['h3'] / G['Dm'],
                   hub_tip=r_root / r_tip, b_stator_mm=B_STATOR * 1e3, b_rotor_mm=B_ROTOR * 1e3,
                   z_stator=zN, z_rotor=zR, z_zweifel_stator=zN_raw, z_zweifel_rotor=zR_raw,
                   throat_stator_mm=o_N * 1e3, h_over_throat=G['h2'] / o_N, shroud_t_mm=T_SHROUD * 1e3,
                   disk_t_mm=T_DISK * 1e3, bore_mm=d_bore * 1e3),
    escoamento=dict(cx=G['cx'], c2=G['c2'], w2=G['w2'], w3=G['w3'], c3=G['c3'], M2=G['M2'], Mw3=G['Mw3'],
                    p2_bar=G['p2'] / 1e5, T2=G['T2'], rho2=G['rho2'], rho3=G['rho3'], T03=G['T03'],
                    A2_cm2=G['A2'] * 1e4, A3_cm2=G['A3'] * 1e4, Re_stator=Re_N),
    tensoes=dict(u_tip=u_tip, u_root=u_root, AN2_m2rpm2=AN2, sigma_untap_MPa=sig_untap / 1e6,
                 sigma_tap_MPa=sig_tap / 1e6, sigma_shroud_MPa=sig_shroud / 1e6,
                 sigma_total_MPa=(sig_tap + sig_shroud) / 1e6),
    rotor=dict(material='MAR-M-247', m_g=m_rot * 1e3, Ip_kgmm2=Ip_rot * 1e6, Id_kgmm2=Id_rot * 1e6,
               partes={k: dict(m_g=v[0] * 1e3, Ip_kgmm2=v[1] * 1e6, Id_kgmm2=v[2] * 1e6) for k, v in parts.items()}),
    cargas=dict(torque_Nm=T_turb, F_tang_N=F_tang, F_ax_pas_kN=F_ax_blade / 1e3,
                F_ax_rotor_kN=F_ax_rotor / 1e3, P_atrito_disco_kW=P_disk / 1e3,
                f_passagem_rotor_Hz=zR * n / 60, f_passagem_estator_Hz=zN * n / 60),
    alternativas=alts,
)
with open(os.path.join(HERE, 'etapa4_turbina.json'), 'w') as f:
    json.dump(res, f, indent=2, default=float)
with open(os.path.join(HERE, 'etapa4_varredura_phi.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(sweep[0]))
    w.writeheader()
    w.writerows([{k: round(v, 4) for k, v in r.items()} for r in sweep])
with open(os.path.join(HERE, 'etapa4_cfturbo.csv'), 'w', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['parametro', 'valor', 'unidade'])
    for row in [('mass_flow', m_N, 'kg/s'), ('p_total_in', p01 / 1e5, 'bar'), ('T_total_in', T01, 'K'),
                ('p_static_out', p3 / 1e5, 'bar'), ('speed', n, 'rpm'), ('gas_R', R, 'J/kgK'),
                ('cp', cp, 'J/kgK'), ('gamma', gam, '-'), ('power', P_req / 1e3, 'kW'),
                ('D_mean', G['Dm'] * 1e3, 'mm'), ('h_stator', G['h2'] * 1e3, 'mm'),
                ('h_rotor', G['h3'] * 1e3, 'mm'), ('reaction', R_DES, '-'),
                ('alpha2_from_axial', S['a2'], 'deg'), ('beta3_from_axial', S['b3'], 'deg'),
                ('z_stator', zN, '-'), ('z_rotor', zR, '-'),
                ('b_axial_stator', B_STATOR * 1e3, 'mm'), ('b_axial_rotor', B_ROTOR * 1e3, 'mm')]:
        w.writerow([row[0], f'{row[1]:.4g}', row[2]])

if __name__ == '__main__':
    def show(title, d):
        print(f'\n== {title}')
        for k, v in d.items():
            print(f'  {k:24s} {v:.4g}' if isinstance(v, (int, float, np.floating)) else f'  {k:24s} {v}')
    for k in ['inputs', 'gas', 'balanco', 'estagio', 'geometria', 'escoamento', 'tensoes', 'cargas']:
        show(k, res[k])
    show('rotor', {k: v for k, v in res['rotor'].items() if k != 'partes'})
    for k, v in res['rotor']['partes'].items():
        show(f'rotor/{k}', v)
    for k, v in alts.items():
        show(f'alternativa/{k}', v)
    print('\n== varredura phi (R=0,5 | impulso)')
    for r in sweep:
        print('  ' + '  '.join(f'{k}={v:.3f}' for k, v in r.items()))
