% this might need to be changed if you have gsl installed somewhere else...
% on linux/unix, you can probably just leave them blank.
GSLFLAGS = ' -I/home/jmillet/.conda/envs/project_fr/include/ -L/home/jmillet/.conda/envs/project_fr/lib/ ';
% for Eigen
EIGENFLAGS = ' -I//home/jmillet/.conda/envs/project_fr/include/eigen3/ ';

% this might need to be changed if you have eigen somewhere else...
% the following assumes that it's installed one directory up
curdir = pwd;
IFLAGS = '';
IFLAGS = [IFLAGS ' -I' curdir '/include/ '];
IFLAGS = [IFLAGS ' -I' curdir '/../common/ '];

% this might need to be changed.  See here:
% http://openmp.org/wp/openmp-compilers/
OMPFLAG = ' -fopenmp ';

DFLAGS = ' -O ';

% if you are not using linux, the included stopwatch class will not work.
% In this case, please replace stopwatch.h or comment out the following
% line. If it is commented out, the 'time' will just be iteration count
DFLAGS = [DFLAGS ' -DUSESTOPWATCH '];

% if you are under memory constraints, you may want to comment out the
% following line. if USEFULL is defined, the counts for the dirichlet prior
% will not be sparse. If USEFULL is not defined, the counts will be stored
% using a sparse hash table. Note that performance is best if this line is
% left *uncommented*.
DFLAGS = [DFLAGS ' -DUSEFULL '];


COMPFLAGS = [' CXXFLAGS="\$CXXFLAGS ' OMPFLAG '" COMPFLAGS="\$COMPFLAGS ' OMPFLAG '" '];
LFLAGS = [' LDFLAGS="\$LDFLAGS ' OMPFLAG '" -lgsl -lgslcblas -lm -lrt -largeArrayDims'];

COMMON_FILES = 'dir_sampled_full.cpp dir_sampled_hash.cpp multinomial.cpp';

cd 'include/';
try
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpmnmm_calc_posterior.cpp ' COMMON_FILES]);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpmnmm_subclusters.cpp clusters_mn.cpp ' COMMON_FILES]);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpmnmm_FSD.cpp clusters_FSD_mn.cpp ' COMMON_FILES]);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpmnmm_sams.cpp ' COMMON_FILES]);
    eval(['mex' DFLAGS IFLAGS COMPFLAGS LFLAGS GSLFLAGS EIGENFLAGS ' dpmnmm_sams_superclusters.cpp ' COMMON_FILES]);
catch exception
	 cd '..';
	 rethrow(exception);
end
cd '..';
