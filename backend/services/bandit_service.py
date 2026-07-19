import subprocess
import json


def run_bandit(filepath):
    try:
        result = subprocess.run(
            [
                "bandit",
                "-f",
                "json",
                filepath
            ],
            capture_output=True,
            text=True
        )

        if result.stdout:
            return json.loads(result.stdout)

        return {
            "results": [],
            "errors": result.stderr
        }

    except Exception as e:
        return {
            "error": str(e)
        }