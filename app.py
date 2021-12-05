#!/usr/bin/env python3
import os

import aws_cdk as cdk

from revlet_reviewservice.revlet_reviewservice_stack import RevletReviewserviceStack


app = cdk.App()
RevletReviewserviceStack(app, "RevletReviewserviceStack")

app.synth()
