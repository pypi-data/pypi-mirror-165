import os
from tracing import Trace,TraceInstruments


PROJECT_REGION = os.getenv('PROJECT_REGION', 'southamerica-east1')
tracer = Trace('INTERNAL').get_tracer()

TraceInstruments.start_requests_instrumentation()