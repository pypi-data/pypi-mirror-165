#!/usr/bin/env python3

if __name__ == "__main__":
    import aws_cdk as cdk
    from src.demo_app_stack import DemoAppStack

    app = cdk.App()
    DemoAppStack(app, "demo-app", env={"region": "eu-west-2"})

    app.synth()
