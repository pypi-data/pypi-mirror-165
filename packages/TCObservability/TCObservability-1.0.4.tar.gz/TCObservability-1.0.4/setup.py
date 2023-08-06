from setuptools import setup

setup(
    name = 'TCObservability',
    version = '1.0.4',
    author = 'Maycon Guimaraes',
    author_email = 'maycon.guimaraes@tc.com.br',
    packages = ['TCObservability'],
    install_requires = [
        "opentelemetry_sdk-1.12.0==1.12.0",
        "opentelemetry-exporter-otlp==1.12.0",
        "opentelemetry-instrumentation-urllib==0.33b0",
        "opentelemetry-instrumentation-requests==0.33b0"

    ],
    description='A lib to easily add observality to Google cloud functions'
)
