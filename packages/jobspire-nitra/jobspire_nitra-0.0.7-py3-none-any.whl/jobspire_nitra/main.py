from typing import Dict, Any, Optional, List
from requests import get, post, patch, delete, put, Response, exceptions
from sys import exit


class Nitra:
    def __init__(
        self,
        username: str,
        secret: str,
        base_url: str,
        ensure_connected: bool = True
    ):
        self.username = username
        self.secret = secret
        self.base_url = base_url
        if ensure_connected:
            res = self.ping()
            if res.status_code != 200:
                try:
                    json = res.json()
                    print(f'Unable to talk with backend.\nReceived status code {res.status_code}\nReceived json: {json}')
                    exit(1)
                except exceptions.JSONDecodeError:
                    print(f'Unable to talk with backend.\nReceived status code {res.status_code} with invalid json body')
                    exit(1)
    
    def req(
        self,
        endpoint: str,
        method: str = 'GET',
        body: Optional[Dict[str, Any]] = None
    ) -> Response:
        # define request method func
        request = get
        if method == 'POST':
            request = post
        elif method == 'PATCH':
            request = patch
        elif method == 'DELETE':
            request = delete
        elif method == 'PUT':
            request = put
        elif method != 'GET':
            raise Exception(f'Method "{method}" is not supported')

        # define headers
        headers = {
            'Authorization': f'Bearer {self.username}:{self.secret}',
            'Accept': 'application/json',
            'X-Nitra': 'OK'
        }

        # define payload
        payload = None
        if method != 'GET' and not (not body):
            payload = body

        # define url
        url = self.base_url + endpoint 

        # send request and return response
        response = request(url=url, json=payload, headers=headers)
        return response


    def ping(self) -> Response:
        return self.req('/ping')


    def delete_job_postings_by_source_id(
        self,
        source_ids: List[str]
    ) -> Response:
        body = {'source_ids': source_ids}
        return self.req(
            '/job_postings/by_source_ids',
            'DELETE',
            body
        )


    def insert_job_postings(
        self,
        job_postings: List[dict]
    ) -> Response:
        
        for job_posting in job_postings:
            job_posting["id"] = str(job_posting["id"])
            job_posting["job_area_id"] = str(job_posting["job_area_id"])

        body = {'job_postings': job_postings}

        return self.req(
            '/job_postings/bulk_insert',
            'POST',
            body
        )


    def insert_job_posting_skills(
        self,
        job_posting_skills: List[dict]
    ) -> Response:
        
        for jps in job_posting_skills:
            jps["skill_id"] = str(jps["skill_id"])
            jps["job_posting_source_id"] = str(jps["job_posting_source_id"])

        body = {'job_posting_skills': job_posting_skills}

        return self.req(
            '/job_posting_skills/bulk_insert',
            'POST',
            body
        )


    def get_skills(self) -> Response:
        return self.req(
            '/skills',
            'GET'
        )


    def get_job_areas(self) -> Response:
        return self.req(
            '/job_areas',
            'GET'
        )


if __name__ == '__main__':
    print('Nitra should not be executed. Import it instead')
    exit(1)
