# Decode the environment variable into our file
echo $CERTUM_TRUSTED_NETWORK_CA > CERTUM_TRUSTED_NETWORK_CA.cer
echo $SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA > SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.cer
echo $SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1 > SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1.cer
echo $JANGERNER_CERT > JANGERNER_CERT.cer

python tweakcertificate.py CERTUM_TRUSTED_NETWORK_CA.cer
python tweakcertificate.py SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.cer
python tweakcertificate.py SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1.cer
python tweakcertificate.py JANGERNER_CERT.cer

# Add
# https://stackoverflow.com/questions/23869177/import-certificate-to-trusted-root-but-not-to-personal-command-line
# https://stackoverflow.com/questions/28690986/code-signing-with-signtool-fails-due-to-private-key-filter

certutil -addstore -user -f "Root" CERTUM_TRUSTED_NETWORK_CA.cer
certutil -addstore -user -f "CA" SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.cer
certutil -addstore -user -f "CA" SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1.cer
certutil -addstore -user -f "My" JANGERNER_CERT.cer

# Certmgr.exe /c /add CERTUM_TRUSTED_NETWORK_CA.cer /s root
# Certmgr.exe /c /add SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.cer /s ca
# Certmgr.exe /c /add SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1.cer /s ca
# Certmgr.exe /c /add JANGERNER_CERT.cer /s my