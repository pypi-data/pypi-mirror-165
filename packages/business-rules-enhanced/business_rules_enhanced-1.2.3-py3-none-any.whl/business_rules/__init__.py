__version__ = '1.2.3'

from .engine import run_all
from .utils import export_rule_data

# Appease pyflakes by "using" these exports
assert run_all
assert export_rule_data
