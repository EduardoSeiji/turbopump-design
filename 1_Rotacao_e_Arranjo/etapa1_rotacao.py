"""
turbopump-design — Etapa 1: rotação do eixo único
Limites: cavitação (n_ss), velocidade específica (n_q), velocidade periférica (u2, u1t),
DN dos mancais e tensão torcional do eixo.
Unidades SI; n em rpm. Referências entre colchetes.
"""
import numpy as np

g = 9.81

# ---------------- Propriedades PROVISÓRIAS (Etapa 0 não encontrada) ----------------
pumps = {
    # rho [kg/m3], pv [Pa] (conservador), mdot [kg/s], p_in [Pa] (total), dp [Pa]
    "OP (HTP 90%)": dict(rho=1385.0, pv=500.0, mdot=17.5, p_in=5e5, dp=230e5),
    "FP (Jet A)":   dict(rho=795.0,  pv=1000.0, mdot=2.5, p_in=5e5, dp=130e5),
}

F_NPSH = 1.20          # margem NPSHA/NPSH3 (premissa; rocket expendable, sem TSH)
NSS = {                # n_ss métrico [rpm, m3/s, m]  (US: N_ss = n_ss/0.0194) [Gülich Eq. T3.4.18]
    "sem indutor (impeller de alta pressão)": 200.0,   # Gülich Tab. D6.1: 160–190 (u1>50 m/s); Huzel: ~10 000 US
    "indutor conservador (~26k US)": 500.0,             # Huzel p.176: 20k–50k US com indutor
    "indutor agressivo (~35k US)": 680.0,
}

def ns_US(nss): return nss / 0.0194

def eta_gulich(Q, nq):
    """Gülich Tab. 3.9, Eq. T3.9.1 (bomba radial, simples estágio, entrada simples). Q_ref = 1 m3/s."""
    a = 1.0
    # rev.2: expoente 0,1 (T3.9.1); a v1 usava 0,08 (é o da T3.9.6, η hidráulico). Válida p/ Q ≥ 0,005 m³/s.
    m = 0.1 * a * (1.0 / Q) ** 0.15 * (45.0 / nq) ** 0.06
    return 1 - 0.095 * (1.0 / Q) ** m - 0.3 * (0.35 - np.log10(nq / 23.0)) ** 2 * (1.0 / Q) ** 0.05

print("=" * 78)
print("1) PONTO DE PROJETO E NPSHA")
for k, p in pumps.items():
    p["Q"] = p["mdot"] / p["rho"]
    p["H"] = p["dp"] / (p["rho"] * g)
    p["NPSHA"] = (p["p_in"] - p["pv"]) / (p["rho"] * g)         # Gülich Eq. 6.3 / Huzel Eq. 6-6
    p["NPSH3_adm"] = p["NPSHA"] / F_NPSH
    print(f"{k:14s} Q={p['Q']*1e3:6.2f} L/s  H={p['H']:6.0f} m  NPSHA={p['NPSHA']:5.1f} m  "
          f"NPSH3,adm={p['NPSH3_adm']:5.1f} m  P_hid={p['Q']*p['dp']/1e3:5.1f} kW")

print("=" * 78)
print("2) ROTAÇÃO MÁXIMA POR CAVITAÇÃO  n = n_ss·NPSH3^0.75/√Q   [Gülich Eq. T15.1.1]")
nmax = {}
for k, p in pumps.items():
    for lab, nss in NSS.items():
        n = nss * p["NPSH3_adm"] ** 0.75 / np.sqrt(p["Q"])
        nmax[(k, lab)] = n
        nq = n * np.sqrt(p["Q"]) / p["H"] ** 0.75
        print(f"{k:14s} {lab:40s} n_ss={nss:4.0f} (S={ns_US(nss):6.0f} US)  "
              f"n_max={n:8.0f} rpm  n_q={nq:5.1f}")

def at_speed(n, verbose=True, phi_ind=0.10, nu_ind=0.30):
    """Avalia ambos os pumps numa rotação n."""
    w = 2 * np.pi * n / 60
    out, P_tot = {}, 0.0
    for k, p in pumps.items():
        Q, H = p["Q"], p["H"]
        nq = n * np.sqrt(Q) / H ** 0.75                              # Gülich Eq. 2.5
        psi = 1.21 * np.exp(-0.77 * nq / 100)                        # Gülich Eq. 3.26 (ψ = 2gH/u2²)
        u2 = np.sqrt(2 * g * H / psi)
        d2 = 60 * u2 / (np.pi * n)
        eta = eta_gulich(Q, nq)
        P = Q * p["dp"] / eta
        P_tot += P
        # indutor: diâmetro de ponta p/ φ (coef. de vazão) e ν (hub/tip) dados [NASA SP-8052 Eq. 65 em SI]
        Dt = (4 * Q * 60 / (np.pi ** 2 * n * phi_ind * (1 - nu_ind ** 2))) ** (1 / 3)
        ut = np.pi * n * Dt / 60
        sigma = 2 * g * p["NPSH3_adm"] / ut ** 2                     # Gülich Eq. T3.4.11
        nss_req = n * np.sqrt(Q) / p["NPSH3_adm"] ** 0.75
        # NPSH que o impeller (n_ss=200) precisa -> head mínimo do indutor
        NPSH_imp = (n * np.sqrt(Q) / 200.0) ** (4 / 3)                # Gülich Eq. T15.1.2
        H_ind = max(NPSH_imp - p["NPSHA"], 0) * 1.2
        psi_ind = 2 * g * H_ind / ut ** 2
        out[k] = dict(nq=nq, psi=psi, u2=u2, d2=d2, eta=eta, P=P, Dt=Dt, ut=ut,
                      sigma=sigma, nss_req=nss_req, H_ind=H_ind, psi_ind=psi_ind)
    T = P_tot / w
    tau_adm = 150e6                         # premissa: Inconel 718 / 17-4PH, com fator p/ concentração
    d_tors = (16 * T / (np.pi * tau_adm)) ** (1 / 3)                 # Huzel Eq. 6-33
    d_bear = max(1.5 * d_tors, 0.012)       # rigidez manda (NASA SP-8100 §2.1.1.3): 1,5×torção (premissa)
    DN = d_bear * 1e3 * n
    out["shaft"] = dict(P_tot=P_tot, T=T, d_tors=d_tors, d_bear=d_bear, DN=DN)
    return out

print("=" * 78)
print("3) VARREDURA EM ROTAÇÃO")
hdr = (" n[rpm]  | OP: nq   ψ    u2[m/s] d2[mm] η    nss_req u1t[m/s] Dt[mm] ψ_ind |"
       " FP: nq   u2   d2[mm] η    | P[kW] T[Nm] d_t[mm] d_b[mm] DN[1e6]")
print(hdr)
for n in [30e3, 40e3, 45e3, 50e3, 55e3, 60e3, 65e3, 70e3, 80e3]:
    r = at_speed(n)
    o, f, s = r["OP (HTP 90%)"], r["FP (Jet A)"], r["shaft"]
    print(f"{n:8.0f} | {o['nq']:5.1f} {o['psi']:5.2f} {o['u2']:6.0f} {o['d2']*1e3:6.1f} {o['eta']:4.2f} "
          f"{o['nss_req']:6.0f} {o['ut']:7.0f} {o['Dt']*1e3:6.1f} {o['psi_ind']:5.2f} | "
          f"{f['nq']:5.1f} {f['u2']:5.0f} {f['d2']*1e3:5.1f} {f['eta']:4.2f} | "
          f"{s['P_tot']/1e3:5.0f} {s['T']:5.1f} {s['d_tors']*1e3:5.1f} {s['d_bear']*1e3:6.1f} {s['DN']/1e6:5.2f}")

print("=" * 78)
print("4) LIMITES DE VELOCIDADE PERIFÉRICA (disco girante, Gülich Eq. T14.1.10 / Timoshenko)")
# σ_t,max no furo de disco de espessura constante ≈ (3+ν)/4 · ρ u²  (disco furado, furo pequeno)
for mat, rho_m, sy, nu in [("Al 6061-T6 (HTP ok)", 2700, 276e6, 0.33),
                           ("Al 7075-T73 (HTP: verificar)", 2810, 435e6, 0.33),
                           ("Inconel 718 (Jet A)", 8190, 1030e6, 0.29),
                           ("17-4PH H1025 (Jet A)", 7800, 1000e6, 0.27)]:
    SF = 1.5
    u_furo = np.sqrt(4 * sy / SF / ((3 + nu) * rho_m))
    u_macico = np.sqrt(8 * sy / SF / ((3 + nu) * rho_m))
    print(f"  {mat:30s} u_adm: furado {u_furo:4.0f} m/s | maciço {u_macico:4.0f} m/s  (SF={SF} no escoamento)")
print("  Huzel Tab. 6-5: Inco 718 forjado em LOX ~274 m/s; Al 357 fundido em LH2 ~363 m/s")
print("  DN: Huzel p.209: 1,6e6 (Conrad/rolos), 2,1e6 (contato angular); NASA SP-8100 Tab. I: 1,0–2,0e6")
