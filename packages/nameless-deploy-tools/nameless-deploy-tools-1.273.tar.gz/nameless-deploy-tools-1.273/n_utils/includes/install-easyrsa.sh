source $(n-include common_tools.sh)

EASYRSA_VERSION=3.0.8
add_gpg_key C8FCA3E7F787072CDEB91D2F72964219390D0D0E
gpg_safe_download "https://github.com/OpenVPN/easy-rsa/releases/download/v$EASYRSA_VERSION/EasyRSA-$EASYRSA_VERSION.tgz" easy-rsa.tgz
mkdir -p /tmp/openvpn/easy-rsa
tar -xzvf easy-rsa.tgz --strip-components=1 --directory /tmp/openvpn/easy-rsa
rm -f easy-rsa.tgz.sig easy-rsa.tgz
cd /tmp/openvpn/easy-rsa/ || return
echo "set_var EASYRSA_ALGO ec" >vars
# Generate a random, alphanumeric identifier of 16 characters for CN and one for server name
SERVER_CN="cn_$(head /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)"
echo "$SERVER_CN" >SERVER_CN_GENERATED
SERVER_NAME="server_$(head /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)"
echo "$SERVER_NAME" >SERVER_NAME_GENERATED

echo "set_var EASYRSA_REQ_CN $SERVER_CN" >>vars

# Create the PKI, set up the CA, the DH params and the server certificate
./easyrsa init-pki
./easyrsa --batch build-ca nopass

./easyrsa build-server-full "$SERVER_NAME" nopass
EASYRSA_CRL_DAYS=3650 ./easyrsa gen-crl

# Generate tls-crypt key
openvpn --genkey --secret /tmp/openvpn/tls-crypt.key
