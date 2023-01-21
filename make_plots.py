# make_plots.py
# Tim Player, 11 January 2023
# Plot longwave and shortwave irradiance.
# Expects input files:
# - output/shackleton.csv
# - output/klenova.csv
# Makes output files:
# - output/figs/irradiance.png
# - output/figs/irradiance.svg

import pandas as pd
import matplotlib.pyplot as plt

# Read in the CSV data as a Pandas Dataframe
shackleton = pd.read_csv('output/shackleton.csv')
klenova = pd.read_csv('output/klenova.csv')

# Convert times to datetime objects
for df in shackleton, klenova:
    df["Datetime"] = pd.to_datetime(df["Datetime"])

# Make plots
fig, axs = plt.subplots(2, 2, figsize=(10,5))

lw_ylim = [None, None]
sw_ylim = [None, None]

# If you want, you can uncomment the lines below to set the Y range.
# lw_ylim = [420, 460]
# sw_ylim = [-10, 15]

# The variable below sets the X range.
xlim = [shackleton.Datetime[0], None]

lw_names = ['A_SL510_LWi_Avg', 'A_SL610_LWo_Avg', 'B_SL510_LWi_Avg',
       'B_SL610_LWo_Avg']
sw_names = ['A_SP510_SWi_Avg', 'A_SP610_SWo_Avg',
       'B_SP510_SWi_Avg', 'B_SP610_SWo_Avg']

# Shackleton longwave
for name in lw_names:
    if name == "Datetime": continue
    axs[0][0].plot(shackleton["Datetime"], shackleton[name], '.', label=name)
    axs[0][0].set_xlim(*xlim)
    axs[0][0].set_ylim(*lw_ylim)
axs[0][0].set_ylabel('LW Flux (W m$^{-2}$)')
# axs[0][0].legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

# Shackleton shortwave
for name in sw_names:
    if name == "Datetime": continue
    axs[1][0].plot(shackleton["Datetime"], shackleton[name], '.', label=name)
    axs[1][0].set_xlim(*xlim)
    axs[1][0].set_ylim(*sw_ylim)
axs[1][0].set_ylabel('SW Flux (W m$^{-2}$)')
# axs[1][0].legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
axs[1][0].set_xlabel('Time (UTC)')

axs[0][0].set_title('Shackleton')

# Klenova longwave
for name in lw_names:
    if name == "Datetime": continue
    axs[0][1].plot(klenova["Datetime"], klenova[name], '.', label=name)
    axs[0][1].set_xlim(*xlim)
    axs[0][1].set_ylim(*lw_ylim)
# axs[0][1].set_ylabel('LW Flux (W m$^{-2}$)')
axs[0][1].legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

# Klenova shortwave
for name in sw_names:
    if name == "Datetime": continue
    axs[1][1].plot(klenova["Datetime"], klenova[name], '.', label=name)
    axs[1][1].set_xlim(*xlim)
    axs[1][1].set_ylim(*sw_ylim)
# axs[1][1].set_ylabel('SW Flux (W m$^{-2}$)')
axs[1][1].legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
axs[1][1].set_xlabel('Time (UTC)')

axs[0][1].set_title('Klenova')

fig.autofmt_xdate(rotation=45)
fig.suptitle('Longwave and Shortwave Irradiance')
fig.tight_layout()

# ultra-high-resolution and vector style
# for pretty papers
plt.savefig('output/figs/irradiance.png', dpi=600)
plt.savefig('output/figs/irradiance.svg')