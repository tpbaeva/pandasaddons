from datetime import datetime
import numpy as np
import pandas as pd


class RandomDataFrame(pd.DataFrame):
    def __init__(self, size=(10,3), index_type='linear', start_date=None, freq=None, columns=None):
        """Creates a random pandas DataFrame
       
        Parameters
        ----------
        size       :  tuple of integers
                      The size of the DataFrame
        
        index_type :  string, default `linear`
                      Can be `linear` or `datetime`
        
        start_date :  string or datetime-like object, default None
                      If index_type is `datetime` this is the starting date of the index, today is used if None
       
        freq       :  string, default None
                      If index_type is `datetime` this is the freq of the index, `D` is used if None
        
        columns    :  list of string, default None
                      List of column names, adjusts to dataframe size
                      
        Example
        -------
        >>> import pandas as pd
        >>> import pandasaddons
        >>> rdf = pd.RandomDataFrame(index_type='datetime')
        >>> rdf
                        col0      col1      col2
        2015-05-05  0.179195  0.319444  0.187299
        2015-05-06  0.440077  0.362801  0.910262
        2015-05-07  0.130515  0.894121  0.179224
        2015-05-08  0.656457  0.728940  0.789680
        2015-05-09  0.129008  0.304318  0.121937
        2015-05-10  0.818146  0.558879  0.979477
        2015-05-11  0.721674  0.836694  0.186717
        2015-05-12  0.389869  0.156821  0.810558
        2015-05-13  0.502213  0.295070  0.166816
        2015-05-14  0.986830  0.438361  0.940494   
        >>> rdf = pd.RandomDataFrame(size=(5,2), columns=['A','B','C'])
        >>> rdf
                  A         B
        0  0.387653  0.753886
        1  0.457717  0.068806
        2  0.209365  0.940149
        3  0.938226  0.374972
        4  0.820601  0.854645     
        """        
        
        _index = None
        if index_type.lower() == 'datetime':
            _startdate = start_date if start_date else datetime.today().date()
            _freq = freq if freq else 'D'
            _index=pd.date_range(_startdate, periods=size[0], freq=_freq) 
        
        if columns is None:
            _columns = []
            rng_start = 0
        else:
            _columns = columns
            rng_start = len(columns)
        _columns = _columns + ['col'+str(i) for i in range(rng_start, size[1])]
        _columns = _columns[:size[1]]
        
        values = np.random.rand(*size)
        super(RandomDataFrame, self).__init__(values, columns=_columns, index=_index)        
        
pd.RandomDataFrame = RandomDataFrame
