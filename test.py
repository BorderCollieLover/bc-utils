from data_to_download.missingcontracts import missingcontracts
from bcutils.config import CONTRACT_MAP
from bcutils.config_old import CONTRACT_MAP as CM_OLD

#Find old CONTRACT_MAP entries so they can be assed to CONTRACT_MAP
#Find instruments in missingcontracts that do not exist in CONTRACT_MAP so I can manually add those entries 

new_map = {}
for k in CM_OLD:
    if k not in CONTRACT_MAP:
        print(k)
        new_map[k] = CM_OLD[k]


print("-------------------------")

for k in missingcontracts.keys():
    if k not in CONTRACT_MAP:
        print(k)


print(new_map)