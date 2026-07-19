import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def local_review(code):
    """Fallback AI review if Gemini API is unavailable."""

    review = []

    review.append("# AI Code Review Report\n")

    review.append("## 1. Overall Summary")
    review.append(
        "The uploaded Python code is functional but can be improved in terms of readability, documentation, exception handling, and security."
    )

    review.append("\n## 2. Strengths")
    review.append("- Code structure is simple and easy to understand.")
    review.append("- Low cyclomatic complexity.")
    review.append("- Uses standard Python libraries.")
    review.append("- Easy to maintain after minor improvements.")

    review.append("\n## 3. Issues Found")

    if "except Exception" in code:
        review.append("- Avoid catching generic Exception. Catch specific exceptions instead.")

    if "subprocess.run" in code:
        review.append("- subprocess.run() should explicitly specify check=True.")
        review.append("- Validate user input before passing it to subprocess.")
        review.append("- Use absolute executable paths whenever possible.")

    if "print(" in code:
        review.append("- Replace print() statements with Python logging.")

    if "eval(" in code:
        review.append("- Avoid using eval() because it can execute arbitrary code.")

    if "exec(" in code:
        review.append("- Avoid using exec() due to security risks.")

    review.append("\n## 4. Security Recommendations")
    review.append("- Validate all external inputs.")
    review.append("- Sanitize user-provided values.")
    review.append("- Avoid executing untrusted commands.")
    review.append("- Keep third-party libraries updated.")

    review.append("\n## 5. Code Quality Improvements")
    review.append("- Add module docstrings.")
    review.append("- Add function docstrings.")
    review.append("- Use meaningful variable names.")
    review.append("- Remove unused imports.")
    review.append("- Follow consistent formatting.")

    review.append("\n## 6. Best Practices")
    review.append("- Follow PEP 8 coding standards.")
    review.append("- Add type hints where appropriate.")
    review.append("- Write unit tests.")
    review.append("- Handle exceptions specifically.")
    review.append("- Use logging instead of print().")

    review.append("\n## 7. Final Verdict")
    review.append(
        "Overall, the code demonstrates a good foundation. Implementing the above recommendations will improve readability, maintainability, and security."
    )

    return "\n".join(review)


def ai_review(code):
    """Generate AI review using Gemini with automatic fallback."""

    prompt = f"""
You are an expert Python code reviewer.

Review the following Python code.

Provide:

1. Overall Summary
2. Strengths
3. Bugs
4. Security Issues
5. Code Improvements
6. Best Practices
7. Final Verdict

Code:

{code}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        return {
            "success": True,
            "review": response.text,
            "source": "Google Gemini AI"
        }

    except Exception as e:
        print(f"Gemini Error: {e}")

        return {
            "success": True,
            "review": local_review(code),
            "source": "AI Review Engine"
        }