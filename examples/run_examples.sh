#!/bin/bash

# S2P De-embedding Tool - Example Runner
# This script runs all example scenarios

echo "=========================================="
echo "S2P De-embedding Tool - Running Examples"
echo "=========================================="
echo ""

# Check if Python script exists
if [ ! -f "../deembed_s2p.py" ]; then
    echo "Error: deembed_s2p.py not found in parent directory"
    exit 1
fi

# Check if example data exists
if [ ! -f "example_measured.s2p" ]; then
    echo "Error: example_measured.s2p not found"
    echo "Please ensure example data files are in the examples/ directory"
    exit 1
fi

echo "Example 1: Identical loads on both ports (80Ω)"
echo "Command: python ../deembed_s2p.py example_measured.s2p 80+0j 80+0j output_example1.s2p"
python ../deembed_s2p.py example_measured.s2p 80+0j 80+0j output_example1.s2p
echo ""

echo "Example 2: Different loads per port (80Ω and 75+10j Ω)"
echo "Command: python ../deembed_s2p.py example_measured.s2p 80+0j 75+10j output_example2.s2p"
python ../deembed_s2p.py example_measured.s2p 80+0j 75+10j output_example2.s2p
echo ""

if [ -f "example_antenna.s1p" ]; then
    echo "Example 3: Using S1P files for frequency-dependent loads"
    echo "Command: python ../deembed_s2p.py example_measured.s2p example_antenna.s1p example_antenna.s1p output_example3.s2p --z0 50"
    python ../deembed_s2p.py example_measured.s2p example_antenna.s1p example_antenna.s1p output_example3.s2p --z0 50
    echo ""
    
    echo "Example 4: Mixed load types (S1P and constant impedance)"
    echo "Command: python ../deembed_s2p.py example_measured.s2p example_antenna.s1p 50+0j output_example4.s2p"
    python ../deembed_s2p.py example_measured.s2p example_antenna.s1p 50+0j output_example4.s2p
    echo ""
else
    echo "Note: example_antenna.s1p not found, skipping Examples 3 and 4"
    echo ""
fi

echo "Example 5: Custom reference impedance (75Ω)"
echo "Command: python ../deembed_s2p.py example_measured.s2p 100+0j 100+0j output_example5.s2p --z0 75"
python ../deembed_s2p.py example_measured.s2p 100+0j 100+0j output_example5.s2p --z0 75
echo ""

echo "=========================================="
echo "All examples completed!"
echo "=========================================="
echo ""
echo "Generated output files:"
ls -lh output_example*.s2p 2>/dev/null || echo "  (check for output_example*.s2p files)"
echo ""
echo "Compare your results with expected_output_example1.s2p for validation"