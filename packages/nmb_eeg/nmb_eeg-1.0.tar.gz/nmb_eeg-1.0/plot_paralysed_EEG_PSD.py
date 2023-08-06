#!/usr/bin/python3
import matplotlib.pyplot as plt
from nmb_eeg import NMB_EEG_From_WhithamEtAl
import numpy as np

# Plot the individual PSDs
for i in range(len(NMB_EEG_From_WhithamEtAl.allsubjectdata)):
    p = NMB_EEG_From_WhithamEtAl(i)
    f = np.linspace(p.f_signal_min,p.f_signal_max,100)
    psd = p.EEGVariance(f)
    totalEEGPower = p.totalEEGPower()
    print("Average EEG voltage is (uV):",round((totalEEGPower**0.5)*1E6))
    plt.plot(f,psd,linewidth=1,label=p.allsubjectdesciption[i])

# Plot the average (no arguments needed here for the constructor)
p = NMB_EEG_From_WhithamEtAl()
f = np.linspace(p.f_signal_min,p.f_signal_max,100)
psd = p.EEGVariance(f)
totalEEGPower = p.totalEEGPower()
print("Average EEG voltage is (uV):",round((totalEEGPower**0.5)*1E6))

plt.ylim([-16,-10])
plt.xlim([0,100])
plt.xlabel("f/Hz")
plt.ylabel("Log Power (V^2 / Hz)")
plt.plot(f,psd,linewidth=3,color="0",label="Average")
plt.legend()
plt.show()
