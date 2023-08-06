from aws_client import AWSClient, AWSCommandParams

def test_push():
    aws_params:AWSCommandParams = AWSCommandParams(account=462223625310, zone='us-east-1')
    client:AWSClient = AWSClient(aws_params)
    client.push_image_to_ecr(source_image='the_tag:latest', repository='runfalcon-test-repository')
