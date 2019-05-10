cut_intervals: 
	python scripts/cut_all.py\
	--excluded-words JE,STOCKE,ICI,I,LIKE,HERE,sp\
	word ./stimuli/intervals outputs/interval_meta_information.csv\
	stimuli/Jeremy_ABX_ENG_corrected.TextGrid,stimuli/Jeremy_ABX_ENG_clean.wav\
	stimuli/Maureen_ABX_ENG_corrected.TextGrid,stimuli/Maureen_ABX_ENG_clean.wav\
	stimuli/Maureen_ABX_FR_corrected.TextGrid,stimuli/Maureen_ABX_FR_clean.wav\
	stimuli/Ewan_ABX_ENG_corrected.TextGrid,stimuli/Ewan_ABX_ENG_clean.wav\
	stimuli/Marc_ABX_FR_corrected.TextGrid,stimuli/Marc_ABX_FR_clean.wav\
	stimuli/Remi_ABX_FR_corrected.TextGrid,stimuli/Remi_ABX_FR_clean.wav\
	stimuli/Veronique_ABX_ENG_corrected.TextGrid,stimuli/Veronique_ABX_ENG_clean.wav\
	stimuli/Veronique_ABX_FR_corrected.TextGrid,stimuli/Veronique_ABX_FR_clean.wav

create_experimental_list:
	python scripts/create_stimlist2.py --seed 26 --nsteps 1000000 112 \
	intervals/interval_meta_information.csv experimental_list.csv

create_experimental_lists:
	python  ./scripts/fill_filenames_to_experimental_list.py  \
	./outputs/experimental_list.csv ./stimuli/intervals/ \
	./outputs/interval_meta_information.csv

concatenate_intervals:
	python ./scripts/concatenate_intervals.py ./stimuli/intervals/ \
	./outputs/Stimuli_list.txt ./stimuli/500ms_silence.wav \
	./stimuli/triplets

make_lmeds_sequence:
	python ./scripts/print_stim_to_table.py ./triplets/wavs \
	./lmeds_materials/sequence_to_be_fixed.txt

normalize_vectors:
	python ./scripts/normalize_vectors.py \
	./stimuli/mfccs/ \
	./stimuli/mfccs_norm/

calculate_distances:
	python ./scripts/dtw_distances.py \
	./outputs/item_info.csv \
	./stimuli/mfccs_norm/ 

anonymize_lmeds_data:
	python ./analysis/scripts/anonymize_lmeds_data_filenames.py \
	./analysis/lmeds_results_not_github/eng \
	./analysis/anon_data/eng \
	./analysis/outputs/anon_table_eng.csv \
	&& python ./analysis/scripts/anonymize_lmeds_data_filenames.py \
	./analysis/lmeds_results_not_github/fr \
	./analysis/anon_data/fr \
	./analysis/outputs/anon_table_fr.csv \
	&& python ./analysis/scripts/anonymize_lmeds_data_filenames.py \
	./analysis/lmeds_results_not_github/fr2 \
	./analysis/anon_data/fr2 \
	

split_output_to_results_files:
	python ./analysis/scripts/split_output_to_results_files.py \
	./analysis/anon_data/ \
	./analysis/outputs/clean_results.csv \
	./analysis/outputs/presurvey.txt \
	./analysis/outputs/postsurvey.txt \
	./analysis/outputs/postsurvey2.txt

combine_output:
	Rscript --vanilla ./analysis/scripts/combine_filter.Rscript \
	./analysis/outputs/presurvey.txt \
	./analysis/outputs/clean_results.csv \
	./analysis/outputs/postsurvey.txt \
	./analysis/outputs/postsurvey2.txt \
	./outputs/item_info.csv \
	./analysis/outputs/experiment_data.csv
