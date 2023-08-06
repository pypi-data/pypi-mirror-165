import pandas as pd

from ..utils import hello_world

class Module2_class():
    
    def __init__(self):
        self._internal_float = 0.2
        
    def create_dataframe(self):
        hello_world()
        return pd.DataFrame([[1,2], [3, 4]], columns=['col1', 'col2'])