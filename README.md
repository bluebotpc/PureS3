# PureS3 Tool

Created to reduce dependacy on Linode's Cloud Manager web interface.

Requires an ```.env``` file in the repo. It will requre a Linode API/PAT key as seen in the example below.

```txt
LINODE_API_KEY=
REGION=
BUCKET_NAME=
LINODE_API_VERSION=v4
```

## Wiindows Project Setup

```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

CTRL+C to break. ```deactivate``` to clean up.

### Linux Project Setup

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 ./app.py
```

CTRL+C to break. ```deactivate``` to clean up.
