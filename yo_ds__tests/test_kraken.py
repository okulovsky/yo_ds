import unittest
from yo_ds import kraken
from collections import OrderedDict
from sklearn.linear_model import Lasso, Ridge
from yo_ds__tests.common import *
import shutil
import os
from typing import *

def kraken_default_method(iteration, a, b):
    return pd.DataFrame(dict(result=pd.Series([a+b,a-b]), is_addition=[True,False]))

def kraken_simple_method(iteration, a, b):
    return a+b

def kraken_throwing_method(iteration, a,  b):
    if iteration==3:
        raise ValueError("I don't like this number")
    return a+b

def kraken_nested_method(iteration, a):
    return pd.DataFrame(dict(result=pd.Series([a.b+a.c])))

class KrakenTests(unittest.TestCase):

    #this method is required to override default value to with_tqdm and pandas_extractor
    def kraken_run(self, method, plan, **kwargs):
        kwargs['with_tqdm'] = maybe(kwargs, ['with_tqdm'], default=False)
        kwargs['pandas_extractor'] = maybe(kwargs,['pandas_extractor'])
        return kraken.release(method, plan, **kwargs)


    def assertResult(self, result: List[Any], kraken_output: List[kraken.IterationResult]):
        actual = [z.result for z in kraken_output]
        self.assertListEqual(result,actual)
        for r in kraken_output:
            self.assertIsInstance(r.condition,OrderedDict)
            self.assertTrue(r.status == kraken.IterationStatus.Success)

    def get_default_plan(self):
        return Query.combinatorics.grid(a=[10,20], b=[1,2]).to_list()


    #the default call to kraken. Each iteration returns Dataframe, and they are later merged with conditions
    def test_default_machinery(self):
        plan = self.get_default_plan()
        df = self.kraken_run(
            kraken_default_method,
            plan,
            pandas_extractor = lambda df, _ : df #the default one. Normally you don't need to override it
        )

        self.assertListEqual([11,9,12,8,21,19,22,18],list(df.result))
        self.assertListEqual([True,False,True,False,True,False,True,False], list(df.is_addition))
        self.assertListEqual([0,0,1,1,2,2,3,3], list(df.iteration))
        self.assertListEqual([10,10,10,10,20,20,20,20],list(df.a))
        self.assertListEqual([1,1,2,2,1,1,2,2],list(df.b))

    # kraken method can return anything.
    # If this case, you can skip the conversion to pandas and process raw outputs/configs
    def test_without_extractor(self):
        plan = self.get_default_plan()
        result = self.kraken_run(
            kraken_simple_method,
            plan,
            pandas_extractor=None)

        self.assertResult([11,12,21,22],result)


    # you can also provide the custom extractor, that will transform method's output to dataframe
    # this method also accepts the condition, but DO NOT MERGE manually! It's done later automatically. It's mostly for the sake of generality
    def test_with_custom_extractor(self):
        plan = self.get_default_plan()
        result = self.kraken_run(
            kraken_simple_method,
            plan,
            pandas_extractor=lambda z, _:pd.DataFrame(dict(result=pd.Series([z]))))
        self.assertIsInstance(result,pd.DataFrame)
        self.assertListEqual([11,12,21,22],list(result.result))
        self.assertListEqual([0,1,2,3],list(result.iteration))
        self.assertListEqual([10,10,20,20], list(result.a))

    # you can run the process on the specific iterations. It is helpful if some of them raised exception
    def test_with_specific_iteration(self):
        plan = self.get_default_plan()
        result = self.kraken_run(
            kraken_simple_method,
            plan,
            special_iterations=[1,3]
        )
        self.assertResult([12, 22], result)


    # By default, if the method throws, the kraken do not handles it
    def test_with_throwing_method_0(self):
        plan = self.get_default_plan()
        self.assertRaises(ValueError,lambda: self.kraken_run(kraken_throwing_method,plan))

    # But if handle_exception_callback is provided, each erroneous exception will be returned for postprocessing,
    # and the erroneous entries will be stored in the resulting report
    def test_with_throwing_method_1(self):
        plan = self.get_default_plan()
        errors = []
        result = self.kraken_run(
            kraken_throwing_method,
            plan,
            handle_exception_callback = lambda z: errors.append(z)
        )
        self.assertEqual(kraken.IterationStatus.Failed, result[3].status)
        self.assertEqual(3,errors[0].iteration)
        good_result = result[0:3]
        self.assertResult([11,12,21],good_result)

    #Erroneous entries are excluded in dataframe report
    def test_with_throwing_method_2(self):
        plan = self.get_default_plan()
        errors = []
        result = self.kraken_run(
            kraken_throwing_method,
            plan,
            handle_exception_callback=lambda z: errors.append(z),
            pandas_extractor = lambda res, _ : pd.DataFrame(pd.Series([res]))
        )
        self.assertListEqual([0,1,2],list(result.iteration))

    # Plan can contain nested fields.
    # It's useful if you want to, e.g., independently test featurizers and models
    # The method will take arguments exactly as specified in the plan. But in the resulting dataframe, the columns will be flattened
    def test_with_nested_field(self):
        plan = Query.combinatorics.grid(a = Query.combinatorics.grid(b=[1,2],c=[10,20]).to_list()).to_list()
        result = self.kraken_run(
            kraken_nested_method,
            plan,
            pandas_extractor=lambda df,_:df
        )
        self.assertListEqual([11,21,12,22], list(result.result))
        self.assertListEqual(['result','iteration','a_b','a_c'],list(result.columns))

    # If you want to test different models, you can make use of kraken.invoke method.
    # To do it, set 'ctor' field to constructor, additional fields in the corresponding constructors arguments, select via kraken.invoke and obtain object from 'instance'
    def test_invoke(self):
        models = Query.combinatorics.grid(ctor=[Lasso,Ridge], alpha=[1,2]).select(kraken.invoke).to_list()
        self.assertIsInstance(models[0]['instance'],Lasso)
        self.assertEqual(models[0]['instance'].alpha,1)
        self.assertIsInstance(models[3]['instance'],Ridge)
        self.assertEqual(models[3]['instance'].alpha, 2)

    # Kraken can run in parallel. The test does not check if it was actually run in parallel, just that the method is working
    def test_parallel(self):
        plan = self.get_default_plan()
        result = self.kraken_run(
            kraken_simple_method,
            plan,
            parallel_kwargs = {}
        )


    # Instead of immediately processing result, Kraken can store them in files. Kraken do noe re-evaluate stored results
    # The stored data can be retrieved in the same format as Kraken return with the method load
    def test_files(self):
        folder = path('kraken_output_files/')
        print(folder)
        if os.path.isdir(folder): #pragma: no cover
            shutil.rmtree(folder)

        plan = self.get_default_plan()

        self.kraken_run(
            kraken_simple_method,
            plan,
            cache_to_folder=folder,
            special_iterations=[3]
        )

        file = Query.folder(folder).single()
        self.assertEqual('3.kraken.pkl',file.name)

        results = self.kraken_run(
            kraken_simple_method,
            plan,
            cache_to_folder=folder
        ) # type: List[kraken.IterationResult]

        for index,result in enumerate(results):
            self.assertEqual(
                kraken.IterationStatus.Skipped if index == 3 else kraken.IterationStatus.Success,
                result.status)
            self.assertIsNone(result.condition)
            self.assertIsNone(result.result)

        loaded_results = Query.en(kraken.load(folder, None)).order_by(lambda z: z.result).to_list()
        self.assertResult([11,12,21,22],loaded_results)

        shutil.rmtree(folder)

    #You can also shuffle result. It's a good option if different entries of the plan require different time,
    #but you want to have more accurate time estimation from tqdm
    def test_shuffle(self):
        plan = self.get_default_plan()
        result = self.kraken_run(
            kraken_simple_method,
            plan,
            shuffle=1
        )
        self.assertResult([22,21,11,12],result)