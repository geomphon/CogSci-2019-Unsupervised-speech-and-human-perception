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
	./outputs/distance_list.csv \
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
	./analysis/outputs/anon_table_fr2.csv

split_output_to_results_files:
	python ./analysis/scripts/split_output_to_results_files.py \
	./analysis/anon_data/ \
	./analysis/outputs/clean_results.csv \
	./analysis/outputs/presurvey.txt \
	./analysis/outputs/postsurvey.txt \
	./analysis/outputs/postsurvey2.txt


append_model_distances_1261:
	python ./scripts/fix_model_names.py \
	./outputs/experimental_list_w_filenames.csv \
	./outputs/model/French_model_vtln_1261_euclidean_distances.csv \
	./outputs/model/French_model_vtln_1261_euclidean_results.csv \
	./outputs/model/English_model_vtln_1261_euclidean_distances.csv \
	./outputs/model/English_model_vtln_1261_euclidean_results.csv \
	./outputs/distances_table_final.csv

append_model_distances_2541:
	python ./scripts/fix_model_names.py \
	./outputs/experimental_list_w_filenames.csv \
	./outputs/model/French_model_vtln_2541_euclidean_distances.csv \
	./outputs/model/French_model_vtln_2541_euclidean_results.csv \
	./outputs/model/English_model_vtln_2541_euclidean_distances.csv \
	./outputs/model/English_model_vtln_2541_euclidean_results.csv \
	./outputs/distances_table_final.csv

analysis_step1:
	Rscript --vanilla ./analysis/scripts/analysis_step1_preprocess_strut.Rscript \
	./analysis/outputs/presurvey.txt \
	./analysis/outputs/clean_results.csv \
	./analysis/outputs/postsurvey.txt \
	./analysis/outputs/postsurvey2.txt \
	./model/supervised/mfccs/distances_mfccs_python.csv \
	./analysis/outputs/analysed_data_mfccs_povey.csv

add_silence_to_ints:
	python ./model/supervised/intervals_for_model/downsampled/ \
	./stimuli/500ms_silence.wav \
	./model/supervised/intervals_for_model/wavs_silence/

supervised_model_files_intervals:
	python model/supervised/scripts/make_abkhazia_files_intervals.py \
	./outputs/distance_list.csv\
	./model/supervised/intervals_for_model

supervised_model_files_triplets:
	python ./model/supervised/scripts/get_times.py \
	./model/supervised/triplets_for_model/textgrid/ \
	./model/supervised/triplets_for_model/triplet_times.csv \
	&& python model/supervised/scripts/make_abkhazia_files_triplets.py \
	./outputs/distance_list.csv \
	./model/supervised/triplets_for_model/triplet_times.csv \
	./model/supervised/triplets_for_model/

supervised_model_files_fullwav:
	python ./model/supervised/scripts/get_full_wav_times.py \
	./model/supervised/full_wavs/txt_grids_full/ \
	./model/supervised/full_wavs/fullwav_times.csv \
	&& python model/supervised/scripts/make_abkhazia_files_entirewav.py \
	./model/supervised/full_wavs/fullwav_times.csv \
	./model/supervised/full_wavs/

trace_int_times:
	python model/supervised/scripts/intNfrom_txtgrids.py \
	model/supervised/full_wavs/clean_txtgrids/ \
	model/supervised/full_wavs/int_times_counts.csv \
	&& python ./model/supervised/scripts/trace_stim_from_wavs.py \
	./outputs/distance_list.csv \
	./model/supervised/full_wavs/int_times_counts.csv \
	./model/supervised/full_wavs/stim_backtraced.csv

# FIX
supervised_model_write_kl_ints:
	python ./model/supervised/scripts/kaldi2features.py \
	./model/supervised/posterior_grams/phones_int_wordLM_5gr_fr.txt \
	./model/supervised/posterior_grams/posteriors_int_wordLM_5gr_fr.post \
	./model/supervised/posterior_grams/int_wordLM_5gr_fr.h5
	&& python ./model/supervised/scripts/model_dtw.py \
	./model/supervised/posterior_grams/ outputs/distance_list.csv

supervised_model_write_kl_entwv:
	python ./model/supervised/scripts/model_dtw_entwav.py \
	./model/supervised/posterior_grams/entwav/ \
	./model/supervised/full_wavs/stim_backtraced.csv \
	./outputs/distance_list.csv

levenshtein_distance_en:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/full_wavs/lexicon.txt \
	./model/supervised/full_wavs/text.txt \
	./model/supervised/levenshtein_distance/ent_wavs/en/ spk

levenshtein_distance_fr:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/full_wavs/lexicon_fr.txt \
	./model/supervised/full_wavs/text_nocap.txt \
	./model/supervised/levenshtein_distance/ent_wavs/fr/ fr

levenshtein_distance_int_fr:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/full_wavs/lexicon_fr.txt \
	./model/supervised/intervals_for_model/text_fr.txt \
	./model/supervised/levenshtein_distance/ints/fr/ spk

levenshtein_distance_int_en:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/full_wavs/lexicon.txt \
	./model/supervised/intervals_for_model/text.txt \
	./model/supervised/levenshtein_distance/ints/en/ spk

#FIX
levenshtein_distance_jul_fr:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/full_wavs/lexicon_fr.txt \
	./model/supervised/full_wavs/text_nocap.txt \
	./model/supervised/levenshtein_distance/ent_wavs/fr/

levenshtein_distance_jul:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/en_corpus_test/lexicon_corpus_en.txt \
	./model/supervised/en_corpus_test/text_test_corpus_en.txt \
	./model/supervised/levenshtein_distance/julien/ph_en/

make_mfccs_python:
	python ./model/supervised/scripts/make_mfccs.py \
	./model/supervised/intervals_for_model/wavs/ \
	./model/supervised/mfccs/povey_mfcc_py/

mfcc_dist:
	python ./model/supervised/scripts/mfcc_dist_python.py \
	./model/supervised/mfccs/povey_mfcc_py/ \
	./model/supervised/mfccs/ \
	./outputs/distance_list.csv


