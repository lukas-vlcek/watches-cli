#!/bin/bash

set -ex

# ----------------------------------------------
# This script installs Search Guard plugins, starts Elasticsearch and finishes
# initialization of Search Guard plugin. It needs to be executed only once. You
# can then shutdown Elasticsearch and start it again and all will be set as needed.
#
# The following env variables are set to enable smooth testing in Travis, you might
# want to tweak them accordingly if testing locally.
# ----------------------------------------------

export ES_VERSION=${ES_VERSION:-2.4.1}
export SG_VER=${SG_VER:-2.4.1.8}
export SG_SSL_VER=${SG_SSL_VER:-2.4.1.16}
export TMP_DIR=${TMP_DIR:-/tmp}
export ES_HOME=${ES_HOME:-$TMP_DIR/elasticsearch}
export ES_CONF=${ES_CONF:-./tests/conf}


# ----------------------------------------------
# Install SSL plugin
# See: <https://github.com/floragunncom/search-guard-ssl-docs/blob/master/installation.md>

[[ -d ${ES_HOME}/bin/plugin/search-guard-ssl ]] && rm -rf ${ES_HOME}/bin/plugin/search-guard-ssl
${ES_HOME}/bin/plugin install -b com.floragunn/search-guard-ssl/${SG_SSL_VER}

# ----------------------------------------------
# Follow Quickstart tutorial
# See: <https://github.com/floragunncom/search-guard-ssl-docs/blob/master/quickstart.md>
# Use PKI scripts: <https://github.com/floragunncom/search-guard-ssl-docs/blob/master/quickstart.md#using-the-example-pki-scripts>

ACTUAL_DIR=`pwd`
[[ -d ${TMP_DIR} ]] || mkdir ${TMP_DIR}
cd ${TMP_DIR}
[[ -d ${TMP_DIR}/search-guard-ssl ]] && rm -rf ${TMP_DIR}/search-guard-ssl
git clone https://github.com/floragunncom/search-guard-ssl.git
cd search-guard-ssl
git checkout v${SG_SSL_VER}
cd example-pki-scripts/
./example.sh
cd ${ACTUAL_DIR}

cp ${TMP_DIR}/search-guard-ssl/example-pki-scripts/truststore.jks ${ES_CONF}
cp ${TMP_DIR}/search-guard-ssl/example-pki-scripts/node-0-keystore.jks ${ES_CONF}

# ----------------------------------------------
# Install Search Guard plugin
# See: <https://github.com/floragunncom/search-guard/#installation>

[[ -d ${ES_HOME}/bin/plugin/search-guard-2 ]] && rm -rf ${ES_HOME}/bin/plugin/search-guard-2
${ES_HOME}/bin/plugin install -b com.floragunn/search-guard-2/${SG_VER}

# ----------------------------------------------
# Start elasticsearch
${ES_HOME}/bin/elasticsearch -d --security.manager.enabled=false --path.conf=./tests/conf/
sleep 15
tail ${ES_HOME}/logs/elasticsearch.log

# ----------------------------------------------
# Make sure sgadmin tool is executable
cd ${ES_HOME}/plugins/search-guard-2/tools
chmod u+x *.sh
cp ${TMP_DIR}/search-guard-ssl/example-pki-scripts/node-0-keystore.jks ${ES_HOME}/plugins/search-guard-2/sgconfig
cp ${TMP_DIR}/search-guard-ssl/example-pki-scripts/truststore.jks ${ES_HOME}/plugins/search-guard-2/sgconfig

cd ${ES_HOME}
plugins/search-guard-2/tools/sgadmin.sh \
  -cd plugins/search-guard-2/sgconfig/ \
  -ks plugins/search-guard-2/sgconfig/node-0-keystore.jks \
  -ts plugins/search-guard-2/sgconfig/truststore.jks \
  -nhnv

# plugins/search-guard-2/tools/hash.sh -p mycleartextpassword

cd ${ACTUAL_DIR}

# ----------------------------------------------
# Make some curl requests to ES node.
# See: <https://github.com/floragunncom/search-guard/blob/master/demo/searchguard_init.sh>

# User kirk is an admin.
curl -sS --insecure -u kirk:kirk 'https://localhost:9200/'
curl -sS --insecure -u kirk:kirk 'https://localhost:9200/_searchguard/sslinfo?pretty'
curl -sS --insecure -u kirk:kirk 'https://localhost:9200/_cluster/health?pretty'

curl -vs -u kirk:kirk 'https://localhost:9200/_cluster/health?pretty' \
  --cacert ${TMP_DIR}/search-guard-ssl/example-pki-scripts/ca/chain-ca.pem

curl -vs 'https://localhost:9200/_cluster/health?pretty' \
  --cacert ${TMP_DIR}/search-guard-ssl/example-pki-scripts/ca/chain-ca.pem \
  --cert ${TMP_DIR}/search-guard-ssl/example-pki-scripts/kirk.crt.pem \
  --key  ${TMP_DIR}/search-guard-ssl/example-pki-scripts/kirk.key.pem

# User spock is NOT an admin
curl -sS --insecure -u kirk:kirk 'https://localhost:9200/'
# This request should be rejected (403)
curl -sS --insecure -u spock:spock 'https://localhost:9200/_cluster/health?pretty'
