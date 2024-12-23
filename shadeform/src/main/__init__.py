"""
Dagger module to manage the lifecycle of a Shadeform VM. Handy for integration in data-science pipelines or in any DAG graph when one or more tasks can benefit from the execution on a GPU machine. See examples for a demonstration on how to use it
"""

from .main import Shadeform as Shadeform
