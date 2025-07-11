#!/usr/bin/env python3

import copier
import sys
import csv
import yaml
import os
import argparse

def read_csv_file(filename):
    with open(filename, mode='r') as csv_file:
        csv_row_dict_list = list()  # list of key-value pairs produced from every CSV row except header
        for row in csv.DictReader(csv_file):
            updated_row_dict = dict()
            for k, v in row.items():
                # remove potential spaces left and right
                k = k.strip()
                if v:
                    v = v.strip()
                updated_row_dict.update({k: v})

            csv_row_dict_list.append(updated_row_dict)

        return csv_row_dict_list

def read_yaml_file(filename, load_all=False):
    with open(filename, mode='r') as f:
        if not load_all:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        else:
            # convert generator to list before returning
            yaml_data = list(yaml.load_all(f, Loader=yaml.FullLoader))
    return yaml_data

def load_extra_vars(data_input_directory):

    extra_vars = dict()
    # load all data from input directory and assign to corresponding dict keys
    data_input_directory_full_path = os.path.join(
        os.getcwd(), data_input_directory)
    if not os.path.isdir(data_input_directory_full_path):
        sys.exit(
            f'ERROR: Can not find data input directory {data_input_directory_full_path}')
    
    # read files from the data input directory and add to extra_vars
    # every file will be added as dictionary with a filename without extension as the parent key
    for a_name in os.listdir(data_input_directory_full_path):
        a_full_path = os.path.join(data_input_directory_full_path, a_name)
        if os.path.isfile(a_full_path):
            if '.csv' in a_name.lower():
                csv_data = read_csv_file(a_full_path)
                
                extra_vars.update({
                    # [:-4] removes .csv
                    a_name.lower()[:-4]: csv_data
                })
            elif '.yml' in a_name.lower():
                data_from_yaml = read_yaml_file(a_full_path)
                extra_vars.update({
                    # [:-4] removes .yml
                    a_name.lower()[:-4]: data_from_yaml
                })
            elif '.yaml' in a_name.lower():
                data_from_yaml = read_yaml_file(a_full_path)
                extra_vars.update({
                    # [:-5] removes .yaml
                    a_name.lower()[:-5]: data_from_yaml
                })

    return extra_vars

if __name__ == "__main__":

    default_template_dir = '.cp'
    default_input_dir = '.cp/extra-vars'

    # get directory to load extra context
    parser = argparse.ArgumentParser(
        prog="copy",
        description="Init new lab from template.")
    parser.add_argument(
        '-in', '--input_directory', default=default_input_dir,
        help='Directory with CSV or YAML files to load as extra context'
    )
    parser.add_argument(
        '-out', '--output_directory', default=os.getcwd(),
        help='Directory where Copier will generate files'
    )
    args = parser.parse_args()

    # run copier
    cp = copier
    extra_vars = load_extra_vars(args.input_directory)
    cpWorker = cp.Worker(src_path=default_template_dir, dst_path=args.output_directory, data=extra_vars, unsafe='True', overwrite=True)
    cpWorker.run_copy()
