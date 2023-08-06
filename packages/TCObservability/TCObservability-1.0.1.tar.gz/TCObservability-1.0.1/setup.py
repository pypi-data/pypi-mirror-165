from setuptools import setup

setup(
    name = 'TCObservability',
    version = '1.0.1',
    author = 'Maycon Guimaraes',
    author_email = 'maycon.guimaraes@tc.com.br',
    packages = ['TCObservability'],
    install_requires = [
        "Deprecated==1.2.13",
        "opentelemetry-api==1.12.0",
        "opentelemetry-instrumentation==0.33b0",
        "opentelemetry-instrumentation-requests==0.33b0",
        "opentelemetry-instrumentation-urllib==0.33b0",
        "opentelemetry-sdk==1.12.0",
        "opentelemetry-semantic-conventions==0.33b0",
        "opentelemetry-util-http==0.33b0",
        "TCObservability==1.0.0",
        "typing_extensions==4.3.0",
        "wrapt==1.14.1"
    ],
    description='A lib to easily add observality to Google cloud functions'
)
