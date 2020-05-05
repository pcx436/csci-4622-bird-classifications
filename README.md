# Classifying Birds
Final project for CSCI 4622 Machine Learning at CU Boulder.

## Data source
Data sourced from a 2011 Caltech and UCSB collaboration.
The dataset can be downloaded [here](http://www.vision.caltech.edu/visipedia/CUB-200-2011.html).  

There are 200 species of birds in this dataset and 11,788 images.

## Usage
In order to use any of the models, you'll need to first download the data from the data source listed above. Downloading the data will provide you a .tgz file which should then be extracted. When running any of the models for the first time, you will need to provide some command line arguments to the script for it to be able to locate the required image data. An example of which is provided below:

`python customModel.py -l CUB_200_2011/images.txt -d CUB_200_2011/images/ -b CUB_200_2011/bounding_boxes.txt -o imageData.npz`

When running the model all successive times, you may use the output file from the first time. The way to do this is `python customModel.py -i imageData.npz`.

Please see `python customModel.py --help` for more details on the command line arguments and their usage.

### Citation
Wah C., Branson S., Welinder P., Perona P., Belongie S. “The Caltech-UCSD Birds-200-2011 Dataset.” Computation & Neural
Systems Technical Report, CNS-TR-2011-001.