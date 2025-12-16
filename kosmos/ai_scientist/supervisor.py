"""
Main Entry Point

Example usage of the CIAS-X AI Scientist Loop framework.
Demonstrates how to configure and run automated scientific discovery.
"""

from kosmos.ai_scientist.scientist_loop import AIScientistLoop
from kosmos.ai_scientist.data_structures import Configuration


def create_design_space():
    """
    Define the design space for SCI experiments.

    Returns:
        Dictionary defining valid configuration options
    """
    return _load_sample_json("design_space_template.json")


def create_initial_configs():
    """
    Create initial seed configurations (human-designed baselines).

    Returns:
        List of initial Configuration objects
    """
    return [Configuration(**config_dict) for config_dict in _load_sample_json("seed_config.json")]


def analyze_results(pareto_set, world_model):
    """
    Analyze and print final results.

    Args:
        pareto_set: Set of Pareto-optimal experiment IDs
        world_model: Final world model with all experiments
    """
    print("\n" + "=" * 60)
    print("Final Results Analysis")
    print("=" * 60)

    print(f"\nPareto frontier configurations: {len(pareto_set)}")

    # Find best configuration on Pareto frontier
    pareto_experiments = [e for e in world_model.experiments if e.id in pareto_set]
    if pareto_experiments:
        best_exp = max(pareto_experiments, key=lambda e: e.metrics.psnr)
        print(f"\nBest configuration:")
        print(f"  Reconstruction family: {best_exp.config.recon_family}")
        print(f"  UQ scheme: {best_exp.config.uq_scheme}")
        print(f"  PSNR: {best_exp.metrics.psnr:.2f} dB")
        print(f"  Coverage: {best_exp.metrics.coverage:.2%}")
        print(f"  Latency: {best_exp.metrics.latency:.1f} ms")

    # Overall statistics
    all_psnr = [e.metrics.psnr for e in world_model.experiments]
    all_coverage = [e.metrics.coverage for e in world_model.experiments]
    print(f"\nOverall statistics:")
    print(f"  PSNR range: {min(all_psnr):.2f} - {max(all_psnr):.2f} dB")
    print(f"  Average PSNR: {sum(all_psnr)/len(all_psnr):.2f} dB")
    print(f"  Average coverage: {sum(all_coverage)/len(all_coverage):.2%}")

    # Performance by reconstruction family
    print(f"\nPerformance by reconstruction family:")
    from collections import defaultdict
    family_stats = defaultdict(list)
    for exp in world_model.experiments:
        family_stats[exp.config.recon_family].append(exp.metrics.psnr)

    for family, psnrs in family_stats.items():
        print(f"  {family}: Avg PSNR = {sum(psnrs)/len(psnrs):.2f} dB ({len(psnrs)} experiments)")


def start():
    """
    Main execution function.

    Sets up and runs the CIAS-X AI Scientist Loop,
    then analyzes and displays results.
    """
    print("CIAS-X AI Scientist Loop - Automated Scientific Discovery")
    print("=" * 60)

    # Configuration
    design_space = create_design_space()
    initial_configs = create_initial_configs()
    budget_max = 10  # Maximum number of experiments

    print(f"\nConfiguration:")
    print(f"  Design space: {len(design_space['recon_families'])} recon families, "
          f"{len(design_space['uq_schemes'])} UQ schemes")
    print(f"  Initial configs: {len(initial_configs)}")
    print(f"  Budget: {budget_max} experiments")

    # Create and run AI Scientist
    ai_scientist = AIScientistLoop(
        design_space=design_space,
        initial_configs=initial_configs,
        budget_max=budget_max
    )

    # Execute main loop
    pareto_set, world_model = ai_scientist.run()

    # Analyze results
    analyze_results(pareto_set, world_model)

def _load_sample_json(name: str):
    import json
    import os

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "data", name)

    with open(json_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    start()
