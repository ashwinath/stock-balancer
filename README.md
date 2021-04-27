# Stock Balancer

Helps to balance your stock with the ratios you provided.


## Getting Started
Setting up environment.
```bash
python3 venv env
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
