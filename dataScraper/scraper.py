import json

import httpx

_HEADERS = {
	# this is internal ID of an instagram backend app. It doesn't change often.
	"x-ig-app-id": "936619743392459",
	# use browser-like features
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept": "*/*",
}

_TIMEOUT = httpx.Timeout(10.0, connect=5.0)
_TRANSPORT = httpx.HTTPTransport(retries=2)

client = httpx.Client(headers=_HEADERS, timeout=_TIMEOUT, transport=_TRANSPORT)


def scrape_user(username: str):
	"""Scrape Instagram user's data.

	Args:
		username: Instagram username to scrape.

	Returns:
		dict: The scraped user data.

	Raises:
		httpx.RequestError: If the HTTP request fails.
		httpx.HTTPStatusError: If the response status indicates an error.
		json.JSONDecodeError: If the response body is not valid JSON.
	"""
	result = client.get(
		f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
	)
	result.raise_for_status()
	return json.loads(result.content)
