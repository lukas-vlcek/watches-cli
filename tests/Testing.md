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