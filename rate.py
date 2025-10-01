import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Permeability Estimator (Radial Flow)")

st.markdown("""
This app estimates permeability k (mD) using the radial flow equation:

\[
k = \dfrac{162.6 \; q \; \mu \; B \; (\ln(r_e/r_w) + s)}{h \; (p_e - p_{wf})}
\]
""")

# --- Inputs ---
q = st.number_input("Flow rate q (STB/day)", value=500.0)
pe = st.number_input("Reservoir pressure Pe (psi)", value=2000.0)
pwf = st.number_input("Bottomhole flowing pressure Pwf (psi)", value=1000.0)
h = st.number_input("Layer thickness h (ft)", value=20.0)
mu = st.number_input("Viscosity μ (cP)", value=1.0)
B = st.number_input("Formation volume factor B (RB/STB)", value=1.0)
re = st.number_input("Drainage radius re (ft)", value=1000.0)
rw = st.number_input("Wellbore radius rw (ft)", value=0.333)
skin = st.number_input("Skin factor s", value=0.0)

# --- Permeability calculation ---
delta_p = pe - pwf
if delta_p <= 0:
    st.error("Pe must be greater than Pwf")
else:
    k = (162.6 * q * mu * B * (np.log(re/rw) + skin)) / (h * delta_p)
    st.success(f"Estimated Permeability: **{k:.2f} mD**")

# --- Sensitivity Analysis ---
st.header("Sensitivity Analysis")

options = st.multiselect(
    "Select parameters to vary:",
    ["Flow rate (q) (STB/day)", "Layer thickness (h) (ft)", "Formation volume factor (B) (RB/STB)", 
     "Drainage radius (re)", "Viscosity (μ)", "ΔP (Pe-Pwf)", "Reservoir Pressure (Pe)", 
     "Bottomhole Flowing Pressure (Pwf)", "Skin (s)"],
    default=["Drainage radius (re)"]
)

fig, ax = plt.subplots()

if "Drainage radius (re)" in options:
    re_range = np.linspace(200, 5000, 50)
    k_values = (162.6 * q * mu * B * (np.log(re_range/rw) + skin)) / (h * delta_p)
    ax.plot(re_range, k_values, label="Sensitivity to re")

if "Viscosity (μ)" in options:
    mu_range = np.linspace(0.2, 5, 50)
    k_values = (162.6 * q * mu_range * B * (np.log(re/rw) + skin)) / (h * delta_p)
    ax.plot(mu_range, k_values, label="Sensitivity to μ")

if "ΔP (Pe-Pwf)" in options:
    dp_range = np.linspace(100, 3000, 50)
    k_values = (162.6 * q * mu * B * (np.log(re/rw) + skin)) / (h * dp_range)
    ax.plot(dp_range, k_values, label="Sensitivity to ΔP")

if "Reservoir Pressure (Pe)" in options:
    pe_range = np.linspace(pwf+100, 5000, 50)
    k_values = (162.6 * q * mu * B * (np.log(re/rw) + skin)) / (h * (pe_range - pwf))
    ax.plot(pe_range, k_values, label="Sensitivity to Pe")

if "Bottomhole Flowing Pressure (Pwf)" in options:
    pwf_range = np.linspace(100, pe-50, 50)
    k_values = (162.6 * q * mu * B * (np.log(re/rw) + skin)) / (h * (pe - pwf_range))
    ax.plot(pwf_range, k_values, label="Sensitivity to Pwf")

if "Skin (s)" in options:
    s_range = np.linspace(-5, 20, 50)
    k_values = (162.6 * q * mu * B * (np.log(re/rw) + s_range)) / (h * delta_p)
    ax.plot(s_range, k_values, label="Sensitivity to Skin")

if "Flow rate (q) (STB/day)" in options:
    q_range = np.linspace(100, 4000, 50)
    k_values = (162.6 * q_range * mu * B * (np.log(re/rw) + skin)) / (h * delta_p)
    ax.plot(q_range, k_values, label="Sensitivity to q")

if "Layer thickness (h) (ft)" in options:
    h_range = np.linspace(5, 100, 50)
    k_values = (162.6 * q * mu * B * (np.log(re/rw) + skin)) / (h_range * delta_p)
    ax.plot(h_range, k_values, label="Sensitivity to h")

ax.set_xlabel("Parameter Value")
ax.set_ylabel("Permeability (mD)")
ax.legend()
ax.grid(True)
st.pyplot(fig)