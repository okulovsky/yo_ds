from yo_fluq_ds__tests.common import *

class DTO:
    def __init__(self,num):
        self.num = num
        self.s = 'test'*num
        self.array = Query.en(range(num)).to_list()


FOLDER = 'test_queries/files/'

class ExtendedMethodsTests(TestCase):

    def test_text_file(self):
        os.makedirs(path(FOLDER),exist_ok=True)
        with open(path(FOLDER,'sample.txt'),'w') as file:
            file.write('1\n2\n\n3\n4')
        data = Query.file.text(path(FOLDER, 'sample.txt')).to_list()
        self.assertListEqual(["1","2","","3","4"],data)

    def test_text_io(self):
        os.makedirs(path(FOLDER), exist_ok=True)
        array = ['23','342','1241','','452']
        Query.en(array).to_text_file(path(FOLDER, 'sample1.txt'), autoflush=True)
        self.assertListEqual(array,Query.file.text(path(FOLDER,'sample1.txt')).to_list())

    def test_zip_io(self):
        os.makedirs(path(FOLDER), exist_ok=True)
        array = ['23', '342', '1241', '', '452']
        Query.en(array).to_zip_text_file(path(FOLDER, 'sample1.txt.gzip'))
        self.assertListEqual(array,Query.file.zipped_text(path(FOLDER,'sample1.txt.gzip')).to_list())


    def test_pickle_unpickle(self):
        os.makedirs(path(FOLDER),exist_ok=True)
        Query.en(range(10)).select(DTO).to_pickle_file(path(FOLDER, 'sample.pickle'))
        result = Query.file.pickle(path(FOLDER,'sample.pickle')).with_indices().all(lambda z:
          z.value.num == z.key and
          z.value.s == 'test'*z.key and
          len(z.value.array) == z.key)
        self.assertTrue(result)

    def test_zip_folder_io(self):
        t = Query.args('a','b','c').select(lambda z: KeyValuePair(z+'.txt',z*10000)).to_dictionary()
        Query.dict(t).to_zip_folder(path(FOLDER,'zipped_folder.zip'))
        result = Query.file.zipped_folder(path(FOLDER,'zipped_folder.zip')).to_dictionary()
        self.assertDictEqual(t,result)

    def test_zip_folder_raises(self):
        self.assertRaises(
            ValueError,
            lambda: Query.args(1,2,3).to_zip_folder(path(FOLDER,'zipped_folder_1.zip'))
        )


