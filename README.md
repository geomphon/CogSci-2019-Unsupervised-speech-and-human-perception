# Cog Sci 2019: Comparing unsupervised speech learning directly to human performance in speech perception

This repository contains everything needed to replicate the human experiment (stimuli, experimental scripts), the model training (DPGMM code: corpora available on request), and the analysis (trained models, data, data analysis code), from the paper,

Millet, Juliette, Jurov, Nika, and Dunbar, Ewan. "Comparing unsupervised speech learning directly to human performance in speech perception." To appear in the proceedings of Cog Sci 2019, Montreal.

## Data analysis

- The R Markdown file `analysis.Rmd` contains the complete set of analyses from the paper.
- Experimental data and acoustic/model distances, as well as cached results of long data analysis steps, are contained under `data`.

The R Markdown file depends on the following packages:

- `magrittr`
- `dplyr`
- `ggplot2`
- `readr`

## Re-training the model

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

##### 1 To export posteriors, use the 'script_extract_posteriors' and give it numpy array in .csv files (same features as the train files), and a .mat file with the model you want to use (you have the models we trained in the models folder)

```python script_extract_posteriors.py /path/2/features/test/files /path/2/model/mat/file path/to/output/folder```


##### 2 To compute ABX scores and distances wanted, use script_ABX.py

```python script_ABX.py path/to/template.csv path/to/posteriors/folder $distances_wanted path/to/output_file```

Note: the template.csv needs to contain the columns 'file_OTH' (wrong stimuli), 'file_TGT' (target stimuli) et 'file_X' (X stimuli), and is filled for each line with the name of the sample files you want to compare, you can have more information than those three columns, the script will take no account of them.

Note2: $distances_wanted can be euclidean, cosine... any distance that the module dtw.py accepts.  

Note3: this script creates 3 files, name_wanted_final.csv is a copy of the template.csv with the distances added, name_wanted_results.csv is of the form A, B, X, real (right answer), result_model (model's answer) and name_wanted_distances.csv same as _results but with AX and BX distances at the end


## Construction of stimuli and human experiment

The repository contains the following files inside the folder `humans` , needed for the ABX discrimination task experiment construction:

* `scripts` folder containing the scripts, needed to generate the tables, to cut the sound files, resample them etc.;
* `outputs` folder containing all the tables, .csvs or other text files, generated by the scripts;
* `stimuli` folder, containing the recorded .wav files and the annotated corresponding .TextGrids. It includes the `intervals` folder, where all the segmented intervals are stored, and the `triplets` folder, where all the sound files used for the experiment are (concatenated three intervals: A, B and X sound);
* `lmeds_material` folder, where all the necessary files for the online experiment are stored;
* `analysis` folder containing the anonymized data, the scripts necessary for the analysis as well as the outputs of those scripts.

### Steps to take:

* Have sound .wav files with their corresponding TextGrids and the silence file ready in `./stimuli` folder
* **make** `cut_intervals`: cuts the .wav files into intervals (only the stimuli)
* **make** `create_experimental_list`: creates the list that has balanced quantity of each possible vowel that will be tested, as well as balanced appearance of each possible speaker and the context *C_C*
* **make** `create_stim_filename_distance_lists`: adds the interval filenames to the experimental lists, creates the `Stimulus_list.txt` needed to concatenate intervals and creates a `distance_list.csv` that has different column names (needed this format for the analysis)
* **make** `concatenate_intervals`: concatenates the intervals with the silence `.wav` file into a concatenated triplet with a new name and creates also the `.mp3` and `.ogg` versions needed for the LMEDS
* **make** `make_lmeds_sequence`: creates the part of the LMEDS sequence where the triplet filenames are inserted as stimuli to be tested

* copy the contents of `lmeds_material` folder to the LMEDS folder on the server, fix the sequences
* run the test

* **make** `calculate_distances`: calculates the euclidean distances with the DTW algorithm and appends them to the `distance_list_final.csv`
* **make** `anonymize_lmeds_data`: anonymizes the names of the participants and creates two new subfolders with a language name where all data is anonymized
* **make** `split_output_to_results_files`: maps the results from the LMEDS to comprehensible tables (sequence, presurvey, postsurvey, postsurvey2)
* **make** `analysis_step1_preprocess_strut`: the data from sequence, postsurveys and the presurvey is combined and ordered into a new csv, ready for the analysis.


### Important

* LMEDS needs to be downloaded separately
* LMEDS sequence needs to be manually fixed
* `.cgi` and folders `lmeds/test_name/individual_sequences` and `lmeds/test_name/\outputs` need to have permissions to be modified by the test takers (`chmod 777 $filename$`)
* results need to be stored in separate subfolders named by *language* to allow the analysis processing

## Analysis tools
## Citations
