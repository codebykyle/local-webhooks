# SQS Passthrough Client

This will download SQS events and publish them to a local website. 

#  Quick Start

Copy the .env.example file to .env

`cp .env.example .env`

Fill out the fields in the .env file

`nano .env`



### Windows:
Install venv:
```
py -m pip install --user virtualenv
```

Create a virtualenv and install requirements.txt
```
py -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

Run the script
```
consume_sqs.py
```

### Linux/Mac
Install venv:
```
python3 -m pip install --user virtualenv
```

Create a virtualenv and install requirements.txt
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
chmod +x consume_sqs.py
```


It requires the following environment variables:
```
DESTINATION_URL=
SQS_QUEUE=
POLL_DELAY=1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
```


### Run the script
```
consume_sqs.py
```
