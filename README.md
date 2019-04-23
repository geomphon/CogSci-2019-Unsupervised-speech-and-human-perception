# Comparing_humans_vs_DPGMM_en_fr
## Model
### I Preparation of the features to train the dpgmm model:

##### 1 If you only want mfccs you can extract your features as numpy array in .csv files from .wav files with the script 'script_create_feature_file'(with name_of_features_wanted=mfccs):

```python script_create_feature_file.py name_of_features_wanted path/2/wav/files path/2/features/created```

##### 1bis If you want more sophisticated features, you can use kaldi to extract vtln features, but you still need to obtain a folder with your csv numpy array feature files in it.
##### 2 If you do not want any validation set (only training set), convert your features file as one big .mat file with 'script_csvnp2mat':

```python script_csvnp2mat.py path/2/feat/files path/2/mat/file```

##### 2bis If you want a validation set (as a csv file) that represents a certain percentage of your original set do:

```python script_csvnp2mat.py path/2/feat/files path/2/train/set/file.mat path/2/validation/set/file.csv $percentage_wanted ```

If you do that, you will obtain two files: one .mat file on wich your dpgmm model is going to be trained, and a .csv file that contains all the validation frames, not used for training, on which you can test the log-likelihood of your model evolving.
### II Training of the model: use of the matlab code

##### 1 Add the lib folder where your gsl library and eigen library are to the environment variable called LD_LIBRARY_PATH:

```export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/2/library```

example:

```export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/yourname/.conda/envs/your_conda_environment/lib/```

##### 2 Launch matlab (you need to go in the gaussian folder of the dpgmm code) and compile the C code (this needs to be done only once, check the path in the compile_MEX.m file, you need to change the GSLFLAGS and the EIGENFLAGS to correspond to your environment)

```cd Gaussian```

```compile_MEX```

##### 3 You can check everything is ok by launching the demo

```demo```

##### 4 If everything is working, you can start using the code:

```my_run_dpgmm_subclusters('path/2/features.mat', 'path/2/model_folder', nb_cpu, true);```

with nb_cpu the number of cpu you can use

######Note: in path/2/model/folder the code will stock the parameters of the models every 20 iterations as .mat files. You will need to have a log/ folder in this folder for the code to also stock the values of the loglikelihood during the training process.
### III Export results

##### 1 To export posteriors, use the 'script_extract_posteriors' and give it numpy array in .csv files (same features as the train files):

```python script_extract_posteriors.py /path/2/features/test/files /path/2/model/mat/file path/to/output/folder```


##### 2 To compute ABX scores and distances wanted, use script_ABX.py

```python script_ABX.py path/to/template.csv path/to/posteriors/folder $distances_wanted path/to/output_file```

Note: the template.csv needs to contain the columns 'file_OTH' (wrong stimuli), 'file_TGT' (target stimuli) et 'file_X' (X stimuli), and is filled for each line with the name of the sample files you want to compare, you can have more information than those three columns, the script will take no account of them.

Note2: $distances_wanted can be euclidean, cosine... any distance that the module dtw.py accepts.  

Note3: this script creates 3 files, name_wanted_final.csv is a copy of the template.csv with the distances added, name_wanted_results.csv is of the form A, B, X, real (right answer), result_model (model's answer) and name_wanted_distances.csv same as _results but with AX and BX distances at the end


## Stimuli
## Analysis tools
## Citations
