"""
Data Structures Module

Defines core data structures for the CIAS-X framework:
- Configuration: Experiment configuration
- Metrics: Performance metrics
- Artifacts: Experiment outputs
- ExperimentRecord: Complete experiment record
- WorldModel: Repository of all experiments
"""

import uuid
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from collections import defaultdict


@dataclass
class Configuration:
    """
    Experiment configuration for SCI reconstruction.

    Attributes:
        forward_config: Forward model configuration (compression, masks, etc.)
        recon_family: Reconstruction architecture family ("CIAS-Core", "CIAS-Core-ELP", etc.)
        recon_params: Architecture-specific parameters (layers, hidden dims, etc.)
        uq_scheme: Uncertainty quantification scheme ("Conformal", "Ensemble", "None")
        uq_params: UQ-specific parameters
        train_config: Training hyperparameters (epochs, lr, batch size, etc.)
    """
    forward_config: Dict[str, Any]
    recon_family: str
    recon_params: Dict[str, Any]
    uq_scheme: str
    uq_params: Dict[str, Any]
    train_config: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)


@dataclass
class Metrics:
    """
    Performance metrics for an experiment.

    Attributes:
        psnr: Peak Signal-to-Noise Ratio (dB)
        coverage: Uncertainty coverage probability
        latency: Inference latency (ms)
        calibration_error: Calibration error for UQ (optional)
        other_metrics: Additional custom metrics
    """
    psnr: float
    coverage: float
    latency: float
    calibration_error: Optional[float] = None
    other_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class Artifacts:
    """
    Experiment artifacts (saved outputs).

    Attributes:
        checkpoint: Model checkpoint path
        uq_params: Fitted UQ parameters
        train_log: Training log path
        eval_samples: Sample reconstruction paths
        fig_scripts: Figure generation scripts
    """
    checkpoint: str
    uq_params: Dict[str, Any]
    train_log: str
    eval_samples: List[str]
    fig_scripts: List[str]


@dataclass
class ExperimentRecord:
    """
    Complete record of a single experiment.

    Attributes:
        id: Unique experiment identifier
        config: Experiment configuration
        metrics: Performance metrics
        artifacts: Saved artifacts
        timestamp: Execution timestamp
    """
    id: str
    config: Configuration
    metrics: Metrics
    artifacts: Artifacts
    timestamp: str = ""

    def __post_init__(self):
        """Generate UUID if id is not provided."""
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class WorldModel:
    """
    World model storing all experiment history.

    The world model maintains:
    - Complete list of all experiments
    - Index structures for fast lookup by config attributes

    Attributes:
        experiments: List of all experiment records
        indices: Index structures (recon_family, uq_scheme, etc.)
    """
    experiments: List[ExperimentRecord] = field(default_factory=list)
    indices: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))

    def get_all_experiments(self) -> List[ExperimentRecord]:
        """Return all experiments in the world model."""
        return self.experiments
