from yo_fluq_ds import *
import re

splitter = re.compile(" +")


def parse_file(file):
    return (Query
        .file.text(file)
        .skip_while(lambda z: not z.startswith('---'))
        .skip(1)
        .take_while(lambda z: not z.startswith('---'))
        .select(lambda z: splitter.split(z))
    )



if __name__ == '__main__':
    bad_files = parse_file('test_coverage/yo_fluq_report.txt').where(lambda z: z[-1]!='100%').select(lambda z: z[0]).to_list()
    Query.en(bad_files).foreach(print)
    assert len(bad_files)==0, '100% coverage is not achieved!'