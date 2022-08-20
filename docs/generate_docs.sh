PROJ_NAME="PstrYve"

cd "$(dirname "$0")"
rm -rf _build
rm -rf source
sphinx-apidoc -e -M -f -t ./templates -o source ../$PROJ_NAME ../dist* ../build* ../$PROJ_NAME.egg* ../$PROJ_NAME/__pycache__ ../$PROJ_NAME/$PROJ_NAME.egg* ../$PROJ_NAM/consts.py ../setup.py
make html
