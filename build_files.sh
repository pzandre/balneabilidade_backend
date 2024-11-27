 echo "BUILD START"
 python3.12 -m pip install -r requirements.txt
 echo "$POSTGRES_SSLROOTCERT" | base64 --decode > cert.crt
 echo "BUILD END"
