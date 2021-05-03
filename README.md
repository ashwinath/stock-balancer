# Stock Balancer

Helps to balance your stock with the ratios you provided.


## Getting Started
Setting up environment.
```bash
python3 -m venv env
make setup
source env/bin/activate
```

Sample config
```yaml
amount_to_dca: 1000
stock_info:
- name: VOO
  desired_weight: 35
  count: 59
- name: IWV
  desired_weight: 35
  count: 89
- name: A35.SI
  desired_weight: 30
  count: 21600
```

Running it:
```bash
python3 main.py --config /path/to/config.yaml
```

Output:
```
NAV: USD 64088.49, SGD 84978.77
Name      Weight    Current Value    Desired Value    Diff Value    Current Quantity    Desired Quantity    Diff Quantity
------  --------  ---------------  ---------------  ------------  ------------------  ------------------  ---------------
VOO           35          22627.7          22781          153.29                  59             59.3997             0.4
IWV           35          22287.4          22781          493.59                  89             90.9711             1.97
A35.SI        30          19173.4          19526.5        353.12               21600          21997.8              397.81
```
