# Cog Sci 2019: Comparing unsupervised speech learning directly to human performance in speech perception

**This repository contains large binary files stored as Git LFS.** Install Git LFS (https://help.github.com/en/articles/installing-git-large-file-storage) before cloning.

This repository contains everything needed to replicate the human experiment (stimuli, experimental scripts), the model training (DPGMM code, requires MATLAB; corpora available on request), and the analysis (trained models, data, data analysis code), from the paper,

> **Millet, Juliette, Jurov, Nika, and Dunbar, Ewan.** *Comparing unsupervised speech learning directly to human performance in speech perception.* To appear in the proceedings of Cog Sci 2019, Montreal.

## Reproducing the DPGMM training

### Input feature preparation

The paper uses MFCCs as inputs. If you do not want to use kaldi, you can extract MFCC features from a directory containing wav files (but no vtln will be applied to it), to corresponding CSVs in another directory, use

```python script_create_feature_file.py mfccs <wav directory> <feature output directory>```

Otherwise you can use kaldi to extract your features following the tutorial in the folder vtln. Once you have all your data as csv files, you can do the following:

The features must be moved into a single `.mat` file  for training, and a single CSV for validation. The paper uses a 90/10 split:

```python script_csvnp2mat.py  <feature output directory> <training data filename>.mat <validation data filename>.csv 10```

The CSV file contains all the validation frames (not used for training) on which you can test the log-likelihood of your model as it learns.

Dependencies:

- `librosa`
- `scipy`
- `numpy`

### Model training

Dependencies:

- MATLAB
- GNU Scientific Library (GSL)
- Eigen

Add your GSL and Eigen library paths to LD_LIBRARY_PATH:

```export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<gsl_path>:<eigen_path>```

Modify the `GSLFLAGS` and `EIGENFLAGS` variables in the file file `dpgmm/dpmm_subclusters_2014-08-06/Gaussian/compile_MEX.m` to correspond to your environment.

Change directories to `dpgmm/dpmm_subclusters_2014-08-06/Gaussian`. Launch MATLAB and do

```compile_MEX```

This will compile the C code. Check that everything is okay by launching the demo:

```demo```

If everything is working, you can start using the code:

```my_run_dpgmm_subclusters('<training data filename>.mat', '<output_folder>', <number of CPUs>, true);```


The folder `<output_folder>` will contain saved parameters of the models every 20 iterations, saved as .mat files. You must create this folder, and a `log/` subfolder, in advance, if you want the log likelihood to be saved during the training process.
