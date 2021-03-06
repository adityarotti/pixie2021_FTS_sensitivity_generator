import os
import numpy as np
datapath = os.path.join(os.path.dirname(__file__),"indata")

def get_pixie2021_sensitivity(hfscfg=[12,6,2],frac=[0.2,0.4],years=2.,fsky=0.7,sdfrac=0.45,return_bw=False,skipch=True):
		'''
		hfscfg : a list of three HFS configurations
		frac : fraction of time spent in each mode. Only two time fractions are input by user. SUM frac = 1 used to constrain others. **Ensure the input fractions do not add to greater than unity.**
		years : 2 - Baseline PIXIE
		sdfrac : Fraction of time spent in SD mode (10% time assumed for calibration.)
		fsky : Assumed fraction of the sky for the final analysis
		returnbw : Currently a dummy variable.
		skipch : Default is true, which skips intermediate channels with worse sensitivity. Setting to false, depending on the combination of HFS cfg's may return a highly oscillators sensitivity curve owing to intermediate channels observed at relatively poor sensitivities.
		'''
		seconds=years*365.*24.*3600.*sdfrac
		renorm=np.sqrt(1.0/seconds)/np.sqrt(fsky)
		zero=1e-16
		if abs(frac[0]-1)<=1e-2:
			frac[1]=zero
			frac=frac + [zero]
			skipch=False
		elif abs(frac[0]+frac[1]-1)<=1e-2:
			frac=frac + [zero]
		else:
			frac=frac + [1.-frac[0]-frac[1]]
		#print(frac[0],frac[1],frac[2],np.sum(frac))

		nucfg={} ; dsens={} ; bw={}
		for ic,cfg in enumerate(hfscfg):
			hfs_filename=datapath + "/write_pixie_noise_hfs_v2_I_bw" + str(int(cfg)) + "_fat.txt"
			data=np.loadtxt(hfs_filename) ; nucfg[ic]=data[1:,0]
			dsens[ic]=dict(zip(nucfg[ic],data[1:,2]/np.sqrt(frac[ic])))
			bw[ic]=np.ones_like(nucfg[ic])*115.3/cfg
		
		
		ch0=[nucfg[1][0],nucfg[2][0]]
		nu=np.unique(np.append(np.append(nucfg[0],nucfg[1]),nucfg[2]))
		sensitivity=np.zeros(len(nu),np.float64)

		for ich, ch in enumerate(nu):
			if ch in nucfg[0] and ch in nucfg[1] and ch in nucfg[2]:
				sensitivity[ich]=1./np.sqrt(1./dsens[0][ch]**2. + 1./dsens[1][ch]**2. + 1./dsens[2][ch]**2.)
			elif ch in nucfg[0] and ch in nucfg[1]:
				if skipch and ch>ch0[1] and frac[2]>zero:
					sensitivity[ich]=-1
				else:
					sensitivity[ich]=1./np.sqrt(1./dsens[0][ch]**2. + 1./dsens[1][ch]**2.)
			elif ch in nucfg[0] and ch in nucfg[2]:
				if skipch:
					sensitivity[ich]=-1
				else:
					sensitivity[ich]=1./np.sqrt(1./dsens[0][ch]**2. + 1./dsens[2][ch]**2.)
			elif ch in nucfg[1] and ch in nucfg[2]:
				if skipch:
					sensitivity[ich]=-1
				else:
					sensitivity[ich]=1./np.sqrt(1./dsens[1][ch]**2. + 1./dsens[2][ch]**2.)
			elif ch in nucfg[0]:
				if ch>=ch0[0] and skipch:
					sensitivity[ich]=-1.
				else:
					sensitivity[ich]=dsens[0][ch]
			elif ch in nucfg[1]:
				if ch>=ch0[1] and skipch:
					sensitivity[ich]=-1.
				else:
					sensitivity[ich]=dsens[1][ch]
			elif ch in nucfg[2]:
				sensitivity[ich]=dsens[2][ch]

		tmask=(sensitivity>0).astype(np.int)
		nu=nu[tmask==1.] ; sensitivity=sensitivity[tmask==1.]

		sensitivity=sensitivity*renorm
		
		return nu,sensitivity
