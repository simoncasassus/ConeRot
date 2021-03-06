import sys
import numpy as np
import re
from copy import copy,deepcopy
import os
from optparse import OptionParser

HOME=os.environ.get('HOME')
include_path='/home/simon/common/python/include/'
#include_path=HOME+'/common/python/conemaps-git/'
sys.path.append(include_path)
import ConeRot.MasterDConeMaps as MasterDConeMaps



sourcedir='/strelka_ssd/simon/HD135344B/Dmoments/12CO_dgauss_contsub_restored_lS0.003_lL0.0_z/'
#sourcedir='/strelka_ssd/simon/HD135344B/Dmoments/12CO_dgauss_contsub_restored_lS0.003_lL0.0_z_commonsigma/'

workdir='work_dgauss_uvmem_restored_g_v0_Merid_noregions'
workdir='work_dgauss_uvmem_restored_g_v0_Merid_noregions'
#workdir='work_dgauss_uvmem_restored_g_v0_Merid_noregions_pix2'


workdir='work_dgauss_uvmem_restored_g_v0_Merid_noregions_xtend'
workdir='work_dgauss_uvmem_restored_g_v0_Merid_noregions_xtend_xcheckvsyst'

#workdir='work_dgauss_uvmem_restored_g_v0_Merid_noregions'
#workdir='work_dgauss_uvmem_restored_g_v0_Merid_noregions_commonsigma'


a_min=0.17
a_max=0.27 # 0.37 #0.37
a_max=0.37 # xtend
#a_max=0.5

a_min_plot=a_min
a_max_plot=0.5
######################################################################

parser = OptionParser()
parser.add_option("-r", "--retrograde", action="store_true", dest="RetroGrade", default=False, help="toggle retrograde orientation (RT trials only)")
parser.add_option("-f", "--forceorient", action="store_true", dest="ForceOrient", default=False, help="toggle force input orientation in FixPAinc run")
parser.add_option("-F", "--farside", action="store_true", dest="DoFarSideOnly", default=False, help="toggle far side only")
parser.add_option("-M", "--MCMC", action="store_true", dest="RunMCMCmaster", default=False, help="toggle MCMC optim")
parser.add_option("-d", "--dry-run", action="store_false", dest="RunMaster", default=True, help="toggle dry run")
parser.add_option("-o", "--NoVarOrient", action="store_false", dest="DoVarOrient", default=True, help="no variable PA, inc profile, use with --forceorient")
parser.add_option("-R", "--Regions", action="store_true", dest="Regions", default=False, help="use regions")

#parser.add_option("-q", "--quiet",
#                  action="store_false", dest="verbose", default=True,
#                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

print("options.RetroGrade:", options.RetroGrade)
print("options.ForceOrient:", options.ForceOrient)
print("options.DoFarSideOnly:", options.DoFarSideOnly)
print("options.RunMCMCmaster:", options.RunMCMCmaster)
print("options.RunMaster:", options.RunMaster)
print("options.DoVarOrient:", options.DoVarOrient)


######################################################################

exec_master_script=sys.argv[0]

RunMCMCmaster=options.RunMCMCmaster
RunMaster=options.RunMaster
Regions=options.Regions

######################################################################
#RunMCMCmaster=False

if RunMaster:
    ClearWorkDir=True
else:
    ClearWorkDir=False

DoExec=False
PlotVarPAinc=False
if options.DoVarOrient:
    DoExec=RunMaster
    PlotVarPAinc=True
    
    

if options.ForceOrient:
    workdir += '_ForceOrient'
if options.DoFarSideOnly:
    workdir += '_FarSide'
if options.RunMCMCmaster:
    workdir += '_MCMC'
    
workdir += '/'

if options.RetroGrade:
    PA=320.-180.
    inc=(180.-40.)*np.pi/180.
else:
    PA=242.9
    inc=24.7*np.pi/180.
    inc=20.*np.pi/180.
    inc=15.*np.pi/180.
    inc=16.*np.pi/180.


    
S=MasterDConeMaps.Setup(
    #filename_source=sourcedir+'im_gmom_8.fits',
    filename_source=sourcedir+'im_g_v0.fits',
    #filename_source=sourcedir+'Smom_8.fits',
    filename_errormap=sourcedir+'im_g_v0_e.fits', #im_g_v0_errormap.fits
    #filename_errormap=sourcedir+'im_velo_errormap.fits',
    workdir=workdir, 
    DoErrorMap=True,
    typicalerror=0.1, #  km/s

    ComputeSystVelo=True,  # best run this only once, then pass value in vsyst
    #vsyst=7.0532376503043, # re-computed with continuum origin
    vsyst=7.087276144556471, 
    
    fieldscale=1., #1.
    pixscale_factor=1.0, #2.0   #6.0
    unitscale=1.,

    PA=PA,
    inc=inc, 
    tanpsi=0.3,

    # using global PA: 312.732843
    # using global inc: 2.330638
    # using global tanpsi: -0.255051

    rangePA=40.,
    rangeinc=35.*np.pi/180.,
    #rangeinc=0.1*np.pi/180.,
    rangetanpsi=0.6,

    #a_min=0.15,
    #a_max=0.75,
    a_min=a_min, #0.17
    #a_max=0.37, #0.27
    a_max=a_max, #0.27

    DoRegions=Regions,
    a_min_regions=a_min,
    #a_max_regions=0.37,
    a_max_regions=a_max,
    n_abins=4,# 6   #minimum 3 for overlap

    DoAccr=False,
    DoAccr_fixPAinc=False,
    DoMerid_fixPAinc=True,
    
    ClearWorkDir=ClearWorkDir,
    DoExec=DoExec,  # Execute the full optimization
    DoFixOrient=RunMaster, # Execute the restricted optimization, with fixed orientation

    DumpAllFitsFiles=False,

    x_center=0.002, # from the continuum
    y_center=0.017,
    #x_center=0.0,
    #y_center=0.0,

    #strelka10:32:55~/common/ppdisks/HD163296/kine/data_1$beam.py dgaussmoments_restored_cube_lS0.0005_lL1e-05_xwide_robust0.5/im_g_v0.fits 
    #python ~/common/python/simon_examplescripts/beam.py    /Users/simon/common/ppdisks/HD163296/kine/data/HD163296_CO.fits
    #0.104 x 0.095 / -80.2 
    bmaj=0.054, # arcsec
    bmin=0.054, # arcsec
    DoConjGrad=True,
    DoMinuit=False,  # BROKEN 

    DoFarSideOnly=options.DoFarSideOnly,
    RunMCMC=RunMCMCmaster,
    RecoverMCMC=RunMCMCmaster, # RunMCMC
    n_cores_MCMC=30, #30
    Nit=300,
    burn_in=150,
    nwalkers= 20,
    exec_master_script=exec_master_script)

S.domain=( ('PA',(S.PA-S.rangePA/2.,S.PA+S.rangePA/2.)), ('inc',(S.inc-S.rangeinc/2.,S.inc+S.rangeinc/2.)),('tanpsi',(S.tanpsi-S.rangetanpsi/2.,S.tanpsi+S.rangetanpsi/2.)))


if S.DoExec:
    S.Run()

SFixOrient=copy(S)
if S.DoFixOrient:
    SFixOrient.RunFixOrient(ForceGlobalOrient=options.ForceOrient, Force_allradsPA=S.PA, Force_allradsinc=S.inc)
else:
    SFixOrient.workdir=re.sub('/$','_fixPAinc/',SFixOrient.workdir)

import ConeRot.RotOrient.PlotRotorient

#ConeRot.RotOrient.PlotRotorient.execfig(S.workdir)
ConeRot.RotOrient.PlotRotorient.execfig(S.workdir,SFixOrient.filename_source, ForceGlobalOrient=options.ForceOrient, Force_allradsPA=S.PA, Force_allradsinc=S.inc,WithComparData=False,WithComparRadTWind=False,PlotVarPAinc=PlotVarPAinc,VarOrient=False,a_min=a_min_plot,a_max=a_max_plot, Plot_vRot_Global=True, Plot_vRot_VarOrient=False,Plot_vRot_VarOrient_FixIncPA=False)

import ConeRot.KineSummaryCompact

#KineSummaryCompact.exec_summary_allrads(SFixOrient.workdir,SFixOrient.filename_source,file_continuum='',vsyst=S.vsyst)



file_continuum='image_out_wl880_smooth.fits'

file_continuum='/home/simon/common/ppdisks/HD135344B/data/Cycle6/clean/tclean_HD135344Bbriggs0.0_self.fits'

ConeRot.KineSummaryCompact.exec_summary_allrads(SFixOrient.workdir,SFixOrient.filename_source,file_continuum=file_continuum,vsyst=S.vsyst,AllRads=False,a_min=a_min_plot,a_max=a_max_plot)


file_continuum='/home/simon/common/ppdisks/HD135344B/polarmaps/polarmaps_tcleanBriggs0_forceorient/HD135344B_Briggs0.0_zoom_stretched.fits'

ConeRot.KineSummaryCompact.exec_summary_faceon(SFixOrient.workdir,SFixOrient.filename_source,file_continuum=file_continuum,vsyst=S.vsyst,AllRads=False,a_min=a_min_plot,a_max=a_max_plot)

#ConeRot.KineSummaryCompact.exec_summary_faceon(SFixOrient.workdir,SFixOrient.filename_source,file_continuum=file_continuum,vsyst=S.vsyst,Zoom=True,side=1.2)
#KineSummaryCompact.exec_summary_faceon(workdir,filename_source,file_continuum=file_continuum,vsyst=5.768)


