import numpy as np
import scipy.io as si


def sdat(c, F):
        data = open(F, "w")
        print "Saving in:", F
        np.save(data, c)
        data.close()
        return 0

var =['TABS', 'RELH', 'CLD', 'MC']
v = len( var )

beg = #Path_to_files

fnames = [ "control_CAM_12288_192", "control_-1_CAM_12288_192", "control_+1_CAM_12288_192", '+2K_CAM_12288_192', '+2K_-1_CAM_12288_192', '+2K_+1_CAM_12288_192'  ]
sf = ["control", "control_-1", "control_+1", "2K_warming", "2K_-1_warming", "2K_+1_warming" ]
f = len( fnames)

for i in range( f ):
	f1 = si.netcdf_file( beg + fnames[i] + "/OUT_STAT/CHANNEL_RCE_test_RCE_256x256x64_16procs.nc", 'r' )
	for j in range( v ):
		data = np.zeros( 64 )
		data[:] = np.mean( f1.variables[var[j]][100:], axis = 0 ) 			#STAT files save 1/day
		sdat( data, "data/mean_profiles_" + sf[i] + "_" + var[j] + ".dat" )
	

