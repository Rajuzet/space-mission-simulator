
#!/usr/bin/env python3
"""
Core_ai.py

Integration layer that ties together:
- core_ai.planner_agent.PlannerAgent
- core_ai.executor_agent.ExecutorAgent
- core_ai.validator_agent.ValidatorAgent
- core_ai.orchestrator.Orchestrator (optional)

If available, can call into space_ai.orbital_ai.plan_mission to generate mission specs.
Provides CoreAI.run_mission(...) and a small CLI.
"""

from __future__ import annotations

import argparse
import json
import logging
from typing import Any, Dict, Optional

# Import the package components. Adjust names if your implementations differ.
try:
    from core_ai.planner_agent import PlannerAgent
    from core_ai.executor_agent import ExecutorAgent
    from core_ai.validator_agent import ValidatorAgent
    from core_ai.orchestrator import Orchestrator
except Exception as exc:  # pragma: no cover - top-level import helper
    raise ImportError(
        "Failed to import core_ai package modules. Ensure core_ai package is available "
        "and the module names match: planner_agent, executor_agent, validator_agent, orchestrator."
    ) from exc

# Optional domain-specific mission generator
try:
    from space_ai.orbital_ai.plan_mission import generate_mission_spec as orbital_generate
except Exception:
    orbital_generate = None  # type: ignore

logger = logging.getLogger("core_ai")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


class CoreAI:
    """
    High level orchestration class to run a mission.

    Components may be passed in (useful for tests or custom implementations),
    otherwise defaults are instantiated.
    """

    def __init__(
        self,
        planner: Optional[PlannerAgent] = None,
        executor: Optional[ExecutorAgent] = None,
        validator: Optional[ValidatorAgent] = None,
        orchestrator: Optional[Orchestrator] = None,
    ) -> None:
        self.planner = planner or PlannerAgent()
        self.executor = executor or ExecutorAgent()
        self.validator = validator or ValidatorAgent()
        self.orchestrator = orchestrator  # orchestrator is optional

    def run_mission(self, mission_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run end-to-end: plan -> (orchestrate/execute) -> validate.

        Returns a result dict with at least:
          - plan
          - execution_result
          - validation_result
          - success (bool)
        """
        logger.info("Starting mission run")
        result: Dict[str, Any] = {"mission_spec": mission_spec}

        # 1. Planning
        logger.info("Running planner_agent.plan()")
        plan = self.planner.plan(mission_spec)
        result["plan"] = plan
        logger.debug("Produced plan: %s", plan)

        # 2. Execution (either via orchestrator or direct executor)
        execution_result = None
        try:
            if self.orchestrator:
                logger.info("Using orchestrator to coordinate execution")
                execution_result = self.orchestrator.orchestrate(plan, self.executor)
            else:
                logger.info("Executing plan with executor_agent.execute()")
                execution_result = self.executor.execute(plan)
            result["execution_result"] = execution_result
            logger.debug("Execution result: %s", execution_result)
        except Exception as exc:
            logger.exception("Execution failed: %s", exc)
            result["execution_error"] = str(exc)
            result["success"] = False
            return result

        # 3. Validation
        logger.info("Validating execution result with validator_agent.validate()")
        try:
            validation_result = self.validator.validate(plan, execution_result)
            result["validation_result"] = validation_result
            result["success"] = bool(validation_result.get("passed", validation_result is True))
        except Exception as exc:
            logger.exception("Validation failed: %s", exc)
            result["validation_error"] = str(exc)
            result["success"] = False

        logger.info("Mission run complete: success=%s", result.get("success"))
        return result


def load_mission_spec_from_path(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a space mission via CoreAI components.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mission-file", "-f", help="Path to mission JSON file")
    group.add_argument(
        "--mission-json", "-j", help="Mission spec as JSON string (escape in your shell)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.mission_file:
        mission_spec = load_mission_spec_from_path(args.mission_file)
    else:
        try:
            mission_spec = json.loads(args.mission_json)
        except Exception as exc:
            logger.error("Failed to parse mission JSON string: %s", exc)
            return 2

    core = CoreAI()
    result = core.run_mission(mission_spec)

    # Print the results as JSON to stdout for easy consumption
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("success") else 1


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
