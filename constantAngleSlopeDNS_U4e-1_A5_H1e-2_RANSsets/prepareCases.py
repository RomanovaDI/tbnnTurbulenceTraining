import subprocess as sp
import numpy as np
import pandas as pd
import fileinput as fi

def timeStepsList(DNSfolder):
	sp.call('ls -1 -d '+DNSfolder+'[0-9]* |xargs -n1 basename > timeStepsList.txt', shell=True)
	timeStepsList = np.loadtxt("timeStepsList.txt", dtype=str)
	index = np.argsort(timeStepsList.astype(np.float))
	timeStepsList = timeStepsList[index]
	return timeStepsList[1:]

def prepareFolders(DNSfolder, RANSfolder, TSL):
	sp.call('rm -rf '+RANSfolder+'[0-9]*', shell=True)
	for n in range(len(TSL)-1):
		sp.run('cp -r '+RANSfolder+'origBM '+RANSfolder+TSL[n]+';\
				cd '+RANSfolder+TSL[n]+';\
				pwd;\
				mapFields -consistent -sourceTime \''+TSL[n][:-1]+'\' ../../constantAngleSlopeDNS_U4e-1_A5_H1e-2_NotDNS/;\
				./Allrun;\
				mv 0 init;\
				mv 1e-05 res;\
				mapFields -consistent -sourceTime \''+TSL[n+1][:-1]+'\' ../../constantAngleSlopeDNS_U4e-1_A5_H1e-2_NotDNS/;\
				mv 0 ref',
				shell=True, check=True)

def main():
	DNSfolder = '../constantAngleSlopeDNS_U4e-1_A5_H1e-2_NotDNS/'
	TSL = timeStepsList(DNSfolder)
	deltaT = 1e-05
	MLturbRANSfolder = 'TIF'
	KEturbRANSfolder = 'KEIF'
	KWturbRANSfolder = 'KWIF'
	prepareFolders(DNSfolder, MLturbRANSfolder, TSL)
	prepareFolders(DNSfolder, KEturbRANSfolder, TSL)
	prepareFolders(DNSfolder, KWturbRANSfolder, TSL)

if __name__ == "__main__":
	main()
