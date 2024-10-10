"""
Dagger module to manage the lifecycle of a Shadeform VM. Handy for integration in data-science pipelines or in 
any DAG graph when one or more tasks can benefit from the execution on a GPU machine. See examples for a demonstration
on how to use it
"""

__all__ = ["shadeform"]

# Import the submodules
from . import shadeform 

