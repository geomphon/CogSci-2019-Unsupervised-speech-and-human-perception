# Cog Sci 2019: Comparing unsupervised speech learning directly to human performance in speech perception

**This repository contains large binary files stored as Git LFS.** Install Git LFS (https://help.github.com/en/articles/installing-git-large-file-storage) before cloning.

This repository contains everything needed to replicate the human experiment (stimuli, experimental scripts), the model training (DPGMM code, requires MATLAB; corpora available on request), and the analysis (trained models, data, data analysis code), from the paper,

> **Millet, Juliette, Jurov, Nika, and Dunbar, Ewan.** *Comparing unsupervised speech learning directly to human performance in speech perception.* To appear in the proceedings of Cog Sci 2019, Montreal.


## Data analysis

- The R Markdown file `analysis.Rmd` contains the complete set of analyses from the paper, and should be knitted to reproduce them
- The output can be seen in `analysis.html` and the figures, in particular, under `figures/`
- A secondary, post-hoc analysis with an additional filtering, mentioned in the paper, can be done by knitting `analysis__filtered.Rmd`
- Experimental data and acoustic/model distances, as well as cached results of long data analysis steps, are contained under `data`

The R Markdown file depends on the following packages:

- `magrittr`
- `dplyr`
- `ggplot2`
- `readr`
- `knitr`

## Re-training the DPGMM model

Corpora are available on request.

### Input feature preparation

The paper uses MFCCs as inputs. To extract MFCC features from a directory containing wav files, to corresponding CSVs in another directory, use

```python script_create_feature_file.py mfccs <wav directory> <feature output directory>```

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

### Calculating posteriors for the experimental stimuli

First use  `script_create_feature_file.py` to extract MFCC features for the experimental stimuli:

```python script_create_feature_file.py mfccs experiment/stimuli/intervals <stimuli feature output directory>```

Then extract posteriors using a trained model:

```python script_extract_posteriors.py <stimuli feature output directory> <saved model mat file> <posterior directory>```

If you want to transform the source files and then cut them (as we did in the paper), you need to extract the posteriors from the features extracted from the big source files and then cut them following the textgrid files:

```python script_extract_posteriors.py <stimuli feature output directory (of source files)> <saved model mat file> <posterior directory source files>```


```python script_cut_from_text_grid.py --excluded-words JE,STOCKE,ICI,I,LIKE,HERE,sp word <cut files folder> <meta information of each cut file.csv> <window size in ms> <stride size in ms> <textgrid file 1>,<posterior file 1> <textgrid file 2>,<posterior file 2> ... ```

### Computing distances

To compute distances on posteriorgrams,

```python script_ABX.py stimuli/triplets_list.csv <posterior directory> kl_divergence <output_prefix>```

To compute distances on MFCCs,

```python script_ABX.py stimuli/triplets_list.csv <stimuli feature output directory> cosine <output_prefix>```


If you wish to compute distances on another set of triplets, you need to create a file analogous to `stimuli/triplets_list.csv`. Critically, it must contain the columns 'file_OTH' (incorrect answer stimulus), 'file_TGT' (target stimulus) et 'file_X' (X stimulus).


This script creates 3 files: <output_prefix>_final.csv is a copy of template.csv with the distances added, <output_prefix>_results.csv is of the form A, B, X, real (right answer), result_model (model's answer) and <output_prefix>_distances.csv same as _results but with AX and BX distances at the end


## Construction of stimuli and human experiment


The current repository contains the following files inside the folder `experiment`  needed for the ABX discrimination task experiment construction:

* `scripts` folder containing the scripts, needed to generate the tables, to cut the sound files, resample them etc.;
* `outputs` folder containing all the tables, .csvs or other text files, generated by the scripts;
* `stimuli` folder, containing the recorded .wav files and the annotated corresponding .TextGrids. It includes the `intervals` folder, where all the segmented intervals are stored, and the `triplets` folder, where all the sound files used for the experiment are (concatenated three intervals: A, B and X sound);
* `lmeds_material` folder, where all the necessary files for the online experiment are stored;
* `analysis` folder containing the anonymized data, the scripts necessary for the analysis as well as the outputs of those scripts.

### Steps to take to re-run the experiment:

* Have sound .wav files with their corresponding TextGrids and the silence file ready in `./stimuli` folder
* **make** `cut_intervals`: cuts the .wav files into intervals (only the stimuli)
* **make** `create_experimental_list`: creates the list that has balanced quantity of each possible vowel that will be tested, as well as balanced appearance of each possible speaker and the context *C_C*
* **make** `create_stim_filename_distance_lists`: adds the interval filenames to the experimental lists, creates the `Stimulus_list.txt` needed to concatenate intervals and creates a `distance_list.csv` that has different column names (needed this format for the analysis)
* **make** `concatenate_intervals`: concatenates the intervals with the silence `.wav` file into a concatenated triplet with a new name and creates also  `.mp3` and `.ogg` versions
* **make** `make_lmeds_sequence`: creates the part of the LMEDS sequence file in which the triplet filenames are inserted as stimuli to be tested

To run the experiment, you must download LMEDS, which you can obtain from here,

https://github.com/geomphon/LMEDS_v

Copy the contents of `lmeds_material` folder to the LMEDS folder on a remote server and modify the the sequence files following the output of `make make_lmeds_sequence`.

On the server, the `.cgi` and folders `lmeds/test_name/individual_sequences` and `lmeds/test_name/\outputs` need to have permissions 777 (`chmod 777 $filename$`)

* **make** `anonymize_lmeds_data`: anonymizes the names of the participants and creates two new subfolders with a language name where all data is anonymized (data provided here is already anonymized)
* **make** `split_output_to_results_files`: maps the results from the LMEDS to comprehensible tables (sequence, presurvey, postsurvey, postsurvey2)
* **make** `combine_output`: the data from sequence, postsurveys and the presurvey is combined and ordered into a new csv and filtered, ready for the analysis (the resulting file, `analysis/outputs/experiment_data.csv` should be identical to the top-level `data/experiment_data.csv`)


