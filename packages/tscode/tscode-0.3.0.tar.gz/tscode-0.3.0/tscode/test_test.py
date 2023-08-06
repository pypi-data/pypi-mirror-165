from tscode.ase_manipulations import ase_vib
from cclib.io import ccread
import numpy as np
data = ccread(r'C:\Users\Nik\Desktop\maleimide\TSCoDe_poses_mal.xyz')
data.atomcoords.shape

# %%
import asyncio, time
from tscode.utils import time_to_string

embedder = ('MOPAC', 'PM6', None, 'thf') # calculator, method, procs, solvent
# for i, coords in enumerate(data.atomcoords):
#     freqs = ase_vib(embedder, coords, data.atomnos, title=f'temp{i}', logfunction=print)

async def F(i):
    return i

async def negatives():

    # return await asyncio.gather(*[ase_vib(embedder, coords, data.atomnos, title=f'temp{i}', logfunction=print)[1]
    #                               for i, coords in enumerate(data.atomcoords)])
                                
    return await asyncio.gather(*[F(i)
                                  for i, coords in enumerate(data.atomcoords)])

t = time.perf_counter()
# main()
freqs = asyncio.run(negatives())
print(time_to_string(time.perf_counter()-t))

for i, n in enumerate(negatives):
    print(i, n, 'negative freqs')


