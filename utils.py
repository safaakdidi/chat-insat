import uuid
from datetime import datetime,timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives.asymmetric import padding

import ipaddress

def createPrivateKey():
    key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
    )
    return key


def extractPublicKey(prvkey):
    return prvkey.public_key()


def createAutoSignedCert(server_IP,h_name):
    key=createPrivateKey()
    name = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, h_name)
    ])

    alt_name=[x509.DNSName(h_name)]
    alt_name.append(x509.DNSName(server_IP))
    alt_name.append(x509.IPAddress(ipaddress.ip_address(server_IP)))
    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    now = datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(1000)
        .not_valid_before(now)
        .not_valid_after(now+timedelta(days=365))
        .add_extension(basic_contraints, True)
        .add_extension(x509.SubjectAlternativeName(alt_name), False)
        .sign(key, hashes.SHA256(), default_backend())
    )
    my_cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    my_key_pem=key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open('CA/CA.cert', 'wb') as c:
        c.write(my_cert_pem)

    with open('CA/CA.key', 'wb') as c:
        c.write(my_key_pem)

def createCertRequest(siteName,country,state,local,orgName,email,certout,privateKeyout):
    private_key = createPrivateKey()
    builder = x509.CertificateSigningRequestBuilder()
    builder = builder.subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, siteName),
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, local),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME,orgName),
            x509.NameAttribute(NameOID.EMAIL_ADDRESS,email)

        ])
    )
    builder= builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    )
    request=builder.sign(
        private_key,hashes.SHA256(), default_backend()
    )
    with open(certout, 'wb') as c:
        c.write(request.public_bytes(encoding=serialization.Encoding.PEM))

    with open(privateKeyout, 'wb') as c:
        c.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    return request

def createCert(certout):
    pem_csr = open(certout, 'rb').read()
    cert = x509.load_pem_x509_csr(pem_csr,default_backend())
    pem_cert = open('CA/CA.cert', 'rb').read()
    ca = x509.load_pem_x509_certificate(pem_cert,default_backend())
    pem_key = open('CA/CA.key', 'rb').read()
    ca_key = serialization.load_pem_private_key(pem_key,password=None, backend=default_backend())



    builder=x509.CertificateBuilder()
    builder = builder.subject_name(cert.subject)
    builder = builder.issuer_name(ca.subject)
    builder = builder.not_valid_before(datetime.now()-timedelta(7))
    builder = builder.not_valid_after(datetime.now()+timedelta(365))
    builder = builder.public_key(cert.public_key())
    builder = builder.serial_number(int(uuid.uuid4()))
    for ext in cert.extensions:
        builder = builder.add_extension(ext.value,ext.critical)


    #sign the cert
    certificate=builder.sign(
        private_key=ca_key,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )
    with open(certout, 'wb') as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))



def verifyCert(certpath):
    # load the certificate
    cert_data = open(certpath, "rb").read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
    # load the CA certificate
    ca_data = open("CA/CA.cert", "rb").read()
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ca_data)
    # load the CA certificate

    issuer = cert.get_issuer()

    # Print the issuer's distinguished name (DN)
    print(issuer)

    issuerc = ca_cert.get_issuer()


    # Print the issuer's distinguished name (DN)
    print(issuerc)

    # print(cert.issuer)
    # # check the expiration date
    # if cert.not_valid_before < datetime.now() < cert.not_valid_after:
    #     print("The certificate is valid")
    # else:
    #     print("The certificate is expired")
    #     return False



    try:
        store = crypto.X509Store()
        print(type(store))
        store.add_cert(cert)
        store.add_cert(ca_cert)

        print(store)

        # Create a certificate context using the store and the downloaded certificate
        store_ctx = crypto.X509StoreContext(store, cert)
        print('psssssssst')

        # Verify the certificate, returns None if it can validate the certificate
        store_ctx.verify_certificate()

        return True

    except Exception as e:
        print(e)
        print('faaaaaalseee')
        return False

def write_keys_to_file(private_key):
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


    private_key_file = open("private_key.pem", "w")
    private_key_file.write(pem_private_key.decode())
    private_key_file.close()

    public_key_file = open("pub.pem_key", "w")
    public_key_file.write(pem_public_key.decode())
    public_key_file.close()

def serialize_key(public_key):
    public_key_data = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_data

def desrialize_key(public_key_data):
    public_key = serialization.load_pem_public_key(public_key_data)
    return public_key

def encrypt_message(public_key , message) :
    message = message.encode()
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_message(private_key , ciphertext):
    try:
        #test to see if the entered text is encrypted or not
        #if it can be decoded then it's not encrypted
        #if it throws an exception then it's encrypted and needs decryption
        ciphertext.decode('utf-8')
        return ciphertext.decode('utf-8')
    except:
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode()

def sign_message(private_key , message ):
    message = message.encode()
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return(signature)

def verify_signature(public_key , signature, message):
    return (public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    ))
