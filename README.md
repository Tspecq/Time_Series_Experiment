# Time_Series_Experiment

The task at end is to predict the bullets sales for year 2018 based on the 6 previous years present.
At first there is need to clean the data and make it readable for the models.
The CSV files can be pivoted with Date as index with meaningful variables after some quick data manipulation.
Numerous features engineering can be made for times series which are more related to stock price predictions,
Those technical indicators used for finance will be added as inputs for the model.
An experiment was made with a LGBM model for curiosity, it seems the LSTM model was more adequate for the task.
A more classic approach using a LSTM model was used with slight better score than the LGBM.
