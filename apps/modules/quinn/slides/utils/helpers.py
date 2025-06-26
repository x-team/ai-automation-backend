from typing import Any


def get_hierarchical_question_structure(
    structured_questions_file_content: list[dict[str, Any]],
) -> dict[str, dict[str, str]]:
    """Hierarchical question structure."""

    id_to_question_map = {
        row.get("ID"): row.get("Question")
        for row in structured_questions_file_content
        if row.get("ID") and row.get("Question")
    }

    hierarchical_questions: dict[str, dict[str, str]] = {}
    for row in structured_questions_file_content:
        question_text = row["Question"]
        depends_on_column_id = row["If Question ID"]
        depends_on_column_value = row["Equal To"]

        if question_text and depends_on_column_id and depends_on_column_value:

            depends_on_question_text = id_to_question_map.get(depends_on_column_id)

            if depends_on_question_text:
                hierarchical_questions[question_text] = {
                    "dependsOn": depends_on_question_text,
                    "value": str(
                        depends_on_column_value,
                    ).lower(),
                }

    return hierarchical_questions
