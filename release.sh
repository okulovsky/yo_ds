#!/bin/bash

VERSION=1.1.8

function make_release() {
    MODULE=$1
    echo
    echo Releasing $MODULE at $VERSION
    echo

    mkdir -p release
    mkdir release/$MODULE

    sed s/VERSIONID/$VERSION/g release_files/setup_$MODULE.py >>release/$MODULE/setup.py

    cp release_files/README_$MODULE.md release/$MODULE/README.md
    cp release_files/MANIFEST.in release/$MODULE/MANIFEST.in

    for i in "${@:2}"
        do
            echo copying $i
            cp -r $i release/$MODULE/$i
        done

    PASSWORD=$(<pypi_password)

    cd release/$MODULE/
    conda remove --name yo_release --all -y
    conda create --name yo_release python=3.6 -y
    source activate yo_release
    pip install twine

    python setup.py test || exit 1

    python setup.py sdist bdist_wheel;
    twine upload -u okulovsky -p $PASSWORD dist/*

    sleep 5
    pip install $MODULE==$VERSION
    sleep 5
    pip install $MODULE==$VERSION

    if [ $? -eq 0 ];
        then
            echo ================ PUBLISHED ======================
        else
            exit
    fi

    source deactivate
    cd ../..
}

./coverage.sh || exit 1

rm -rf release
make_release yo_fluq yo_fluq yo_fluq__tests
make_release yo_fluq_ds yo_fluq_ds yo_fluq__tests yo_fluq_ds__tests
make_release yo_ds yo_extensions yo_extensions__tests yo_ds yo_ds__tests
