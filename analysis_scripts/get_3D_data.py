import numpy as np
import scipy.io as si


def sdat(c, F):
        data = open(F, "w")
        print "Saving in:", F
        np.save(data, c)
        data.close()
        return 0


opt = "control" #ElNino, LaNina, +2K, +2K_EL, +2KNL, 290, 310

beg = "path/to/files/OUT_3D/CHANNEL_RCE_test_RCE_256x256x64_16procs_64_0000"" 
t = 864000
l = 400 #data saved every 6 hours

for i in range( l ):
	if i%10 == 0:
		print "Doing: ", i, " / ", l
	f1 = si.netcdf_file( beg + str(t) + ".nc", 'r' )
	if i == 0:
		d1, d2, d3 = np.shape( f1.variables['QV'][0, :] )
		u = np.zeros( ( d1, d2 ) )
		w = np.zeros( ( d1, d2 ) )
		relh = np.zeros( ( d1, d2 ) )
		temp = np.zeros( ( d1, d2 ) )
		qv = np.zeros( ( d1, d2 ) )
		pp = np.zeros( ( d1, d2 ) )
		press = np.zeros( d1 )
                qn = np.zeros( ( d1, d2 ) )
	u += np.mean( f1.variables['V'][0, :], axis = 2 ) / float( l )
	w += np.mean( f1.variables['W'][0, :], axis = 2 ) / float( l )
	pp += np.mean( f1.variables['P'][0, :], axis = 2 ) / float( l )

	qv += np.mean( f1.variables['QV'][0, :], axis = 2 ) / float( l ) / 1000.
	temp += np.mean( f1.variables['TABS'][0, :], axis = 2 ) / float( l )
        qn += np.mean( f1.variables['QN'][0, :], axis = 2 ) / float( l ) / 1000.

	t += 2160


sdat( u, "data/3D_channel_" + opt + "K_U.dat" )
sdat( w, "data/3D_channel_" + opt + "K_W.dat" )
sdat( temp, "data/3D_channel_" + opt + "K_temp.dat" )
sdat( qv, "data/3D_channel_" + opt + "K_qv.dat" )
sdat( qn, "data/3D_channel_" + opt + "K_qn.dat" )
sdat( pp, "data/3D_channel_" + opt + "K_press.dat" )


for i in range( 1 ):
	temp -= 273.15 #convert to C

	d1, d2 = np.shape( temp )
	relh = np.zeros( ( d1, d2 ) )
	for j in range( d1 ):
		for k in range( d2 ):
			if temp[j, k] >= 0.:
				e_s = 0.61078 * np.exp( (17.27 * temp[j, k] ) / (temp[j, k] + 237.3) )
				e_s *= 1000. #convert from kpa to pa
				qv_s = 0.622 * e_s / (press[j] - e_s )
				relh[j, k] = qv[j, k] / qv_s 
			else:
				temp[j, k] += 273.15
				e_s = np.exp( 9.550426 - 5723.265/temp[j, k] + 3.53068* np.log(temp[j, k] ) - 0.00728332* temp[j, k] )
				qv_s = 0.622 * e_s / (press[j] - e_s )
				relh[j, k] = qv[j, k] / qv_s 
	sdat( relh, "data/3D_channel_" + opt + "K_relh.dat" )
