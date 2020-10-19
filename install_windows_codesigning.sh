# Decode the environment variable into our file
echo $CERTUM_TRUSTED_NETWORK_CA > CERTUM_TRUSTED_NETWORK_CA.cer
echo $SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA > SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.cer
echo $SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1 > SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1.cer
echo $JANGERNER_CERT > JANGERNER_CERT.cer
# echo $JANGERNER_P12 > JANGERNER.p12.base64encoded
# python tweakcertificate.py JANGERNER.p12.base64encoded
# python -m base64 -d JANGERNER.p12.base64encoded > JANGERNER.p12
# echo $JANGERNER_P12 > JANGERNER.pfx
# python base32decode.py JANGERNER.pfx
# certutil -decode JANGERNER.p12.base64encoded JANGERNER.p12
# base64 -d JANGERNER.p12.base64encoded > JANGERNER.p12

#echo $JANGERNER_P12 | python -m base64 -d > JANGERNER.p12
# echo $JANGERNER_P12 > JANGERNER.p12.base64
# cat JANGERNER.p12.base64

#echo $JANGERNER_P12
# base64 --help

# pk12util -i JANGERNER.pfx -d/path/to/database -W password

python tweakcertificate.py CERTUM_TRUSTED_NETWORK_CA.cer
python tweakcertificate.py SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.cer
python tweakcertificate.py SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1.cer
python tweakcertificate.py JANGERNER_CERT.cer

# Add
# https://stackoverflow.com/questions/23869177/import-certificate-to-trusted-root-but-not-to-personal-command-line
# https://stackoverflow.com/questions/28690986/code-signing-with-signtool-fails-due-to-private-key-filter

certutil -addstore "Root" CERTUM_TRUSTED_NETWORK_CA.cer
certutil -addstore "CA" SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.cer
certutil -addstore "CA" SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1.cer
certutil -addstore -user "My" JANGERNER_CERT.cer
# certutil -addstore -user "My" jangerner.pfx -p $JANGERNER_P12_PASSWORD
# certutil -addstore -user "TRUSTEDPEOPLE" jangerner.pfx -p $JANGERNER_P12_PASSWORD

# https://stackoverflow.com/questions/5171117/import-pfx-file-into-particular-certificate-store-from-command-line
certutil -f -p $JANGERNER_P12_PASSWORD -enterprise -importpfx My "jangerner.pfx"

# Certmgr.exe /c /add CERTUM_TRUSTED_NETWORK_CA.cer /s root
# Certmgr.exe /c /add SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.cer /s ca
# Certmgr.exe /c /add SSL_COM_CODE_SIGNING_INTERMEDIATE_CA_RSA_R1.cer /s ca
# Certmgr.exe /c /add JANGERNER_CERT.cer /s my