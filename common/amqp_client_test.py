from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://hilhtjts:H48lD7TxF_1DQdcZhBOsOvFpmgJOmwQW@otter.rmq.cloudamqp.com/hilhtjts"

QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

    sentMsg = {'test':'test'}
    client.sendMessage(sentMsg)

    receivedMsg = client.getMessage()

    assert sentMsg == receivedMsg

    print('test_basic passed')

if __name__ == "__main__":
    test_basic()