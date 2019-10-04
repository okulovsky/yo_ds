from ._common import *


def _assign(df: pd.DataFrame, items, name: str, smth: Union[str,pd.Series]):
    if smth is None:
        raise ValueError('Parameter for {0} cannot be None'.format(name))
    elif isinstance(smth, pd.Series):
        if len(smth) != df.shape[0]:
            raise ValueError('Length of a series, given as {0}, does not match dataframe'.format(name))
        column = smth
    else:
        column = df[smth]

    for item, value in zip(items,column):
        setattr(item,name,value)

def _get_name(smth: Union[None,str,pd.Series]):
    if smth is None:
        return None
    elif isinstance(smth,pd.Series):
        return smth.name
    else:
        return str(smth)



class _DbarItem:
    def __init__(self):
        self.value = 0
        self.color = ''
        self.group = ''
        self.error = None
        self.caption = None

        self.low_value = None
        self.high_value = 0

        self.color_index = 0
        self.group_index = 0

        self.x = 0

    def finalize(self, value_format, color_indices, group_indices):
        if isinstance(self.value, pd.Interval):
            self.error = self.value.mid - self.value.left
            self.value = self.value.mid

        if value_format is not None and self.caption is None:
            if self.error is not None:
                self.caption = value_format.format(self.value,self.error)
            else:
                self.caption = value_format.format(self.value)

        if self.error is None:
            self.low_value = None
            self.high_value = self.value
        else:
            self.low_value = self.value - self.error
            self.high_value = self.value + self.error

        self.color_index = color_indices[self.color]
        self.group_index = group_indices[self.group]

        self.group_width = 1
        self.group_draw_width = 0.8
        self.color_width = self.group_draw_width / (len(color_indices))

        self.x = self.group_index * self.group_width + self.color_index * self.color_width




def _plot_dbar_vertical(ax, items: List[_DbarItem], group_label, value_label):
    gitems = Query.en(items).group_by(lambda z: z.color_index).select(list).to_list()
    for color_items in gitems:
        rects = ax.bar(
            Query.en(color_items).select(lambda z: z.x).to_list(),
            Query.en(color_items).select(lambda z: z.high_value).to_list(),
            width=color_items[0].color_width,
            label=color_items[0].color
        )

        with_low = Query.en(color_items).where(lambda z: z.low_value is not None).to_list()
        if len(with_low)>0:
            ax.bar(
                Query.en(with_low).select(lambda z: z.x).to_list(),
                Query.en(with_low).select(lambda z: z.low_value).to_list(),
                width=with_low[0].color_width,
                color='white',
                alpha=0.6
            )

        for item, rect in zip(color_items, rects):
            if item.caption is None:
                continue
            ax.text(
                rect.get_x() + rect.get_width() / 2.,
                rect.get_height(),
                item.caption,
                ha='center', va='bottom')

    labels = Query.en(items).distinct(lambda z: z.group_index).to_series(lambda z: z.group,lambda z: z.group_index)
    ax.xaxis.set_ticks([x * items[0].group_width + items[0].group_draw_width / 2 - items[0].color_width / 2 for x in labels.index])
    ax.xaxis.set_ticklabels(labels)
    if group_label is not None:
        ax.set_xlabel(group_label)
    ax.set_ylabel(value_label)
    return ax


def _plot_dbar_horizontal(ax, items: List[_DbarItem], group_label, value_label):
    gitems = Query.en(items).group_by(lambda z: z.color_index).select(list).to_list()
    for color_items in gitems:
        rects = ax.barh(
            Query.en(color_items).select(lambda z: z.x).to_list(),
            Query.en(color_items).select(lambda z: z.high_value).to_list(),
            height=color_items[0].color_width,
            label=color_items[0].color
        )
        with_low = Query.en(color_items).where(lambda z: z.low_value is not None).to_list()
        if len(with_low) > 0:
            ax.barh(
                Query.en(with_low).select(lambda z: z.x).to_list(),
                Query.en(with_low).select(lambda z: z.low_value).to_list(),
                height=with_low[0].color_width,
                color='white',
                alpha=0.6
            )

        for item, rect in zip(color_items, rects):
            if item.caption is None:
                continue
            ax.text(
                rect.get_width(),
                rect.get_y() + rect.get_height() / 2.,
                item.caption,
                ha='left', va='center')

    labels = Query.en(items).distinct(lambda z: z.group_index).to_series(lambda z: z.group, lambda z: z.group_index)
    ax.yaxis.set_ticks(
        [x * items[0].group_width + items[0].group_draw_width / 2 - items[0].color_width / 2 for x in labels.index])
    ax.yaxis.set_ticklabels(labels)
    if group_label is not None:
        ax.set_ylabel(group_label)
    ax.set_xlabel(value_label)
    return ax




def grbar_plot(
         df: pd.DataFrame,
         value_column: Union[str, pd.Series],
         color_column: Union[str, pd.Series, None] = None,
         group_column: Union[str, pd.Series, None] = None,
         error_column: Union[str, pd.Series, None] = None,
         caption_column: Union[str, pd.Series, None] = None,
         value_format: Optional[str] = None,
         ax = None,
         orient = 'v'
         ):
    items = [_DbarItem() for _ in range(df.shape[0])]

    _assign(df, items, 'value', value_column)
    if color_column is not None:
        _assign(df, items, 'color', color_column)
    else:
        if group_column is None:
            raise ValueError('At least one of `color_column` or `group_column` must be not None')
    if group_column is not None:
        _assign(df, items, 'group', group_column)
    if error_column is not None:
        _assign(df, items, 'error', error_column)
    if caption_column is not None:
        _assign(df, items, 'caption', caption_column)

    color_indices = (Query
                     .en(items)
                     .select(lambda z: z.color)
                     .distinct()
                     .with_indices()
                     .to_dictionary(lambda z: z.value, lambda z: z.key)
                     )

    group_indices = (Query
                     .en(items)
                     .select(lambda z: z.group)
                     .distinct()
                     .with_indices()
                     .to_dictionary(lambda z: z.value, lambda z: z.key)
                     )

    Query.en(items).foreach(lambda z: z.finalize(value_format, color_indices, group_indices))

    group_label = _get_name(group_column)
    value_label = _get_name(value_column)

    if orient=='v':
        ax = _plot_dbar_vertical(default_ax(ax), items, group_label, value_label)
    else:
        ax = _plot_dbar_horizontal(default_ax(ax), items, group_label, value_label)

    return ax




