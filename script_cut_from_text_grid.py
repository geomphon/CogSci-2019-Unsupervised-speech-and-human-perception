#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on December 11 2018
@author: Juliette MILLET (adapted from Ewan DUNBAR
# Cut all labelled intervals in a TextGrid

"""
from __future__ import print_function

from textgrid import TextGrid
import numpy as np
import sys, argparse
import os
import os.path as osp
import pandas as pd

class TextGridError(RuntimeError):
    pass

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs) # FIXME WRAP

def get_intervals(textgrid_fn, tier_name):
    tg = TextGrid()
    tg.read(textgrid_fn)
    try:
        tier_i = tg.getNames().index(tier_name)
    except ValueError:
        raise TextGridError("Cannot find tier named " + tier_name)
    return tg[tier_i]



def BUILD_ARGPARSE():
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--excluded-words',
            help="Comma-separated list of excluded words",
            type=str)
    parser.add_argument('tier_name', help="Name of TextGrid tier",
            type=str)
    parser.add_argument('output_folder', help="Name of the output folder",
            type=str)
    parser.add_argument('table_filename', help="Name of the output table",
            type=str)
    parser.add_argument('size_window_feat', help="Size in ms of the window used creating the features", type=int)
    parser.add_argument('size_stride_feat', help="Size in ms of the stride used creating the features", type=int)
    parser.add_argument('textgrid_wavfile_pairs',
            help="Comma-separated pairs of filenames: <TextGrid>,<WavFile>",
            type=str, nargs="+")
    return parser


if __name__ == "__main__":
    parser = BUILD_ARGPARSE()
    args = parser.parse_args(sys.argv[1:])
    print(args)

    excluded_words = args.excluded_words.split(",")

    if not os.path.isdir(args.output_folder):
        os.makedirs(args.output_folder)



    columns_meta = ["orig_file", "indexnumber", "int_name", "int_filename",
                    "speaker", "vowel", "context", "language"]
    meta_info = pd.DataFrame(columns = columns_meta)


    for tw in args.textgrid_wavfile_pairs:
        try:
            f_tg, f_csv = tw.split(",")
        except ValueError:
            eprint(
"""ERROR: Need to provide paired TextGrid/wave file names""".replace(
    "\n", " "))
            sys.exit(1)
        try:
            tier = get_intervals(f_tg, args.tier_name)
        except Exception as e:
            eprint(
"""Problem reading TextGrids: <M>""".replace(
    "<M>", str(e)).replace(
    "\n", " "))
            sys.exit(1)
        try:
            feat = np.loadtxt(f_csv, delimiter=',')
        except Exception as e:
            eprint(
"""Problem reading feature file: <M>""".replace(
    "<M>", str(e)).replace(
    "\n", " "))
            sys.exit(1)

        index_number = 1
        for interval in tier:
            label = interval.mark.strip()
            if label != "" and label not in excluded_words:
                int_name_split = osp.basename(f_csv).split("_")
                speaker = int_name_split[0].lower()
                language = int_name_split[2].lower()

                if label[0:2] == "SH":
                    char1 = "SH"
                else:
                    char1 = label[0]

                if label[-2:] == "SH":
                    char2 = "SH"
                else:
                    char2 = label[-1]

                context = char1 + "_" + char2
                no_first_letter = label[len(char1):]
                vowel = no_first_letter[:-len(char2)]

                item_filename = "_".join([speaker,
                                          language,
                                          str(index_number)]) + ".csv"

                start_time_ms = float(interval.minTime*1000)
                end_time_ms = float(interval.maxTime*1000)
                start_seq = int(start_time_ms/float(args.size_stride_feat))
                end_seq = int((end_time_ms)/float(args.size_stride_feat))
                segment = feat[start_seq:(end_seq+1)]

                np.savetxt(args.output_folder + "/" + item_filename,segment, delimiter=',')

                int_filename = "_".join([speaker,
                                         language,
                                         str(index_number)])

                row_index = meta_info.shape[0]
                meta_info.loc[row_index] = [f_csv, index_number, label,
                                            int_filename, speaker, vowel,
                                            context, language]

                index_number += 1
                if index_number % 20 == 0:
                    print(index_number, "done")


    meta_info.to_csv(args.table_filename, index=False)