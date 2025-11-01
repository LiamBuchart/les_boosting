"""
    
    Quick plot of the terrain height 
    field used in the LES simulation.
    
    lbuchart@eoas.ubc.ca
    October 6, 2025
    
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import json

from context import json_dir

hgt = np.loadtxt("input_ht", skiprows=1).T

print("Height field shape:", np.shape(hgt))
print("Max height (m):", np.max(hgt))

# load grid dimensions which are saved in the context file
with open(str(json_dir) + "config.json") as f:
    config = json.load(f)
    
dx = config["grid_dimensions"]["dx"]  # grid dimensions
min_h = config["topo"]["base_ht"]

# combine the two plots into one figure
fig, (ax1, ax2) = plt.subplots(2, 1,
                            sharex=True,
                            gridspec_kw={"height_ratios":[4, 1]})

ax1.imshow(hgt, cmap="terrain", aspect="auto")
ax1.set_title("Terrain Height Field")
ax1.set_xlabel("Zonal Distance [km]")
ax1.set_ylabel("Meridional Distance [km]")

# shrink the second plot

ax2.plot(hgt[0, :], color="k", label="Cross-section at Y=0")
ax2.set_xlabel("Zonal Distance [km]") 
ax2.set_ylabel("Height (m)")
ax2.legend()

# ticks in km
x_ticks = np.arange(0, hgt.shape[1]+20, 20)
x_labels = [f"{int(x*dx/1000)} km" for x in x_ticks]
ax1.set_xticks(x_ticks)
ax1.set_xticklabels(x_labels)
ax2.set_xticks(x_ticks)
ax2.set_xticklabels(x_labels)

hticks = [min_h, 750, 1000]
ax2.set_yticks(hticks)
ax2.set_yticklabels(hticks)

# rotate the xlabels 45 degrees
plt.setp(ax2.get_xticklabels(), rotation=45)

# yticks with 0 at bottom
y_ticks = np.arange(0, hgt.shape[0]+20, 20)
# add labels in reverese
y_labels = [f"{int(y*dx/1000)} km" for y in y_ticks[::-1]]
       
ax1.set_yticks(y_ticks)
ax1.set_yticklabels(y_labels)

# colorbar with ticks every 100m place it 
# have it span both plots
fig.tight_layout() 
cbar = fig.colorbar(ax1.images[0], ax=[ax1, ax2], 
                    orientation="vertical")
ys =  np.arange(400, 1201, 100)
# replace first tick with min height
ys = np.delete(ys, 0)
ys = np.insert(ys, 0, min_h)

cbar.set_ticks(ys)
cbar.set_label("Height (m)")    

# remove the xtick labels from the first plot
plt.setp(ax1.get_xticklabels(), visible=False)

plt.savefig("terrain_height_field.png", dpi=300)
plt.show()
# %%
