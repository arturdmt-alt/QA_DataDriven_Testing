import pandas as pd
import json
import os
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class DataReader:
    
    @staticmethod
    def read_csv(filepath: str) -> pd.DataFrame:
        try:
            if not os.path.exists(filepath):
                logger.error(f"CSV file not found: {filepath}")
                raise FileNotFoundError(f"File not found: {filepath}")
            
            df = pd.read_csv(filepath)
            
            if df.empty:
                logger.error(f"CSV file is empty: {filepath}")
                raise ValueError(f"Test data file is empty: {filepath}")
            
            logger.info(f"Successfully loaded CSV: {filepath} ({len(df)} rows)")
            return df
            
        except pd.errors.EmptyDataError:
            logger.error(f"CSV file has no data: {filepath}")
            raise ValueError(f"CSV file is empty: {filepath}")
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing CSV: {e}")
            raise ValueError(f"Invalid CSV format: {e}")
        except Exception as e:
            logger.error(f"Unexpected error reading CSV: {e}")
            raise
    
    @staticmethod
    def read_excel(filepath: str, sheet_name: str = 0) -> pd.DataFrame:
        try:
            if not os.path.exists(filepath):
                logger.error(f"Excel file not found: {filepath}")
                raise FileNotFoundError(f"File not found: {filepath}")
            
            df = pd.read_excel(filepath, sheet_name=sheet_name, engine='openpyxl')
            
            if df.empty:
                logger.error(f"Excel file is empty: {filepath}")
                raise ValueError(f"Test data file is empty: {filepath}")
            
            logger.info(f"Successfully loaded Excel: {filepath} ({len(df)} rows)")
            return df
            
        except ValueError as e:
            logger.error(f"Error reading Excel: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error reading Excel: {e}")
            raise
    
    @staticmethod
    def read_json(filepath: str) -> Dict[str, Any]:
        try:
            if not os.path.exists(filepath):
                logger.error(f"JSON file not found: {filepath}")
                raise FileNotFoundError(f"File not found: {filepath}")
            
            with open(filepath, 'r') as file:
                data = json.load(file)
            
            if not data:
                logger.error(f"JSON file is empty: {filepath}")
                raise ValueError(f"Test data file is empty: {filepath}")
            
            logger.info(f"Successfully loaded JSON: {filepath}")
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            logger.error(f"Unexpected error reading JSON: {e}")
            raise
    
    @staticmethod
    def csv_to_list_of_dicts(filepath: str) -> List[Dict[str, Any]]:
        df = DataReader.read_csv(filepath)
        return df.to_dict('records')
    
    @staticmethod
    def excel_to_list_of_dicts(filepath: str, sheet_name: str = 0) -> List[Dict[str, Any]]:
        df = DataReader.read_excel(filepath, sheet_name)
        return df.to_dict('records')
    