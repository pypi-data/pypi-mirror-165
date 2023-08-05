# Plagy  

A Simple Plagiarism detector. It supports .txt, .c, ,cpp, ,py, ,java or any other utf-8 encoded text files.  

It Provides 3 Scenarios to check the Plagiarism.  
1. **One2One** : Check the plagiarism score between two files. The files must be of same type.

2. **One2Many** : Checks the Plagiarism score betweem one query file and a list of source files. One typical use case would be a newly published journals vs a list of already published journals, to check if the new journal is plagiarized from other sources or not. 

3. **Many2Many** : Checks the similiarity between every pair of files in a collection of files.


## Installation

Install this package from pip directly

```
pip install plagiarism-MCA2022temp
```
or 
```
pip3 install plagiarism-MCA2022temp
```

or clone this repo in your local environment and

```
python setup.py
```


### Uses

```
from plagy.plagy import *
obj = One2One(path_to_file1, path_to_file2)
obj.preprocess_files()
obj.run()
obj.display()
```

```
obj = One2Many(path_to_source_folder, path_to_query_file)
obj.preprocess()
obj.run()
obj.display()
```

```
obj = Many2Many(path_to_collection_folder)
obj.preprocess()
obj.run(threshold = 0.7)
obj.display()
```

 