import os
import pathlib 
from typing import (
    List,
    Dict,
    Optional,
    Any,
    Tuple,
)

import torch
import numpy as np 
import pandas as pd 
import anndata as an
import warnings 
from functools import cached_property

import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from sklearn.preprocessing import LabelEncoder 
import urllib 

import os 
from os.path import join

from .data import generate_dataloaders, compute_class_weights
here = pathlib.Path(__file__).parent.absolute()

class DataModule(pl.LightningDataModule):
    def __init__(
        self, 
        class_label: str,
        datafiles: List[str]=None,
        labelfiles: List[str]=None,
        urls: Dict[str, List[str]]=None,
        sep: str=None,
        unzip: bool=True,
        datapath: str='',
        batch_size=32,
        num_workers=0,
        device=('cuda:0' if torch.cuda.is_available() else None),
        split=True,
        *args,
        **kwargs,
    ):
        """
        Creates the DataModule for PyTorch-Lightning training.

        This either takes a dictionary of URLs with the format 
            urls = {dataset_name.extension: 
                        [
                            datafileurl,
                            labelfileurl,
                        ]
                    }

        OR two lists containing the absolute paths to the datafiles and labelfiles, respectively.

        :param class_label: Class label to train on. Must be in all label files 
        :type class_label: str
        :param datafiles: List of absolute paths to datafiles, if not using URLS. defaults to None
        :type datafiles: List[str], optional
        :param labelfiles: List of absolute paths to labelfiles, if not using URLS. defaults to None
        :type labelfiles: List[str], optional
        :param urls: Dictionary of URLS to download, as specified in the above docstring, defaults to None
        :type urls: Dict[str, List[str, str]], optional
        :param unzip: Boolean, whether to unzip the datafiles in the url, defaults to False
        :type unzip: bool, optional
        :param sep: Separator to use in reading in both datafiles and labelfiles. WARNING: Must be homogeneous between all datafile and labelfiles, defaults to '\t'
        :type sep: str, optional
        :param datapath: Path to local directory to download datafiles and labelfiles to, if using URL. defaults to None
        :type datapath: str, optional
        :param assume_numeric_label: If the class_label column in all labelfiles is numeric. Otherwise, we automatically apply sklearn.preprocessing.LabelEncoder to the intersection of all possible labels, defaults to True
        :type assume_numeric_label: bool, optional
        :raises ValueError: If both a dictionary of URL's is passed and labelfiles/datafiles are passed. We can only handle one, not a mix of both, since there isn't a way to determine easily if a string is an external url or not. 

        """    
        super().__init__()

        # Make sure we don't have datafiles/labelfiles AND urls at start
        if urls is not None and datafiles is not None or urls is not None and labelfiles is not None:
            raise ValueError("Either a dictionary of data to download, or paths to datafiles and labelfiles are supported, but not both.")

        self.device = device 
        self.class_label = class_label
        self.urls = urls 
        self.unzip = unzip 
        self.datapath = datapath 
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.split = split 

        # If we have a list of urls, we can generate the list of paths of datafiles/labelfiles that will be downloaded after self.prepare_data()
        if self.urls is not None:
            self.datafiles = [join(self.datapath, f) for f in self.urls.keys()] 
            self.labelfiles = [join(self.datapath, f'labels_{f}') for f in self.urls.keys()] 
        else:
            self.datafiles = datafiles 
            self.labelfiles = labelfiles

        # Warn user in case tsv/csv ,/\t don't match, this can be annoying to diagnose
        suffix = pathlib.Path(self.labelfiles[0]).suffix
        if (sep == '\t' and suffix == 'csv') or (sep == ',' and suffix == '.tsv'):
            warnings.warn(f'Passed delimiter sep={sep} doesn\'t match file extension, continuing...')

        # Infer sep based on .csv/.tsv of labelfile (assumed to be homogeneous in case of delimited datafiles) if sep is not passed
        if sep is None:
            if suffix == '.tsv':
                self.sep = '\t'
            elif suffix == '.csv':
                self.sep = ','
            else:
                warnings.warn(f'Separator not passed and not able to be inferred from suffix={suffix}. Falling back to ","')
                self.sep = ','
        else:
            self.sep = sep 

        self.args = args 
        self.kwargs = kwargs

    def prepare_data(self):
        if self.urls is not None:
            download_raw_expression_matrices(
                self.urls,
                unzip=self.unzip,
                sep=self.sep,
                datapath=self.datapath,
            )

        self._encode_labels()

    def _encode_labels(self):
        unique_targets = np.array(list(
            set(
                np.concatenate(
                    [pd.read_csv(df, sep=self.sep).loc[:, self.class_label].unique() for df in self.labelfiles]
                )
            )
        ))
        
        if not np.issubdtype(unique_targets.dtype, np.number):
            print('Labels are non-numeric, using sklearn.preprocessing.LabelEncoder to encode.')
            self.label_encoder = LabelEncoder()
            self.label_encoder = self.label_encoder.fit(unique_targets)
            
            for idx, file in enumerate(self.labelfiles):
                print(f'Transforming labelfile {idx + 1}/{len(self.labelfiles)}')

                labels = pd.read_csv(file, sep=self.sep)
                
                if f'categorical_{self.class_label}' not in labels.columns:
                    labels.loc[:, f'categorical_{self.class_label}'] = labels.loc[:, self.class_label]

                    labels.loc[:, self.class_label] = self.label_encoder.transform(
                        labels.loc[:, f'categorical_{self.class_label}']
                    )

                    labels.to_csv(file, index=False, sep=self.sep) # Don't need to re-index here 
            
    def setup(self, stage: Optional[str] = None):
        if self.split:
            print('Creating train/val/test DataLoaders...')
            trainloader, valloader, testloader = generate_dataloaders(
                datafiles=self.datafiles,
                labelfiles=self.labelfiles,
                class_label=self.class_label,
                sep=self.sep,
                batch_size=self.batch_size,
                num_workers=self.num_workers,
                pin_memory=True, # For gpu training
                *self.args,
                **self.kwargs,
            )

            print('Done, continuing to training.')
            self.trainloader = trainloader
            self.valloader = valloader
            self.testloader = testloader
        else:
            pass 
        
        print('Calculating weights')
        self.weights = compute_class_weights(
            labelfiles=self.labelfiles, 
            class_label=self.class_label, 
            sep=self.sep, 
            device=self.device,
        )

    def train_dataloader(self):
        return self.trainloader

    def val_dataloader(self):
        return self.valloader

    def test_dataloader(self):
        return self.testloader

    @cached_property
    def num_labels(self):
        val = []
        for file in self.labelfiles:
            val.extend(list(pd.read_csv(file, sep=self.sep).loc[:, self.class_label].values))

        return len(set(val))

    @cached_property
    def num_features(self):
        if self.urls is not None and not os.path.isfile(self.datafiles[0]):
            print('Trying to calcuate num_features before data has been downloaded. Downloading and continuing...')
            self.prepare_data()

        if 'refgenes' in self.kwargs:
            return len(self.kwargs['refgenes'])
        elif hasattr(self, 'trainloader'):
            return next(iter(self.trainloader))[0].shape[1]
        elif pathlib.Path(self.datafiles[0]).suffix == '.h5ad':
            return an.read_h5ad(self.datafiles[0]).X.shape[1]
        else:
            return pd.read_csv(self.datafiles[0], nrows=1, sep=self.sep).shape[1]

    @cached_property
    def input_dim(self):
        return self.num_features

    @cached_property
    def output_dim(self):
        return self.num_labels

    def __len__(self):
        l = [pd.read_csv(f, sep=self.sep).shape[0] for f in self.labelfiles]

        return sum(l)

def generate_trainer(
    datafiles: List[str],
    labelfiles: List[str],
    class_label: str,
    batch_size: int,
    num_workers: int,
    optim_params: Dict[str, Any]={
        'optimizer': torch.optim.Adam,
        'lr': 0.02,
    },
    weighted_metrics: bool=None,
    scheduler_params: Dict[str, float]=None,
    wandb_name: str=None,
    weights: torch.Tensor=None,
    max_epochs=500,
    *args,
    **kwargs,
):
    """
    Generates PyTorch Lightning trainer and datasets for model training.

    :param datafiles: List of absolute paths to datafiles
    :type datafiles: List[str]
    :param labelfiles: List of absolute paths to labelfiles
    :type labelfiles: List[str]
    :param class_label: Class label to train on 
    :type class_label: str
    :param weighted_metrics: To use weighted metrics in model training 
    :type weighted_metrics: bool
    :param batch_size: Batch size in dataloader
    :type batch_size: int
    :param num_workers: Number of workers in dataloader
    :type num_workers: int
    :param optim_params: Dictionary defining optimizer and any needed/optional arguments for optimizer initializatiom
    :type optim_params: Dict[str, Any]
    :param wandb_name: Name of run in Wandb.ai, defaults to ''
    :type wandb_name: str, optional
    :return: Trainer, model, datamodule 
    :rtype: Trainer, model, datamodule 
    """

    device = ('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(f'Device is {device}')
    
    here = pathlib.Path(__file__).parent.absolute()
    data_path = os.path.join(here, '..', '..', '..', 'data')

    wandb_logger = WandbLogger(
        project=f"tabnet-classifer-sweep",
        name=wandb_name
    )

    early_stop_callback = EarlyStopping(
        monitor=("weighted_val_accuracy" if weighted_metrics else "val_accuarcy"), 
        min_delta=0.00, 
        patience=3, 
        verbose=False, 
        mode="max"
    )

    module = DataModule(
        datafiles=datafiles, 
        labelfiles=labelfiles, 
        class_label=class_label, 
        batch_size=batch_size,
        num_workers=num_workers,
    )

    model = SIMSClassifier(
        input_dim=module.num_features,
        output_dim=module.num_labels,
        weighted_metrics=weighted_metrics,
        optim_params=optim_params,
        scheduler_params=scheduler_params,
        weights=weights,
    )
    
    trainer = pl.Trainer(
        gpus=(1 if torch.cuda.is_available() else 0),
        auto_lr_find=False,
        # gradient_clip_val=0.5,
        logger=wandb_logger,
        max_epochs=max_epochs,
        callbacks=[
            uploadcallback, 
        ],
        val_check_interval=0.25, # Calculate validation every quarter epoch instead of full since dataset is large, and would like to test this 
    )

    return trainer, model, module



def download_raw_expression_matrices(
    datasets: Dict[str, Tuple[str, str]],
    unzip: bool=True,
    datapath: str=None
) -> None:
    """Downloads all raw datasets and label sets from cells.ucsc.edu, and then unzips them locally

    :param datasets: Dictionary of datasets such that each key maps to a tuple containing the expression matrix csv url in the first element,
                    and the label csv url in the second url, defaults to None
    :type datasets: Dict[str, Tuple[str, str]], optional
    :param upload: Whether or not to also upload data to the braingeneersdev S3 bucket , defaults to False
    :type upload: bool, optional
    :param unzip: Whether to also unzip expression matrix, defaults to False
    :type unzip: bool, optional
    :param datapath: Path to folder to download data to. Otherwise, defaults to data/
    :type datapath: str, optional
    """    
    # {local file name: [dataset url, labelset url]}
    data_path = (datapath if datapath is not None else os.path.join(here, '..', '..', '..', 'data'))

    for file, links in datasets.items():
        datafile_path = os.path.join(data_path, 'raw', file)

        labelfile = f'{file[:-4]}_labels.tsv'

        datalink, _ = links

        # First, make the required folders if they do not exist 
        for dir in 'raw':
            os.makedirs(os.path.join(data_path, dir), exist_ok=True)

        # Download and unzip data file if it doesn't exist 
        if not os.path.isfile(datafile_path):
            print(f'Downloading zipped data for {file}')
            urllib.request.urlretrieve(
                datalink,
                f'{datafile_path}.gz',
            )

            if unzip:
                print(f'Unzipping {file}')
                os.system(
                    f'zcat < {datafile_path}.gz > {datafile_path}'
                )

                print(f'Deleting compressed data')
                os.system(
                    f'rm -rf {datafile_path}.gz'
                )
