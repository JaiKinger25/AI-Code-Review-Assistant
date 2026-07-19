import subprocess

def run_pylint(filepath):
    try:
        result = subprocess.run(
            [
                "pylint",
                filepath,
                "--output-format=text"
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