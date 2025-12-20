"""
World Model Manager Module

Implements Algorithm 2: WORLD_MODEL_UPDATE
Manages the repository of all experiment results and maintains index structures.
"""

import uuid
from typing import Dict, Any
from .data_structures import WorldModel, Configuration, Metrics, Artifacts, ExperimentRecord


class WorldModelManager:
    """
    Manager for the world model.

    Responsible for:
    - Adding new experiments to the world model
    - Maintaining index structures for efficient lookup
    - Updating experiment metadata
    """

    @staticmethod
    def update(world_model: WorldModel, 
               config: Configuration, 
               metrics: Metrics, 
               artifacts: Artifacts) -> WorldModel:
        """
        Algorithm 2: WORLD_MODEL_UPDATE

        Updates the world model by adding a new experiment record.
        Maintains index structures for fast retrieval by configuration attributes.

        Args:
            world_model: Current world model
            config: Experiment configuration
            metrics: Performance metrics
            artifacts: Experiment artifacts

        Returns:
            Updated world model
        """
        # Create new experiment record
        experiment = ExperimentRecord(
            id=str(uuid.uuid4()),
            config=config,
            metrics=metrics,
            artifacts=artifacts
        )

        # Add to world model
        world_model.experiments.append(experiment)

        # Update index structures for fast lookup
        world_model.indices['recon_family'].append(
            (config.recon_family, experiment.id)
        )
        world_model.indices['uq_scheme'].append(
            (config.uq_scheme, experiment.id)
        )

        return world_model
