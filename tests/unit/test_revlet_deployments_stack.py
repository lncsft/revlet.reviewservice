import aws_cdk as core
import aws_cdk.assertions as assertions

from revlet_deployments.revlet_deployments_stack import RevletDeploymentsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in revlet_deployments/revlet_deployments_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RevletDeploymentsStack(app, "revlet-deployments")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
