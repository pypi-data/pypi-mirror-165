
cacha_version = $1
pip install cacha==$(cacha_version)


python - << EOF
import cacha
string = "This is a long string"

def split(string: str) -> list:
    return string.split()

cacha.cache(split, (string,))

cached_string = cacha.cache(split, (string,))

EOF

