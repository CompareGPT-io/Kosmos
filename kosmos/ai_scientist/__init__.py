"""
CIAS-X AI Scientist Loop Framework
A modular implementation of automated scientific discovery for SCI.

Author: Auto-generated
Date: 2025-12-16
"""

__version__ = "1.0.0"

from .data_structures import Configuration, Metrics, Artifacts, ExperimentRecord, WorldModel
from .world_model import WorldModelManager
from .executor import Executor
from .analysis import AnalysisAgent
from .planner import Planner
from .scientist_loop import AIScientistLoop

__all__ = [
    "Configuration",
    "Metrics", 
    "Artifacts",
    "ExperimentRecord",
    "WorldModel",
    "WorldModelManager",
    "Executor",
    "AnalysisAgent",
    "Planner",
    "AIScientistLoop",
]
