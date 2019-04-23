% this might need to be changed if you have gsl installed somewhere else...
% on linux/unix, you can probably just leave them blank.
GSLFLAGS = ' -I/home/jmillet/.conda/envs/project_fr/include/ -L/home/jmillet/.conda/envs/project_fr/lib/ ';
% for Eigen
EIGENFLAGS = ' -I/home/jmillet/.conda/envs/project_fr/include/eigen3/ ';

% this might need to be changed if you have eigen somewhere else...
% the following assumes that it's installed one directory up
curdir = pwd;
IFLAGS = '';
IFLAGS = [IFLAGS ' -I' curdir '/include/ '];
IFLAGS = [IFLAGS ' -I' curdir '/../common/ '];
IFLAGS = [IFLAGS ' -I' curdir '/../eigen/ '];

% this might need to be changed.  See here:
% http://openmp.org/wp/openmp-compilers/
OMPFLAG = ' -fopenmp ';

DFLAGS = ' -O ';

% if you are not using linux, the included stopwatch class will not work.
% In this case, please replace stopwatch.h or comment out the following
% line. If it is commented out, the 'time' will just be iteration count
DFLAGS = [DFLAGS ' -DUSESTOPWATCH '];

COMPFLAGS = [' CXXFLAGS="\$CXXFLAGS ' OMPFLAG '" COMPFLAGS="\$COMPFLAGS ' OMPFLAG '" '];
LFLAGS = [' LDFLAGS="\$LDFLAGS ' OMPFLAG '" -lgsl -lgslcblas -lm -lrt'];

cd 'include/';
try
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpgmm_calc_posterior.cpp niw.cpp']);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpgmm_subclusters.cpp clusters.cpp niw_sampled.cpp normal.cpp']);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpgmm_subclusters_out_data.cpp clusters.cpp niw_sampled.cpp normal.cpp']);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpgmm_FSD.cpp clusters_FSD.cpp niw_sampled.cpp normal.cpp']);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpgmm_sams.cpp cluster_single.cpp niw.cpp normal.cpp']);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpgmm_sams_superclusters.cpp cluster_single.cpp niw.cpp normal.cpp']);
catch exception
	 cd '..';
	 rethrow(exception);
end
cd '..';
