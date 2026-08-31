import os
import requests


class JobSearchService:

    SEARCH_URL = "https://google.serper.dev/search"

    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "SERPER_API_KEY is not configured"
            )

    def search_jobs(
        self,
        role,
        location,
        experience=None
    ):

        queries = self._build_queries(
            role,
            location,
            experience
        )

        all_results = []

        for query in queries:

            results = self._search(query)

            all_results.extend(results)

        return self._remove_duplicates(
            all_results
        )

    def _build_queries(
        self,
        role,
        location,
        experience
    ):

        experience_text = (
            experience
            if experience
            else ""
        )

        return [

            f'"{role}" "{location}" '
            f'"{experience_text}" "apply"',

            f'"{role}" "{location}" '
            f'"{experience_text}" "job opening"',

            f'"{role}" "{location}" '
            f'"{experience_text}" "hiring"',

            f'"{role}" "{location}" '
            f'"{experience_text}" "job at"',
        ]
    def _search(self, query):

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query,
            "num": 10
        }

        response = requests.post(
            self.SEARCH_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        if not response.ok:

            raise Exception(
                f"Serper API error: "
                f"{response.status_code} - "
                f"{response.text}"
            )

        data = response.json()

        return self._format_results(
            data
        )

    def _format_results(self, data):

        results = []

        for item in data.get(
            "organic",
            []
        ):

            results.append(
                {
                    "title": item.get(
                        "title",
                        ""
                    ),

                    "url": item.get(
                        "link",
                        ""
                    ),

                    "snippet": item.get(
                        "snippet",
                        ""
                    ),

                    "source": self._extract_domain(
                        item.get(
                            "link",
                            ""
                        )
                    )
                }
            )

        return results

    @staticmethod
    def _extract_domain(url):

        if not url:
            return ""

        url = url.replace(
            "https://",
            ""
        )

        url = url.replace(
            "http://",
            ""
        )

        return url.split("/")[0]

    def _is_likely_job_page(self, result):

        title = result.get("title", "").lower()
        url = result.get("url", "").lower()
        snippet = result.get("snippet", "").lower()

        # Obvious job listing/search pages
        listing_indicators = [
            "jobs in",
            "job search",
            "job openings",
            "job vacancies",
            "jobs available",
            "fresher jobs",
            "jobs for freshers",
            "search?",
            "/jobs?",
            "/jobs-in-",
            "/search?",
        ]

        for indicator in listing_indicators:

            if indicator in title:
                return False

            if indicator in url:
                return False

        # Strong indicators that this is an individual job
        individual_indicators = [
            "job-listings",
            "/job/",
            "/jobs/",
            "apply to",
            "apply now",
            "job at",
        ]

        for indicator in individual_indicators:

            if indicator in url or indicator in snippet:
                return True

        return False

    def _remove_duplicates(self, results):

        seen = set()

        unique_results = []

        for result in results:

            url = result.get("url", "")

            if not url:
                continue

            if url in seen:
                continue

            seen.add(url)

            if self._is_likely_job_page(result):

                unique_results.append(result)

        return unique_results[:20]