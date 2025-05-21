# Weather Classification
- Tim Johnson
- Beckett Jaeger
- Edward Kang
- Tyler Moore

## Dataset
- weather_classification_data.csv: main dataset for training and testing, synthetic
- live_weather_classification_data.csv: secondary testing dataset, real-life data pulled from National Weather Service API
- live_weather_classificaiton_data_presentation.csv: secondary testing dataset used in in-class presentation

### How to pull live weather data
1. Open Windows PowerShell
2. Change directory (cd) into the project file path
3. Run install_script_dependencies.bat
4. Run run_python_script.bat
5. Input cities to pull live data from
6. Live data will be stored in live_weather_classification_data.csv

## ML files
- PrelimWork.ipynb: preliminary work to explore and analyze training dataset
- Baseline.ipynb: first baseline classification model, predicts the mode
- KNN_Classifier.ipynb, SVM.ipynb: manually trained classification models
- FeatureEngineering.ipynb: feature engineering exploration with Random Forest classificiation model
- ModelsComparison.ipynb: trains and tests KNN, Random Forest, and SVM classification models on main dataset then tests them on the live dataset
- ModelsComparison_PCA.ipynb: same as ModelsComparison.ipynb but trains the models on the dataset treated with PCA

## Live weather data API
- script.py: main script for live data API
- config.json: stores the API key
- install_script_dependencies.bat: installs script dependencies
- run_python_script.bat: runs the main script

## Deprecated files
- weather_prediction_dataset.csv: non-synthetic weather dataset from Europe, discarded due to lack of features
- PrelimWork_Europe.ipynb: preliminary work done on weather_prediction_dataset.csv
- PrelimWork_BadDataset.ipynb: preliminary work done on non-synthetic weather dataset from US airports