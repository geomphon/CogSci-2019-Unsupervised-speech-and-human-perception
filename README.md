# Cog Sci 2019: Comparing unsupervised speech learning directly to human performance in speech perception

**This repository contains large binary files stored as Git LFS.** Install Git LFS (https://help.github.com/en/articles/installing-git-large-file-storage) before cloning.

This repository contains everything needed to replicate the human experiment (stimuli, experimental scripts), the model training (DPGMM code, requires MATLAB; corpora available on request), and the analysis (trained models, data, data analysis code), from the paper,

> **Millet, Juliette, Jurov, Nika, and Dunbar, Ewan.** *Comparing unsupervised speech learning directly to human performance in speech perception.* To appear in the proceedings of Cog Sci 2019, Montreal.


## Reproducing the data analysis

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


## Reproducing the human experiment


The current repository contains the following files inside the folder `experiment`  needed for the ABX discrimination task experiment construction:

* `scripts` folder containing the scripts, needed to generate the tables, to cut the sound files, resample them etc.;
* `outputs` folder containing all the tables, .csvs or other text files, generated by the scripts;
* `stimuli` folder, containing the recorded .wav files and the annotated corresponding .TextGrids. It includes the `intervals` folder, where all the segmented intervals are stored, and the `triplets` folder, where all the sound files used for the experiment are (concatenated three intervals: A, B and X sound);
* `lmeds_material` folder, where all the necessary files for the online experiment are stored;
* `analysis` folder containing the anonymized data, the scripts necessary for the analysis as well as the outputs of those scripts.

See `experiment/README.md` for details on reproducing the experiment.



## Reproducing the DPGMM training

Training corpora are open source and are available on request (they are too large for this repository). Further details on reproducing training can be found in `README_DPGMM_training.md`. Trained model (`.mat`) files can be found in `models/`.

## Applying the trained models to the experimental stimuli


### Method for generating posteriorgrams used in the paper

If you want to transform the entire source files and then cut them (as we did in the paper), you need to extract features for the uncut wav files:

```python script_create_feature_file.py mfccs Stimuli/wavs_source <stimuli feature output directory>```

Then extract posteriors:

```python script_extract_posteriors.py <stimuli feature output directory> <saved model mat file> <posterior directory source files>```

Then cut out the relevant portions:

```python script_cut_from_text_grid.py --excluded-words JE,STOCKE,ICI,I,LIKE,HERE,sp word <cut files folder> <meta information of each cut file.csv> <window size in ms> <stride size in ms> <textgrid file 1>,<posterior file 1> <textgrid file 2>,<posterior file 2> ... ```


### Alternative: Conceptually more sensible (but worse-performing) method to generate posteriorgrams

To apply the features directly to the cut-out experimental stimuli use  `script_create_feature_file.py` to extract MFCC features for the cut-out experimental stimuli:

```python script_create_feature_file.py mfccs experiment/stimuli/intervals <stimuli feature output directory>```

Then extract posteriors using a trained model:

```python script_extract_posteriors.py <stimuli feature output directory> <saved model mat file> <posterior directory>```

This is not what we did in the paper (see above) because Kaldi feature extraction for short files is problemeatic. The approach of using the source files also (some improve the quality of the speaker normalization.

### Computing distances

To compute distances on posteriorgrams,

```python script_ABX.py stimuli/triplets_list.csv <posterior directory> kl_divergence <output_prefix>```

To compute distances on MFCCs,

```python script_ABX.py stimuli/triplets_list.csv <stimuli feature output directory> cosine <output_prefix>```


If you wish to compute distances on another set of triplets, you need to create a file analogous to `stimuli/triplets_list.csv`. Critically, it must contain the columns 'file_OTH' (incorrect answer stimulus), 'file_TGT' (target stimulus) et 'file_X' (X stimulus).


This script creates 3 files: <output_prefix>_final.csv is a copy of template.csv with the distances added, <output_prefix>_results.csv is of the form A, B, X, real (right answer), result_model (model's answer) and <output_prefix>_distances.csv same as _results but with AX and BX distances at the end





