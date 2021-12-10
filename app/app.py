import boto3
from boto3.dynamodb.conditions import Key
import uuid
import json

DYNAMO_CLIENT = boto3.client("dynamodb", region_name="eu-west-2")
REVIEWS_TABLE = DYNAMO_CLIENT.Table("linsoft-reviews")
PROPERTIES_TABLE = DYNAMO_CLIENT.Table("linsoft-properties")


def get_reviews(event, context):
    if "id" in event:
        response = REVIEWS_TABLE.get_item(
            Key={"ReviewId": {"S": event["id"]}},
        )
    elif "propertyId" in event:
        response = REVIEWS_TABLE.query(
            KeyConditionExpression=Key("PropertyId").eq(event["propertyId"]),
        )
    else:
        response = REVIEWS_TABLE.scan()

    if "Item" in response:
        return get_lambda_response(200, json.dumps(response["Item"]))
    elif "Items" in response:
        return get_lambda_response(200, json.dumps(response["Items"]))

    return get_lambda_response(404, "No property found")


def post_review(event, context):
    data = json.loads(event["body"])
    reviewId = str(uuid.uuid4())

    # Validate the property exists
    property = PROPERTIES_TABLE.get_item(
        Key={"PropertyId": {"S": data["propertyId"]}},
    )
    if not "Item" in property:
        return get_lambda_response(400, "Property ID is invalid")

    response = REVIEWS_TABLE.put_item(
        Item={
            "ReviewId": {"S": reviewId},
            "PropertyId": {"S": data["propertyId"]},
            "Title": {"S": data["title"]},
            "Description": {"S": data["description"]},
        },
    )

    return get_lambda_response(200, json.dumps({"reviewId": response}))


def get_lambda_response(status=200, data="", isBase64=False, headers={}):
    return {
        "isBase64Encoded": isBase64,
        "statusCode": status,
        "headers": headers,
        "body": data,
    }
