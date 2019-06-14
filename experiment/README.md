# Cog Sci 2019: Comparing unsupervised speech learning directly to human performance in speech perception

**This repository contains large binary files stored as Git LFS.** Install Git LFS (https://help.github.com/en/articles/installing-git-large-file-storage) before cloning.

This repository contains everything needed to replicate the human experiment (stimuli, experimental scripts), the model training (DPGMM code, requires MATLAB; corpora available on request), and the analysis (trained models, data, data analysis code), from the paper,

> **Millet, Juliette, Jurov, Nika, and Dunbar, Ewan.** *Comparing unsupervised speech learning directly to human performance in speech perception.* To appear in the proceedings of Cog Sci 2019, Montreal.


## Reproducing the human experiment

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
