import numpy as np
import scipy.io as si

def sdat(c, F):
	print "Saving in:", F
	data = open(F, "w")
	np.save(data, c)
	data.close()
	return 0

var = ['Prec', 'W500', 'USFC', 'VSFC', 'CLD', 'SWNT', 'LWNT', 'SWNTC', 'LWNTC']
v = len( var )

beg = #Path_to_files

fnames = [ "control_CAM_12288_192", "control_-1_CAM_12288_192", "control_+1_CAM_12288_192", '+2K_CAM_12288_192', '+2K_-1_CAM_12288_192', '+2K_+1_CAM_12288_192'  ]
sf = ["control", "control_-1", "control_+1", "2K_warming", "2K_-1_warming", "2K_+1_warming" ]
f = len( fnames)

for j in range( v ):
	for i in range( f):
		f1 = si.netcdf_file( beg + fnames[i] + "/OUT_2D/CHANNEL_RCE_test_RCE_256x256x64_16procs_64.2Dcom_1.nc", 'r' )
		f2 = si.netcdf_file( beg + fnames[i] + "/OUT_2D/CHANNEL_RCE_test_RCE_256x256x64_16procs_64.2Dcom_2.nc", 'r' )
		f3 = si.netcdf_file( beg + fnames[i] + "/OUT_2D/CHANNEL_RCE_test_RCE_256x256x64_16procs_64.2Dcom_3.nc", 'r' )
		d1, d2, d3 = np.shape( f1.variables[var[j]][:] )
		d4, d2, d3 = np.shape( f2.variables[var[j]][:] )
		d5, d2, d3 = np.shape( f3.variables[var[j]][:] )
		data = np.zeros( ( d1 + d4 + d5, d2 ) )
		data[:d1] = np.mean( f1.variables[var[j]][:], axis = 2 )
		data[d1:d1 + d4] = np.mean( f2.variables[var[j]][:], axis = 2 )
		data[d1 + d4:] = np.mean( f3.variables[var[j]][:], axis = 2 )

#Data collected every 4 hours. Save last 100 days
sdat( np.mean( data[400:], axis = 0 ), "data/" + sf[i] + "_" + var[j] + ".dat" )
