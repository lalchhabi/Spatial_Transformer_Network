import argparse
import os
import random
from packaging import version
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from model.input_fn import *
from model.model_fn import *
from model.training import *
from  utils.utils import Params

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', default='./result',
                    help="Directory containing the dataset")

parser.add_argument('--log_dir', default="./log",
                    help="log directory for the trained model")

parser.add_argument('--mode', default='train', 
                    help="train or test mode")

parser.add_argument('--v', default=False,
                    help ='verbose mode')

if __name__ == '__main__':
    
    # Set the random seed for the whole graph for reproductible experiments
    tf.random.set_seed(230)
    print("TensorFlow version: ", tf.__version__)
    assert version.parse(tf.__version__).release[0] >= 2, \
    "This notebook requires TensorFlow 2.0 or above."

    # Load the parameters from json file
    args = parser.parse_args()
    json_path = './params.json'
    assert os.path.isfile(json_path), "No json configuration file found at {}".format(json_path)
    params = Params(json_path)

    # check if the data is available
    assert os.path.exists(args.data_dir), "No data file found at {}".format(args.data_dir)

    # check if the log file is available
    if not os.path.exists(args.log_dir):
        os.mkdir(args.log_dir)

    train_data_dir = os.path.join(args.data_dir, 'train')
    eval_data_dir = os.path.join(args.data_dir, 'eval')

    # Get the filenames from the train and dev sets
    train_filenames = [os.path.join(train_data_dir, f) for f in os.listdir(train_data_dir)]
    eval_filenames = [os.path.join(eval_data_dir, f) for f in os.listdir(eval_data_dir)]

    # Get the aligned images list
    aligned_images_list_train = glob.glob(train_filenames[1] + '/*.jpg')
    aligned_images_list_eval = glob.glob(eval_filenames[1] + '/*.jpg')

    # Get the raw images list
    raw_images_list_train = glob.glob(train_filenames[0] + '/*.jpg')
    raw_images_list_eval = glob.glob(eval_filenames[0] + '/*.jpg')

    # Specify the sizes of the dataset we train on and evaluate on
    params.train_size = len(aligned_images_list_train)
    params.eval_size = len(aligned_images_list_eval)

    # Create the two iterators over the two datasets
    print('=================================================')
    print('[INFO] Dataset is built by {0} training images and {1} eval images '
            .format(len(aligned_images_list_train), len(aligned_images_list_eval)))

    tf.debugging.set_log_device_placement(args.v)
    train_dataset = input_fn(True, raw_images_list_train, aligned_images_list_train, params= params)
    eval_dataset  = input_fn(False, raw_images_list_eval, aligned_images_list_eval, params= params)
    print('[INFO] Data pipeline is built')

    # Define the model
    print('=================================================')
    print('[INFO] Creating the model...')
    model_spec = model_fn(args.mode, params) 
    if args.v:
        model_spec['model'].summary()

    # Train the model
    print('=================================================')
    train_model = Train_and_Evaluate(model_spec, train_dataset, eval_dataset, args.log_dir)
    train_model.train_and_eval(params)
    model = train_model.model
    print('=================================================')
    model.summary()

    best_final_path = os.path.join("./test", "best_full_model_path")
    model.save(best_final_path)
    tf.saved_model.save(model, best_final_path)
    print("[INFO] Final model save in {}".format(best_final_path))
