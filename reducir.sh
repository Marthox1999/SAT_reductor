#!/bin/bash
echo Python version is: $(python3 --version)
if [[ $1 == "-m" ]]
then
    if [[ ! -z $2 ]]
    then
        if [[ $(python3 --version) == *"Python"* ]];
        then
            echo "The app will reduce all the files on Instancias SAT to $2 and store them on X-SAT"
            echo "Python3 is installed"
            echo "Running script with python3"
            cd ./Reductor && python3 main.py $1 $2
            echo "Finished, please check the X-SAT folder"
        elif [[ $(python3 --version) == *"Python"* ]]
        then
            echo "The app will reduce all the files on Instancias SAT to $2 and store them on X-SAT"
            echo "Python2 is installed"
            echo "Running script with python2"
            cd ./Reductor && python main.py $1 $2
            echo "Finished, please check the X-SAT folder"
        else
            echo "Please install python"
        fi
    else 
        echo "Please type a X-SAT value to reduce to [-m x]"
    fi
else
    echo "Please type a valir argument [-m]"
fi