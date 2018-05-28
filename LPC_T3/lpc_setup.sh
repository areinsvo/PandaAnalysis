#!/bin/bash                                                                                                                                                                                                 
export PATH=${PATH}:${CMSSW_BASE}/src/PandaCore/bin/

#submission number
export SUBMIT_NAME="v_8029_May26_diboson"
#scratch space
export scratch_area="/uscms_data/d3"
export PANDA="${CMSSW_BASE}/src/PandaAnalysis"
#cfg file
#export PANDA_CFG="http://t3serv001.mit.edu/~mcremone/eoscatalog/test_009.cfg"
#export PANDA_CFG="http://home.fnal.gov/~sudha/LPC-DM/20180521.cfg"
#export PANDA_CFG="http://sundleeb.web.cern.ch/sundleeb/panda_config/DYJets_20180525.cfg"
#export PANDA_CFG="http://sundleeb.web.cern.ch/sundleeb/panda_config/QCD_20180525.cfg"
export PANDA_CFG="http://sundleeb.web.cern.ch/sundleeb/panda_config/Diboson_20180525.cfg"
#export PANDA_CFG="http://sundleeb.web.cern.ch/sundleeb/panda_config/Top_20180525.cfg"
#export PANDA_CFG="http://sundleeb.web.cern.ch/sundleeb/panda_config/WJets_20180525.cfg"
#export PANDA_CFG="http://sundleeb.web.cern.ch/sundleeb/panda_config/ZtoNuNu_20180525.cfg"
#export PANDA_CFG="http://sundleeb.web.cern.ch/sundleeb/panda_config/MET_20180525.cfg"
#export PANDA_CFG="http://sundleeb.web.cern.ch/sundleeb/panda_config/SingleElectron_20180525.cfg"
#skim
export SUBMIT_TMPL="skim_monojet_tmpl.py"
#panda's 
export PANDA_FLATDIR="${scratch_area}/${USER}/panda/"${SUBMIT_NAME}"/flat/"
#export SUBMIT_OUTDIR="${scratch_area}/${USER}/panda/"${SUBMIT_NAME}"/batch/"
export SUBMIT_OUTDIR="/store/user/${USER}/panda/"${SUBMIT_NAME}"/batch/"
#condor's
export SUBMIT_WORKDIR="${scratch_area}/${USER}/condor/"${SUBMIT_NAME}"/work/"
export SUBMIT_LOGDIR="${scratch_area}/${USER}/condor/"${SUBMIT_NAME}"/logs/"
mkdir -p $PANDA_FLATDIR $SUBMIT_WORKDIR $SUBMIT_LOGDIR
eosmkdir -p $SUBMIT_OUTDIR

export SUBMIT_CONFIG=T2  # allow running on T3 or T2. if $SUBMIT_CONFIG==T3, then only run on T3
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ""
echo ""
cat << "EOF"
  _____        _   _ _____                      ______ _   _          _          _____  __  __ 
 |  __ \ /\   | \ | |  __ \   /\        ____   |  ____| \ | |   /\   | |        |  __ \|  \/  |
 | |__) /  \  |  \| | |  | | /  \      / __ \  | |__  |  \| |  /  \  | |  ______| |  | | \  / |
 |  ___/ /\ \ | . ` | |  | |/ /\ \    / / _` | |  __| | . ` | / /\ \ | | |______| |  | | |\/| |
 | |  / ____ \| |\  | |__| / ____ \  | | (_| | | |    | |\  |/ ____ \| |____    | |__| | |  | |
 |_| /_/    \_\_| \_|_____/_/    \_\  \ \__,_| |_|    |_| \_/_/    \_\______|   |_____/|_|  |_|
                                       \____/                                                  
EOF
echo ""
echo "Checking ENV path"
echo "======================================================================="

for path in $PANDA_FLATDIR /eos/uscms${SUBMIT_OUTDIR} $SUBMIT_WORKDIR $SUBMIT_LOGDIR
do
if [ -e $path ];then
echo "Path : ${path} is properly set"
else
echo "Path : ${path} does not exist, please fix it."
fi
done
echo "======================================================================"
echo "INFO"
echo "======================================================================"
echo "Submit Name  = ${SUBMIT_NAME}"
echo "cfg selected = ${PANDA_CFG}"
echo "submit tmpl  = ${SUBMIT_TMPL}"
echo "======================================================================"
echo ""
echo ""
