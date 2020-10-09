echo "Current folder: $PWD"

# Mac Code Signing
sh install_mac_codesigning.sh


python -m pip install -r requirements.txt

python -m pip install -I git+https://github.com/yanone/python-pubsub.git

# # Replace 
# importlib_version = $(pip show importlib_metadata | sed -n -e 's/Version: \([[:alnum:][:punct:]]\)/\1/p')
# echo $importlib_version
# sed -i 's/old-text/new-text/g' input.txt

# Download Sparkle
curl -O -L https://github.com/sparkle-project/Sparkle/releases/download/1.23.0/Sparkle-1.23.0.tar.bz2
mkdir sparkle
tar -xf Sparkle-1.23.0.tar.bz2 --directory sparkle

# Google Cloud Storage Key
echo $GOOGLE_APPLICATION_CREDENTIALS_KEY > "typeworld2-559c851e351b.json"

# ynlib
git clone https://github.com/yanone/ynlib.git
#export PYTHONPATH="~/projects/guiapp/ynlib/Lib/"

# Build target folder
mkdir build
mkdir dist
mkdir dmg

# ls -la .
# ls -la ynlib
# ls -la ynlib/Lib
# ls -la ynlib/Lib/ynlib

# Python
# Link .dylib
# Apparently, they're the same file:
# https://groups.google.com/a/continuum.io/forum/#!topic/anaconda/4HKVl8Jhy9E
ln -s ~/.localpython3.7.7/lib/libpython3.7m.dylib ~/.localpython3.7.7/lib/libpython3.7.dylib

# ls -la ~/venv3.7.7/lib/python3.7/site-packages

# ls -la ~/venv3.7.7/lib/python3.7/site-packages/typeworld
# ls -la ~/venv3.7.7/lib/python3.7/site-packages/typeworld/client
