from .._common import *
from pathlib import Path
import gzip
import pickle
import zipfile
import os

class ToTextFile(yo_fluq.agg.PushQueryElement):
    def __init__(self, filename: Union[str,Path], autoflush: bool = False, separator: str ='\n', **kwargs):
        self.filename = filename
        self.autoflush = autoflush
        self.separator = separator
        self.kwargs = kwargs

    def on_enter(factory,instance):
        instance.file = open(factory.filename, 'w', **factory.kwargs)
        
    def on_process(factory, instance, element):
        instance.file.write(element+factory.separator)
        if factory.autoflush:
            instance.file.flush()

    def on_report(factory, instance):
        return None

    def on_exit(factory, instance,exc_type, exc_val, exc_tb):
        instance.file.__exit__(exc_type, exc_val, exc_tb)



class ToZipTextFile(yo_fluq.agg.PushQueryElement):
    def __init__(self, filename: Union[str,Path], separator: str = '\n', **kwargs):
        self.filename = filename
        self.separator = separator
        self.kwargs = kwargs

    def on_enter(factory, instance):
        instance.file = gzip.open(factory.filename, 'wb', **factory.kwargs)

    def on_process(factory, instance, element):
        element += factory.separator
        element = bytes(element, 'utf-8')
        instance.file.write(element)

    def on_report(factory, instance):
        return None

    def on_exit(factory, instance, exc_type, exc_val, exc_tb):
        instance.file.__exit__(exc_type, exc_val, exc_tb)


class ToPickleFile(yo_fluq.agg.PushQueryElement):
    def __init__(self, filename: Union[str,Path], file_opener = None):
        self.filename = filename
        if file_opener is None:
            file_opener = lambda fname: open(fname, 'wb')
        self.file_opener = file_opener

    def on_enter(factory, instance):
        instance.file = factory.file_opener(factory.filename)

    def on_process(factory, instance, element):
        dump = pickle.dumps(element)
        length = len(dump)
        length_bytes = length.to_bytes(4, byteorder='big')
        instance.file.write(length_bytes)
        instance.file.write(dump)

    def on_report(factory, instance):
        return None

    def on_exit(factory, instance, exc_type, exc_val, exc_tb):
        instance.file.__exit__(exc_type, exc_val, exc_tb)



class ToZipFolder(yo_fluq.agg.PushQueryElement):
    def __init__(self, filename: Union[str,Path],  writer: Callable = pickle.dumps, replace=True,compression = zipfile.ZIP_DEFLATED):
        self.filename = filename
        self.compression = compression
        self.writer = writer
        self.replace = replace

    def on_enter(factory, instance):
        if factory.replace and os.path.isfile(factory.filename):
            os.remove(factory.filename)
        instance.file = zipfile.ZipFile(factory.filename, 'a', compression=factory.compression)

    def on_process(factory, instance, element):
        if not isinstance(element,KeyValuePair):
            raise ValueError('Item must be a key-value pair, but was {0}'.format(element))
        instance.file.writestr(element.key, factory.writer(element.value))

    def on_report(factory, instance):
        return None

    def on_exit(factory, instance, exc_type, exc_val, exc_tb):
        instance.file.__exit__(exc_type, exc_val, exc_tb)


