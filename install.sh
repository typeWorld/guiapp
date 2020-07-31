python -m pip install -r requirements.txt

# Download Sparkle
curl -O -L https://github.com/sparkle-project/Sparkle/releases/download/1.23.0/Sparkle-1.23.0.tar.bz2
mkdir sparkle
tar -xf Sparkle-1.23.0.tar.bz2 --directory sparkle

# Secret Keys
echo $GOOGLE_APPLICATION_CREDENTIALS_KEY
echo $GOOGLE_APPLICATION_CREDENTIALS_KEY > "typeworld2-559c851e351b.json"
cat "typeworld2-559c851e351b.json"

# Build target folder
mkdir build
mkdir dist
