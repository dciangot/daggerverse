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
    "aweris": {
        "name": "Ali AKCA",
        "job": "Freelancer / Consultant",
        "year": 2024,
        "description": """
Ali’s passion for Dagger and eagerness to share his knowledge with others is infectious. Since joining the Dagger community,
he’s always been quick to test new features and provide valuable feedback to improve the experience for everyone.
        """,
        "says": "Get involved with the Dagger community. There are amazing people who can help you succeed."
    },
    "developerguy": {
        "name": "Batuhan Apaydın",
        "job": "Platform Engineer, Trendyol",
        "year": 2024,
        "description": """
Batuhan has essentially launched his own Dagger roadshow across Turkey, spreading the word about Dagger at various conferences.
He’s made numerous contributions to the Daggerverse, improving workflows and driving innovation.
        """,
        "says": "Keep calm and Dagger!"
    },
    "emmzw": {
        "name": "Emmanuel Sibanda",
        "job": "Founder/Software Engineer, AdAlchemyAI",
        "year": 2024,
        "description": """
Emmanuel takes highly technical concepts and breaks them down in a way that anyone can understand, demonstrating innovative Dagger use cases.
He has used Dagger to automate an AI-driven financial pipeline, showcasing its flexibility beyond CI.
        """,
        "says": "The more you use Dagger, the more you appreciate its value."
    },
    "jice_": {
        "name": "Jean-Christophe Sirot",
        "job": "Staff Engineer, Decathlon",
        "year": 2024,
        "description": """
Jean-Christophe is actively bringing the experimental Java SDK to life and contributing to the community with valuable insights and help.
        """,
        "says": "Experiment with simple projects, read the documentation, and don’t hesitate to ask questions on Discord."
    },
    "siafu7795": {
        "name": "Kambui Nurse",
        "job": "Staff Engineer Innovation, Marsh McLennan",
        "year": 2024,
        "description": """
Kambui is pushing Dagger’s boundaries in AI-driven workflows and has garnered praise from the community for his in-depth demos.
        """,
        "says": "Dream big—you can do anything with it!"
    },
    "kjuulh": {
        "name": "Kasper Hermansen",
        "job": "Platform Engineer, Lunar",
        "year": 2024,
        "description": """
Kasper is a Rust enthusiast who is building an entire platform on top of Dagger, sharing his expertise and feedback generously with the community.
        """,
        "says": "Start simple. Dagger has excellent quickstarts on building sample code projects."
    },
    "sagikazarmark": {
        "name": "Márk Sági-Kazár",
        "job": "Head of OSS, OpenMeter",
        "year": 2024,
        "description": """
Mark has been a vocal member of the Dagger community and a champion of Code>YAML, sharing experiences of integrating Dagger at OpenMeter.
        """,
        "says": "Go through the quickstart. Then grab a Dockerfile of yours and try to rewrite it to Dagger."
    },
    "mangocrysis": {
        "name": "Nipuna Perera",
        "job": "Director of Cloud Engineering, Fidelity Investments",
        "year": 2024,
        "description": """
Nipuna is tackling challenging corporate use cases with Dagger and providing invaluable feedback to improve Dagger in enterprise environments.
        """,
        "says": "Join the Discord server. Start by creating a simple Dagger module to solve a problem you have today."
    },
    "nfr_ribeiro": {
        "name": "Nuno Ribeiro",
        "job": "DevOps Engineer, Cleva Solutions",
        "year": 2024,
        "description": """
Nuno envisions a future where pipelines are managed programmatically. He actively shares his experiences with Dagger in the Portugal tech community.
        """,
        "says": "If you run into a problem, join the Discord community and share the issues you’re facing."
    },
    "delegate_": {
        "name": "Patrick Magee",
        "job": "Engineering Lead, LexisNexis Risk Solutions",
        "year": 2024,
        "description": """
Patrick has been an enthusiastic contributor to the Dagger community, especially for Windows OS users, and frequently participates in community calls.
        """,
        "says": "Embrace Dagger’s programmable approach to CI/CD to fully understand its flexibility."
    },
    "pauldragoonis": {
        "name": "Paul Dragoonis",
        "job": "CTO, ByteHire",
        "year": 2024,
        "description": """
Paul is the force behind the experimental PHP SDK for Dagger and is passionate about showcasing the benefits of Dagger to the PHP community.
        """,
        "says": "Burn your YAML. Build more code."
    },
    "peterj": {
        "name": "Peter Jausovec",
        "job": "Senior Principal Platform Advocate, solo.io",
        "year": 2024,
        "description": """
Peter has provided valuable feedback to improve Dagger’s developer experience and built a Dagger module for Envoy Proxy.
        """,
        "says": "Take one of your existing scripts, refer to the Dagger docs, and convert it into Dagger functions."
    },
    "wingyplus": {
        "name": "Thanabodee Charoenpiriyakij",
        "job": "Software Engineer, LINE Company",
        "year": 2024,
        "description": """
Thanabodee created the experimental Elixir SDK and is exploring using Dagger for managing Kubernetes configurations with modules.
        """,
        "says": "Pick up the SDK for your favorite language and experiment with existing use cases."
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
