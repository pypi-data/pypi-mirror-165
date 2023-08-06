import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider, Tracer
from opentelemetry.semconv.resource import CloudProviderValues
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import CLOUD_PROVIDER,CLOUD_REGION,SERVICE_NAME, Resource
from opentelemetry.trace import NonRecordingSpan

# Instruments Imports
from opentelemetry.instrumentation.urllib import URLLibInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


ENV = os.getenv('ENVIRONMENT', 'dev')
PROJECT_REGION = os.getenv('FUNCTION_REGION')
FUNCTION_NAME = os.getenv('FUNCTION_NAME')
OTEL_EXPORTER_ENDPOINT = os.getenv('OTEL_EXPORTER_ENDPOINT', '')
OTEL_EXPORTER_HEADERS_AUTH = os.getenv('OTEL_EXPORTER_HEADERS_AUTH', '')


class Trace:
    def __init__(self, service_name: str) -> None:
        resource = Resource.create(attributes={
            SERVICE_NAME: service_name,
            'deployment.environment': ENV,
            CLOUD_PROVIDER: CloudProviderValues.GCP.value,
            CLOUD_REGION: PROJECT_REGION
        })

        provider = TracerProvider(resource=resource)

        if ENV == 'dev':
            processor = BatchSpanProcessor(ConsoleSpanExporter())
        else:
            processor = BatchSpanProcessor(
                OTLPSpanExporter(
                    endpoint=OTEL_EXPORTER_ENDPOINT,
                    headers={
                        'authorization': OTEL_EXPORTER_HEADERS_AUTH
                    }
                )
            )

        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

        self.tracer = trace.get_tracer(service_name)

    def get_tracer(self) -> Tracer:
        return self.tracer

    def get_current_span(self):
        return trace.get_current_span()

    def set_span_in_context(self, ctx):
        return trace.set_span_in_context(NonRecordingSpan(ctx))

class TraceInstruments:
    @staticmethod
    def start_requests_instrumentation():
        RequestsInstrumentor().instrument()

    @staticmethod
    def start_urllib_instrumentation():
        URLLibInstrumentor().instrument()