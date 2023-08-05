import requests

remote_file_url = "https://filesamples.com/samples/document/txt/sample3.txt"
response: requests.Response = requests.head(remote_file_url)
response_header_fields = response.headers
print(response_header_fields)
