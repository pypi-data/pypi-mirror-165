##############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

"""
Definitions of LHCb PID MC datasets (ROOT files produced by WG productions). 
The ROOT files can contain several trees corresponding to different calibration samples. 
These dictionaries are used further in the definitions of calibration samples (see samples/ subdir). 
"""

run2sim09_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen/MC/Run2Sim09"
photon_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDGen2/calibration/photon/"

dstar_run2sim09_datasets = {
  'MagDown_2018': [f"{run2sim09_dir}/tuple_dstar_mc18_magdown.root" ], 
  'MagUp_2018':   [f"{run2sim09_dir}/tuple_dstar_mc18_magup.root" ], 
  'MagDown_2017': [f"{run2sim09_dir}/tuple_dstar_mc17_magdown.root" ], 
  'MagUp_2017':   [f"{run2sim09_dir}/tuple_dstar_mc17_magup.root" ], 
  'MagDown_2016': [f"{run2sim09_dir}/tuple_dstar_mc16_magdown.root" ], 
  'MagUp_2016':   [f"{run2sim09_dir}/tuple_dstar_mc16_magup.root" ], 
  'MagDown_2015': [f"{run2sim09_dir}/tuple_dstar_mc15_magdown.root" ], 
  'MagUp_2015':   [f"{run2sim09_dir}/tuple_dstar_mc15_magup.root" ], 
}

photon_run1sim09_datasets_kstargamma = {
  "2011-2012" : [f"{photon_dir}/mc_run0_mode0.root"], 
}

photon_run2sim09_datasets_kstargamma = {
  "2016" : [f"{photon_dir}/mc_run1_mode0.root"], 
  "2017" : [f"{photon_dir}/mc_run2_mode0.root"], 
  "2018" : [f"{photon_dir}/mc_run3_mode0.root"], 
}
