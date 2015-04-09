PySQSd
====

Python based SQS consumer


## Installation


- Install python 2.7 and [pip](http://www.pythoncentral.io/how-to-install-virtualenv-python/)
- Setup a virtualenv

	`$ virtualvenv venv`
	
- Activate the virtualenv

	`$ source venv/bin/activate`
	
-  install dependencies

	`(venv)$ pip install`
	
## Environement

- AWS_ACCESS_KEY_ID
- AWS_SECRET_KEY
- SQS_QUEUE: Queue name (not an URL)

Optional:

- SQS_REGION: (defaut to 'us-east-1')
- WORKER_HOST: (default to 'localhost:5000')
- WORKER_PATH: (default to '/' )
- SQS_READ_TIMEOUT: (default to None)
- SQS_SLEEP: (time to sleep between messages, default 3)

## run

	`(venv)$ python application.py`
	
## How it works:

When a new message is available, PySQSd will issue a **POST** request to the **WORKER_HOST** at the **WORKER_PATH**.

The request body will be the message body.

The request will contain the following headers:

	"Content-type": "application/json"
	"Accept": "text/plain"
	"User-Agent": "aws-sqspyd"
	"X-Aws-Sqsd-Msgid": // Message id
	"X-Aws-Sqsd-Queue": SQS_QUEUE
	"X-Aws-Sqsd-Sent-At": // SentTimestamp as ISO-8601
	"X-Aws-Sqsd-First-Received-At": // ApproximateFirstReceiveTimestamp as ISO-8601
	"X-Aws-Sqsd-First-Sender-Id": // SenderId
	"X-Aws-Sqsd-Receive-Count": // message ApproximateReceiveCount
	"X-Aws-Sqsd-Receipt-Handle": // receipt handle 
	"X-Aws-Sqsd-Message-Timeout": // Read timeout


The ISO-8601 format is : 
	
	'%Y-%m-%d %H:%M:%S'

Additionnaly Number and String message_attributes are parsed and added to the header list:
	
Depending the data_type attribute, the string_value is parsed to String, float or int

	"X-aws-sqsd-attr-(attribute_key)" = attribute_value
 


