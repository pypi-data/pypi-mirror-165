from aws_cdk.core import App

from b_cfn_api_v2_test.integration.infrastructure.main_stack import MainStack

app = App()
MainStack(app)
app.synth()
