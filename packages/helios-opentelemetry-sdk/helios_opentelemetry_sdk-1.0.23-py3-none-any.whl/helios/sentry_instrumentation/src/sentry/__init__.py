import os
import sentry_sdk

from logging import getLogger
from typing import Collection
from wrapt import wrap_function_wrapper

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap

from helios.defaults import DEFAULT_HS_API_ENDPOINT
from helios.sentry_instrumentation.src.sentry.package import _instruments
from helios.utils import encode_id_as_hex_string

HS_API_ENDPOINT = os.environ.get('HS_API_ENDPOINT') or DEFAULT_HS_API_ENDPOINT
_LOG = getLogger(__name__)


def _instrument():
    def wrap_capture_call(func, instance, args, kwargs):
        span = trace.get_current_span()

        if span and span.is_recording():
            trace_id = ''
            span_id = ''

            try:
                span_context = span.get_span_context()
                trace_id = encode_id_as_hex_string(span_context.trace_id)
                span_id = encode_id_as_hex_string(span_context.span_id, 8)
            except Exception as error:
                _LOG.debug('sentry instrumentation wrap_capture_call error: %s.', error)

            with sentry_sdk.push_scope() as scope:
                try:
                    scope.set_context('Helios', {'Trace visualization': f'{HS_API_ENDPOINT}&actionTraceId={trace_id}?spanId={span_id}&source=sentry'})
                    scope.set_tag('helios-trace-id', trace_id)
                except Exception as error:
                    _LOG.debug('sentry instrumentation wrap_capture_call error: %s.', error)

                return func(*args, **kwargs)

        return func(*args, **kwargs)

    wrap_function_wrapper('sentry_sdk', 'capture_event', wrap_capture_call)
    wrap_function_wrapper('sentry_sdk', 'capture_exception', wrap_capture_call)
    wrap_function_wrapper('sentry_sdk', 'capture_message', wrap_capture_call)


class SentrySdkInstrumentor(BaseInstrumentor):

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        _instrument()

    def _uninstrument(self, **kwargs):
        unwrap(sentry_sdk, 'capture_event')
        unwrap(sentry_sdk, 'capture_exception')
        unwrap(sentry_sdk, 'capture_message')
