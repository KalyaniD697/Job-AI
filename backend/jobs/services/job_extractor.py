import requests

from bs4 import BeautifulSoup


class JobExtractor:

    def extract_page_text(self, url):

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove elements that don't contain useful job information.
        for element in soup(
            [
                "script",
                "style",
                "noscript",
                "svg"
            ]
        ):
            element.decompose()

        text = soup.get_text(
            separator="\n"
        )

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        text = "\n".join(lines)

        return text