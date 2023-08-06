ZFunds-Services
-----------------
Sahi. Asaan


## Development Setup
### System Dependency

* Python 3.10.2
* poetry

### Step 
1) Clone the repo 
2) cd zfunds-services
3) poetry install
4) poetry shell

Start developing

## Package zfunds-services
python version must be 3.10.2 or higher

### Build

python setup.py build

### Distribute
python setup.py sdist

### Upload 
twine upload dist/*

### Python Dependency
* pymongo
* dynamodb
* s3



### Use 
It wil load environment variable automatically, so all you need to do is make sure these environment variables are present. 
It will also autoload .env ( example .env.dist , rename it to .env) file before running, so you can also put these variables in your .env file. 

Needed Environment variables are 

```
# Application
APP_NAME=redisconnection
LOG_LEVEL=DEBUG
ENVIRONMENT=staging
REGION=ind

# 



```
from redisconnection import redis_connection
rc = redis_connection.RedisConnection()
conn = rc.connection

```




