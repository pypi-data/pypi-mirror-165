import numpy as np
from handyscikit import lbm

dmqn = lbm.D3Q7(float_dtype=np.float32)
print(dmqn.e)