from posixpath import split
import shutil
from roboflow import Roboflow
import os
from config import BASE_DIR
import splitfolders
import json
import os
import zipfile
import re
import datasets

#Utility method to unzip any zipped files
def extract_nested_zip(zippedFile, toFolder):
    """ Extract a zip file including any nested zip files
        Delete the zip file(s) after extraction
    """
    if os.path.exists(zippedFile):
        with zipfile.ZipFile(zippedFile, 'r') as zfile:
            zfile.extractall(path=toFolder)

        os.remove(zippedFile)
        for root, dirs, files in os.walk(toFolder):
            for filename in files:
                if re.search(r'\.zip$', filename):
                    fileSpec = os.path.join(root, filename)
                    extract_nested_zip(fileSpec, root)

def download_to_local_directory_hf(api_info):
    datasets.disable_caching()
    dataset = datasets.load_dataset(api_info['dataset-name'], )
    dataset.save_to_disk(os.path.abspath(os.path.join(api_info["output-working-dir"], api_info["output-dirname"])))

def download_to_local_directory_kaggle(api_info):

    print('Downloading kaggle dataset ...')

    auth_info = None

    with open(os.path.join(api_info['output-working-dir'], api_info['kaggle-json-file-name']), 'r') as f:
        auth_info = json.load(f)
        os.environ["KAGGLE_username"] = auth_info['username']
        os.environ["KAGGLE_key"] = auth_info['key']
    
    #Kaggle auto-authenticates as soon as you import it, and it looks for the os.environ data above, so this statement must be placed here
    from kaggle.api.kaggle_api_extended import KaggleApi

    if auth_info == None:
        raise Exception(f'Cannot find authorization json file {api_info["kaggle-json-file-name"]} in path: {os.path.join(api_info["output-working-dir"], api_info["kaggle-json-file-name"])}')

    api = KaggleApi(auth_info)
    api.authenticate()

    print('Sucessfully authenticated with Kaggle')

    if api_info['kaggle-data-type'] == 'dataset':
        print('Recognized dataset. Downloading ...')
        api.dataset_download_files(api_info['dataset-name'], path=os.path.join(api_info['output-working-dir']), unzip=True)
    elif api_info['kaggle-data-type'] == 'competition':
        print('Recognized competition. Downloading ...')

        print('NOTE that you must accept the kaggle rules for the kaggle competition on the website before being able to download the dataset')
        api.competition_download_files(api_info['dataset-name'], path=os.path.join(api_info['output-working-dir']))
    
        if os.path.exists(os.path.join(api_info['output-working-dir'], f'{api_info["dataset-name"]}.zip')):
            print('The file appears to be zipped. Unzipping it ...')

            extract_nested_zip(os.path.join(api_info['output-working-dir'], f'{api_info["dataset-name"]}.zip'), os.path.join(api_info['output-working-dir'], api_info['output-dirname']))
    else:
        raise Exception(f'Unidentifiable kaggle-data-type attribute: {api_info["kaggle-data-type"]}')

    if api_info['dataset-format'] == 'classnames':
        splitfolders.ratio(os.path.join(api_info['output-working-dir'], api_info['dataset-name']), os.path.join(api_info['output-working-dir'], api_info['output-dirname']), seed = 1337, ratio = api_info['train-val-test-split'], move = True)

def download_to_local_directory_robo(api_info):
    rf = Roboflow(api_key = api_info['api-key'])
    project = rf.workspace(api_info['workspace-name']).project(api_info['project-name'])
    dataset = project.version(api_info['project-version']).download("yolov5", location = os.path.join(api_info['output-working-dir'], api_info['output-dirname']))


def download_dataset(dataset_type, api_info):
    if dataset_type == 'roboflow':
        download_to_local_directory_robo(api_info)
    elif dataset_type == 'kaggle':
        print('Trying to download to kaggle')
        download_to_local_directory_kaggle(api_info)
    elif dataset_type == 'huggingface':
        download_to_local_directory_hf(api_info)

def zipfolder(foldername, target_dir):            
    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])


def export_dataset(api_info):
    zipfolder(os.path.abspath(os.path.join(api_info['output-working-dir'], api_info['input-dir'])), os.path.abspath(os.path.join(api_info['output-working-dir'], api_info['output-dir'])))

    if 'delete-input-dir' in api_info and api_info['delete-input-dir']:
        shutil.rmtree(os.path.abspath(os.path.join(api_info['output-working-dir'], api_info['input-dir'])))
        if os.path.exists(os.path.abspath(os.path.join(api_info['output-working-dir'], api_info['input-dir']))):
            os.rmdir(os.path.abspath(os.path.join(api_info['output-working-dir'], api_info['input-dir'])))