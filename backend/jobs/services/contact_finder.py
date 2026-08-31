import os
import re
import requests


class ContactFinderService:

    def __init__(self):

        self.serper_api_key = os.getenv(
            "SERPER_API_KEY"
        )

        self.serper_url = "https://google.serper.dev/search"

        self.headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json",
        }


    def find_contacts(
        self,
        company,
        job_title="",
        location=""
    ):

        result = {
            "contact_name": None,
            "contact_email": None,
            "linkedin_url": None,
            "company_website": None,
            "contact_source": None,
            "confidence": 0.0,
        }


        if not company:
            return result


        if not self.serper_api_key:
            print("SERPER_API_KEY is missing")
            return result


        try:

            # ------------------------------------------------
            # Search company
            # ------------------------------------------------

            search_query = (
                f'"{company}" '
                f'"{location}" '
                f'contact email careers LinkedIn'
            )


            response = requests.post(
                self.serper_url,
                headers=self.headers,
                json={
                    "q": search_query,
                    "num": 10,
                },
                timeout=10,
            )


            response.raise_for_status()

            data = response.json()
            print("\n========== CONTACT SEARCH ==========")
            print("Company:", company)
            print("Search response:")
            print(data)
            print("====================================\n")

            results = data.get(
                "organic",
                []
            )

            print("Organic results count:", len(results))

            for item in results:
                print(
                    "TITLE:",
                    item.get("title"),
                    "\nLINK:",
                    item.get("link"),
                    "\nSNIPPET:",
                    item.get("snippet"),
                    "\n-------------------------"
                )
            # ------------------------------------------------
            # Analyze search results
            # ------------------------------------------------

            for item in results:

                title = item.get(
                    "title",
                    ""
                )

                link = item.get(
                    "link",
                    ""
                )

                snippet = item.get(
                    "snippet",
                    ""
                )


                text = (
                    title
                    + " "
                    + snippet
                )


                # --------------------------------------------
                # LinkedIn
                # --------------------------------------------

                if (
                    "linkedin.com/company"
                    in link.lower()
                    and not result["linkedin_url"]
                ):

                    result["linkedin_url"] = link


                # --------------------------------------------
                # Company website
                # --------------------------------------------

                if (
                    not result["company_website"]
                    and self._is_company_website(
                        link,
                        company
                    )
                ):

                    result["company_website"] = (
                        link
                    )


                # --------------------------------------------
                # Email
                # --------------------------------------------

                email = self._extract_email(
                    text
                )


                if (
                    email
                    and not result["contact_email"]
                ):

                    result["contact_email"] = (
                        email
                    )

                    result["contact_source"] = (
                        link
                    )

                    result["confidence"] = 0.8


            # ------------------------------------------------
            # Second search specifically for email
            # ------------------------------------------------

            if not result["contact_email"]:

                email_query = (
                    f'"{company}" '
                    f'email OR contact OR careers'
                )


                email_response = requests.post(
                    self.serper_url,
                    headers=self.headers,
                    json={
                        "q": email_query,
                        "num": 10,
                    },
                    timeout=10,
                )


                email_response.raise_for_status()

                email_data = (
                    email_response.json()
                )


                email_results = (
                    email_data.get(
                        "organic",
                        []
                    )
                )


                for item in email_results:

                    text = (
                        item.get(
                            "title",
                            ""
                        )
                        + " "
                        + item.get(
                            "snippet",
                            ""
                        )
                    )


                    email = self._extract_email(
                        text
                    )


                    if email:

                        result[
                            "contact_email"
                        ] = email

                        result[
                            "contact_source"
                        ] = item.get(
                            "link"
                        )

                        result[
                            "confidence"
                        ] = 0.8

                        break


            # ------------------------------------------------
            # Confidence
            # ------------------------------------------------

            if (
                result["contact_email"]
                and result["linkedin_url"]
            ):

                result["confidence"] = 0.9

            elif (
                result["contact_email"]
                or result["company_website"]
            ):

                result["confidence"] = 0.8

            elif result["linkedin_url"]:

                result["confidence"] = 0.5


            return result


        except Exception as exc:

            print(
                f"Contact finder error: {exc}"
            )

            return result


    def _extract_email(self, text):

        emails = re.findall(
            r"""
            [A-Za-z0-9._%+-]+
            @
            [A-Za-z0-9.-]+
            \.
            [A-Za-z]{2,}
            """,
            text,
            re.VERBOSE,
        )


        excluded_domains = {
            "example.com",
            "example.org",
            "test.com",
        }


        for email in emails:

            email = email.lower()

            domain = email.split("@")[-1]

            if domain not in excluded_domains:

                return email


        return None


    def _is_company_website(
        self,
        url,
        company
    ):

        if not url:
            return False


        excluded_domains = [
            "linkedin.com",
            "indeed.com",
            "naukri.com",
            "glassdoor.com",
            "glassdoor.co.in",
            "facebook.com",
            "instagram.com",
            "twitter.com",
            "x.com",
            "cutshort.io",
            "instahyre.com",
        ]


        url_lower = url.lower()


        for domain in excluded_domains:

            if domain in url_lower:
                return False


        return (
            url_lower.startswith("http")
        )