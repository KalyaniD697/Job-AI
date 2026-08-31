import os
import json
import requests


class JobAnalyzer:

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

    def analyze_job(self, job,role,location,experience):

        prompt = f"""
You are a job information extraction system and job relevance analysis system.
The user is searching for a job with the following criteria:
User's requested role: {role}
User's requested location: {location}
User's requested experience: {experience}
Analyze the following job search result.

Extract ONLY information that can reasonably
be determined from the provided title and snippet.

Never invent information.
Determine whether the job is relevant to the user's requested role, location, and experience.
Return ONLY valid JSON.

Required format:

{{
    "title": "",
    "company": "",
    "location": "",
    "experience": "",
    "skills": [],
    "description": "",
    "requirements": [],
    "contact_name": "",
    "contact_email": "",
    "application_url": "",
    "is_relevant": true,
    "match_score": 0.0,
    "match_reason": ""
}}

Job title:
{job.get("title", "")}

Search result snippet:
{job.get("snippet", "")}

Job URL:
{job.get("url", "")}

Source:
{job.get("source", "")}
"""

        response = requests.post(
            self.OPENROUTER_URL,
            headers={
                "Authorization": (
                    f"Bearer {self.api_key}"
                ),
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1
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

        content = data["choices"][0]["message"]["content"]

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