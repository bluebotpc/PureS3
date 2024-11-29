# Goobs Linode Object Storage GUI

Created for my personal use.

Requires an ```.env.prod``` file in the repo. It will requre a Linode API/PAT key as seen in the example below.

```txt
LINODE_API_KEY=
REGION=
BUCKET_NAME=
```

## Windows

- Clone the repo
- Setup Virtual Environment ```python3 -m venv venv```
- Activate the new Virtual Environment

**Wiindows:** ```.\venv\Scripts\activate```

**MacOS/Linux:** ```source venv/bin/activate```

- Install the dependencies ```pip install -r requirements.txt```
- Run GoobsS3_GUI.py ```python app.py```
- Exit the virtual environment. ```deactivate```
- Remove leftover data. ```rm -rf venv```
