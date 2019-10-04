import pandas as pd
import numpy as np
from ._add_ordering_column import add_ordering_column
from typing import *


#https://cs.stackexchange.com/questions/29709/algorithm-to-distribute-items-evenly
#by https://cs.stackexchange.com/users/70760/lungj
def _generate(item_counts):
    '''
    item_counts is a list of counts of "types" of items. E.g., [3, 1, 0, 2] represents
    a list containing [1, 1, 1, 2, 4, 4] (3 types of items/distinct values). Generate
    a new list with evenly spaced values.
    '''
    # Sort number of occurrences by decreasing value.
    item_counts.sort(reverse=True)
    # Count the total elements in the final list.
    unplaced = sum(item_counts)
    # Create the final list.
    placements = [None] * unplaced

    # For each type of item, place it into the list item_count times.
    for item_type, item_count in enumerate(item_counts):
        # The number of times the item has already been placed
        instance = 0
        # Evenly divide the item amongst the remaining unused spaces, starting with
        # the first unused space encountered.
        # blank_count is the number of unused spaces seen so far and is reset for each
        # item type.
        blank_count = -1
        for position in range(len(placements)):
            if placements[position] is None:
                blank_count += 1
                # Use an anti-aliasing technique to prevent bunching of values.
                if blank_count * item_count // unplaced == instance:
                    placements[position] = item_type
                    instance += 1
        # Update the count of number of unplaced items.
        unplaced -= item_count

    return placements

def _generate_index(placements, counts):
    result = []
    for _class in placements:
        counts[_class]-=1
        result.append(counts[_class])
    return result

class stratify(Callable[[pd.DataFrame],pd.DataFrame]):
    def __init__(self,
        columns: Union[str,List[str]],
        stratify_column_name: str='stratify_index',
        random_state: Optional[Union[int,np.random.RandomState]]= None):
        self.columns = columns
        self.stratify_column_name = stratify_column_name
        self.random_state = random_state

    def __call__(self, df: pd.DataFrame)->pd.DataFrame:
        if self.random_state is None:
            self.random_state = np.random.RandomState()
        elif isinstance(self.random_state,int):
            self.random_state = np.random.RandomState(self.random_state)

        random_order = self.random_state.permutation(df.shape[0])
        df = df.assign(_rand_order = random_order)
        df = add_ordering_column(self.columns, '_rand_order', '_order', '_group')(df)
        #print(df)

        counts = df.groupby('_group').size().to_frame('counts').sort_values('counts',ascending=False).reset_index()
        #print(counts)

        group_index = _generate(list(counts.counts))

        order_index = _generate_index(group_index,list(counts.counts))

        result = pd.DataFrame(dict(group_index=group_index, _order=order_index))
        result = result.merge(counts._group.to_frame(),left_on='group_index',right_index=True).sort_index()
        result = result.reset_index().rename(columns=dict(index=self.stratify_column_name)).drop('group_index',axis=1)
        result = result.set_index(['_group','_order'])
        result = result.merge(df,left_index=True,right_on=['_group','_order']).set_index(self.stratify_column_name)
        result = result.drop(['_rand_order','_order','_group'],axis=1)
        return result


