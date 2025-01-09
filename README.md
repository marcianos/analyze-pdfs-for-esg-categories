# analyze-pdfs-for-esg-categories
Define words for category E, S and G. Analyze pdf documents and count the frequencies of the words in the corresponding category. Print the categories with the frequencies

## Structure
### Categories
This folder contains the csv files for the corresponding categories.

### Nachhaltigkeitsberichte
This folder contains the pdf documents which should be analyzed

### analysisOfWordFrequencies
This folder is the output folder which contains a txt file for each pdf document corresponding to the category. This is an example output:
category_S: 457
category_E: 1275
category_G: 1666


## Executable file
An executable file is placed as zip file in the ```executable``` folder. To use the given file structure without compiling or code changes unzip ```ESG-Analysis``` and run the executable. The executable file is not signed so you maybe need to adjust your system security settings or install python and pyinstaller and compile it on your own. 


## Create executable file
After changes to the application file (MyApplication.py) you need to create/ recreate an executable file. You need to configure [pyinstaller](https://pyinstaller.org/en/stable/). After install and configuration run:

```bash
 pyinstaller --onefile \
    --add-data "/Users/marcel/.pyenv/versions/3.12.7/lib/python3.12/site-packages/en_core_web_sm/en_core_web_sm-3.8.0:en_core_web_sm" \
    --add-data "Nachhaltigkeitsberichte:Nachhaltigkeitsberichte" \
    --add-data "categories:categories" \
    --add-data "analysisOfWordFrequencies:analysisOfWordFrequencies" \
    --hidden-import spacy \
    --hidden-import spacy.cli \
    --hidden-import thinc.backends \
    --name "ESG-Analysis" MyApplication.py
````
