from aws_cdk import (
    # Duration,
    Stack,
    aws_apigateway,
    aws_ecr,
    aws_lambda,
    aws_dynamodb,
)
from constructs import Construct


class RevletReviewserviceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        reviews_table = aws_dynamodb.Table(
            self,
            "revlet-reviews",
            partition_key=aws_dynamodb.Attribute(
                name="ReviewId", type=aws_dynamodb.AttributeType.STRING
            ),
        )

        repo = aws_ecr.Repository(self, "revlet.reviewservice")
        fn = aws_lambda.DockerImageFunction(
            self,
            "revlet-reviewservice-get",
            code=aws_lambda.DockerImageCode.from_ecr(repo),
        )
        api = aws_apigateway.LambdaRestApi(
            self,
            "revlet-reviewservice-api",
            handler=fn,
            proxy=False,
        )
        reviewsResource = api.root.add_resource("reviews")
        reviewsResource.add_method("GET")
