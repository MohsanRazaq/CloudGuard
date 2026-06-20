import json


def load_data():
    with open("mock_data/s3_buckets.json", "r") as f:
        return json.load(f)


def list_buckets():
    buckets = load_data()

    print("\n=== S3 Buckets ===")
    for bucket in buckets:
        print(bucket["name"])

    return buckets


if __name__ == "__main__":
    list_buckets()