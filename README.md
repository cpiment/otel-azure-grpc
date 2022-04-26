## otel-azure-grpc

Minimal implementation to reproduce issue [24189](https://github.com/Azure/azure-sdk-for-python/issues/24189)

# Steps to reproduce

Easiest way to reproduce it is from Azure Cloud Shell since it already has `az` installed and logged in, but it also can be reproduced in any machine with azcli installed. 

Clone this repository in Azure Cloud Shell and `cd` to it

```
$ python -m virtualenv venv
$ pip install -r requirements.txt
$ export SUBSCRIPTION_ID='your_subscription_id' # Get it from 'az account list'
$ export VM_NAME='name_of_a_VM' # Get this from the azure portal or 'az vm list' 
$ export RESOURCE_GROUP='resource_group_of_the_VM' 
$ python otel-azure-grpc.py
```

The result of those commands should be something like this:

```
E0426 15:59:53.243314495     372 fork_posix.cc:70]           Fork support is only compatible with the epoll1 and poll polling strategies
Exception while exporting Span batch.
Traceback (most recent call last):
  File "/home/carlos/azure-python/otel-azure-grpc/venv/lib/python3.7/site-packages/opentelemetry/sdk/trace/export/__init__.py", line 358, in _export_batch
    self.span_exporter.export(self.spans_list[:idx])  # type: ignore
  File "/home/carlos/azure-python/otel-azure-grpc/venv/lib/python3.7/site-packages/opentelemetry/exporter/otlp/proto/grpc/trace_exporter/__init__.py", line 291, in export
    return self._export(spans)
  File "/home/carlos/azure-python/otel-azure-grpc/venv/lib/python3.7/site-packages/opentelemetry/exporter/otlp/proto/grpc/exporter.py", line 293, in _export
    request=self._translate_data(data),
  File "/home/carlos/azure-python/otel-azure-grpc/venv/lib/python3.7/site-packages/opentelemetry/exporter/otlp/proto/grpc/trace_exporter/__init__.py", line 277, in _translate_data
    f"SPAN_KIND_{sdk_span.kind.name}",
AttributeError: 'NoneType' object has no attribute 'name'
```

See the [issue](https://github.com/Azure/azure-sdk-for-python/issues/24189) for more info
