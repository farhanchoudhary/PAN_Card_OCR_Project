#!/usr/bin/env python
import json
import csv
import sys
import glob

NESTING_SEP = '/'
FIELD_SEP = '\t'

def encode(s):
    return s.replace('\n', ' ').encode('utf-8') if type(s) not in [int, float] else s

def flatten(data, prefix=''):
    flattened = {}
    for key in data:
        value = data[key]
        if type(value) is dict:
            x = flatten(value, prefix = prefix + key + NESTING_SEP)
            flattened.update(x)
        elif type(value) is list:
            x = flatten(dict(zip(map(str, range(len(value))), value)), prefix = prefix + key + NESTING_SEP)
            flattened.update(x)
        else:
            flattened[prefix + key] = encode(value)

    return(flattened)

def main():
    if len(sys.argv) < 2:
        print('Usage:', sys.argv[0], '<folder_name> [output_file]')
        return
    folder_name = sys.argv[1]
    output = open(sys.argv[2], 'w') if len(sys.argv) >= 3 else sys.stdout

    if folder_name[-1] != '/':
        folder_name += '/'

    columns = set()
    flattened_all = []

    # get column names
    for f_name in glob.iglob(folder_name + '/*.json'):
        with open(f_name, 'r') as f:
            data = json.load(f)
            flattened = flatten(data)
            columns = columns.union(flattened.keys())
            flattened['filename'] = f_name[len(folder_name):-len('.json')]
            flattened_all.append(flattened)

    headers = sorted(list(columns))
    headers.insert(0, 'filename')

    writer = csv.DictWriter(output, delimiter = FIELD_SEP, fieldnames = headers)
    writer.writeheader()

    for flattened in flattened_all:
        writer.writerow(flattened)

if __name__ == '__main__':
    main()