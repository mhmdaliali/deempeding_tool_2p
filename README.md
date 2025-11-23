# deempeding_tool_2p
Two-Port S-Parameter De-Embedding Tool
This Python tool removes the loading effects of measurement probes or test fixtures
from a two-port network measurement (S21). It reconstructs the actual network S21
before the loads, enabling more accurate validation of RF components.

### Capabilities
- Reads standard Touchstone files (`.s2p`)
- Performs de-embedding using standard 2-port network transformations
- Produces corrected S21 as Touchstone output
- Must be given the load data, ZL & and probe location

### Usage
```python
from deembed import deembed_s21

corrected = deembed_s21(
    meas_file="data/measured_s21.s2p",
    load_file="data/load_model.s2p"
)
