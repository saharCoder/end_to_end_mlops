import os
import urllib.request as request
import zipfile
import pandas as pd
from mlProject import logger
from mlProject.utils.common import get_size
from pathlib import Path
from mlProject.entity.config_entity import ( DataValidationConfig)

class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    def validate_all_columns(self)-> bool:
        try:
            validation_status = None
            errors=[]

            data = pd.read_csv(self.config.unzip_data_dir)
            
            all_cols = list(data.columns)
            all_schema = self.config.all_schema
            
            logger.info(f"Columns in data: {all_cols}")
            logger.info(f"Expected schema: {all_schema}")
            
            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                        errors.append(f"Missing column: {col}")
                else:
                    actual_dtype = str(data[col].dtype)
                    expected_dtype = str(all_schema[col])
                    if actual_dtype != expected_dtype:
                        validation_status = False
                        errors.append(
                            f"Type mismatch in column '{col}': expected {expected_dtype}, got {actual_dtype}"
                        )
                    else:
                        validation_status = True
                    
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

            return validation_status
        
        except Exception as e:
            raise e
