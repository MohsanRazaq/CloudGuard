from cloudguard.aws.session import create_session


def list_buckets():
    session= create_session()
    s3=session.client('s3')
    response = s3.list_buckets()

    return [bucket["Name"] for bucket in response["Buckets"]]


if __name__ == "__main__":
    print(list_buckets())