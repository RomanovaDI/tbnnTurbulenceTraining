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

def prepareFolders(DNSfolder, RANSfolder, TSL, deltaT):
	sp.call('rm -rf '+RANSfolder+'[0-9]*', shell=True)
	for time in TSL:
		sp.run('cp -r '+RANSfolder+'orig '+RANSfolder+time+';\
				cd '+RANSfolder+time+';\
				pwd;\
				cp ../'+DNSfolder+time+'/USpAv 0/U;\
				cp ../'+DNSfolder+time+'/awSpAv 0/alpha.water;\
				cp ../'+DNSfolder+time+'/p_rghSpAv 0/p_rgh;\
				mv 0 '+time, shell=True, check=True)
		with fi.FileInput(RANSfolder+time+'/system/controlDict', inplace=True) as file:
			for line in file:
				print(line.replace('startTimePattern', time), end='')
		with fi.FileInput(RANSfolder+time+'/system/controlDict', inplace=True) as file:
			for line in file:
				print(line.replace('endTimePattern', str(float(time)+deltaT)), end='')
		with fi.FileInput(RANSfolder+time+'/system/controlDict', inplace=True) as file:
			for line in file:
				print(line.replace('deltaTPattern', str(deltaT)), end='')
		sp.run('cd '+RANSfolder+time+';\
				./Allrun', shell=True, check=True)
	for n in range(len(TSL)-1):
		sp.run('cp '+DNSfolder+TSL[n+1]+'/USpAv '+RANSfolder+TSL[n]+'/'+TSL[n+1]+'/Uref', shell=True, check=True)
	for n in range(len(TSL)-1):
		sp.run('cp '+DNSfolder+TSL[n+1]+'/awSpAv '+RANSfolder+TSL[n]+'/'+TSL[n+1]+'/AWref', shell=True, check=True)
	for n in range(len(TSL)-1):
		sp.run('cp '+DNSfolder+TSL[n+1]+'/p_rghSpAv '+RANSfolder+TSL[n]+'/'+TSL[n+1]+'/p_rghref', shell=True, check=True)
	for n in range(len(TSL)-1):
		sp.run('cp -r '+RANSfolder+TSL[n]+'/'+TSL[n+1]+' '+RANSfolder+TSL[n]+'/'+TSL[n]+'/res', shell=True, check=True)

def main():
	DNSfolder = '../constantAngleSlopeDNS_U4e-1_A5_H1e-2_NotDNS/'
	TSL = timeStepsList(DNSfolder)
	deltaT = 1e-05
	MLturbRANSfolder = 'TIF'
	KEturbRANSfolder = 'KEIF'
	KWturbRANSfolder = 'KWIF'
	prepareFolders(DNSfolder, MLturbRANSfolder, TSL, deltaT)
	prepareFolders(DNSfolder, KEturbRANSfolder, TSL, deltaT)
	prepareFolders(DNSfolder, KWturbRANSfolder, TSL, deltaT)

if __name__ == "__main__":
    main()
