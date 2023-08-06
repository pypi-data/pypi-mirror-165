from src.so4gp import so4gp
import json

# out_json, gps = so4gp.rsgps('DATASET.csv', max_iteration=20, return_gps=True)
# out_json, gps = so4gp.graank('DATASET.csv', return_gps=True)
out_json, gps = so4gp.clugps('DATASET.csv', e_probability=0, return_gps=True)
print(out_json)
print(so4gp.compare_gps('DATASET.csv', 0.5, gps))

# out_obj = json.loads(out_json)
# print(out_obj["Invalid Count"])
