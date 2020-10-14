# Update pip
python -m pip install --upgrade pip

# Install requirements
python -m pip install -r requirements_windows.txt

# ynlib
git clone https://github.com/yanone/ynlib.git

# Build target folder
mkdir build
mkdir dist
mkdir dmg

# Google Cloud Storage Key
echo $GOOGLE_APPLICATION_CREDENTIALS_KEY > "typeworld2-559c851e351b.json"
cat "typeworld2-559c851e351b.json"
