
CERT_DIR=$(pwd)"/certificates"
CLA_DIR=$(pwd)"/digivote-cla/src"
CTF_DIR=$(pwd)"/digivote-ctf/src"
CLA_CNF_NAME=$(pwd)"/cla.ssl.conf"
CTF_CNF_NAME=$(pwd)"/ctf.ssl.conf"
CA_KEY_NAME="$CERT_DIR/auth.key"
CA_CRT_NAME="$CERT_DIR/auth.crt"
CLA_CRT_NAME="$CLA_DIR/cla.crt"
CLA_CSR_NAME="$CLA_DIR/cla.csr"
CLA_KEY_NAME="$CLA_DIR/cla.key"
CTF_CRT_NAME="$CTF_DIR/ctf.crt"
CTF_CSR_NAME="$CTF_DIR/ctf.csr"
CTF_KEY_NAME="$CTF_DIR/ctf.key"

if [ ! -d "$CERT_DIR" ]; then
  echo "$CERT_DIR not found..."
  echo "creating $CERT_DIR"
  mkdir $CERT_DIR
fi


if [ ! -f "$CA_CRT_NAME" ] || [ ! -f "$CA_KEY_NAME" ]; then
  echo "Authoritative cert and key not found..."
  echo "Generating CA cert and key at: "
  echo "    $CA_CRT_NAME"
  echo "    $CA_KEY_NAME"
  openssl req -x509 -nodes -newkey rsa:4096 -keyout $CA_KEY_NAME -out $CA_CRT_NAME -days 365 -sha256 -subj "/C=US/ST=Texas/L=San Antonio/O=St. Mary's University/OU=Computer Science Cyberlab/CN=authority.cyber.stmarytx.edu"

fi

echo "Generating CLA key at: "
echo "    $CLA_KEY_NAME"
openssl genrsa -out "$CLA_KEY_NAME" 4096

echo "Generating CLA CSR at: "
echo "    $CLA_CSR_NAME"
openssl req -new -key $CLA_KEY_NAME -out $CLA_CSR_NAME -config $CLA_CNF_NAME
# openssl req -text -noout -in $CLA_CSR_NAME

echo "Generating CTF key at: "
echo "    $CTF_KEY_NAME"
openssl genrsa -out $CTF_KEY_NAME 4096

echo "Generating CTF CSR at: "
echo "    $CTF_CSR_NAME"
openssl req -new -key $CTF_KEY_NAME -out $CTF_CSR_NAME -config $CTF_CNF_NAME
# openssl req -text -noout -in $CTF_CSR_NAME

echo "Signing $CLA_CRT_NAME with CA $CA_CRT_NAME"
openssl x509 -req -in $CLA_CSR_NAME -CA $CA_CRT_NAME -CAkey $CA_KEY_NAME -CAcreateserial -out $CLA_CRT_NAME -extensions req_ext -extfile $CLA_CNF_NAME
# openssl x509 -text -in $CLA_CRT_NAME -noout

echo "Signing $CTF_CRT_NAME with CA $CA_CRT_NAME"
openssl x509 -req -in $CTF_CSR_NAME -CA $CA_CRT_NAME -CAkey $CA_KEY_NAME -CAcreateserial -out $CTF_CRT_NAME -extensions req_ext -extfile $CTF_CNF_NAME
# openssl x509 -text -in $CTF_CRT_NAME -noout

echo "Certificates generated. Cleaning up CSR files..."
rm $CLA_CSR_NAME
rm $CTF_CSR_NAME

echo "Copying CA cert and to CTF"
cp $CA_CRT_NAME $CTF_DIR
echo "Copying CA cert and to CLA"
cp $CA_CRT_NAME $CLA_DIR

if [ ! -d $(pwd)"/sandbox" ]; then
  echo $(pwd)"/sandbox not found..."
  echo "creating"$(pwd)"/sandbox"
  mkdir $(pwd)"/sandbox"
fi
echo "Copying CA cert and to sandbox"
cp $CA_CRT_NAME $(pwd)"/sandbox"

