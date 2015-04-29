
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

    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
    SQS_QUEUE = os.environ['SQS_QUEUE']
    SQS_REGION = os.environ['SQS_REGION'] if 'SQS_REGION' in os.environ else 'us-east-1'
    SQS_READ_TIMEOUT = os.environ['SQS_READ_TIMEOUT'] if 'SQS_READ_TIMEOUT' in os.environ else None
    WORKER_HOST = os.environ['WORKER_HOST'] if 'WORKER_HOST' in os.environ else 'localhost:5000'
    WORKER_PATH = os.environ['WORKER_PATH'] if 'WORKER_PATH' in os.environ else '/'
    SQS_SLEEP = os.environ['SQS_SLEEP'] if 'SQS_SLEEP' in os.environ else 5

    sqs_connection = boto.sqs.connect_to_region(
         SQS_REGION,
         aws_access_key_id=AWS_ACCESS_KEY,
         aws_secret_access_key=AWS_SECRET_KEY)
    q = sqs_connection.get_queue(SQS_QUEUE)
    visibility_timeout = q.get_timeout() if SQS_READ_TIMEOUT == None else SQS_READ_TIMEOUT
    logger.info("started")
    while True and q:
        # set 30 seconds of inavailability
        conn = httplib.HTTPConnection(WORKER_HOST)
        rs = sqs_connection.receive_message(q, visibility_timeout=SQS_READ_TIMEOUT,attributes=['All'], message_attributes=['All'])
        if len(rs) == 1:
            m = rs[0]
            # import pprint
            # for property, value in vars(m).iteritems():
            #     print property, ": ", value
            body = m.get_body()
            logger.info(WORKER_PATH)
            logger.info(body)
            sent_at = m.attributes['SentTimestamp']
            first_recieved = m.attributes['ApproximateFirstReceiveTimestamp']

            sent_at = datetime.datetime.fromtimestamp(float(int(sent_at)/1000)).strftime('%Y-%m-%d %H:%M:%S')
            first_recieved = datetime.datetime.fromtimestamp(float(int(first_recieved)/1000)).strftime('%Y-%m-%d %H:%M:%S')
            # Get the response
            try:
                logger.info("Received message "+m.id)

                # Default python server port
                headers = { "Content-type": "application/json", 
                        "Accept": "text/plain",
                        "User-Agent": "aws-sqspyd",
                        "X-Aws-Sqsd-Msgid": m.id,
                        "X-Aws-Sqsd-Queue": SQS_QUEUE,
                        "X-Aws-Sqsd-Sent-At": sent_at,
                        "X-Aws-Sqsd-First-Received-At": first_recieved,
                        "X-Aws-Sqsd-Receive-Count": m.attributes['ApproximateReceiveCount'],
                        "X-Aws-Sqsd-Receipt-Handle": m.receipt_handle,
                        "X-Aws-Sqsd-Message-Timeout": visibility_timeout,
                        "X-Aws-Sqsd-Sender-Id": m.attributes['SenderId'],
                        }

                for key in m.message_attributes:
                    value = m.message_attributes[key]
                    header_name = "X-aws-sqsd-attr-"+key
                    if header_name not in headers:
                        string_value = value["string_value"]
                        data_type = value["data_type"]
                        value = None
                        if "String" in data_type:
                            value = string_value
                        elif "Number" in data_type:
                            # parse as a number
                            try:
                                value = float(string_value)
                                value = int(string_value)
                            except:
                                pass
                        if value:
                            headers[header_name] = value
                        else:
                            logger.info("Unable to parse message attribute "+key)
                    else:
                        logger.info("Skipping message attribute "+key+" as header is already set")
                # Post to local server
                conn.request("POST", WORKER_PATH, body, headers)
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
                time.sleep(float(SQS_SLEEP))

if __name__ == '__main__':
    main()

