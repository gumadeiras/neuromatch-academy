from oneibl.onelight import ONE
from brainrender.scene import Scene
import brainrender

# https://github.com/FedeClaudi/brainrenderscenes/blob/master/scenes/Steinmetz_probes.py

# set shader style
brainrender.SHADER_STYLE = "cartoon"

# use ONE to download probe locations from the Steinmetz dataset
one = ONE()
one.set_figshare_url("https://figshare.com/articles/steinmetz/9974357")

# select sessions with trials
sessions = one.search(["trials"])


# for each session get the position of the probes electrodes
probes_locs = []
for sess in sessions:
    probes_locs.append(one.load_dataset(sess, "channels.brainLocation"))


# Get a color for each session
# colors = choices(list(colors_dict.keys()), k=len(sessions))


# Create brainrender scene
scene = Scene()

# Add spheres where each probe electrode is
# for locs, col in zip(probes_locs, colors):
for locs in probes_locs:
    spheres = scene.add_cells(locs, col_names=["ccf_ap", "ccf_dv", "ccf_lr"], color="olivedrab", res=12, alpha=1)

# Add brain regions
regions = scene.add_brain_regions(["VISp", "RSP", "TH", "SCm"], alpha=0.4)
for reg in regions:
    scene.add_actor(reg.silhouette().lw(1).c("k"))


# render
# scene.render()

scene.export_for_web("steinmetz.html")
