from yo_fluq_ds._fluq import *
import yo_fluq_ds._push_queries.aggregations as _agg

class to_pickle_file(_agg.ToPickleFile):
    pass

class to_text_file(_agg.ToTextFile):
    pass

class to_zip_text_file(_agg.ToZipTextFile):
    pass

class to_zipped_folder(_agg.ToZipFolder):
    pass
