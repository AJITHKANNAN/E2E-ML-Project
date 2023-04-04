   #DATA INGESTION

"""
Data ingestion is the process of reading data from multiple sources and split them into train and test for performing data transformation.

This process is needed because every company will have a seperate BIG  DATA team and they'll  
collect the data from multiple sources to read them we use Data Ingestion """


import os
import sys
from src.exception import CustomException
#from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass #decorator for input data for processing
class DataIngestionConfig:  
    
    #artifacts is an OUTPUT folder and create files for the raw, train, test data
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    
    def __init__(self):
      self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
       #logging.info('Entered the data ingestion Component or method')
       try:
          #read the data from the sources
          df =pd.read_csv('notebook\data\stud.csv')
          #logging.info('Read the dataset as dataframe')
          #create a directory of the output path
          os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok= True)

          df.to_csv(self.ingestion_config.raw_data_path, index=False, header= True)

          #logging.info('Train test split initated')

          train_set, test_set = train_test_split(df, test_size= .2 , random_state= 42)

          train_set.to_csv(self.ingestion_config.train_data_path, index = False, header =True)

          test_set.to_csv(self.ingestion_config.test_data_path, index =False, header =True)

          #logging.info('Data Ingestion steps were completed')

          return (
             self.ingestion_config.train_data_path,
             self.ingestion_config.test_data_path)

       except Exception as e:
          raise CustomException
          

#this step will create my Artifacts folder

if __name__== "__main__":
   obj =DataIngestion()
   obj.initiate_data_ingestion()