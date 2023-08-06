#!/bin/bash
# This script os a helper script for checking if the pip-published 
# package works.

cacha_version = $1
pip install cacha==$(cacha_version)


python - << EOF
import cacha
string = "This should be split"


def split(string: str) -> list:
    return string.split()


cacha.cache(split, (string,))

result = cacha.cache(split, (string,))

print(result)

EOF
