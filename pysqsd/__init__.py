
#logging.basicConfig(filename="sqs.log", level=logging.DEBUG)

def main():
    import os
    import httplib
    import logging
    import datetime
    import time
    import sys
    import boto.sqs

    logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    SQS_QUEUE = os.environ['SQS_QUEUE'];
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
    S3_REGION = 'us-east-1'
    SQS_QUEUE_TIMEOUT = 30
    WORKER_HOST = os.environ['WORKER_HOST'] if 'WORKER_HOST' in os.environ else 'localhost:5000'
    conn = boto.sqs.connect_to_region(
         S3_REGION,
         aws_access_key_id=AWS_ACCESS_KEY,
         aws_secret_access_key=AWS_SECRET_KEY)
    q = conn.get_queue(SQS_QUEUE)
    logger.info("started")
    while True and q:
        # set 30 seconds of inavailability
        conn = httplib.HTTPConnection(WORKER_HOST)
        m = q.read(SQS_QUEUE_TIMEOUT)
        if m:
            # import pprint
            # for property, value in vars(m).iteritems():
            #     print property, ": ", value
            body = m.get_body()
            # Get the response
            try:
                logger.info("Received message "+m.id)
                # Default python server port
                headers = { "Content-type": "application/json", 
                        "Accept": "text/plain",
                        "User-Agent": "aws-sqspyd",
                        "X-Aws-Sqsd-Msgid": m.id,
                        "X-Aws-Sqsd-Queue": SQS_QUEUE,
                        "X-Aws-Sqsd-First-Received-At": str(datetime.datetime.utcnow()),
                        "X-Aws-Sqsd-Receive-Count": len(m),
                        "X-Aws-Sqsd-Receipt-Handle": m.receipt_handle,
                        "X-Aws-Sqsd-Message-Timeout": SQS_QUEUE_TIMEOUT,
                        }
                # Post to local server
                conn.request("POST", "/", body, headers)
                response = conn.getresponse()
            # The server retuns a 200, we can delete
                logger.info('Response status '+`response.status`)
                if response.status == 200:
                    q.delete_message(m)
                    logger.info('Deleted message '+m.id)
                else:
                    m.change_visibility(0)
                    logger.error(`response.status`+":"+`response.reason`)
            except:
                m.change_visibility(0)
                logger.error("Connection closed abruptly")
                time.sleep(5000)

if __name__ == '__main__':
    main()

