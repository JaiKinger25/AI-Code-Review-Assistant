import subprocess


def run_radon(filepath):
    try:
        result = subprocess.run(
            [
                "radon",
                "cc",
                filepath,
                "-s",
                "-j"
            ],
            capture_output=True,
            text=True
        )

        return {
            "success": True,
            "report": result.stdout,
            "errors": result.stderr
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }