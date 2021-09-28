import os
from pylab import *
from eval_pixie_sensitivity import get_pixie2021_sensitivity

figure()
#O1
nu,sensitivity=get_pixie2021_sensitivity(hfscfg=[12,4,2],frac=[0.25,0.25],skipch=True)
plot(nu,sensitivity,".-",label="O1")

#O2
nu,sensitivity=get_pixie2021_sensitivity(hfscfg=[12,4,1],frac=[0.25,0.25],skipch=True)
plot(nu,sensitivity,".-",label="O2")

#O3
nu,sensitivity=get_pixie2021_sensitivity(hfscfg=[12,1,1],frac=[0.25,0.75],skipch=True)
plot(nu,sensitivity,".-",label="O3")

#O4
nu,sensitivity=get_pixie2021_sensitivity(hfscfg=[6,1,1],frac=[1.0,0.],skipch=True)
plot(nu,sensitivity,".-",label="O4")

legend(loc=0)
grid(which="both",linestyle="--",alpha=0.3)
xlabel("Frequency GHz")
ylabel(r"$\Delta I_{\nu}$ Jy/sr")
loglog()

figpath = os.path.join(os.path.dirname(__file__),"figures")

savefig( figpath + "/test_sensitivity_fig.pdf",bbox_inches="tight")
