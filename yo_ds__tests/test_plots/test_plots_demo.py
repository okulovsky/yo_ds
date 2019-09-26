from yo_ds__tests.test_plots.test_fluent_plot import TestFluentPlot
from yo_ds__tests.test_plots.test_grbar import TestGrBar
from yo_ds__tests.test_plots.test_other_plots import TestOtherPlots
from yo_ds__tests.common import *



## TODO: this file is currently invalid, because no tests are available

class PlotDemoTest(TestCase):

    def make_nbook_section(self, filename, testtype, header):
        this_file_name = path('test_plots',filename)
        lines = Query.file.text(this_file_name).to_list()
        insertion = Query.en(lines).with_indices().where(lambda z: not z.value.startswith('from')).first().key
        lines.insert(insertion, 'class TestCase:')
        lines.insert(insertion + 1, '    pass')
        lines = Query.en(lines).select(lambda z: z + "\n").to_list()
        lines.append('tc = {0}()'.format(testtype.__name__))

        cells = [MD_CELL_TEMPLATE(['# '+header]), CELL_TEMPLATE(lines)]

        ts = testtype()
        Query.en(dir(ts)).where(lambda z: z.startswith('test')).select('tc.{0}()'.format).select(CELL_TEMPLATE).foreach(cells.append)

        return cells



    def test_mkbook(self):

        c1 = self.make_nbook_section('test_fluent_plot.py', TestFluentPlot, 'Fluent plot examples')
        c2 = self.make_nbook_section('test_grbar.py', TestGrBar, 'GRBAR plot examples')
        c3 = self.make_nbook_section('test_other_plots.py',TestOtherPlots, 'Other plots examples')


        nb = NOTEBOOK_TEMPLATE(c1+c2+c3)
        FileIO.write_json(nb,FileIO.relative_to_file(__file__,'Plots demo.ipynb'))


def NOTEBOOK_TEMPLATE(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.6.7"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }


def CELL_TEMPLATE(lines):
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": lines
    }

def MD_CELL_TEMPLATE(lines):
    return {
   "cell_type": "markdown",
   "metadata": {},
   "source": lines
  }
