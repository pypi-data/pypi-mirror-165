
import time
from heinlein import load_dataset, Region
import astropy.units as u
center = (141.23246,2.32358)
radius = 120*u.arcsec


setup_start = time.time()
d = load_dataset("hsc")

setup_end = time.time()
print(f"Setup took {setup_end - setup_start} seconds")

get_start = time.time()
a = d.cone_search(center, radius)
get_end = time.time()
print(f"get took {get_end - get_start} seconds")

get_start = time.time()
a = d.cone_search(center, radius)
get_end = time.time()
print(f"second get took {get_end - get_start} seconds")
cat = a['catalog']

import matplotlib.pyplot as plt

plt.scatter(cat['ra'], cat['dec'])
plt.show()
