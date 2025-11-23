import skrf as rf
import numpy as np

def deembed_s2p(meas_s2p_path, ant_input, output_s2p_path, z0=50.0):
    # Load measured S2P file
    ntw_meas = rf.Network(meas_s2p_path)
    freqs = ntw_meas.f
    n_freq = len(freqs)
    
    # Handle antenna input (S1P file or complex impedance)
    if isinstance(ant_input, str) and ant_input.lower().endswith('.s1p'):
        ntw_ant = rf.Network(ant_input)
        if len(ntw_ant.f) != n_freq:
            raise ValueError("S1P frequencies must match S2P")
        z_ant = ntw_ant.z[:, 0, 0]  # Extract Z11
    else:
        try:
            z_ant_val = complex(ant_input)
            z_ant = np.full(n_freq, z_ant_val)
        except ValueError:
            raise ValueError("ant_input must be complex number or .s1p file")
    
    # Initialize output S-matrix
    s_intrinsic = np.zeros((n_freq, 2, 2), dtype=complex)
    
    # De-embed using Y-matrix
    for i in range(n_freq):
        y_meas = ntw_meas[i].y  # Measured Y-matrix
        y_ant = 1 / z_ant[i]  # Antenna admittance (symmetric for both ports)
        y_intr = y_meas.copy()
        y_intr[0, 0] -= y_ant  # Subtract antenna admittance
        y_intr[1, 1] -= y_ant
        s_intrinsic[i] = rf.y2s(y_intr, z0=z0)  # Convert back to S
    
    # Create output network
    ntw_intrinsic = rf.Network(frequency=ntw_meas.f, s=s_intrinsic, z0=z0)
    
    # Write to output S2P file
    ntw_intrinsic.write(output_s2p_path, form='ri')

# Define inputs
meas_s2p_path = r"L:\PythonProjects\Probe_Measure.s2p"  # Use forward slashes for compatibility
ant_input = "80+0j"  # Antenna impedance
output_s2p_path = "intrinsic.s2p"

# Run de-embedding
deembed_s2p(meas_s2p_path, ant_input, output_s2p_path)