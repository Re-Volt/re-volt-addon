import rvstruct
import json

# with open("closed_n.ncp", "rb") as f:
with open("muse1.ncp", "rb") as f:
    ncp = rvstruct.NCP(f)
    print(json.dumps(ncp.as_dict(), indent=2))
