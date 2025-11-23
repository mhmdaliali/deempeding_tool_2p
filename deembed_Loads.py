import skrf as rf
import numpy as np
import argparse
import sys

def deembed_s2p(meas_s2p_path, ant1_input, ant2_input, output_s2p_path, z0=None):
    """
    De-embed antenna/loads from a measured 2-port S2P file.
    
    Parameters:
    -----------
    meas_s2p_path : str
        Path to measured 2-port S2P file
    ant1_input : str
        Port 1 load: complex number (e.g., '80+0j') or S1P file path
    ant2_input : str
        Port 2 load: complex number (e.g., '80+0j') or S1P file path
    output_s2p_path : str
        Path to save the de-embedded S2P file
    z0 : float, optional
        Reference impedance (default: use S2P file's Z0)
    """
    # Load measured S2P file
    ntw_meas = rf.Network(meas_s2p_path)
    freqs = ntw_meas.f
    n_freq = len(freqs)
    
    # Use measured network's Z0 if not specified
    if z0 is None:
        z0 = ntw_meas.z0[0].real  # Use Z0 from S2P file
    
    # Helper function to parse antenna/load input
    def parse_load(load_input, port_name):
        if isinstance(load_input, str) and load_input.lower().endswith('.s1p'):
            ntw_load = rf.Network(load_input)
            if len(ntw_load.f) != n_freq:
                raise ValueError(f"{port_name} S1P frequencies must match S2P")
            return ntw_load.z[:, 0, 0]  # Extract Z11
        else:
            try:
                z_load_val = complex(load_input)
                return np.full(n_freq, z_load_val)
            except ValueError:
                raise ValueError(f"{port_name} must be complex number or .s1p file")
    
    # Parse both loads
    z_ant1 = parse_load(ant1_input, "Port 1 load")
    z_ant2 = parse_load(ant2_input, "Port 2 load")
    
    # Initialize output S-matrix
    s_intrinsic = np.zeros((n_freq, 2, 2), dtype=complex)
    
    # De-embed using Y-matrix
    for i in range(n_freq):
        y_meas = ntw_meas[i].y  # Measured Y-matrix (shape: (1, 2, 2))
        y_ant1 = 1 / z_ant1[i]  # Port 1 load admittance
        y_ant2 = 1 / z_ant2[i]  # Port 2 load admittance
        y_intr = y_meas.copy()
        y_intr[0, 0, 0] -= y_ant1  # De-embed from port 1
        y_intr[0, 1, 1] -= y_ant2  # De-embed from port 2
        s_intrinsic[i] = rf.y2s(y_intr, z0=z0)[0]  # Extract from (1, 2, 2) to (2, 2)
    
    # Create output network
    ntw_intrinsic = rf.Network(frequency=ntw_meas.frequency, s=s_intrinsic, z0=z0)
    
    # Write to output S2P
    ntw_intrinsic.write_touchstone(output_s2p_path, form='ri')
    print(f"De-embedded S2P saved to {output_s2p_path} (Z0={z0} Ω)")

# ------------------------
# Command-line interface
# ------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="De-embed antenna/loads from measured 2-port S2P file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Identical loads on both ports
  python deembed_loads.py measured_data.s2p 80+0j 80+0j output.s2p
  
  # Different loads per port
  python deembed_loads.py measured_data.s2p 75+10j 50-5j output.s2p
  
  # Using S1P files
  python deembed_loads.py measured_data.s2p ant1.s1p ant2.s1p output.s2p --z0 50
  
  # Mixed: S1P for port 1, complex for port 2
  python deembed_loads.py measured_data.s2p antenna.s1p 80+0j output.s2p
        """
    )
    parser.add_argument("meas_s2p", help="Path to measured 2-port S2P file")
    parser.add_argument("ant1_input", help="Port 1 load: complex number 'R+Xj' or S1P file path")
    parser.add_argument("ant2_input", help="Port 2 load: complex number 'R+Xj' or S1P file path")
    parser.add_argument("output_s2p", help="Path to output de-embedded S2P file")
    parser.add_argument("--z0", type=float, default=None, 
                       help="Reference impedance (default: use S2P file's Z0)")
    args = parser.parse_args()
    
    try:
        deembed_s2p(args.meas_s2p, args.ant1_input, args.ant2_input, 
                   args.output_s2p, z0=args.z0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
