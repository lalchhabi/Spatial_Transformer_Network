import argparse
import os
import sys

from utils.utils import Params
from utils.data import load_data_withIdx

parser = argparse.ArgumentParser(description ='Image Alignment Dataset')

parser.add_argument('--data_dir', default='./dataset',
                    help="Directory containing the dataset")

parser.add_argument('--output_dir', default='./result',
                    help="Where to write the new data")
                
parser.add_argument('-v', dest ='verbose', 
                    action ='store_true', help ='verbose mode')

if __name__ == '__main__':

    # Load the parameters from json file
    args = parser.parse_args()
    json_path = './params.json'
    assert os.path.isfile(json_path), "No json configuration file found at {}".format(json_path)
    params = Params(json_path)

    assert os.path.isdir(args.data_dir), "Couldn't find the dataset at {}".format(args.data_dir)

    # Define the data directories
    train_data_dir = os.path.join(args.output_dir, 'train')
    test_data_dir = os.path.join(args.output_dir, 'test')
    eval_data_dir = os.path.join(args.output_dir, 'eval')
    dataset_dir = args.data_dir

    filenames = {'train': train_data_dir,
                'eval': eval_data_dir,
                'test': test_data_dir,
                'data': dataset_dir}

    # Check that we are not overwriting some previous experiment
    if  os.path.exists(args.output_dir):
        print ("[Error]: output dir {} already exists !".format(args.output_dir)) 
        sys.exit()

    print('[INFO] Making the data directory ... ')
    os.mkdir(args.output_dir)
    os.mkdir(train_data_dir)
    os.mkdir(test_data_dir)
    os.mkdir(eval_data_dir)
             
    subjIdx_list = [1] # MUST SPECIFY THE IDX LIST HERE
    load_data_withIdx(subjIdx_list, filenames)
    print('[INFO] Done building data')

