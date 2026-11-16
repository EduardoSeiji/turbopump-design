"""Consolida os resultados das etapas 1-5 num unico arquivo de parametros.

Le os JSON gerados por cada etapa e grava:
  docs/parametros_mestres.json  (para scripts: CAD, rotodinamica)
  docs/parametros_mestres.md    (para leitura)

Nenhum numero e digitado aqui, exceto os requisitos de entrada (REQ).
Rode de novo sempre que uma etapa for refeita:
    python tools/consolidar_parametros.py
"""
import json
import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"

# Requisitos de entrada (docs/requisitos.md)
REQ = {
    "OP": {"fluido": "HTP 90 %", "mdot_kg_s": 17.5, "p_in_bar": 5.0, "p_out_bar": 235.0, "T_in_K": 300.0},
    "FP": {"fluido": "Jet A", "mdot_kg_s": 2.5, "p_in_bar": 5.0, "p_out_bar": 135.0, "T_in_K": 300.0},
    "turbina": {"p_in_bar": 150.0, "T_in_K": 1150.0, "p_out_bar": 130.0, "mdot_kg_s": 17.5},
    "p_camara_bar": 100.0,
}


def ler(rel):
    return json.loads((RAIZ / rel).read_text(encoding="utf-8"))


def f(x, nd=1):
    """Formata numero com virgula decimal."""
    return f"{x:.{nd}f}".replace(".", ",")


def main():
    e1 = ler("1_Rotacao_e_Arranjo/resultados_etapa1.json")
    e2 = ler("2_Bomba_HTP/etapa2_bomba_htp.json")
    e3 = ler("3_Bomba_JetA/fuel_pump_geometry.json")
    e4 = ler("4_Turbina/etapa4_turbina.json")
    e5 = ler("5_Eixo_Mancais_Selos/etapa5_eixo_mancais.json")

    n = e5["operacao"]["n_rpm"]
    omega = n * math.pi / 30.0
    ind, imp, vol, perf = e2["inducer"], e2["impeller"], e2["volute"], e2["performance"]
    fdp, fimp, fvol = e3["design_point"], e3["impeller"], e3["volute"]
    tb, tg, tgeo, trot = e4["balanco"], e4["estagio"], e4["geometria"], e4["rotor"]
    rot, crit = e5["rotor"], e5["critica"]

    m = {
        "meta": {
            "projeto": "turbopump-design",
            "descricao": "Parametros consolidados das etapas 1-5 (meanline 1D, preliminar)",
            "gerado_por": "tools/consolidar_parametros.py",
            "unidades": "SI; mm, graus, rpm, bar e kW onde indicado no nome",
        },
        "requisitos": REQ,
        "operacao": {
            "n_rpm": n,
            "omega_rad_s": omega,
            "arranjo": e1["decisao"]["arranjo"],
            "criterio_cavitacao_OP": e1["decisao"]["criterio_cavitacao"],
            "P_OP_kW": perf["P_shaft_kW"],
            "P_FP_kW": fdp["P_shaft_cycle_kW"],
            "P_turbina_requerida_kW": tb["P_req_kW"],
            "P_turbina_disponivel_kW": tb["P_disp_kW"],
            "margem_potencia_turbina": tb["margem"],
            "torque_Nm": e5["operacao"]["torques_nominais_Nm"],
            "torque_projeto_Nm": e5["operacao"]["torques_projeto_Nm"],
        },
        "bomba_OP": {
            "ponto": e2["ponto"],
            "indutor": ind,
            "impeller": imp,
            "voluta": {k: v for k, v in vol.items() if k != "single_alternative"},
            "desempenho": perf,
            "cargas": e2["loads"],
            "massa_inercia": e2["mass_inertia_Al6061"],
        },
        "bomba_FP": {
            "ponto": fdp,
            "indutor": e3["inducer"],
            "impeller": fimp,
            "voluta": fvol,
            "cargas": e3["loads"],
            "massa_inercia": e3["rotordynamics"],
        },
        "turbina": {
            "gas": e4["gas"],
            "balanco": tb,
            "estagio": tg,
            "geometria": tgeo,
            "escoamento": e4["escoamento"],
            "tensoes": e4["tensoes"],
            "rotor": trot,
            "cargas": e4["cargas"],
        },
        "rotor": {
            "z_ref": e5["meta"]["z_ref"],
            "eixo": e5["eixo"],
            "pecas": rot["pecas"],
            "eixo_massa": rot["eixo"],
            "total": rot["total"],
            "mancais": e5["mancais"],
            "selos": e5["selos"],
            "empuxo_axial_N": e5["empuxo_axial_N"],
            "empuxo_radial": e5["empuxo_radial"],
            "critica": crit,
        },
    }
    DOCS.mkdir(exist_ok=True)
    (DOCS / "parametros_mestres.json").write_text(
        json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---------------- markdown ----------------
    L = []
    w = L.append
    w("# Parâmetros mestres — turbopump-design")
    w("")
    w("> Arquivo **gerado** por `tools/consolidar_parametros.py` a partir dos JSON das etapas 1–5.")
    w("> Não edite à mão: refaça a etapa e rode o script de novo. Versão para scripts: `parametros_mestres.json`.")
    w("> Status: dimensionamento meanline (1D, numa linha média do escoamento), preliminar, ainda sem validação no CFTurbo.")
    w("")
    w("## 1. Operação")
    w("| Grandeza | Valor |")
    w("|---|---|")
    w(f"| Rotação nominal n | {n:.0f} rpm (ω = {omega:.0f} rad/s) |")
    w(f"| Potência de eixo, bomba de oxidante (OP) | {f(perf['P_shaft_kW'])} kW (η = {f(perf['eta_pump'], 3)}) |")
    w(f"| Potência de eixo, bomba de combustível (FP) | {f(fdp['P_shaft_cycle_kW'])} kW (η = {f(fdp['eta_cycle'], 2)}) |")
    w(f"| Potência requerida da turbina | {f(tb['P_req_kW'])} kW (η mecânica {f(e4['inputs']['eta_mec'], 2)}) |")
    w(f"| Potência disponível da turbina | {f(tb['P_disp_kW'])} kW (margem +{tb['margem'] * 100:.0f} %) |")
    tq = e5["operacao"]["torques_nominais_Nm"]
    w(f"| Torque nominal FP / OP / turbina | {f(tq['FP'])} / {f(tq['OP'])} / {f(tq['turbina'])} N·m |")
    w(f"| Torque de projeto no trecho OP → turbina | {f(e5['operacao']['torques_projeto_Nm']['OP-T'])} N·m |")
    w("")
    w("## 2. Bomba de oxidante (OP, HTP 90 %)")
    p = e2["ponto"]
    w("| Grandeza | Valor |")
    w("|---|---|")
    w(f"| Vazão útil Q / altura H | {f(p['Q_util_m3s'] * 1000, 1)} L/s / {f(p['H_m'], 0)} m |")
    w(f"| Velocidade específica n_q | {f(p['nq'])} |")
    w(f"| NPSH disponível / admissível | {f(p['NPSHA_m'])} / {f(p['NPSH3_adm_m'])} m |")
    w(f"| Indutor: Ø ponta entrada → saída / cubo | {f(ind['D_tip_inlet_mm'])} → {f(ind['D_tip_exit_mm'])} / {f(ind['d_hub_mm'])} mm |")
    w(f"| Indutor: pás / passo / comprimento axial | {ind['z']} / {f(ind['lead_mm'])} mm / {f(ind['L_axial_mm'])} mm |")
    w(f"| Indutor: ângulo de pá na ponta β1B / número de cavitação K | {f(ind['beta1B_tip_deg'])}° / {f(ind['K_op'], 4)} (limite {f(ind['K_lim'], 3)}) |")
    w(f"| Indutor: altura gerada | {f(ind['H_m'])} m |")
    w(f"| Impeller: d2 / b2 / d1 | {f(imp['d2_mm'], 2)} / {f(imp['b2_mm'], 2)} / {f(imp['d1_mm'])} mm |")
    w(f"| Impeller: pás / β1B (shroud, cubo) / β2B | {imp['z']} / {f(imp['beta1B_shroud_deg'])}°, {f(imp['beta1B_hub_deg'])}° / {f(imp['beta2B_deg'])}° |")
    w(f"| Impeller: u2 / coeficiente de pressão ψ | {f(imp['u2'])} m/s / {f(imp['psi'], 3)} |")
    w(f"| Anéis de desgaste (frente e trás) | Ø{f(imp['d_wear_ring_mm'], 0)} mm, folga {f(imp['wear_ring_clearance_mm'], 2)} mm |")
    w(f"| Voluta | {vol['baseline']}; garganta Ø{f(vol['double']['d3q_mm'], 2)} mm cada |")
    w(f"| Empuxo radial nominal / de projeto | {f(e2['loads']['FR_double_N'], 0)} / {f(e2['loads']['FR_design_kR015_N'], 0)} N |")
    w("")
    w("## 3. Bomba de combustível (FP, Jet A)")
    w("| Grandeza | Valor |")
    w("|---|---|")
    w(f"| Vazão Q / altura H | {f(fdp['Q_m3_s'] * 1000, 1)} L/s / {f(fdp['H_m'], 0)} m |")
    w(f"| Velocidade específica n_q | {f(fdp['nq'])} |")
    w(f"| NPSH disponível / NPSH3 estimado | {f(fdp['NPSHA_m'])} / {f(fdp['NPSH3_est_m'])} m (sem indutor) |")
    w(f"| Tipo | {fimp['type']} |")
    w(f"| Impeller: d2 / b2 / d1 | {f(fimp['d2'], 2)} / {f(fimp['b2'], 2)} / {f(fimp['d1_eye_tip'])} mm |")
    w(f"| Impeller: pás + splitters / β1B (cubo, ponta) / β2B | {fimp['z_blades']} + {fimp['z_splitters']} / {f(fimp['beta1B_hub'])}°, {f(fimp['beta1B_tip'])}° / {f(fimp['beta2B'])}° |")
    w(f"| Furo do eixo / cubo no olho | {f(fimp['d_bore_shaft'], 0)} / {f(fimp['d_hub_eye'], 0)} mm |")
    w(f"| Anel traseiro de balanceamento | Ø{f(fimp['rear_ring']['d_E'])} mm, folga {f(fimp['rear_ring']['s_radial'], 2)} mm |")
    w(f"| Voluta | {fvol['type']}; garganta Ø{f(fvol['d_throat'], 2)} mm |")
    w(f"| Empuxo radial nominal / de projeto | {e3['loads']['F_radial_nominal_N']} / {e3['loads']['F_radial_design_N']} N |")
    w("")
    w("## 4. Turbina")
    w("| Grandeza | Valor |")
    w("|---|---|")
    w(f"| Tipo | {tg['tipo']} |")
    w(f"| Gás (HTP 90 % decomposto): cp / γ / R | {f(e4['gas']['cp'], 0)} J/(kg·K) / {f(e4['gas']['gamma'], 3)} / {f(e4['gas']['R'])} J/(kg·K) |")
    w(f"| Razão de pressões / queda isentrópica | {f(tb['PR'], 3)} / {f(tb['dh_is_kJkg'])} kJ/kg |")
    w(f"| Grau de reação / ψ / φ | {f(tg['R'], 2)} / {f(tg['psi'], 2)} / {f(tg['phi'], 2)} |")
    w(f"| Eficiência total-estática estimada / mínima necessária | {f(tg['eta_ts'], 3)} / {f(tb['eta_min'], 3)} |")
    w(f"| Diâmetro médio / ponta / raiz | {f(tgeo['Dm_mm'])} / {f(tgeo['d_tip_mm'])} / {f(tgeo['d_root_mm'])} mm |")
    w(f"| Altura de pá estator / rotor | {f(tgeo['h_stator_mm'])} / {f(tgeo['h_rotor_mm'])} mm |")
    w(f"| Bocais / pás do rotor | {tgeo['z_stator']} / {tgeo['z_rotor']} |")
    w(f"| Ângulos α2 / β3 (medidos do eixo) | {f(tg['alpha2'])}° / {f(tg['beta3'])}° |")
    w(f"| Velocidade periférica média / na ponta | {f(tgeo['u'])} / {f(e4['tensoes']['u_tip'])} m/s |")
    w(f"| Tensão na raiz da pá (estimada) | {f(e4['tensoes']['sigma_total_MPa'], 0)} MPa |")
    w("")
    w("## 5. Rotor (entrada para a rotodinâmica)")
    w(f"Referência axial: {e5['meta']['z_ref']}.")
    w("")
    w("### 5.1 Eixo")
    w(f"Material {e5['eixo']['material']}, E = {e5['eixo']['E_Pa'] / 1e9:.0f} GPa, ρ = {e5['eixo']['rho']:.0f} kg/m³.")
    w("")
    w("| z inicial [mm] | z final [mm] | Ø [mm] |")
    w("|---|---|---|")
    for a, b, d in e5["eixo"]["segmentos_mm"]:
        w(f"| {a:g} | {b:g} | {d:g} |")
    w("")
    w("### 5.2 Peças montadas")
    w("Ip = momento de inércia polar (em torno do eixo de rotação); Id = diametral (transversal), no centro de massa da própria peça.")
    w("")
    w("| Peça | Material | m [g] | z do CG [mm] | Ip [kg·mm²] | Id [kg·mm²] |")
    w("|---|---|---|---|---|---|")
    for pc in rot["pecas"]:
        w(f"| {pc['nome']} | {pc['material']} | {f(pc['m_kg'] * 1e3)} | {f(pc['z_cg_mm'])} | "
          f"{f(pc['Ip_kgm2'] * 1e6)} | {f(pc['Id_kgm2'] * 1e6)} |")
    ex, tot = rot["eixo"], rot["total"]
    w(f"| Eixo (distribuído) | {e5['eixo']['material']} | {f(ex['m_kg'] * 1e3)} | {f(ex['z_cg_mm'])} | {f(ex['Ip_kgm2'] * 1e6)} | — |")
    w(f"| **Rotor total** | | **{f(tot['m_kg'] * 1e3, 0)}** | **{f(tot['z_cg_mm'])}** | **{f(tot['Ip_kgm2'] * 1e6, 0)}** | "
      f"**{f(tot['Id_cg_kgm2'] * 1e6, 0)}** (no CG do rotor) |")
    w("")
    w("### 5.3 Mancais")
    b1, b2 = e5["mancais"]["B1"], e5["mancais"]["B2"]
    w("| Mancal | Tipo | Posição z [mm] | Furo [mm] | Refrigeração |")
    w("|---|---|---|---|---|")
    w(f"| B1 | {b1['tipo']} | {b1['z_fileiras_mm'][0]} e {b1['z_fileiras_mm'][1]} | {b1['bore_mm']} | {b1['refrigeracao']} |")
    w(f"| B2 | {b2['tipo']} | {b2['z_mm']} | {b2['bore_mm']} | {b2['refrigeracao']} |")
    w("")
    w(f"DN (furo em mm × rpm) = {e5['mancais']['DN'] / 1e6:.2f}·10⁶.".replace(".", ",", 1))
    w("")
    w("### 5.4 Cargas")
    er = e5["empuxo_radial"]
    w("| Caso | F radial FP [N] | F radial OP [N] | Reação B1 [N] | Reação B2 [N] |")
    w("|---|---|---|---|---|")
    for nome, c in er.items():
        w(f"| {nome} | {c['F_FP']:.0f} | {c['F_OP']:.0f} | {c['R_B1']:.0f} | {c['R_B2']:.0f} |")
    ea = e5["empuxo_axial_N"]
    w("")
    w(f"Empuxo axial líquido: **{ea['liquido']:.0f} N** (sinal negativo = em direção à FP), com o escape da turbina saindo para +z. "
      f"Se o escape sair para −z, o valor passa a {ea['se_escape_turbina_menos_z']:.0f} N (ver `pendencias_e_decisoes.md`).")
    w("")
    w("### 5.5 Primeira velocidade crítica")
    w("Modelo de viga de Euler-Bernoulli em elementos finitos, com efeito giroscópico dos discos, precessão direta síncrona.")
    w("")
    w("| Rigidez B1 / B2 [MN/m] | 1ª crítica [rpm] | Razão crítica / nominal |")
    w("|---|---|---|")
    for c in crit["k_sweep"]:
        k1, k2 = c["k_B1"], c["k_B2"]
        rot_k = "rígidos" if (k1 is None or k1 >= 1e10) else f"{k1 / 1e6:.0f} / {k2 / 1e6:.0f}"
        w(f"| {rot_k} | {c['n_c_rpm']:.0f} | {f(c['n_c_rpm'] / n, 2)} |")
    w("")
    w("Frequências naturais com o rotor parado (mancais 50/100 MN/m): "
      + ", ".join(f"{x:.0f}" for x in crit["f_nao_girando_Hz"]) + " Hz.")
    w("")
    (DOCS / "parametros_mestres.md").write_text("\n".join(L), encoding="utf-8")
    print("Gravado: docs/parametros_mestres.json e docs/parametros_mestres.md")


if __name__ == "__main__":
    main()
