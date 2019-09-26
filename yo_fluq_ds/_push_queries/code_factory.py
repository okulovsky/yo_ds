from ._common import *
from . import aggregations as agg
from pathlib import Path
import pickle
import zipfile



class AggregationCodeFactory(yo_fluq._push_queries.AggregationCodeFactory):
    def __init__(self, method_concatenator: Callable):
        super(AggregationCodeFactory, self).__init__(method_concatenator)

    def to_dataframe(self, **kwargs):
        return self.method_concatenator(agg.ToDataframe(**kwargs))

    def to_ndarray(self):
        return self.method_concatenator(agg.ToNDArray())

    def to_series(self, value_selector: Optional[Callable] = None, key_selector: Optional[Callable]=None, **kwargs):
        return self.method_concatenator(agg.ToSeries(value_selector, key_selector, **kwargs))

    def to_text_file(self,filename: Union[str,Path], autoflush: bool = False, separator: str ='\n', **kwargs):
        return self.method_concatenator(agg.ToTextFile(filename,autoflush,separator,**kwargs))

    def to_zip_text_file(self, filename: Union[str,Path], separator: str = '\n', **kwargs):
        return self.method_concatenator(agg.ToZipTextFile(filename,separator,**kwargs))

    def to_pickle_file(self, filename):
        return self.method_concatenator(agg.ToPickleFile(filename))

    def to_zip_folder(self, filename: Union[str,Path],  writer: Callable = pickle.dumps, replace=True,compression = zipfile.ZIP_DEFLATED):
        return self.method_concatenator(agg.ToZipFolder(filename,writer,replace,compression))

    

