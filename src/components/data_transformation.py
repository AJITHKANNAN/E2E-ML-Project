import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
# ColumnTransformer was helpful in building a pipeline
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
#from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransforationConfig:
    preprocessor_obj_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:

    def __init__(self):
        self.transformation_config = DataTransforationConfig()


#PREPARING THE DATA FOR TEH TRANSFORMATION
    def get_data_transformer_obj(self):
        #this function will be responsible for my data transformation

        try:
            num_columns = ['writing_score','reading_score']
            cat_columns = [
                "gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"
            ]

            # CREATING A PIPELINE FOR TRAINING MODELS

            num_pipeline = Pipeline(
                steps = [

                ("imputer", SimpleImputer(strategy ='median')),  #this will ipute all missing vlues with median
                ("scaler", StandardScaler()) #this will scale the values inbetween a specific range
                ] 
            )

            cat_pipeline = Pipeline(
                steps = [
                
                ("imputer", SimpleImputer(strategy= 'most_frequent')),#this will ipute all missing vlues with mode
                ('oh_encoder', OneHotEncoder()), #this will convert all categroial variables into numeric
                ('scaler', StandardScaler(with_mean= False)) #this will scale the values inbetween a specific range
                ]
                )
            
            '''logging.info(f"Categroical columns: {cat_columns}")
            logging.info(f"Numeric columns:{num_columns}")'''

            #We need to combine the variables num_pipeline and Cat_pipeline. so We use ColumnTransformer

            preprocessor = ColumnTransformer(
                [
                ('Num_pipeline',num_pipeline, num_columns),
                ('Cat_pipeline', cat_pipeline, cat_columns)

                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        

    #INITIATE MY DATA TRANSFORMATION

    def initiate_transformation(self, train_path, test_path):

        try: #reading data from data_ingestion.pys
            train_df = pd.read_csv(train_path)
            test_df =pd.read_csv(test_path)

            '''logging.info('Reading terain and test data Completed')

            logging.info('Obtaining preprocessing object')
'''
            preprocesssing_obj = self.get_data_transformer_obj()

            target_column_name = "math_score"
            num_columns = ['writing_score','reading_score']

            #TRAINING DF
            input_feature_train_df = train_df.drop(columns= [target_column_name], axis =1)
            target_feature_train_df =train_df[target_column_name]

            #TESTING DF
            input_feature_test_df = test_df.drop(columns= [target_column_name], axis =1)
            target_feature_test_df =test_df[target_column_name]

            #logging.info('Apply prerocessing on Train and Test dataframes')

            input_train_arr =preprocesssing_obj.fit_transform(input_feature_train_df)
            input_test_arr =preprocesssing_obj.transform(input_feature_test_df)


            train_arr = np.c_[ input_train_arr, np.array(target_feature_train_df)]

            test_arr = np.c_[ input_test_arr, np.array(target_feature_test_df)]

            #logging.info('Saved Preprocessing Object')

            #CREATING A --PKL-- FILE

            save_object (  
                file_path = self.transformation_config.preprocessor_obj_path,
                obj = preprocesssing_obj
             )

            return (train_arr, 
                    test_arr,
                    self.transformation_config.preprocessor_obj_path)

        except Exception as e:
            raise CustomException(e,sys)
    
