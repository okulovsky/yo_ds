from yo_fluq_ds import *

def maybe_shift_line(line,shift):
    if line.startswith('#'):
        return '#'*shift+line
    return line

def maybe_open_and_shift_file(line):
    if line.startswith('#>'):
        index = int(line[2])
        fname = line[3:].strip()
        fname = FileIO.relative_to_file(__file__,fname)
        return Query.file.text(fname).select(lambda z: maybe_shift_line(z,index))
    else:
        return [line]


def process_file(src,dst):
    Query.file.text(src).select_many(maybe_open_and_shift_file).to_text_file(dst)

if __name__=='__main__':
    process_file(
        FileIO.relative_to_file(__file__, 'README_yo_fluq.md'),
        FileIO.relative_to_file(__file__, '../release_files/README_yo_fluq.md'),
    )

    process_file(
        FileIO.relative_to_file(__file__, 'README_yo_fluq_ds.md'),
        FileIO.relative_to_file(__file__, '../release_files/README_yo_fluq_ds.md'),
    )