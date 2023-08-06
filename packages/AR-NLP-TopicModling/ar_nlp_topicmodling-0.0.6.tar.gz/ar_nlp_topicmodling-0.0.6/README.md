# AR_NLP_TopicModling

AR_NLP_TopicModling is a Python package for modeling the similarities of texts into the same topic using LDA
NMF

## Installation
```bash

pip install AR_NLP_TopicModling
```

## Usage

```python
from AR_NLP_TopicModling import *


Topic_modling=Topic_modling('YourCsvFilePath','ColumnName')

Topic_modling.DataCleaning()# Text cleaning

Topic_modling.TopicModleingLDA(4) #specify the number of n topics
Topic_modling.TopicModleingNMF(4) #specify the number of n topics
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


