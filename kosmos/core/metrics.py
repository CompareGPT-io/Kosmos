"""
Metrics collection for monitoring Kosmos performance.

Tracks:
- API calls and costs
- Experiment execution times
- Agent activity
- System health
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import logging


logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Collect and aggregate metrics.

    Thread-safe metrics collection with aggregation and export capabilities.

    Example:
        ```python
        from kosmos.core.metrics import get_metrics

        metrics = get_metrics()

        # Record API call
        metrics.record_api_call(
            model="claude-3-5-sonnet",
            input_tokens=100,
            output_tokens=50,
            duration_seconds=1.2
        )

        # Record experiment
        metrics.record_experiment(
            experiment_type="data_analysis",
            duration_seconds=30.5,
            status="success"
        )

        # Get statistics
        stats = metrics.get_statistics()
        print(stats["total_api_calls"])
        ```
    """

    def __init__(self):
        """Initialize metrics collector."""
        self._lock = threading.Lock()
        self.start_time = datetime.utcnow()

        # API metrics
        self.api_calls = 0
        self.api_errors = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_api_duration = 0.0
        self.api_call_history: List[Dict[str, Any]] = []

        # Experiment metrics
        self.experiments_started = 0
        self.experiments_completed = 0
        self.experiments_failed = 0
        self.total_experiment_duration = 0.0
        self.experiments_by_type = defaultdict(int)
        self.experiment_history: List[Dict[str, Any]] = []

        # Agent metrics
        self.agents_created = 0
        self.messages_sent = 0
        self.messages_received = 0
        self.agent_errors = 0

        # System metrics
        self.errors_encountered = 0
        self.warnings_logged = 0

        logger.info("Metrics collector initialized")

    # ========================================================================
    # API METRICS
    # ========================================================================

    def record_api_call(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        duration_seconds: float,
        success: bool = True
    ):
        """
        Record Claude API call.

        Args:
            model: Model used
            input_tokens: Input tokens
            output_tokens: Output tokens
            duration_seconds: Call duration
            success: Whether call succeeded
        """
        with self._lock:
            self.api_calls += 1
            if not success:
                self.api_errors += 1

            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.total_api_duration += duration_seconds

            # Store in history
            self.api_call_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "duration_seconds": duration_seconds,
                "success": success
            })

            # Keep history limited to last 1000 calls
            if len(self.api_call_history) > 1000:
                self.api_call_history.pop(0)

    def get_api_statistics(self) -> Dict[str, Any]:
        """
        Get API call statistics.

        Returns:
            dict: API statistics
        """
        with self._lock:
            avg_duration = (self.total_api_duration / self.api_calls
                          if self.api_calls > 0 else 0)
            error_rate = (self.api_errors / self.api_calls
                        if self.api_calls > 0 else 0)

            # Estimate cost (Claude 3.5 Sonnet pricing)
            input_cost = (self.total_input_tokens / 1_000_000) * 3.0
            output_cost = (self.total_output_tokens / 1_000_000) * 15.0
            total_cost = input_cost + output_cost

            return {
                "total_calls": self.api_calls,
                "successful_calls": self.api_calls - self.api_errors,
                "failed_calls": self.api_errors,
                "error_rate": error_rate,
                "total_input_tokens": self.total_input_tokens,
                "total_output_tokens": self.total_output_tokens,
                "total_tokens": self.total_input_tokens + self.total_output_tokens,
                "total_duration_seconds": self.total_api_duration,
                "average_duration_seconds": avg_duration,
                "estimated_cost_usd": total_cost,
            }

    # ========================================================================
    # EXPERIMENT METRICS
    # ========================================================================

    def record_experiment_start(self, experiment_id: str, experiment_type: str):
        """
        Record experiment start.

        Args:
            experiment_id: Unique experiment ID
            experiment_type: Type of experiment
        """
        with self._lock:
            self.experiments_started += 1
            self.experiments_by_type[experiment_type] += 1

            self.experiment_history.append({
                "experiment_id": experiment_id,
                "experiment_type": experiment_type,
                "status": "running",
                "start_time": datetime.utcnow().isoformat(),
                "end_time": None,
                "duration_seconds": None
            })

    def record_experiment_end(
        self,
        experiment_id: str,
        duration_seconds: float,
        status: str = "success"
    ):
        """
        Record experiment completion.

        Args:
            experiment_id: Experiment ID
            duration_seconds: Total duration
            status: Final status (success or failure)
        """
        with self._lock:
            if status == "success":
                self.experiments_completed += 1
            else:
                self.experiments_failed += 1

            self.total_experiment_duration += duration_seconds

            # Update history
            for exp in reversed(self.experiment_history):
                if exp["experiment_id"] == experiment_id:
                    exp["status"] = status
                    exp["end_time"] = datetime.utcnow().isoformat()
                    exp["duration_seconds"] = duration_seconds
                    break

            # Keep history limited
            if len(self.experiment_history) > 1000:
                self.experiment_history.pop(0)

    def get_experiment_statistics(self) -> Dict[str, Any]:
        """
        Get experiment statistics.

        Returns:
            dict: Experiment statistics
        """
        with self._lock:
            avg_duration = (self.total_experiment_duration / self.experiments_completed
                          if self.experiments_completed > 0 else 0)
            success_rate = (self.experiments_completed / self.experiments_started
                          if self.experiments_started > 0 else 0)

            return {
                "experiments_started": self.experiments_started,
                "experiments_completed": self.experiments_completed,
                "experiments_failed": self.experiments_failed,
                "experiments_running": self.experiments_started - self.experiments_completed - self.experiments_failed,
                "success_rate": success_rate,
                "total_duration_seconds": self.total_experiment_duration,
                "average_duration_seconds": avg_duration,
                "experiments_by_type": dict(self.experiments_by_type),
            }

    # ========================================================================
    # AGENT METRICS
    # ========================================================================

    def record_agent_created(self):
        """Record agent creation."""
        with self._lock:
            self.agents_created += 1

    def record_message_sent(self):
        """Record inter-agent message sent."""
        with self._lock:
            self.messages_sent += 1

    def record_message_received(self):
        """Record inter-agent message received."""
        with self._lock:
            self.messages_received += 1

    def record_agent_error(self):
        """Record agent error."""
        with self._lock:
            self.agent_errors += 1

    def get_agent_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics.

        Returns:
            dict: Agent statistics
        """
        with self._lock:
            return {
                "agents_created": self.agents_created,
                "messages_sent": self.messages_sent,
                "messages_received": self.messages_received,
                "agent_errors": self.agent_errors,
            }

    # ========================================================================
    # SYSTEM METRICS
    # ========================================================================

    def record_error(self):
        """Record system error."""
        with self._lock:
            self.errors_encountered += 1

    def record_warning(self):
        """Record warning."""
        with self._lock:
            self.warnings_logged += 1

    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Get system statistics.

        Returns:
            dict: System statistics
        """
        with self._lock:
            uptime = (datetime.utcnow() - self.start_time).total_seconds()

            return {
                "start_time": self.start_time.isoformat(),
                "uptime_seconds": uptime,
                "errors_encountered": self.errors_encountered,
                "warnings_logged": self.warnings_logged,
            }

    # ========================================================================
    # AGGREGATION
    # ========================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get all statistics.

        Returns:
            dict: Complete statistics
        """
        return {
            "system": self.get_system_statistics(),
            "api": self.get_api_statistics(),
            "experiments": self.get_experiment_statistics(),
            "agents": self.get_agent_statistics(),
        }

    def get_recent_activity(self, minutes: int = 60) -> Dict[str, Any]:
        """
        Get recent activity in last N minutes.

        Args:
            minutes: Number of minutes to look back

        Returns:
            dict: Recent activity summary
        """
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)

        with self._lock:
            # Recent API calls
            recent_api_calls = [
                call for call in self.api_call_history
                if datetime.fromisoformat(call["timestamp"]) > cutoff_time
            ]

            # Recent experiments
            recent_experiments = [
                exp for exp in self.experiment_history
                if datetime.fromisoformat(exp["start_time"]) > cutoff_time
            ]

            return {
                "time_window_minutes": minutes,
                "recent_api_calls": len(recent_api_calls),
                "recent_experiments": len(recent_experiments),
                "recent_experiments_completed": sum(
                    1 for exp in recent_experiments if exp["status"] == "success"
                ),
                "recent_experiments_failed": sum(
                    1 for exp in recent_experiments if exp["status"] == "failure"
                ),
            }

    def export_metrics(self) -> Dict[str, Any]:
        """
        Export all metrics for external monitoring.

        Returns:
            dict: Complete metrics dump
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "statistics": self.get_statistics(),
            "recent_activity": self.get_recent_activity(),
            "api_call_history": self.api_call_history[-100:],  # Last 100
            "experiment_history": self.experiment_history[-100:],  # Last 100
        }

    def reset(self):
        """Reset all metrics (useful for testing)."""
        with self._lock:
            self.__init__()


# Singleton metrics collector
_metrics: Optional[MetricsCollector] = None


def get_metrics(reset: bool = False) -> MetricsCollector:
    """
    Get or create metrics collector singleton.

    Args:
        reset: If True, create new collector instance

    Returns:
        MetricsCollector: Metrics collector instance
    """
    global _metrics
    if _metrics is None or reset:
        _metrics = MetricsCollector()
    return _metrics
