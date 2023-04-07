import os
import subprocess
from pathlib import Path
import shutil
from yo_fluq_ds import FileIO

VERSION = '1.1.15'
conda_path = Path('/home/yura/anaconda3/')
repo_path = Path(__file__).parent.absolute()
release_files_path = repo_path/'release_files'
release_path = repo_path/'release'

def copy_files(lib):
    lib_path = release_path/lib
    shutil.rmtree(lib_path, ignore_errors=True)
    os.makedirs(lib_path)
    shutil.copytree(repo_path/lib, lib_path/lib)
    shutil.copy(release_files_path/'MANIFEST.in', lib_path)
    setup = FileIO.read_text(release_files_path/f'setup_{lib}.py')
    setup = setup.replace('VERSIONID',VERSION)
    FileIO.write_text(setup, lib_path/'setup.py')
    readme = FileIO.read_text(release_files_path/f'README_{lib}.md')
    FileIO.write_text(readme, lib_path/'README.md')




def test_lib(python_version, libs):
    subprocess.call([conda_path/'bin/conda','remove','--name','yo_release','--all','-y'])
    subprocess.call([conda_path/'bin/conda','create','--name','yo_release','python='+python_version,'-y'])
    python = conda_path/'envs/yo_release/bin/python'
    for lib in libs:
        subprocess.call([python, '-m','pip','install','-e',release_path/lib])
    for lib in libs:
        if subprocess.call([python, '-m', 'unittest', 'discover',repo_path/f'{lib}__tests'])!=0:
            print (f'\n\nFAILED lib {lib} on python {python_version}')
            exit(1)



if __name__ == '__main__':
    python_versions = ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11']
    copy_files('yo_fluq')
    for python in python_versions:
        test_lib(python, ['yo_fluq'])
    copy_files('yo_fluq_ds')
    for python in python_versions:
        test_lib(python, ['yo_fluq', 'yo_fluq_ds'])
