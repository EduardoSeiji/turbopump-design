"""
turbopump-design — Etapa 3: bomba de combustivel (FP, Jet A), meanline 1D. rev. 2
(rev. 2: eixo/cubo, anel traseiro + furos de balanceamento e k_R vindos de 06; ver 04-resultados).

Inputs: 00-requisitos (vazao, pressoes), 01-etapa0 (propriedades), 02-etapa1 (n = 55 000 rpm).
Referencias (Gulich, Centrifugal Pumps, 2a ed.):
  Eq. 2.5/T3.4.15 n_q | Eq. 3.26 psi_opt | T3.9.1, T3.9.2, T3.9.6 eficiencias estatisticas
  T3.6.2/T3.6.3 atrito de disco | T3.7(1) selo anular | Eq. 6.10 + Fig. 6.20 NPSH3
  Tab. 7.1 (T7.1.7 beta1B, T7.1.8 slip, T7.1.9 altura) | Eq. 7.1 b2* | Eq. 3.14/7.24 voluta
  Tab. 9.2 empuxo axial | Tab. 9.4 empuxo radial | Cap. 7.3 n_q baixo (Barske)
Huzel & Huang cap. 6 (Eq. 6-9..6-11, p.178 indutor, p.186 difusor). NASA SP-8052 (indutor).
SI internamente; JSON em mm / graus.
"""
import json, math, copy
from scipy.optimize import brentq

g = 9.81
FL = dict(rho=795.0, mu=1.3e-3, pv=400.0, cp=2000.0)   # Jet A @300 K (01-etapa0)
mdot, p_in, p_out = 2.5, 5e5, 135e5                     # 00-requisitos
N_RPM = 55000.0                                         # 02-etapa1

BASE = dict(
    shroud='open',     # 'open' (semiaberto) | 'closed' (fechado)
    z=6, z_split=6, L_split=0.6,   # pas inteiras + splitters (z_ef p/ slip = z + z_split*L_split)
    beta2B=25.0,       # Gulich 7.2: 15-45 (tipico 20-27); 25 -> desvio delta2 ~15 graus
    etah=0.75,         # eta_h de projeto (T3.9.6 industrial = 0,70; foguete usinado, Re ~3e6 -> 0,75)
    beta1a_tip=10.0,   # rev.2: 12 -> 10 graus p/ recuperar F_NPSH com cubo 20 (Fig. 6.20/6.21: faixa 5-25)
    i1_deg=3.0,        # incidencia (T7.1.7: 0-4)
    e1=0.8e-3, e2=0.8e-3,
    d_shaft=14e-3, d_hub=20e-3,    # 06 par.9: eixo 0-20 mm = Ø14 (furo); cubo/porca no olho Ø20
    d_E=None,          # anel traseiro (+ furos de balanceamento): diametro [m]; None = sem anel; resolvido p/ F_ax = 0
    s_E=0.05e-3, N_E=5, L_E=5e-3,   # anel traseiro labirinto (igual ao frontal do fechado)
    s_sp=0.05e-3, N_lab=5, L_sp=6e-3,          # fechado: selo labirinto frontal
    s_tip=0.10e-3, k_tip=1.0,      # semiaberto: perda de eta_h ~ k_tip*s_tip/b2 (ordem de grandeza)
    sax_r2=0.04, k_rot=0.5, lam_c=1.1,
    t_rear=2.2e-3, t_front=1.2e-3, L_hub=18e-3,   # 06 par.2: FP ocupa z 0-18 mm
    dz_d2=1.07, b3_b2=2.0, c_out=8.0, c_in=5.0, cone_deg=8.0,
    kR_bep=0.016, kR_0=0.10, kR_dyn=0.03, kR_design=0.15,   # 06 par.5.1 (Gulich Fig. 9.27/9.28, Tab. 9.4 item 13)
)

def eta_T391(Q, nq):
    m = 0.1*(1/Q)**0.15*(45/nq)**0.06
    return 1 - 0.095*(1/Q)**m - 0.3*(0.35 - math.log10(nq/23))**2*(1/Q)**0.05
def eta_T392(Q, nq):
    m = 0.1*(1/Q)**0.15*(45/nq)**0.06
    return 1 - 0.116*(1/Q)**m - 0.4*(0.26 - math.log10(nq/25))**2
def etah_T396(Q, nq):
    m = 0.08*(1/Q)**0.15*(45/nq)**0.06
    return 1 - 0.055*(1/Q)**m - 0.2*(0.26 - math.log10(nq/25))**2*(1/Q)**0.1
def k_RR(Re, sax_r2):                       # T3.6.3, liso
    return math.pi/(2*Re*sax_r2) + 0.0625/Re**0.2

def seal_leak(dH, d_sp, s, L, u_sp, nu, N_lab):
    """Selo anular/labirinto: c_ax = sqrt(2g dH/(1,5 + N_lab + lam L/2s)); lam c/ fator de rotacao (T3.7)."""
    cax = 10.0
    for _ in range(100):
        Re = cax*2*s/nu
        lam0 = 0.3164/Re**0.25 if Re > 2000 else 96/Re
        lam = lam0*(1 + (u_sp/(2*cax))**2)**0.375
        c_new = math.sqrt(2*g*dH/(1.5 + N_lab + lam*L/(2*s)))
        if abs(c_new-cax) < 1e-7: break
        cax = c_new
    return math.pi*d_sp*s*cax, cax

def design(n_rpm=N_RPM, prm=BASE, fl=FL):
    p = prm
    rho, nu = fl['rho'], fl['mu']/fl['rho']
    w = 2*math.pi*n_rpm/60
    Q = mdot/rho; H = (p_out-p_in)/(rho*g)
    nq = n_rpm*math.sqrt(Q)/H**0.75
    NPSHA = (p_in-fl['pv'])/(rho*g)
    Pu = rho*g*H*Q
    x = nq/100
    b2s = 0.017 + 0.262*x - 0.08*x**2 + 0.0093*x**3        # Eq. 7.1
    z = p['z']; z_ef = z + p['z_split']*p['L_split']; z_out = z + p['z_split']
    dh = p['d_hub']; bb = math.radians(p['beta2B'])
    opened = p['shroud'] == 'open'

    def head(d2, QLa, d1m, etah):
        u2 = w*d2/2; b2 = b2s*d2
        eps = math.exp(-8.16*math.sin(bb)/z_ef)
        kw = 1.0 if d1m/d2 <= eps else 1 - ((d1m/d2-eps)/(1-eps))**3
        gam = 0.98*(1 - math.sqrt(math.sin(bb))/z_ef**0.7)*kw         # T7.1.8
        tau2 = 1/(1 - z_out*p['e2']/(math.pi*d2*math.sin(bb)))
        return etah*u2**2/g*(gam - QLa*tau2/(math.pi*d2*b2*u2*math.tan(bb))), gam, tau2   # T7.1.9

    etav, b2_prev, Qsp = 0.95, 2.8e-3, 0.0
    for it in range(80):
        QLa = Q/etav
        t = math.tan(math.radians(p['beta1a_tip']))      # tan(beta1a) = c1m/u1 na ponta
        d1 = brentq(lambda d: QLa/(math.pi/4*(d**2-dh**2)) - t*w*d/2, dh*1.01, 0.1)
        A1 = math.pi/4*(d1**2-dh**2); c1m = QLa/A1; u1 = w*d1/2; w1 = math.hypot(c1m, u1)
        d1m = math.sqrt((d1**2+dh**2)/2)
        etah = p['etah']*(1 - p['k_tip']*p['s_tip']/b2_prev) if opened else p['etah']
        d2 = brentq(lambda d: head(d, QLa, d1m, etah)[0]-H, 0.03, 0.12)
        b2 = b2s*d2; u2 = w*d2/2
        _, gam, tau2 = head(d2, QLa, d1m, etah)
        Hth = H/etah; c2u = g*Hth/u2; c2m = QLa*tau2/(math.pi*d2*b2); c2 = math.hypot(c2u, c2m)
        Hp = Hth - (c2**2 - c1m**2)/(2*g) - 0.5*(Hth-H)
        if opened:
            d_sp = dH_sp = float('nan')
            if p['d_E']:   # anel traseiro: camara interna ventilada a ~p_in pelos furos
                u_E = w*p['d_E']/2
                dH_sp = Hp - p['k_rot']**2*(u2**2 - u_E**2)/(2*g)
                Qsp, _ = seal_leak(dH_sp, p['d_E'], p['s_E'], p['L_E'], u_E, nu, p['N_E'])
            else:
                Qsp = 0.0
            etav_new = Q/(Q+Qsp)
        else:              # fechado: anel frontal + anel traseiro igual + furos (vazamento x2), como 03/06
            d_sp = d1 + 2*p['t_front'] + 2e-3; u_sp = w*d_sp/2
            dH_sp = Hp - p['k_rot']**2*(u2**2 - u_sp**2)/(2*g)
            q1, _ = seal_leak(dH_sp, d_sp, p['s_sp'], p['L_sp'], u_sp, nu, p['N_lab'])
            Qsp = 2*q1
            etav_new = Q/(Q+Qsp)
        if abs(etav_new-etav) < 1e-10 and abs(b2-b2_prev) < 1e-10: break
        etav, b2_prev = etav_new, b2
    QLa = Q + Qsp
    psi = 2*g*H/u2**2; r2 = d2/2

    lam_w3 = 0.3*(c1m/u1)**0.57                                       # Fig. 6.20
    NPSH3 = p['lam_c']*c1m**2/(2*g) + lam_w3*w1**2/(2*g)              # Eq. 6.10
    nss = n_rpm*math.sqrt(Q)/NPSH3**0.75
    p_in_min = 1.2*NPSH3*rho*g + fl['pv']

    beta1 = {}
    for name, d in (('hub', dh), ('mean', d1m), ('tip', d1)):
        u = w*d/2; bf = math.atan(c1m/u)
        for _ in range(30):
            bB = bf + math.radians(p['i1_deg'])
            tau1 = 1/(1 - z*p['e1']/(math.pi*d*math.sin(bB)))
            bf_new = math.atan(c1m*tau1/u)
            if abs(bf_new-bf) < 1e-11: break
            bf = bf_new
        beta1[name] = dict(d_mm=d*1e3, u=u, beta1_flow=math.degrees(bf), beta1B=math.degrees(bf)+p['i1_deg'], tau1=tau1)

    w2u = u2 - c2u
    beta2_flow = math.degrees(math.atan(c2m/w2u)); delta2 = p['beta2B'] - beta2_flow
    alpha2 = math.degrees(math.atan(c2m/c2u)); w2 = math.hypot(c2m, w2u)

    Re = w*r2**2/nu; kRR = k_RR(Re, p['sax_r2'])
    P_rear = kRR*rho*w**3*r2**5*(1-(dh/d2)**5)
    P_front = 0.0 if opened else kRR*rho*w**3*r2**5*(1-(d_sp/d2)**5)
    PRR = P_rear + P_front
    P_shaft = rho*g*H*QLa/etah + PRR
    eta = Pu/P_shaft
    loss = dict(hidraulica_kW=(rho*g*H*Q/etah - Pu)/1e3, vazamento_kW=rho*g*H*Qsp/etah/1e3,
                disco_tras_kW=P_rear/1e3, disco_frontal_kW=P_front/1e3)

    rz = p['dz_d2']*r2; b3 = p['b3_b2']*b2
    vol = []
    for e_deg in range(30, 361, 30):                 # voluta simples, secao circular, r*cu = cte (Eq. 3.14)
        Qe = Q*e_deg/360
        f = lambda dq: c2u*r2*2*math.pi*((rz+dq/2) - math.sqrt((rz+dq/2)**2 - (dq/2)**2)) - Qe
        dq = brentq(f, 1e-6, 0.05)
        vol.append(dict(eps_deg=e_deg, d_section=dq*1e3, A_mm2=math.pi/4*dq**2*1e6, r_center=(rz+dq/2)*1e3))
    d3q = vol[-1]['d_section']/1e3; A3q = math.pi/4*d3q**2; c3q = Q/A3q
    d_out = math.sqrt(4*Q/(math.pi*p['c_out'])); d_suc = math.sqrt(4*Q/(math.pi*p['c_in']))
    L_diff = (d_out-d3q)/(2*math.tan(math.radians(p['cone_deg']/2)))

    b2tot = b2 + p['t_rear'] + (0 if opened else p['t_front'])
    qRH = rho*g*H*d2*b2tot     # Gulich Eq. 9.6
    FR_bep = (p['kR_bep']+p['kR_dyn'])*qRH; FR_0 = (p['kR_0']+p['kR_dyn'])*qRH; FR_design = p['kR_design']*qRH

    p2 = p_in + rho*g*Hp; kk = p['k_rot']
    def F_gap(ra, rb):   # camara lateral com fluido a k*omega: p(r) = p2 - rho k^2 w^2 (r2^2-r^2)/2
        return math.pi*(p2 - rho*kk**2*w**2*r2**2/2)*(rb**2-ra**2) + math.pi*rho*kk**2*w**2/4*(rb**4-ra**4)
    if opened and p['d_E']:
        F_rear = F_gap(p['d_E']/2, r2) + p_in*math.pi*((p['d_E']/2)**2-(dh/2)**2)
    elif opened:
        F_rear = F_gap(dh/2, r2)
    else:
        d_sp_ = d1 + 2*p['t_front'] + 2e-3
        F_rear = F_gap(d_sp_/2, r2) + p_in*math.pi*((d_sp_/2)**2-(dh/2)**2)
    if opened:   # face dianteira do disco = pressao no canal, ~linear em r^2 de p_in (r1) a p2 (r2)
        r1 = d1/2
        F_front = p_in*math.pi*(r1**2-(dh/2)**2) + math.pi*(p_in*(r2**2-r1**2) + (p2-p_in)*(r2**2-r1**2)/2)
        F_eye = 0.0
    else:
        F_front = F_gap(d_sp/2, r2); F_eye = p_in*math.pi*((d_sp/2)**2-(dh/2)**2)
    F_mom = rho*QLa*c1m
    F_ax = F_rear - F_front - F_eye - F_mom             # + = para a succao

    def ring(ro, ri, L, rm, z0):
        m = rm*math.pi*(ro**2-ri**2)*L
        return m, m*(ro**2+ri**2)/2, m*(3*(ro**2+ri**2)+L**2)/12, z0
    def mass(rm):
        parts = [ring(r2, dh/2, p['t_rear'], rm, p['t_rear']/2),
                 ring(dh/2, p['d_shaft']/2, p['L_hub'], rm, p['L_hub']/2 - 3e-3)]
        if opened and p['d_E']:
            parts.append(ring(p['d_E']/2, p['d_E']/2-1.5e-3, p['L_E'], rm, -p['L_E']/2))
        if not opened:
            parts.append(ring(d_sp/2, d_sp/2-1.5e-3, p['L_sp'], rm, -p['L_sp']/2))
            parts.append(ring(r2, d1/2+p['t_front'], p['t_front'], rm, p['t_rear']+b2+p['t_front']/2))
            parts.append(ring(d_sp/2, d_sp/2-1.5e-3, p['L_sp'], rm, p['t_rear']+b2+p['t_front']+p['L_sp']/2))
        bmed = math.radians((beta1['mean']['beta1B']+p['beta2B'])/2)
        Lb = (r2-d1m/2)/math.sin(bmed)
        mb = rm*z_ef*0.5*(p['e1']+p['e2'])*Lb*0.5*(b2+(d1-dh)/2)
        rg2 = (r2**2+(d1m/2)**2)/2
        parts.append((mb, mb*rg2, mb*rg2/2, p['t_rear']+b2/2))
        m = sum(q[0] for q in parts); zc = sum(q[0]*q[3] for q in parts)/m
        Ip = sum(q[1] for q in parts); Id = sum(q[2]+q[0]*(q[3]-zc)**2 for q in parts)
        return dict(m_kg=m, z_cg_mm=zc*1e3, Ip_kgm2=Ip, Id_kgm2=Id, Ip_Id=Ip/Id)
    V_fl = math.pi*(r2**2-(d1m/2)**2)*0.5*(b2+(d1-dh)/2)

    return dict(n=n_rpm, w=w, Q=Q, H=H, nq=nq, Ns_US=nq*51.6, NPSHA=NPSHA, Pu=Pu,
                eta_T391=eta_T391(Q, nq), etah_T396=etah_T396(Q, nq), etah=etah, etav=etav,
                psi=psi, u2=u2, d2=d2, b2=b2, b2s=b2s, z_ef=z_ef, z_out=z_out, slip=gam, tau2=tau2,
                d1=d1, d1m=d1m, dh=dh, c1m=c1m, u1=u1, w1=w1, beta1=beta1, lam_w3=lam_w3,
                NPSH3=NPSH3, nss=nss, F_NPSH=NPSHA/NPSH3, p_in_min=p_in_min,
                c2u=c2u, c2m=c2m, c2=c2, alpha2=alpha2, beta2_flow=beta2_flow, delta2=delta2, w2_w1=w2/w1,
                Hp=Hp, d_sp=d_sp, dH_sp=dH_sp, Qsp=Qsp, Re=Re, kRR=kRR, PRR=PRR, PRR_Pu=PRR/Pu,
                P_shaft=P_shaft, eta=eta, loss=loss, T=P_shaft/w, dT=(P_shaft-Pu)/(mdot*fl['cp']),
                rz=rz, b3=b3, volute=vol, d3q=d3q, A3q=A3q, c3q=c3q, c3q_c2=c3q/c2,
                d_out=d_out, d_suc=d_suc, L_diff=L_diff, FR_bep=FR_bep, FR_0=FR_0, FR_design=FR_design,
                p2=p2, F_rear=F_rear, F_front=F_front, F_eye=F_eye, F_mom=F_mom, F_ax=F_ax,
                m174=mass(7800.0), mal=mass(2810.0), m_fluid=rho*V_fl,
                Ip_fluid=rho*V_fl*(r2**2+(d1m/2)**2)/2, prm=copy.deepcopy(p))

def inducer_optional(R, phi=0.10, nu_ht=0.30):
    """Indutor de reserva: NASA SP-8052 Eq. 65 (SI); Huzel p.178 (phi 0,06-0,10)."""
    Q, n = R['Q'], R['n']
    Dt = (4*Q*60/(math.pi**2*n*phi*(1-nu_ht**2)))**(1/3)
    return dict(D_tip_mm=Dt*1e3, D_hub_mm=nu_ht*Dt*1e3, u_tip=math.pi*Dt*n/60, phi=phi)

def summary(R, tag):
    print(f"--- {tag}: shroud={R['prm']['shroud']} n={R['n']:.0f}")
    print(f" nq={R['nq']:.2f} psi={R['psi']:.3f} u2={R['u2']:.1f} d2={R['d2']*1e3:.2f} b2={R['b2']*1e3:.2f} mm etah={R['etah']:.3f} etav={R['etav']:.3f}")
    print(f" d1={R['d1']*1e3:.2f} d1m={R['d1m']*1e3:.2f} c1m={R['c1m']:.2f} u1={R['u1']:.1f} w1={R['w1']:.1f} lam_w3={R['lam_w3']:.3f} NPSH3={R['NPSH3']:.1f} nss={R['nss']:.0f} F={R['F_NPSH']:.2f} p_in_min={R['p_in_min']/1e5:.2f} bar")
    for k, v in R['beta1'].items(): print(f"   beta1 {k}: d={v['d_mm']:.2f} flow={v['beta1_flow']:.2f} B={v['beta1B']:.2f} tau1={v['tau1']:.3f}")
    print(f" slip={R['slip']:.3f} c2u={R['c2u']:.1f} c2m={R['c2m']:.2f} alpha2={R['alpha2']:.2f} beta2={R['beta2_flow']:.2f} delta2={R['delta2']:.1f} w2/w1={R['w2_w1']:.2f} Hp={R['Hp']:.0f}")
    print(f" Qsp/Q={R['Qsp']/R['Q']:.3f} PRR/Pu={R['PRR_Pu']:.3f} losses={ {k: round(v,2) for k,v in R['loss'].items()} }")
    print(f" P_shaft={R['P_shaft']/1e3:.2f} kW eta={R['eta']:.3f} (T3.9.1 {R['eta_T391']:.3f}) T={R['T']:.2f} Nm dT={R['dT']:.1f} K")
    print(f" volute rz={R['rz']*1e3:.2f} b3={R['b3']*1e3:.2f} d3q={R['d3q']*1e3:.2f} c3q/c2={R['c3q_c2']:.2f} d_out={R['d_out']*1e3:.1f} Ldiff={R['L_diff']*1e3:.0f} d_suc={R['d_suc']*1e3:.1f}")
    print(f" FR={R['FR_bep']:.0f}/{R['FR_0']:.0f} N  Fax={R['F_ax']:.0f} N (rear {R['F_rear']:.0f}, front {R['F_front']:.0f}, eye {R['F_eye']:.0f}) p2={R['p2']/1e5:.1f} bar")
    print(f" mass 17-4PH { {k: round(v,7) for k,v in R['m174'].items()} }")
    print(f" mass Al     { {k: round(v,7) for k,v in R['mal'].items()} }  fluid {R['m_fluid']*1e3:.1f} g Ip_fl={R['Ip_fluid']:.2e}")

def solve_rear_ring(prm, n=N_RPM):
    """Diametro do anel traseiro que zera o empuxo axial (camara interna a ~p_in pelos furos)."""
    f = lambda dE: design(n, {**prm, 'd_E': dE})['F_ax']
    lo, hi = prm['d_hub']+4e-3, 0.050
    return brentq(f, lo, hi) if f(lo)*f(hi) < 0 else None

if __name__ == '__main__':
    import csv
    R0 = design()                                         # semiaberto sem anel (para comparacao)
    dE = solve_rear_ring(BASE)
    BASE2 = {**BASE, 'd_E': round(dE*1e3, 1)/1e3}         # arredonda p/ 0,1 mm
    R = design(prm=BASE2)                                 # BASELINE rev. 2
    Rc = design(prm={**BASE, 'shroud': 'closed'})         # alternativa fechada (anel frontal + traseiro + furos)
    summary(R, 'BASELINE rev.2 (semiaberto + anel traseiro + furos)')
    print(f" d_E={BASE2['d_E']*1e3:.1f} mm  Q_E/Q={R['Qsp']/R['Q']:.3f}  p(r_hub) atras ~ p_in")
    summary(R0, 'semiaberto SEM anel'); summary(Rc, 'FECHADO')
    # empuxo do semiaberto com aletas traseiras (alternativa ao anel)
    kbv, rr2, rrh = 0.85, R0['d2']/2, R0['dh']/2
    F_rear_bv = math.pi*(R0['p2']-FL['rho']*kbv**2*R0['w']**2*rr2**2/2)*(rr2**2-rrh**2) + math.pi*FL['rho']*kbv**2*R0['w']**2/4*(rr2**4-rrh**4)
    F_bv = F_rear_bv - R0['F_front'] - R0['F_mom']
    p_hub_bv = R0['p2'] - FL['rho']*kbv**2*R0['w']**2*(rr2**2-rrh**2)/2
    print(f"aletas traseiras k={kbv}: F_ax={F_bv:.0f} N, p no cubo atras={p_hub_bv/1e5:.1f} bar")
    # residuo do empuxo (06 usa faixa 0,10-0,20 do desbalanceado): sensibilidade a p da camara +-
    for dp_bar in (1.0, 3.0):
        Fres = dp_bar*1e5*math.pi*((BASE2['d_E']/2)**2-(R['dh']/2)**2)
        print(f"  camara +{dp_bar} bar acima de p_in -> F_ax +{Fres:.0f} N")
    print("sensibilidade (baseline):")
    for k, vals in (('s_tip', (0.05e-3, 0.10e-3, 0.15e-3)), ('etah', (0.70, 0.75, 0.80)), ('s_E', (0.05e-3, 0.075e-3, 0.10e-3)),
                    ('beta2B', (22.0, 25.0, 30.0)), ('d_hub', (18e-3, 20e-3, 24e-3))):
        for v in vals:
            r = design(prm={**BASE2, k: v})
            print(f"  {k}={v}: d2={r['d2']*1e3:.1f} d1={r['d1']*1e3:.1f} eta={r['eta']:.3f} P={r['P_shaft']/1e3:.1f} kW F_NPSH={r['F_NPSH']:.2f} Fax={r['F_ax']:.0f} N")
    Q, H, n, w = R['Q'], R['H'], R['n'], R['w']
    psiB = 1.35; u2B = math.sqrt(2*g*H/psiB); d2B = 2*u2B/w
    nq2 = n*math.sqrt(Q)/(H/2)**0.75; psi2 = 1.21*math.exp(-0.77*nq2/100)
    ALT = {
        'A1_fechado_aneis_furos': dict(d2=Rc['d2']*1e3, eta=Rc['eta'], P=Rc['P_shaft']/1e3),
        'A2_semiaberto_anel_tras_furos': dict(d2=R['d2']*1e3, eta=R['eta'], P=R['P_shaft']/1e3),
        'A2b_semiaberto_sem_anel': dict(d2=R0['d2']*1e3, eta=R0['eta'], P=R0['P_shaft']/1e3, F_ax=R0['F_ax']),
        'B_Barske_emissao_parcial': dict(psi=psiB, u2=u2B, d2=d2B*1e3, eta=(0.38, 0.45),
                                         d_throat=math.sqrt(4*Q/(0.8*u2B)/math.pi)*1e3, P=(R['Pu']/0.45/1e3, R['Pu']/0.38/1e3)),
        'C_2_estagios': dict(nq=nq2, d2=2*math.sqrt(2*g*(H/2)/psi2)/w*1e3, eta_T392=eta_T392(Q, nq2), P=R['Pu']/eta_T392(Q, nq2)/1e3),
    }
    print(json.dumps(ALT, indent=1, default=float))
    IND = inducer_optional(R); print("indutor reserva:", IND)
    R60 = design(60000.0, BASE2); print(f"@60k: d2={R60['d2']*1e3:.2f} eta={R60['eta']:.3f} F_NPSH={R60['F_NPSH']:.2f} P={R60['P_shaft']/1e3:.1f}")

    mm = lambda v: round(float(v)*1e3, 3)
    P = BASE2
    geo = {
        "meta": {"component": "fuel_pump", "project": "turbopump-design", "stage": "3_Bomba_JetA", "revision": 2,
                 "units": {"length": "mm", "angle": "deg", "mass": "kg", "inertia": "kg*m^2"},
                 "status": "meanline 1D preliminar; substituir contorno meridional e pas pelo export do CFTurbo",
                 "z_ref": "z_local=0 na face traseira do disco do impeller, + para a succao (no rotor da etapa 5: FP em z 0-18 mm)"},
        "design_point": {"fluid": "Jet A", "rho": FL['rho'], "mdot_kg_s": mdot, "Q_m3_s": round(Q, 7),
                         "H_m": round(H, 1), "n_rpm": N_RPM, "nq": round(R['nq'], 2), "NPSHA_m": round(R['NPSHA'], 1),
                         "NPSH3_est_m": round(R['NPSH3'], 1), "eta_meanline": round(R['eta'], 3), "eta_cycle": 0.55,
                         "P_shaft_meanline_kW": round(R['P_shaft']/1e3, 2), "P_shaft_cycle_kW": round(R['Pu']/0.55/1e3, 2)},
        "inducer": {"present": False, "reserve_design": {k: round(v, 3) for k, v in IND.items()},
                    "trigger": "adicionar se NPSH3 (CFTurbo/teste) > %.0f m ou p_in < %.1f bar" % (R['NPSHA']/1.2, R['p_in_min']/1e5)},
        "impeller": {
            "type": "radial semiaberto (sem disco frontal), simples estagio, entrada axial, em balanco",
            "d_bore_shaft": mm(P['d_shaft']), "d_hub_eye": mm(R['dh']), "d1_eye_tip": mm(R['d1']), "d1m": mm(R['d1m']),
            "d2": mm(R['d2']), "b2": mm(R['b2']), "b1": mm((R['d1']-R['dh'])/2),
            "z_blades": P['z'], "z_splitters": P['z_split'], "L_splitter_frac": P['L_split'],
            "e1_LE": mm(P['e1']), "e2_TE": mm(P['e2']),
            "beta1B_hub": round(R['beta1']['hub']['beta1B'], 2), "beta1B_mean": round(R['beta1']['mean']['beta1B'], 2),
            "beta1B_tip": round(R['beta1']['tip']['beta1B'], 2), "beta2B": P['beta2B'],
            "t_rear_disk": mm(P['t_rear']), "L_hub": mm(P['L_hub']),
            "s_tip_axial": mm(P['s_tip']), "sax_rear_gap": mm(P['sax_r2']*R['d2']/2),
            "rear_ring": {"d_E": mm(P['d_E']), "s_radial": mm(P['s_E']), "N_teeth": P['N_E'], "L": mm(P['L_E']),
                          "balance_holes": "furos no disco entre d_hub e d_E, ventilando a camara a ~p_in (dimensionar p/ Q_E)"},
            "meridional_simple": {"L_ax": mm(R['b2'] + 0.6*(R['d1']-R['dh'])),
                                  "R_shroud_arc": mm(0.5*(R['d1']-R['dh'])), "R_hub_arc": mm(0.8*(R['d1']-R['dh']))}},
        "volute": {"type": "espiral simples, secao circular, 360 graus", "d_cutwater": mm(2*R['rz']), "b3": mm(R['b3']),
                   "sections": [{"eps_deg": v['eps_deg'], "d_section": round(v['d_section'], 3), "r_center": round(v['r_center'], 3)} for v in R['volute']],
                   "d_throat": mm(R['d3q']), "diffuser_cone_total_deg": P['cone_deg'], "diffuser_L": mm(R['L_diff']),
                   "d_discharge": mm(R['d_out'])},
        "suction": {"d_suction_flange": mm(R['d_suc'])},
        "loads": {"F_axial_N_to_suction": round(R['F_ax']), "F_axial_no_ring_N": round(R0['F_ax']),
                  "F_radial_nominal_N": round(R['FR_bep']), "F_radial_shutoff_N": round(R['FR_0']),
                  "F_radial_design_N": round(R['FR_design']), "torque_meanline_Nm": round(R['T'], 2),
                  "torque_cycle_Nm": round(R['Pu']/0.55/R['w'], 2)},
        "rotordynamics": {"impeller_17-4PH": {k: round(v, 9) for k, v in R['m174'].items()},
                          "impeller_Al7075-T73": {k: round(v, 9) for k, v in R['mal'].items()},
                          "entrained_fluid": {"m_kg": round(R['m_fluid'], 5), "Ip_kgm2": round(R['Ip_fluid'], 9)},
                          "blade_passing_Hz": {"full_blades": round(P['z']*N_RPM/60), "with_splitters": round((P['z']+P['z_split'])*N_RPM/60)}},
        "alternative_closed": {"d2": mm(Rc['d2']), "b2": mm(Rc['b2']), "d1": mm(Rc['d1']), "d_rings": mm(Rc['d_sp']),
                               "s_seal": mm(BASE['s_sp']), "N_lab": BASE['N_lab'], "eta": round(Rc['eta'], 3),
                               "m_17-4PH_kg": round(Rc['m174']['m_kg'], 4)},
    }
    json.dump(geo, open('fuel_pump_geometry.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    json.dump({'baseline': R, 'semiaberto_sem_anel': R0, 'closed': Rc, 'alt': ALT}, open('etapa3_raw.json', 'w', encoding='utf-8'),
              indent=1, default=float, ensure_ascii=False)
    rows = [("secao", "campo", "valor", "unidade"),
            ("design_point", "Q", round(Q*1e3, 4), "L/s"), ("design_point", "H", round(H, 1), "m"),
            ("design_point", "n", N_RPM, "rpm"), ("design_point", "rho", FL['rho'], "kg/m3"),
            ("design_point", "nu", round(FL['mu']/FL['rho']*1e6, 3), "mm2/s"), ("design_point", "p_v", FL['pv']/1e3, "kPa"),
            ("design_point", "NPSHA", round(R['NPSHA'], 1), "m"),
            ("design_point", "eta_h_est", round(R['etah'], 3), "-"), ("design_point", "eta_v_est", round(R['etav'], 3), "-"),
            ("main_dim", "d_shaft", mm(P['d_shaft']), "mm"), ("main_dim", "d_hub", mm(R['dh']), "mm"),
            ("main_dim", "d1", round(R['d1']*1e3, 2), "mm"), ("main_dim", "d2", round(R['d2']*1e3, 2), "mm"),
            ("main_dim", "b2", round(R['b2']*1e3, 2), "mm"), ("main_dim", "psi", round(R['psi'], 3), "-"),
            ("main_dim", "shroud", "open", "-"), ("main_dim", "tip_clearance", mm(P['s_tip']), "mm"),
            ("blades", "z_full", P['z'], "-"), ("blades", "z_splitter", P['z_split'], "-"),
            ("blades", "splitter_length_frac", P['L_split'], "-"), ("blades", "e_LE", mm(P['e1']), "mm"), ("blades", "e_TE", mm(P['e2']), "mm"),
            ("blades", "beta1B_hub", round(R['beta1']['hub']['beta1B'], 2), "deg"), ("blades", "beta1B_mean", round(R['beta1']['mean']['beta1B'], 2), "deg"),
            ("blades", "beta1B_shroud", round(R['beta1']['tip']['beta1B'], 2), "deg"), ("blades", "incidence", P['i1_deg'], "deg"),
            ("blades", "beta2B", P['beta2B'], "deg"),
            ("volute", "type", "single spiral 360 circular", "-"), ("volute", "d_cutwater", round(2*R['rz']*1e3, 2), "mm"),
            ("volute", "b3", round(R['b3']*1e3, 2), "mm"), ("volute", "A_throat", round(R['A3q']*1e6, 2), "mm2"),
            ("volute", "d_throat", round(R['d3q']*1e3, 2), "mm"), ("volute", "diffuser_cone_total", P['cone_deg'], "deg"),
            ("volute", "d_discharge", round(R['d_out']*1e3, 2), "mm"), ("suction", "d_suction", round(R['d_suc']*1e3, 2), "mm"),
            ("rear", "d_rear_ring", mm(P['d_E']), "mm"), ("rear", "s_rear_ring", mm(P['s_E']), "mm")]
    with open('cfturbo_fuel_pump_inputs.csv', 'w', newline='', encoding='utf-8') as fp:
        csv.writer(fp).writerows(rows)
