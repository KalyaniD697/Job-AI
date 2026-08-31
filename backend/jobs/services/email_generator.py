import os
import json
import requests


class EmailGeneratorService:

    OPENROUTER_URL = (
        "https://openrouter.ai/api/v1/chat/completions"
    )

    def __init__(self):

        self.api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is not configured"
            )

    def generate_email(
        self,
        job,
        candidate
    ):

        prompt = f"""
You are a professional job application
email writer.

Create a concise, professional and
personalized job application email.

JOB INFORMATION

Job title:
{job.get("title", "")}

Company:
{job.get("company", "")}

Location:
{job.get("location", "")}

Experience:
{job.get("experience", "")}

Skills:
{job.get("skills", [])}

Description:
{job.get("description", "")}

Requirements:
{job.get("requirements", [])}


CANDIDATE INFORMATION

Candidate name:
{candidate.get("name", "")}

Candidate skills:
{candidate.get("skills", [])}

Candidate experience:
{candidate.get("experience", "")}


CONTACT INFORMATION

Contact name:
{job.get("contact_name", "")}

Contact email:
{job.get("contact_email", "")}


INSTRUCTIONS

1. Write a professional application email.

2. Keep it concise.

3. Personalize it for the specific job.

4. Mention relevant candidate skills.

5. Do not invent experience.

6. Do not invent projects.

7. Do not invent achievements.

8. If contact name is empty, use
   "Dear Hiring Team".

9. Do not include an email address
   in the body unless it was provided.

10. Return ONLY valid JSON.

Required format:

{{
    "subject": "",
    "body": ""
}}
"""

        response = requests.post(
            self.OPENROUTER_URL,
            headers={
                "Authorization": (
                    f"Bearer {self.api_key}"
                ),
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.4
            },
            timeout=60
        )

        if not response.ok:

            raise Exception(
                f"OpenRouter API error: "
                f"{response.status_code} - "
                f"{response.text}"
            )

        data = response.json()

        content = data[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]

        return self._parse_json(content)

    @staticmethod
    def _parse_json(content):

        content = content.strip()

        if content.startswith("```"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            )

            content = content.strip()

        return json.loads(content)