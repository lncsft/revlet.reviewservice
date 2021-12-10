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

        api = aws_apigateway.RestApi(self, "revlet-reviews-api")
        reviewsResource = api.root.add_resource("reviews")

        repo = aws_ecr.Repository(self, "revlet.reviewservice")
        fn = aws_lambda.DockerImageFunction(
            self,
            "revlet-reviewservice-get",
            code=aws_lambda.DockerImageCode.from_ecr(
                repository=repo, cmd=["app.get_reviews"], tag="latest"
            ),
        )

        get_reviews_integration = aws_apigateway.LambdaIntegration(fn)
        reviewsResource.add_method("GET", get_reviews_integration)
