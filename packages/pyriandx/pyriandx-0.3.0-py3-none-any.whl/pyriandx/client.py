# -*- coding: utf-8 -*-
import json
import logging
import ntpath
import os
import shutil
import time

import pkg_resources
import requests

from pyriandx.utils import retry_session

logger = logging.getLogger(__name__)

__all__ = ['Client']


class Client:

    def __init__(self, email, key, institution, base_url, key_is_auth_token=False):
        self.baseURL = base_url
        self.headers = {
            'X-Auth-Email': email,
            'X-Auth-Institution': institution
        }
        if key_is_auth_token:
            self.headers['X-Auth-Token'] = key
        else:
            self.headers['X-Auth-Key'] = key
        # this is required to import static data from the module
        self.data_path = pkg_resources.resource_filename('pyriandx', 'json/')

    def create_case(self, case_data_file):
        """Creates case with given case data file"""
        with open(case_data_file, 'r') as f:
            request_data = json.load(f)
        logger.debug("Creating case with data:")
        logger.debug(request_data)
        response = self._post_api("/case", data=request_data).json()
        return response['id']

    def create_sequencer_run(self, accession_number, run_id, request_data=None):
        """Creates sequencer run with given accession number"""
        if request_data is None:
            with open(self.data_path + 'create_sequencer_run.json', 'r') as f:
                request_data = json.load(f)
        request_data['runId'] = run_id
        request_data['specimens'][0]['accessionNumber'] = accession_number
        logger.debug(f"Creating sequencer run with data: {request_data}")
        response = self._post_api("/sequencerRun", data=request_data).json()
        return response['id']

    def create_job(self, case, run_id, request_data=None):
        """Creates job with given case and sequence run id"""
        if request_data is None:
            with open(self.data_path + 'create_job.json', 'r') as f:
                request_data: dict = json.load(f)
        accession_number = str(case['specimens'][0]['accessionNumber'])
        request_data['input'][0]['accessionNumber'] = str(accession_number)
        request_data['input'][0]['sequencerRunInfos'][0]['runId'] = str(run_id)
        request_data['input'][0]['sequencerRunInfos'][0]['files'] = case['caseFiles']
        logger.debug(f"Creating job for Case ID: {str(case['id'])} with input payload:")
        logger.debug(request_data)
        endpoint = f"/case/{str(case['id'])}/informaticsJobs"
        response = self._post_api(endpoint, data=request_data).json()
        return response['jobId']

    def create_job_vcf(self, case_id):
        """Creates job with given case id"""
        logger.debug(f"Creating job for vcf with case ID: {str(case_id)}")
        endpoint = f"/case/{str(case_id)}/informaticsJobsVCF"
        self._post_api(endpoint)

    def get_job_status(self, case_id, job_id):
        """Gets the status of an informatics job."""
        logger.debug(f"Getting status of job {job_id} for case ID: {str(case_id)}")
        case_info = self.get_case_info(case_id)

        job = None
        for j in case_info['informaticsJobs']:
            if j['id'] == job_id:
                job = j

        try:
            status = job['status']
        except KeyError:
            status = "NO_JOB_AVAILABLE"

        logger.debug(f"Got status: {status}")

        return status

    def get_report(self, case, output_dir=None):
        """
        Downloads report to output_dir.
        If report_index is None, downloads all reports.
        If output_dir is None, downloads to working directory.
        """
        for r in case['reports']:
            report_id = r['id']
            local_filename = f"case-{str(case['id'])}_report-{report_id}.pdf.gz"
            endpoint = f"/case/{str(case['id'])}/reports/{report_id}?format=pdf"
            url = self.baseURL + endpoint

            if output_dir is not None:
                os.makedirs(output_dir, exist_ok=True)
                local_filename = output_dir + "/" + local_filename
            logger.info(f"Found report with ID {report_id}. Downloading as {local_filename} from {url}")

            r = requests.get(url, stream=True, headers=self.headers)
            if r.ok:
                with open(local_filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            else:
                logger.critical(f"Issue downloading file from {endpoint}. {r.status_code} ::: {r.text}")

    def upload_file(self, filename, case_id):
        """Upload file to given accession number"""
        files = {'file': open(filename, 'rb')}
        remote_filename = ntpath.basename(filename)
        endpoint = f"/case/{str(case_id)}/caseFiles/{remote_filename}/"
        logger.debug(f"Upload file to endpoint: {endpoint}")
        self._post_api(endpoint, files=files)

    def get_case_info(self, case_id):
        """Get case info for given case ID"""
        return self._get_api(f"/case/{str(case_id)}")

    def list_cases(self, filters: dict = None):
        """List cases, optionally apply query filters if pass-in"""
        return self._get_api(f"/case", params=filters)

    def get(self, endpoint, params):
        """Expose GET API to caller/client
        Retain _get_api() for backward compatible
        """
        return self._get_api(endpoint=endpoint, params=params)

    def _get_api(self, endpoint, params=None):
        """Internal function to create get requests to the API"""
        url = self.baseURL + endpoint
        logger.debug(f"Sending request to {url}")
        t0 = time.time()
        try:
            response = retry_session(self.headers).get(url, params=params)
        except Exception as x:
            logger.critical(f"{endpoint} call failed after retry: {x}")
        else:
            if response.status_code == 200:
                logger.debug(f"Call to {endpoint} succeeded")
                return json.loads(response.text)
            else:
                logger.critical(f"Call to {endpoint} failed. Error code was {response.status_code}")
                logger.critical(f"Server responded with {response.text}")

        finally:
            t1 = time.time()
            logger.debug(f"Call took {t1 - t0} seconds")

    def post(self, endpoint, data=None, files=None):
        """Expose POST API to caller/client
        Retain _post_api() for backward compatible
        """
        return self._post_api(endpoint, data=data, files=files)

    def _post_api(self, endpoint, data=None, files=None):
        """Internal function to create post requests to the API"""
        url = self.baseURL + endpoint
        logger.debug(f"Sending request to {url}")
        t0 = time.time()
        post_headers = self.headers.copy()
        if data is not None:
            post_headers['Content-Type'] = "application/json"
            post_headers['Accept-Encoding'] = "*"
        if files is None:
            upload = False
        else:
            upload = True  # prevents seeing every. single. byte. in file upload during verbose mode
        # uncomment if you like to inspect the json data we're sending
        # with open("request-debug.json", "w") as data_file:
        #         json.dump(data, data_file, indent=2)
        try:
            response = retry_session(post_headers, upload=upload).post(url, json=data, files=files)
        except Exception as x:
            logger.critical(f"{endpoint} call failed after retry: {x}")
        else:
            if response.status_code == 200:
                logger.debug(f"Call to {endpoint} succeeded")
                logger.debug(f"Response was {response.text}")
            else:
                logger.critical(f"Call to {endpoint} failed. Error code was {response.status_code}")
                logger.critical(f"Server responded with {response.text}")
            return response
        finally:
            t1 = time.time()
            logger.debug(f"Call took {t1 - t0} seconds")
