from typing import *
import pandas as pd

class add_ordering_column(Callable[[pd.DataFrame],pd.DataFrame]):
    def __init__(self,
        group_by_columns: Union[str,List[str]],
        order_by_column: Optional[Union[str,Tuple[str,bool]]],
        ordering_column_name = 'order',
        group_id_column_name = None):
        self.group_by_columns = group_by_columns
        self.order_by_column = order_by_column
        self.ordering_column_name = ordering_column_name
        self.group_id_column_name = group_id_column_name

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:

        if isinstance(self.group_by_columns,str):
            self.group_by_columns = [self.group_by_columns]


        sort_column = list(self.group_by_columns)
        ascendings = [True for z in sort_column]

        if self.order_by_column is not None:
            if isinstance(self.order_by_column,str):
                sort_column.append(self.order_by_column)
                ascendings.append(True)
            elif (
                    isinstance(self.order_by_column,tuple)
                    and len(self.order_by_column)==2
                    and isinstance(self.order_by_column[0],str)
                    and isinstance(self.order_by_column[1],bool)
            ):
                sort_column.append(self.order_by_column[0])
                ascendings.append(self.order_by_column[1])
            else:
                raise ValueError('ordering_by_column expected to be str or Tuple[str,bool], but was {0}'.format(self.order_by_column)) #pragma: no cover

        df = df.sort_values(sort_column,ascending=ascendings)
        sizes = df.groupby(self.group_by_columns).size()
        ordering = [o for sz in sizes for o in range(sz)]
        df = df.assign(**{self.ordering_column_name : ordering})
        if self.group_id_column_name is not None:
            group_id = [index for index, sz in enumerate(sizes) for _ in range(sz)]
            df = df.assign(**{self.group_id_column_name : group_id})
        return df

