# How to run tests

Tests are executed against **secured Elasticsearch cluster** running on `https://localhost:9200`.
For securing Elasticsearch we use [Search Guard 2](https://github.com/floragunncom/search-guard/)
plugins configured according to its tutorials. For the convenience we provide
a simple script that can handle installation of SG plugins, generating required
certificates, starting Elasticsearch search and configuring SG plugins as needed
by tests (read below for details). 

## Travis CI

CI testing is all set up and running on Travis via [travis.yml](`../.travis.yml`)
 and [sg_init.sh](setup/sg_init.sh) scripts automatically so you do not need
 to worry about anything.
 
## Testing manually

Before you can execute tests you need to make sure that you can run Elasticsearch
locally with all the needed security plugins. You can use
provided [sg_init.sh](setup/sg_init.sh) script to configure Elasticsearch for the tests.

Before you run this script make sure that:

  - Elasticsearch of required version is installed on
your machine
  - Setup `ES_HOME` env variable and point it to home folder of Elasticsearch
  - Elasticsearch is stopped and SG plugins **ARE NOT** installed
  - Elasticsearch data folder (`path.data`) should be empty too 
  
For example, assume you want to use `Elasticsearch 2.4.1` for testing and it
 is installed in folder `/home/elasticsearch-2.4.1`:
 
    # Make sure ES_HOME is set correctly
    export ES_HOME=/home/elasticsearch-2.4.1
        
    # First we clear all SG plugins, data and logs
    $ cd $ES_HOME
    $ rm -rf data/ plugins/ logs/
    
Then switch to `watches-cli` root folder and run init script:

    $ cd <watches-cli.git.CLONE>_HOME
    ./tests/setup/sg_init.sh
    
This script will install SG plugins, generate certificates, start Elasticsearch
node and configure SG plugins as needed. When the script finishes you should be able
to execute the following command:

    curl -sS -u kirk:kirk 'https://localhost:9200/_cluster/health?pretty'
    
If you get correct response then this means you have successfully executed request to
  secured Elasticsearch as an admin user called kirk.
  
Now you can run all `watches` tests by calling:

    $ python setup.py test
    
## cURL with OpenSSL on MacOS

If you are a MacOS user you might run into the following error when running cURL command
with provided certs:

    curl -vs 'https://localhost:9200/_cluster/health?pretty' \
      --cacert /tmp/search-guard-ssl/example-pki-scripts/ca/chain-ca.pem \
      --cert /tmp/search-guard-ssl/example-pki-scripts/kirk.crt.pem \
      --key /tmp/search-guard-ssl/example-pki-scripts/kirk.key.pem
    *   Trying ::1...
    * Connected to localhost (::1) port 9200 (#0)
    * WARNING: SSL: CURLOPT_SSLKEY is ignored by Secure Transport. The private key must be in the Keychain.
    * WARNING: SSL: Certificate type not set, assuming PKCS#12 format.
    * SSL: Can't load the certificate "/tmp/search-guard-ssl/example-pki-scripts/kirk.crt.pem" and its private key: OSStatus -25299
    * Closing connection 0
    
In this case you are most likely running into [issue explained here](https://github.com/curl/curl/issues/283).
One of the solutions is to switch cURL from using SecureTransport:

    $ curl --version
    curl 7.49.1 (x86_64-apple-darwin16.0) libcurl/7.49.1 SecureTransport zlib/1.2.8
    Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
    Features: AsynchDNS IPv6 Largefile GSS-API Kerberos SPNEGO NTLM NTLM_WB SSL libz UnixSockets
    
to use openSSL instead (follow [this tip](https://github.com/curl/curl/issues/283#issuecomment-243398486) to make it happen):
 
    $ curl --version
    curl 7.49.1 (x86_64-apple-darwin16.1.0) libcurl/7.49.1 OpenSSL/1.0.2h zlib/1.2.8
    Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
    Features: IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP UnixSockets