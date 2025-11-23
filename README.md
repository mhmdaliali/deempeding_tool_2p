# deempeding_tool_2p
A Python tool for de-embedding antenna or load impedances from 2-port S-parameter measurements. This tool removes the effects of terminating impedances to extract the intrinsic behavior of the device under test.

## Overview

When measuring RF devices with integrated antennas or non-50Ω terminations, the measured S-parameters include both the device characteristics and the loading effects. This tool mathematically removes those load impedances using Y-parameter matrix operations, revealing the intrinsic device response.

### What It Does

1. Loads a measured 2-port S-parameter file (S2P)
2. Converts S-parameters to Y-parameters (admittance matrix)
3. Subtracts the load admittances from ports 1 and 2
4. Converts back to S-parameters to obtain the de-embedded response
5. Saves the result as a new S2P file in real-imaginary format

## Requirements

- Python 3.7+
- scikit-rf (`skrf`)
- numpy

Install dependencies:
```bash
pip install scikit-rf numpy
```

## Usage

```bash
python deembed_loads.py <measured_s2p> <port1_load> <port2_load> <output_s2p> [--z0 Z0]
```

### Arguments

- `<measured_s2p>`: Path to measured 2-port S2P file
- `<port1_load>`: Port 1 load impedance as complex number (e.g., `80+0j`) or S1P file path
- `<port2_load>`: Port 2 load impedance as complex number (e.g., `80+0j`) or S1P file path
- `<output_s2p>`: Path to save the de-embedded S2P file
- `--z0 Z0`: Optional. Reference impedance in ohms (default: use S2P file's Z0)

### Load Input Formats

Each port's load can be specified as:

1. **Complex impedance** (frequency-independent):
   - Format: `R+Xj` where R is resistance and X is reactance in ohms
   - Examples: `50+0j`, `75+10j`, `80-25j`

2. **S1P file** (frequency-dependent):
   - Must have the same frequency points as the measured S2P file
   - The tool extracts Z11 from the S1P file

## Examples

### 1. Identical Loads on Both Ports (Default Z0)
```bash
python deembed_s2p.py measured_data.s2p 80+0j 80+0j deembedded.s2p
```

### 2. Different Loads per Port
```bash
python deembed_s2p.py measured_data.s2p 75+10j 50-5j deembedded.s2p
```

### 3. Using S1P Files for Frequency-Dependent Loads
```bash
python deembed_s2p.py measured_data.s2p antenna1.s1p antenna2.s1p output.s2p --z0 50
```

### 4. Mixed Load Types
```bash
python deembed_s2p.py measured_data.s2p antenna.s1p 80+0j output.s2p
```

### 5. Custom Reference Impedance
```bash
python deembed_s2p.py measured_data.s2p 75+0j 75+0j output.s2p --z0 75
```

### 6. Pure Resistive Loads
```bash
python deembed_s2p.py measured_data.s2p 50+0j 50+0j output.s2p
```

### 7. Capacitive Load (Negative Reactance)
```bash
python deembed_s2p.py measured_data.s2p 80-50j 80-50j output.s2p
```

### 8. Inductive Load (Positive Reactance)
```bash
python deembed_s2p.py measured_data.s2p 100+75j 100+75j output.s2p
```

## Theory of Operation

The de-embedding process uses the following steps:

1. **Convert to Y-parameters**: The measured S-parameters are converted to Y-parameters (admittance matrix).

2. **Subtract load admittances**: 
   - Port 1: `Y11_intrinsic = Y11_measured - Y_load1`
   - Port 2: `Y22_intrinsic = Y22_measured - Y_load2`
   - Off-diagonal terms (Y12, Y21) remain unchanged

3. **Convert back to S-parameters**: The modified Y-matrix is converted back to S-parameters using the specified reference impedance.

This approach assumes:
- Loads are in shunt configuration at each port, which is typical in probe measurements
- The device is linear and passive
- Frequency points match between all input files

## Output Format

The output S2P file is saved in Touchstone format with:
- **Format**: Real-Imaginary (`RI`)
- **Frequency unit**: Same as input file
- **Reference impedance**: As specified or from input file

## Error Handling

The tool will report errors for:
- Mismatched frequency points between S2P and S1P files
- Invalid complex number format
- Missing or inaccessible files
- Invalid file formats

## Use Cases

- **Antenna-integrated devices**: Remove antenna impedance effects to characterize the RF front-end
- **Non-standard terminations**:  De-embed measurements taken with impedances other than 50Ω
- **Impedance matching studies**: Extract intrinsic device behavior before/after matching networks
- **Calibration corrections**: Remove known parasitic impedances from measurements

## Limitations

- Assumes shunt load configuration (parallel connection)
- Does not handle series impedances or cascaded networks
- Load impedances must be known or characterized separately
- Does not account for electromagnetic coupling between loads and device

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author
mhmdaliali

