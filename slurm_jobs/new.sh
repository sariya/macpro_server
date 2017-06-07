#!/usr/bin/env bash

printf "hello\n"

#Submitting on colonial one using sbatch and command line parameter and values
#
# sbatch -J test_new -t 2 -p defq --wrap="bash new.sh"
