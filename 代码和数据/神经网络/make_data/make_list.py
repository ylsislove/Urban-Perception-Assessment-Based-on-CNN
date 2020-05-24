import os
import csv

def make_list(image_type, mode):
    source_path = os.path.abspath(r'G:\scores\{}\src\{}\480_300'.format(image_type, mode))
    output_path = os.path.abspath(r'G:\scores\{}\{}.lst'.format(image_type, mode))
    matedata_path = os.path.abspath(r'G:\scores\{}\auto_save_scores_{}.csv'.format(image_type, image_type))

    # read metedata
    # create a dict to store the csv line data
    data = dict()   
    if os.path.exists(matedata_path):
        with open(matedata_path, encoding='utf-8') as f:
            csv_reader_lines = csv.reader(f)
            for one_line in csv_reader_lines:
                data[one_line[0]] = one_line[1]
            print('{} total lines : {:d}'.format(str(matedata_path), len(data)))
    else:
        print('matedata_path is wrong...' + matedata_path)
        exit(1)

    # process data
    data_str = ''
    if os.path.exists(source_path):
        dirs = os.listdir(source_path)
        for f in dirs:
            data_str = data_str + f + data[f[:-4]] + '\n'
    else:
        print("source_path is wrong..." + source_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(data_str)

if __name__ == "__main__":
    image_type = 'depressing'
    modes = ['train', 'test']
    for mode in modes:
        make_list(image_type, mode)
