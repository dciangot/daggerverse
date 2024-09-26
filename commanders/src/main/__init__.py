"""A generated module for Commanders functions

This module has been generated via dagger init and serves as a reference to
basic module structure as you get started with Dagger.

Two functions have been pre-created. You can modify, delete, or add to them,
as needed. They demonstrate usage of arguments and return types using simple
echo and grep commands. The functions can be called from the dagger CLI or
from one of the SDKs.

The first line in this comment block is a short description line and the
rest is a long description with more detail on the module's purpose or usage,
if appropriate. All modules should have a short description.
"""

# NOTE: it's recommended to move your code into other files in this package
# and keep __init__.py for imports only, according to Python's convention.
# The only requirement is that Dagger needs to be able to import a package
# called "main" (i.e., src/main/).
#
# For example, to import from src/main/main.py:
# >>> from .main import Commanders as Commanders

import dagger
from dagger import dag, function, object_type

commanders = {
    "dciangot": {
        "name": "Diego Ciangottini",
        "job": "Technologist at INFN",
        "year": 2024,
        "description": """
Calling all Data Scientists! If you’re a Data Scientist, or play one on TV, Diego is the Daggernaut you need to meet.
He bridges the gap between scientific communities and Dagger by sharing real-world examples through his live-streaming series.
As part of his Dagger exploration, Diego has also integrated an end-to-end test suite for Kubernetes using Dagger,
which has gotten rave reviews from the many Daggernauts seeking best practices with K8s.
        """,
        "says": "Start with simple CI/testing implementations, feel the power of it, and then extend to any workflow that makes sense to you."
    }
}

@object_type
class Commanders:
    @function
    def commander(self, username: str) -> str:
        """Returns a container that echoes whatever string argument is provided"""
        cmder = commanders[username]
        return f"\033[1;34m{cmder['name']} - {cmder['year']} Commander - {cmder['job']}\033[0m\n\033[0;32m{cmder['description']}\033[0m"

    @function
    def commander_says(self, username: str) -> str:
        """Returns a container that echoes whatever string argument is provided"""
        cmder = commanders[username]
        return f"\033[1;34m Commander {cmder['name']} always says: \033[0m\033[0;32m{cmder['says']}\033[0m"

    @function
    def list_commanders(self) -> str:
        """Returns a container that echoes whatever string argument is provided"""
        return f"{list(commanders.keys())}"
