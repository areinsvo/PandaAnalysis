#!/usr/bin/env python
from re import sub
from math import *
from array import array
from sys import argv,exit
from os import path,getenv
import os
import ROOT as r
from glob import glob
import argparse
parser = argparse.ArgumentParser(description='make forest')
parser.add_argument('--region',metavar='region',type=str,default=None)
parser.add_argument('--analysis',metavar='analysis',type=str,default=None)
#parser.add_argument('--ddt',metavar='ddt',type=bool,default=False)
parser.add_argument('--input',metavar='input',type=str,default=getenv('PANDA_FLATDIR'))

args = parser.parse_args()
nddt = False
drddt= False
region = args.region  
#out_region = args.region
#region = out_region.split('_')[0]
if region=='test':
    is_test = True 
    region = 'signal'
else:
    is_test = False

argv=[]
import PandaAnalysis.Flat.fitting_forest as forest 
from PandaCore.Tools.Misc import *
import PandaCore.Tools.Functions # kinematics
import PandaAnalysis.SuperMonoJet.BoostedSelection as sel

if args.analysis == "boosted":
    import PandaAnalysis.SuperMonoJet.BoostedSelection as sel                            
    nddt = True
if args.analysis == "resolved":
    import PandaAnalysis.SuperMonoJet.ResolvedSelection as sel
    drddt = True
if args.analysis == "monojet":
    import PandaAnalysis.SuperMonoJet.MonojetSelection as sel

basedir = args.input
lumi = 35900

def f(x):
    return basedir + x + '.root'
    print basedir + x + '.root'
def addN2DDT(rootfile):
        #load the map
	trans = r.TFile('DDT.root')
	f56 = trans.Get("DDT_5by6")
	f53 = trans.Get("DDT_5by3")
        #open the file
        output = rootfile+"_tmp"
	fi = r.TFile(rootfile)
        fo = r.TFile(output,"RECREATE")
        for tkey in fi.GetListOfKeys():
            key=tkey.GetName()
            t = fi.Get("%s"%key)
            clonet = t.CloneTree(0)
            n = t.GetEntries()	
            ndd56 = array('f', [-99])
            clonet.Branch("n2ddt56", ndd56, 'n2ddt56'+'/F')
            ndd53 = array('f', [-99])
            clonet.Branch("n2ddt53", ndd53, 'n2ddt53'+'/F')
            for j in range(0,int(n)):
                t.GetEntry(j)
                pt = t.fjpt
                mass = t.fjmass
                n2 = t.n2
                if (mass*mass/pt/pt)>0:
                    rho = log(mass*mass/pt/pt)

                    rind6 = f56.GetXaxis().FindBin(rho)
                    pind6 = f56.GetYaxis().FindBin(pt)
                    
                    rind3 = f53.GetXaxis().FindBin(rho)
                    pind3 = f53.GetYaxis().FindBin(pt)		
		
                    if rho >  f56.GetXaxis().GetBinUpEdge( f56.GetXaxis().GetNbins() ) :
                        rind6 = f56.GetXaxis().GetNbins()
                    if rho <  f56.GetXaxis().GetBinLowEdge( 1 ) :
                        rind6 = 1
                    if pt >  f56.GetYaxis().GetBinUpEdge( f56.GetYaxis().GetNbins() ) :
                        pind6 = f56.GetYaxis().GetNbins()
                    if pt < f56.GetYaxis().GetBinLowEdge( 1 ) :
                        pind6 = 1

                    if rho > f53.GetXaxis().GetBinUpEdge( f53.GetXaxis().GetNbins() ) :
                        rind3 = f53.GetXaxis().GetNbins()
                    if rho <  f53.GetXaxis().GetBinLowEdge( 1 ) :
                        rind3 = 1
                    if pt > f53.GetYaxis().GetBinUpEdge( f53.GetYaxis().GetNbins() ) :
                        pind3 = f53.GetYaxis().GetNbins()
                    if pt < f53.GetYaxis().GetBinLowEdge( 1 ) :
                        pind3 = 1
                
                    ndd56[0] = n2 - f56.GetBinContent(rind6,pind6)
                    ndd53[0] = n2 - f53.GetBinContent(rind3,pind3)

                clonet.Fill()
            fo.Write()
            
        fo.Close()
        fi.Close()
	trans.Close()
        os.system("mv -f %s %s" % (output, rootfile))


def shift_btags(additional=None):
    shifted_weights = {}
    #if not any([x in region for x in ['signal','top','w']]):
    #    return shifted_weights 
    for shift in ['BUp','BDown','MUp','MDown']:
        for cent in ['sf_btag']:
            shiftedlabel = ''
            if 'sj' in cent:
                shiftedlabel += 'sj'
            if 'B' in shift:
                shiftedlabel += 'btag'
            else:
                shiftedlabel += 'mistag'
            if 'Up' in shift:
                shiftedlabel += 'Up'
            else:
                shiftedlabel += 'Down'
            weight = sel.weights[region+'_'+cent+shift]%lumi
            if additional:
                weight = tTIMES(weight,additional)
            shifted_weights[shiftedlabel] = weight
    return shifted_weights

#vmap definition
vmap = {}
mc_vmap = {'genBosonPt':'genBosonPt'}
if 'signal' in region or 'test' in region:
    u,uphi, = ('pfmet','dphipfmet')
elif 'pho' in region:
    u,uphi = ('pfUAmag','dphipfUA')
elif 'wmn' in region or 'wen' in region or 'ten' in region or 'tmn' in region:
    u,uphi = ('pfUWmag','dphipfUW')
elif 'zee' in region or 'zmm' in region or 'tem' in region or 'tme' in region:
    u,uphi = ('pfUZmag','dphipfUZ')
vmap['met'] = 'min(%s,999.9999)'%u 
if nddt:
    vmap['fjpt'] = 'fj1Pt'
    vmap['fjmass'] = 'fj1MSD_corr'
    vmap['n2'] = 'fj1ECFN_2_3_10/pow(fj1ECFN_1_2_10,2.00)'
    vmap['doubleb'] = 'fj1DoubleCSV'

if drddt:
    vmap['fjpt'] = 'bosonpt'
    vmap['fjmass'] = 'bosonm'
    vmap['n2'] = 'bosondr'
    vmap['doubleb'] = 'min(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])'

#weights
weights = {'nominal' : sel.weights[region]%lumi}
weights.update(shift_btags())

factory = forest.RegionFactory(name = region if not(is_test) else 'test',
                               cut = sel.cuts[region],
                               variables = vmap, 
                               mc_variables = mc_vmap, 
                               mc_weights = weights)

#Process and creation of new ntuples process
if is_test:
    factory.add_process(f('Diboson'),'Diboson')

#photon CR
elif 'pho' in region:
    factory.add_process(f('GJets'),'Pho')
    factory.add_process(f('SinglePhoton'),'Data',is_data=True)
    #factory.add_process(f('SinglePhoton'),'QCD',is_data=True,
    #                    extra_weights='sf_phoPurity',extra_cut=sel.triggers['pho'])
    factory.add_process(f('QCD'),'QCD')


else:
    factory.add_process(f('ZJets'),'Zll')
    factory.add_process(f('Diboson'),'Diboson')
    factory.add_process(f('TTbar'),'ttbar')

    if 'zee' in region or 'en' in region:
        factory.add_process(f('SingleElectron'),'Data',is_data=True,extra_cut=sel.eleTrigger)

    if 'zmm' in region or 'mn' in region:
        factory.add_process(f('MET'),'Data',is_data=True,extra_cut=sel.metTrigger)
    
    if 'signal' in region or 'en' in region or 'mn' in region:
        factory.add_process(f('WJets'),'Wlv')
        factory.add_process(f('SingleTop'),'ST')
        factory.add_process(f('QCD'),'QCD')
        if 'signal' in region:
            factory.add_process(f('MET'),'Data',is_data=True,extra_cut=sel.metTrigger)
            factory.add_process(f('ZtoNuNu'),'Zvv')



forestDir = basedir + '/limits/'
os.system('mkdir -p %s'%(forestDir))
factory.run(forestDir+'/fittingForest_%s.root'%region)

#Computing n2ddt variables in the ntuples stored inside the basedir directory
if nddt:
    print 'adding n2ddt'
    addN2DDT(forestDir+'/fittingForest_%s.root'%region)
if drddt:
    print 'adding drddt'
    addN2DDT(forestDir+'/fittingForest_%s.root'%region)
