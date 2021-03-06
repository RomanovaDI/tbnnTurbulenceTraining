import subprocess as sp
import numpy as np
import pandas as pd
import fileinput as fi

def timeStepsList():
	sp.run("ls -1 -d 0.* [1-9]* > timeStepsList.txt", shell=True)
	timeStepsList = np.loadtxt("timeStepsList.txt", dtype=str)
	index = np.argsort(timeStepsList.astype(np.float))
	timeStepsList = timeStepsList[index]
	return timeStepsList

def spaceMean(TSL, Fs, sizes):
	for folder in TSL:
		for fileName in Fs:
			if fileName == 'U':
				spaceMeanU(folder, fileName, sizes)
			elif fileName == 'alpha.water':
				spaceMeanAlphaWater(folder, fileName, sizes)
			elif fileName == 'p_rgh':
				spaceMeanP_rgh(folder, fileName, sizes)
	return

def spaceMeanU(folder, fileName, sz):
	sz1 = sz[0]
	sz1S = sz1[0]*sz1[1]*sz1[2]
	sz2 = sz[1]
	nrows = sz1S + sz2[0] * sz2[1] * sz2[2]
	uArr = pd.read_csv(folder+'/'+fileName, header=None, skiprows=23, nrows=nrows, dtype=str)
	uArr.iloc[:,0] = uArr.iloc[:,0].str.replace('[(,)]', '', regex=True)
	uArr = uArr.iloc[:,0].str.split(expand=True)
	uArrXNp = np.concatenate((avComp(uArr.iloc[:sz1S,0].to_numpy(dtype=float), sz1), avComp(uArr.iloc[sz1S:,0].to_numpy(dtype=float), sz2)), axis=0)
	uArrYNp = np.concatenate((avComp(uArr.iloc[:sz1S,1].to_numpy(dtype=float), sz1), avComp(uArr.iloc[sz1S:,1].to_numpy(dtype=float), sz2)), axis=0)
	uArrZNp = np.concatenate((avComp(uArr.iloc[:sz1S,2].to_numpy(dtype=float), sz1), avComp(uArr.iloc[sz1S:,2].to_numpy(dtype=float), sz2)), axis=0)
	uArrAv = pd.DataFrame(data=np.transpose(np.stack((uArrXNp, uArrYNp, uArrZNp))), dtype=str, columns=['x', 'y', 'z'])
	uArrAv['strings'] = '( '+uArrAv['x']+' '+uArrAv['y']+' '+uArrAv['z']+' )'
	sp.run("cp patterns/USpaceAvaragePatternBeginning "+folder+"/USpAv", shell=True, check=True)
	with open(folder+'/USpAv', 'a') as f:
		f.write(str(int(nrows/8))+'\n(\n')
	with fi.FileInput(folder+'/USpAv', inplace=True) as file:
		for line in file:
			print(line.replace('folderName', '"'+folder+'"'), end='')
	with fi.FileInput(folder+'/USpAv', inplace=True) as file:
		for line in file:
			print(line.replace('fieldName', 'USpAv'), end='')
	uArrAv['strings'].to_csv(folder+'/USpAv', mode='a', index=False, header=False)
	with open(folder+'/USpAv', 'a') as fout, fi.input('patterns/USpaceAvaragePatternEnding') as fin:
		for line in fin:
			fout.write(line)

def spaceMeanAlphaWater(folder, fileName, sz):
	sz1 = sz[0]
	sz1S = sz1[0]*sz1[1]*sz1[2]
	sz2 = sz[1]
	nrows = sz1S + sz2[0] * sz2[1] * sz2[2]
	awArr = pd.read_csv(folder+'/'+fileName, header=None, skiprows=23, nrows=nrows, dtype=str)
	awArrNp = np.concatenate((avComp(awArr.iloc[:sz1S,0].to_numpy(dtype=float), sz1), avComp(awArr.iloc[sz1S:,0].to_numpy(dtype=float), sz2)), axis=0)
	awArrAv = pd.DataFrame(data=awArrNp, dtype=str, columns=['aw'])
	sp.run("cp patterns/alpha.waterSpaceAvaragePatternBeginning "+folder+"/awSpAv", shell=True, check=True)
	with open(folder+'/awSpAv', 'a') as f:
		f.write(str(int(nrows/8))+'\n(\n')
	with fi.FileInput(folder+'/awSpAv', inplace=True) as file:
		for line in file:
			print(line.replace('folderName', '"'+folder+'"'), end='')
	with fi.FileInput(folder+'/awSpAv', inplace=True) as file:
		for line in file:
			print(line.replace('fieldName', 'awSpAv'), end='')
	awArrAv['aw'].to_csv(folder+'/awSpAv', mode='a', index=False, header=False)
	with open(folder+'/awSpAv', 'a') as fout, fi.input('patterns/alpha.waterSpaceAvaragePatternEnding') as fin:
		for line in fin:
			fout.write(line)

def spaceMeanP_rgh(folder, fileName, sz):
	sz1 = sz[0]
	sz1S = sz1[0]*sz1[1]*sz1[2]
	sz2 = sz[1]
	nrows = sz1S + sz2[0] * sz2[1] * sz2[2]
	pArr = pd.read_csv(folder+'/'+fileName, header=None, skiprows=23, nrows=nrows, dtype=str)
	pArrNp = np.concatenate((avComp(pArr.iloc[:sz1S,0].to_numpy(dtype=float), sz1), avComp(pArr.iloc[sz1S:,0].to_numpy(dtype=float), sz2)), axis=0)
	pArrAv = pd.DataFrame(data=pArrNp, dtype=str, columns=['p_rgh'])
	sp.run("cp patterns/p_rghSpaceAvaragePatternBeginning "+folder+"/p_rghSpAv", shell=True, check=True)
	with open(folder+'/p_rghSpAv', 'a') as f:
		f.write(str(int(nrows/8))+'\n(\n')
	with fi.FileInput(folder+'/p_rghSpAv', inplace=True) as file:
		for line in file:
			print(line.replace('folderName', '"'+folder+'"'), end='')
	with fi.FileInput(folder+'/p_rghSpAv', inplace=True) as file:
		for line in file:
			print(line.replace('fieldName', 'p_rghSpAv'), end='')
	pArrAv['p_rgh'].to_csv(folder+'/p_rghSpAv', mode='a', index=False, header=False)
	with open(folder+'/p_rghSpAv', 'a') as fout, fi.input('patterns/alpha.waterSpaceAvaragePatternEnding') as fin:
		for line in fin:
			fout.write(line)

def avComp(arr, sz):
	arr = np.average(np.reshape(arr, (-1,2)), axis=1)
	arr = np.transpose(np.reshape(np.average(np.reshape(np.transpose(np.reshape(arr, (-1,int(sz[0]/2)))), (-1,2)), axis=1), (int(sz[0]/2),-1)))
	arr = np.transpose(np.reshape(np.average(np.reshape(np.transpose(np.reshape(arr, (-1,int(sz[0]*sz[1]/4)))), (-1,2)), axis=1), (int(sz[0]*sz[1]/4),-1)))
	arr = arr.flatten()
	return arr

def main():
	TSL = timeStepsList()
	Fs = list(['alpha.water', 'U', 'p_rgh'])
	sizes = list([[1000, 20, 100], [1000, 20, 20]])
	spaceMean(TSL, Fs, sizes)

if __name__ == "__main__":
    main()
