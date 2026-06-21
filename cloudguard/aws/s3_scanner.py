from cloudguard.aws.session import create_session


def list_buckets():
    s3 = create_session()

    response = s3.list_buckets()

    return [bucket["Name"] for bucket in response["Buckets"]]


if __name__ == "__main__":
    print(list_buckets())