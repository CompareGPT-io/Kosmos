"""
Analysis Agent Module

Implements Algorithm 5: ANALYSIS_STEP (CIAS-Discovery)
Computes Pareto frontiers, calibration statistics, and trend summaries.
"""

from typing import List, Set, Dict, Tuple, Any
from collections import defaultdict
from .data_structures import WorldModel, ExperimentRecord


class AnalysisAgent:
    """
    CIAS-Discovery analysis agent.

    Responsible for:
    - Computing multi-objective Pareto frontiers
    - Calculating calibration statistics
    - Summarizing design trends in natural language
    - Identifying promising configurations
    """

    @staticmethod
    def compute_pareto_front(experiments: List[ExperimentRecord], 
                            objectives: List[str] = ['psnr', 'coverage']) -> Set[str]:
        """
        Compute Pareto frontier for multi-objective optimization.

        A configuration is Pareto-optimal if no other configuration
        dominates it (i.e., is better in all objectives).

        Assumes all objectives are to be maximized.

        Args:
            experiments: List of experiment records
            objectives: List of objective metric names to optimize

        Returns:
            Set of experiment IDs on the Pareto frontier
        """
        if not experiments:
            return set()

        pareto_set = set()

        for exp1 in experiments:
            is_dominated = False
            metrics1 = exp1.metrics

            for exp2 in experiments:
                if exp1.id == exp2.id:
                    continue

                metrics2 = exp2.metrics

                # Check if exp1 is dominated by exp2
                # exp2 dominates exp1 if:
                # - exp2 is >= exp1 on all objectives, AND
                # - exp2 is strictly > exp1 on at least one objective
                dominates = True
                strictly_better_in_one = False

                for obj in objectives:
                    val1 = getattr(metrics1, obj, 0)
                    val2 = getattr(metrics2, obj, 0)

                    if val2 < val1:  # Assuming maximization
                        dominates = False
                        break
                    if val2 > val1:
                        strictly_better_in_one = True

                if dominates and strictly_better_in_one:
                    is_dominated = True
                    break

            if not is_dominated:
                pareto_set.add(exp1.id)

        return pareto_set

    @staticmethod
    def compute_calibration_stats(experiments: List[ExperimentRecord]) -> Dict[str, float]:
        """
        Compute calibration statistics for UQ schemes.

        Args:
            experiments: List of experiment records

        Returns:
            Dictionary with mean, max, and min calibration errors
        """
        calib_errors = [
            exp.metrics.calibration_error 
            for exp in experiments 
            if exp.metrics.calibration_error is not None
        ]

        if not calib_errors:
            return {"mean_error": 0.0, "max_error": 0.0}

        return {
            "mean_error": sum(calib_errors) / len(calib_errors),
            "max_error": max(calib_errors),
            "min_error": min(calib_errors)
        }

    @staticmethod
    def summarize_trends(experiments: List[ExperimentRecord], 
                        pareto_ids: Set[str],
                        calib_stats: Dict[str, float]) -> str:
        """
        Summarize design patterns and trends in natural language.

        Args:
            experiments: List of experiment records in this stratum
            pareto_ids: Set of Pareto-optimal experiment IDs
            calib_stats: Calibration statistics

        Returns:
            Natural language summary string
        """
        pareto_exps = [e for e in experiments if e.id in pareto_ids]

        if not pareto_exps:
            return "No significant trends found."

        avg_psnr = sum(e.metrics.psnr for e in pareto_exps) / len(pareto_exps)
        best_config = max(pareto_exps, key=lambda e: e.metrics.psnr)

        summary = f"Pareto frontier contains {len(pareto_exps)} configurations. "
        summary += f"Average PSNR: {avg_psnr:.2f} dB. "
        summary += f"Best config uses {best_config.config.recon_family}, "
        summary += f"PSNR={best_config.metrics.psnr:.2f} dB. "

        if calib_stats["mean_error"] > 0:
            summary += f"Average calibration error: {calib_stats['mean_error']:.3f}."

        return summary

    @staticmethod
    def analysis_step(world_model: WorldModel) -> Tuple[Set[str], List[str]]:
        """
        Algorithm 5: ANALYSIS_STEP

        Analyzes the world model to compute Pareto frontiers and trends.
        Groups experiments by strata (e.g., recon_family × uq_scheme),
        computes Pareto frontiers and calibration stats for each stratum,
        and generates natural language summaries.

        Args:
            world_model: Current world model

        Returns:
            Tuple of (all Pareto-optimal IDs, list of trend summaries)
        """
        all_experiments = world_model.get_all_experiments()

        # Group experiments by strata (simplified: recon_family × uq_scheme)
        strata = defaultdict(list)
        for exp in all_experiments:
            key = (exp.config.recon_family, exp.config.uq_scheme)
            strata[key].append(exp)

        pareto_set_all = set()
        trends_all = []

        for stratum_key, exps_in_stratum in strata.items():
            # Compute Pareto frontier for this stratum
            pareto_ids = AnalysisAgent.compute_pareto_front(
                exps_in_stratum, 
                objectives=['psnr', 'coverage']
            )
            pareto_set_all.update(pareto_ids)

            # Compute calibration statistics
            calib_stats = AnalysisAgent.compute_calibration_stats(exps_in_stratum)

            # Summarize trends
            trend_summary = AnalysisAgent.summarize_trends(
                exps_in_stratum, 
                pareto_ids, 
                calib_stats
            )
            trends_all.append(f"[{stratum_key}] {trend_summary}")

        return pareto_set_all, trends_all
