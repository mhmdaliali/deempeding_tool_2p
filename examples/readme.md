# Examples

This directory contains example files and usage scenarios for the S2P de-embedding tool.

## Quick Start

```bash
cd examples
python ../deembed_s2p.py example_measured.s2p 80+0j 80+0j output.s2p
```

Or run all examples at once:
```bash
chmod +x run_examples.sh  # Linux/Mac
./run_examples.sh

# Windows
run_examples.bat
```

## Example Files

### Provided Data Files

- **`example_measured.s2p`**: 2-port S-parameter measurement of a device with 80Ω resistive loads on both ports (1-6 GHz)
- **`example_antenna.s1p`**: Frequency-dependent antenna impedance data (1-6 GHz)
- **`expected_output_example1.s2p`**: Expected result for Example 1 (verification reference)

### Generated Output Files

After running examples, you'll see:
- `output_example1.s2p` - Identical loads de-embedding
- `output_example2.s2p` - Different loads per port
- `output_example3.s2p` - Using S1P file for loads
- `output_example4.s2p` - Mixed load types

## Example Scenarios

### Example 1: Identical Loads on Both Ports

**Scenario**: Device measured with identical 80Ω resistive loads on ports 1 and 2.

**Command**:
```bash
python ../deembed_s2p.py example_measured.s2p 80+0j 80+0j output_example1.s2p
```

**What it does**: Removes the 80Ω resistive loading effect from both ports, revealing the intrinsic 50Ω S-parameters of the device.

**Expected result**: The de-embedded S11 and S22 should show improved return loss (lower reflection) compared to the measured data.

---

### Example 2: Different Loads per Port

**Scenario**: Port 1 has an 80Ω resistive load, Port 2 has a 75Ω + 10Ω inductive load.

**Command**:
```bash
python ../deembed_s2p.py example_measured.s2p 80+0j 75+10j output_example2.s2p
```

**What it does**: Removes different load impedances from each port.

**Use case**: Common when measuring asymmetric devices or when ports have different termination conditions.

---

### Example 3: Using S1P Files (Frequency-Dependent Loads)

**Scenario**: Both ports terminated with frequency-dependent antenna impedances.

**Command**:
```bash
python ../deembed_s2p.py example_measured.s2p example_antenna.s1p example_antenna.s1p output_example3.s2p --z0 50
```

**What it does**: De-embeds frequency-varying impedances (e.g., real antennas whose impedance changes with frequency).

**Use case**: Antenna-integrated RF front-ends, where antenna impedance varies significantly across the band.

---

### Example 4: Mixed Load Types

**Scenario**: Port 1 uses frequency-dependent S1P data, Port 2 uses constant complex impedance.

**Command**:
```bash
python ../deembed_s2p.py example_measured.s2p example_antenna.s1p 50+0j output_example4.s2p
```

**What it does**: Demonstrates flexibility—one port with varying impedance, one with fixed.

**Use case**: Hybrid measurement setups where one port is well-matched (50Ω) and the other has an antenna.

---

### Example 5: Custom Reference Impedance

**Scenario**: Measurement system uses 75Ω reference instead of standard 50Ω.

**Command**:
```bash
python ../deembed_s2p.py example_measured.s2p 100+0j 100+0j output_example5.s2p --z0 75
```

**What it does**: De-embeds loads while maintaining 75Ω reference impedance throughout.

**Use case**: Cable TV systems, some test equipment that uses 75Ω standard.

---

## Interpreting Results

### What to Expect After De-embedding

1. **S11 and S22 (Reflection Coefficients)**:
   - Should show **better matching** (lower magnitude) after removing mismatched loads
   - If loads were 80Ω and device is 50Ω-designed, de-embedded S11/S22 will be closer to 50Ω

2. **S21 and S12 (Transmission Coefficients)**:
   - Magnitude may **increase** slightly after de-embedding (less mismatch loss)
   - Phase should remain similar unless loads had significant reactance

3. **Frequency Dependence**:
   - If using S1P files, the de-embedding effect varies with frequency
   - Constant impedances produce uniform correction across all frequencies

### Validation

Compare your output with `expected_output_example1.s2p` to verify the tool is working correctly:

```bash
# Visual comparison (if you have plotting tools)
python -c "
import skrf as rf
import matplotlib.pyplot as plt

measured = rf.Network('example_measured.s2p')
deembedded = rf.Network('output_example1.s2p')
expected = rf.Network('expected_output_example1.s2p')

measured.s21.plot_s_db(label='Measured')
deembedded.s21.plot_s_db(label='Your Result')
expected.s21.plot_s_db(label='Expected')
plt.legend()
plt.title('S21 Comparison')
plt.show()
"
```

## Tips for Using Your Own Data

1. **Check frequency alignment**: Ensure S1P files have the same frequency points as your S2P measurement
2. **Verify load values**: Double-check your antenna/load impedance values before de-embedding
3. **Start with known loads**: Test with simple resistive loads (e.g., 75Ω) before complex impedances
4. **Save intermediate results**: Keep both measured and de-embedded files for comparison
5. **Plot before/after**: Visual inspection helps catch errors

## Troubleshooting

**Error: "S1P frequencies must match S2P"**
- Solution: Interpolate your S1P data to match S2P frequency points using `skrf.Network.interpolate()`

**Unexpected results (S-parameters > 1)**
- Check: Are your load impedances correct? 
- Check: Is the reference impedance appropriate?
- Verify: Does your measurement include the loads you're trying to remove?

**Large phase changes**
- Normal if loads had significant reactance
- Verify load impedance has correct sign (±j for inductive/capacitive)

## Further Reading

- [scikit-rf Documentation](https://scikit-rf.readthedocs.io/)
- [Touchstone File Format](https://ibis.org/touchstone_ver2.0/touchstone_ver2_0.pdf)
- [RF De-embedding Techniques](https://www.keysight.com/us/en/assets/7018-01515/application-notes/5989-5935.pdf)

## Questions?

If you encounter issues or have questions about these examples, please open an issue on GitHub.