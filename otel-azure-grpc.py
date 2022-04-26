import os

from azure.mgmt.compute import ComputeManagementClient
from azure.identity import AzureCliCredential

from azure.core.settings import settings
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource, SERVICE_VERSION, DEPLOYMENT_ENVIRONMENT
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter, BatchSpanProcessor

# Change this with appropriate values
SUBSCRIPTION_ID=os.environ['SUBSCRIPTION_ID']
RESOURCE_GROUP=os.environ['RESOURCE_GROUP']
VM_NAME=os.environ['VM_NAME']

# Init OTEL
resource = Resource(attributes={
  SERVICE_NAME: "otel-azure-grpc",
  SERVICE_VERSION: "1.0.0",
  DEPLOYMENT_ENVIRONMENT: "dev"
})

# Change Azure SDK Tracing Implementation
settings.tracing_implementation = OpenTelemetrySpan

# Configure OTEL Exporter and Processor

#exporter = ConsoleSpanExporter()
exporter = OTLPSpanExporter()
trace.set_tracer_provider(TracerProvider(resource=resource))
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(exporter)
)   

# Get tracer
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span(name="otel-azure-grpc"):
  # Needs az CLI
  credential = AzureCliCredential()
  
  # Creates compute client 
  compute_client = ComputeManagementClient(
    subscription_id=SUBSCRIPTION_ID,
    credential=credential
  )
  
  # Retrieves VM
  vm = compute_client.virtual_machines.get(
    resource_group_name=RESOURCE_GROUP,
    vm_name=VM_NAME
  )

