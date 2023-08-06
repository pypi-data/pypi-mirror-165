# -*- coding: utf-8 -*-
"""PierianDx API Client ::: API client CLI/SDK for PierianDx web services

Usage:
    pyriandx <command> [options] [<args>...]

Command:
    help        Print help and exit
    version     Print version and exit
    case        Get a case from Case API
    list        List cases from Case API, optionally apply filters to limit results
    create      Accession a new case from given input JSON file
    upload      Upload case files for given Case ID
    run         Create sequencer run for given Case ID
    job         Create informatics job for given Case ID and Run ID
    poll        Poll informatics job status for given Case ID and Job ID
    report      Get a report for given Case ID

(See 'pyriandx <command> help' for more information on a specific command)

Options:
    -b, --base_url=base_url         Base URL.
    -u, --username=username         Required if PDX_USERNAME does not exist. Usually email address.
    -p, --password=password         Required if PDX_PASSWORD does not exist.
    -i, --institution=institution   Required if PDX_INSTITUTION does not exist.
    -d, --debug                     Make output more verbose innit.
    -t, --trace                     Make output more and more verbose innit.

Environment variables:
    PDX_USERNAME       If defined, uses this as username for authenticating to PierianDx
    PDX_PASSWORD       If defined, uses this as password for authenticating to PierianDx
    PDX_INSTITUTION    If defined, uses this as institution for authenticating to PierianDx
    PDX_BASE_URL       If defined, uses this as base URL for PierianDx service
"""
import json
import logging
import os
import sys
import time

import coloredlogs
import verboselogs
from docopt import docopt

from pyriandx.client import Client
from . import __version__

logger = verboselogs.VerboseLogger(__name__)
verboselogs.add_log_level(verboselogs.SPAM, 'TRACE')
verboselogs.install()

coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s %(name)-12s \t %(levelname)-8s %(message)s'
coloredlogs.DEFAULT_LEVEL_STYLES = dict(
    spam=dict(color='green', faint=True),
    debug=dict(color='green'),
    verbose=dict(),
    info=dict(),
    notice=dict(color='magenta'),
    warning=dict(color='yellow'),
    success=dict(color='green', bold=True),
    error=dict(color='red'),
    critical=dict(color='red', bold=True),
)
coloredlogs.install()

DEFAULT_BASE_URL = "https://app.uat.pieriandx.com/cgw-api/v2.0.0"


def _help(msg):
    print(msg)
    sys.exit(0)


def _die(msg):
    print(__doc__)
    logger.critical(f"{msg}.")
    sys.exit(1)


def _halt(msg, doc):
    print(doc)
    logger.critical(f"{msg}.")
    sys.exit(1)


def _build(global_args):
    username = global_args.get('--username', None)
    if username is None:
        username = os.getenv('PDX_USER', None)  # backward compatible
    if username is None:
        username = os.getenv('PDX_USERNAME', None)
    assert username is not None, _die("Please provide username via -u flag or PDX_USERNAME environment variable")

    pw = global_args.get('--password', None)
    if pw is None:
        pw = os.getenv('PDX_SECRET', None)  # backward compatible
    if pw is None:
        pw = os.getenv('PDX_PASSWORD', None)
    assert pw is not None, _die("Please provide password via -p flag or PDX_PASSWORD environment variable")

    inst = global_args.get('--institution', None)
    if inst is None:
        inst = os.getenv('PDX_INSTITUTION', None)
    assert inst is not None, _die("Please provide institution via -i flag or PDX_INSTITUTION environment variable")

    base_url = global_args.get('--base_url', None)
    if base_url is None:
        base_url = os.getenv('PDX_BASE_URL', None)
        if base_url is None:
            base_url = DEFAULT_BASE_URL

    if "uat" in base_url:
        logger.warning(f"You are working on PierianDx CGW 'UAT' environment -- {base_url}")
    else:
        logger.notice(f"Your working PierianDx CGW environment is -- {base_url}")

    return Client(email=username, key=pw, institution=inst, base_url=base_url)


def _dispatch():
    global_args: dict = docopt(__doc__, sys.argv[1:], version=__version__)

    if global_args['--debug']:
        coloredlogs.install(level=logging.DEBUG)

    if global_args['--trace']:
        coloredlogs.install(level=verboselogs.SPAM)
        os.environ['DEBUG_HTTP'] = "true"

    command_argv = [global_args['<command>']] + global_args['<args>']

    logger.spam(f"Global arguments:\n {global_args}")
    logger.spam(f"Command arguments:\n {command_argv}")

    cmd = global_args['<command>']
    if cmd == 'help':
        _help(__doc__)
    elif cmd == 'version':
        _help(__version__)
    elif cmd == 'case':
        Case(global_args, command_argv)
    elif cmd == 'list' or cmd == 'ls':
        List(global_args, command_argv)
    elif cmd == 'create':
        Create(global_args, command_argv)
    elif cmd == 'upload':
        Upload(global_args, command_argv)
    elif cmd == 'run':
        Run(global_args, command_argv)
    elif cmd == 'job':
        Job(global_args, command_argv)
    elif cmd == 'poll':
        Poll(global_args, command_argv)
    elif cmd == 'report':
        Report(global_args, command_argv)
    else:
        _die(f"Command '{cmd}' is invalid. See 'pyriandx help'")


class Command:

    def __int__(self):
        # sub-class should set these
        self.case_id = None
        self.client = None
        self.resources = None

    def get_case(self):
        assert str(self.case_id).isnumeric(), _halt(f"Invalid Case ID: {self.case_id}", self.__doc__)
        logger.info(f"Get a case with ID: {self.case_id}")
        case = self.client.get_case_info(self.case_id)
        assert case is not None and "id" in case, _halt(f"Case not found for ID: {self.case_id}", self.__doc__)
        logger.debug(f"Found case with ID: {self.case_id}")
        return case

    def upload_case_files(self):
        files = []
        for r in self.resources:
            if os.path.isdir(r):
                case_files = [f for f in os.listdir(r) if os.path.isfile(os.path.join(r, f))]
                for cf in case_files:
                    files.append(os.path.join(r, cf))
            else:
                files.append(r)

        for f in files:
            logger.info(f"Uploading case file: {f}")
            self.client.upload_file(f, self.case_id)


class Case(Command):
    """Usage:
    pyriandx case help
    pyriandx case [options] <case-id>

Description:
    Get a case by given ID from PierianDx CGW. It returns in JSON
    format. You can further process it e.g. pretty print by pipe
    through with program such as jq.

Example:
    pyriandx case 69695
    pyriandx case 69695 | jq
    """

    def __init__(self, global_args, command_argv):
        args: dict = docopt(self.__doc__, argv=command_argv)
        logger.spam(f"Case arguments:\n {args}")
        assert args['case'] is True, _die("Command mismatch: Case")

        if args['help']:
            _help(self.__doc__)

        self.client: Client = _build(global_args)
        self.case_id = args['<case-id>']
        self.case = self.get_case()
        print(json.dumps(self.case))  # print here is intended i.e. pyriandx case 1234 | jq


class List(Command):
    """Usage:
    pyriandx list help
    pyriandx list [options] [<filters>...]

Description:
    List all cases by from PierianDx CGW. It returns in JSON format.
    You can further process it e.g. pretty print by pipe through with
    program such as jq. Optionally you can provide filters to limit
    the return list.

Allow filters:
    id                      Case ID
    accessionNumber         Accession Number
    panel                   The name of the case's panel
    dateCreatedStart        Inclusive start range for the date created
    dateCreatedEnd          Exclusive end range for the date created
    dateSignedOutStart      Inclusive start range for the date signed out
    dateSignedOutEnd        Exclusive end range for the date signed out

Example:
    pyriandx list
    pyriandx list | jq
    pyriandx list id=1234
    pyriandx list accessionNumber=SBJ000123
    pyriandx list dateSignedOutStart=2020-04-01
    """

    _F = ['id', 'accessionNumber', 'panel', 'dateCreatedStart',
          'dateCreatedEnd', 'dateSignedOutStart', 'dateSignedOutEnd']

    def __init__(self, global_args, command_argv):
        args: dict = docopt(self.__doc__, argv=command_argv)
        logger.spam(f"List arguments:\n {args}")
        assert args['list'] is True, _die("Command mismatch: List")

        if args['help']:
            _help(self.__doc__)

        self.client: Client = _build(global_args)
        self.filters = args['<filters>']

        logger.debug(f"Filters: {self.filters}")

        params = {}
        for ftr in self.filters:
            assert '=' in ftr, _halt(f"Invalid filter supplied: {ftr}", self.__doc__)
            fil = ftr.split('=')
            assert fil[0] in self._F, _halt(f"Invalid filter supplied: {ftr}", self.__doc__)
            params.update({fil[0]: fil[1]})

        self.cases = self.client.list_cases(filters=params)
        print(json.dumps(self.cases))  # print here is intended i.e. pyriandx list | jq


class Upload(Command):
    """Usage:
    pyriandx upload help
    pyriandx upload [options] <case-id> FILES...

Description:
    FILES... can be a directory that contains list of files that
    stage to upload. Or, you can also provide individual file with
    space separated for multiple of them.

Example:
    pyriandx upload 69695 path/to/SBJ00123/
    pyriandx upload 69695 file1.vcf.gz file2.vcf.gz file3.cnv
    """

    def __init__(self, global_args, command_argv):
        args: dict = docopt(self.__doc__, argv=command_argv)
        logger.spam(f"Create arguments:\n {args}")
        assert args['upload'] is True, _die("Command mismatch: Upload")

        if args['help']:
            _help(self.__doc__)

        self.case_id = args['<case-id>']
        self.resources = args['FILES']
        self.client: Client = _build(global_args)

        if self.get_case():
            self.upload_case_files()


class Create(Command):
    """Usage:
    pyriandx create help
    pyriandx create [options] <json-file> [FILES...]

Description:
    Accession a new case from given input JSON file. Optionally,
    FILES... can be a directory that contains list of files that
    stage to upload. Or, you can also provide individual file with
    space separated for multiple of them.

Example:
    pyriandx create my_case.json path/to/SBJ00123/
    pyriandx create my_case.json file1.vcf.gz file2.vcf.gz file3.cnv
    """

    def __init__(self, global_args, command_argv):
        args: dict = docopt(self.__doc__, argv=command_argv)
        logger.spam(f"Create arguments:\n {args}")
        assert args['create'] is True, _die("Command mismatch: Create")

        if args['help']:
            _help(self.__doc__)

        self.input_file = args['<json-file>']
        self.resources = args['FILES']

        assert str(self.input_file).endswith('.json'), _halt(f"Case input file must be in JSON format", self.__doc__)
        assert os.path.exists(self.input_file), _halt(f"No such file: {self.input_file}", self.__doc__)

        self.client: Client = _build(global_args)

        logger.info(f"Creating case from input file: {self.input_file}")
        self.case_id = self.client.create_case(self.input_file)
        logger.success(f"Created case with ID: {self.case_id}")

        if self.resources:
            self.upload_case_files()


class Run(Command):
    """Usage:
    pyriandx run help
    pyriandx run [options] <case-id>

Description:
    Create sequencer run for given Case ID. Note that each invocation
    will create a sequencer run for given case. At the moment, it uses
    internal `create_sequencer_run.json` template to create a sequencer
    run. It returns Run ID. It will associate this Run ID with accession
    number of given case. You typically need at least 1 sequencer run
    after case has accessioned.

Example:
    pyriandx run 69695
    > 1
    pyriandx run 69695
    > 2
    pyriandx case 69695 | jq
    pyriandx case 69695 | jq '.sequencerRuns[] | select(.runId == "1")'
    """

    def __init__(self, global_args, command_argv):
        args: dict = docopt(self.__doc__, argv=command_argv)
        logger.spam(f"Run arguments:\n {args}")
        assert args['run'] is True, _die("Command mismatch: Run")

        if args['help']:
            _help(self.__doc__)

        self.client: Client = _build(global_args)
        self.case_id = args['<case-id>']

        case = self.get_case()

        if case:
            self.accession_number = str(case['specimens'][0]['accessionNumber'])
            next_run_id = 1  # start from 1

            # check existing sequence run
            if 'sequencerRuns' in case:
                logger.info(f"Case ID {self.case_id} has existing sequencer runs:")
                run_ids = []
                for run in case['sequencerRuns']:
                    rid = run['runId']
                    logger.info(f"\tRun ID: {rid}, Date Created: {run['dateCreated']}")
                    if str(rid).isnumeric():  # ignore if not numeric
                        run_ids.append(rid)
                if len(run_ids) > 0:
                    next_run_id = int(sorted(run_ids, reverse=True)[0]) + 1  # increase serial

            logger.info(f"Creating sequencer run for case {self.case_id}")
            id_ = self.client.create_sequencer_run(self.accession_number, next_run_id)
            self.run_id = next_run_id
            logger.success(f"Created sequencer run with ID: {self.run_id}")


class Job(Command):
    """Usage:
    pyriandx job help
    pyriandx job [options] <case-id> <run-id>

Description:
    Create informatics job for given Case ID and Run ID. At the moment,
    it uses internal `create_job.json` template to create analysis job.
    It returns Job ID. It will associate this informatics job with given
    case. The analysis informatics job will kick off right away for the
    given case and uploaded case files. Note that each invocation will
    create a new informatics job for given case. It also implies that
    you should create a case, a sequencer run and uploaded case files
    before running informatics analysis job.

Example:
    pyriandx job 69695 1
    > 19635
    pyriandx job 69695 1
    > 19636
    pyriandx case 69695 | jq
    pyriandx case 69695 | jq '.informaticsJobs[] | select(.id == "19635")'
    """

    def __init__(self, global_args, command_argv):
        args: dict = docopt(self.__doc__, argv=command_argv)
        logger.spam(f"Job arguments:\n {args}")
        assert args['job'] is True, _die("Command mismatch: Job")

        if args['help']:
            _help(self.__doc__)

        self.client: Client = _build(global_args)
        self.case_id = args['<case-id>']
        self.run_id = args['<run-id>']

        case = self.get_case()

        if 'caseFiles' not in case:
            logger.warning(f"No case files found in your accessioned case. Very likely that informatics job may fail!")

        assert 'sequencerRuns' in case, _halt(f"No sequencer run found in case {self.case_id}", self.__doc__)

        found = False
        for run in case['sequencerRuns']:
            if run['runId'] == self.run_id:
                found = True
                continue
        assert found is True, _halt(f"Sequencer run ID {self.run_id} is not found in case {self.case_id}", self.__doc__)

        if case:
            logger.info(f"Creating informatics job for case {self.case_id}")
            self.job_id = self.client.create_job(case, self.run_id)
            logger.success(f"Created informatics job with ID: {self.job_id}")


class Poll(Command):
    """Usage:
    pyriandx poll help
    pyriandx poll [options] <case-id> <job-id>

Description:
    Poll informatics job for given Case ID and Job ID. Maximum wait
    time for polling job status is 30 minutes. It will timeout after
    30 minutes. You can poll again. Alternatively, you can check the
    informatics job status in PierianDx CGW dashboard. Or, get a case
    and filter job ID on the return JSON using jq.

    CAVEAT: Polling job status through API is not perfected yet. Please
            do not rely on this feature for status check.

Example:
    pyriandx poll 69695 19635
    pyriandx poll 69695 19636
    pyriandx case 69695 | jq
    pyriandx case 69695 | jq '.informaticsJobs[] | select(.id == "19635")'
    pyriandx case 69695 | jq '.informaticsJobs[] | select(.id == "19635") | .status'
    """

    def __init__(self, global_args, command_argv):
        args: dict = docopt(self.__doc__, argv=command_argv)
        logger.spam(f"Poll arguments:\n {args}")
        assert args['poll'] is True, _die("Command mismatch: Poll")

        if args['help']:
            _help(self.__doc__)

        self.client: Client = _build(global_args)
        self.case_id = args['<case-id>']
        self.job_id = args['<job-id>']

        case = self.get_case()
        self.accession_number = str(case['specimens'][0]['accessionNumber'])
        logger.info(f"Accession Number: {self.accession_number}")

        self.complete = False
        self.__start_poll()

    def __start_poll(self):
        status = self.client.get_job_status(self.case_id, self.job_id)
        logger.info(f"Started polling job {self.job_id} status... (Ctrl+C to exit) ")

        count = 0
        while status != "complete" and status != "failed" and count < 60:  # wait 30 minutes max
            logger.info(f"Status is: {status}")
            time.sleep(30)  # Check API every 30 seconds
            status = self.client.get_job_status(self.case_id, self.job_id)
            count = count + 1

        if count == 60:
            logger.info("Job polling has reached timeout 30 minutes")
        elif status == "complete":
            logger.warning(f"Informatics job {self.job_id} for case {self.case_id} with accession number "
                           f"{self.accession_number} might have completed")
            logger.warning(f"You should check in CGW dashboard to make sure it has completed successfully")
            logger.warning(f"CLI API call does not able to differentiate `status` transition effectively at the moment")
            self.complete = True
        elif status == "failed":
            logger.critical(f"Job did not complete, status was {status}")
            logger.info(f"Please send support request to support@pieriandx.com with the following info:")
            logger.info(f"Case ID: {self.case_id}")
            logger.info(f"Job ID: {self.job_id}")
            logger.info(f"Accession Number: {self.accession_number}")


class Report(Command):
    """Usage:
    pyriandx report help
    pyriandx report [options] <case-id>

Description:
    Get a report for given Case ID. It will download report in
    PDF format and save it into ./output folder.

    CAVEAT: Download report through API is not perfected yet.
            Please do not rely on this feature.

Example:
    pyriandx report 69695
    """

    def __init__(self, global_args, command_argv):
        args: dict = docopt(self.__doc__, argv=command_argv)
        logger.spam(f"Report arguments:\n {args}")
        assert args['report'] is True, _die("Command mismatch: Report")

        if args['help']:
            _help(self.__doc__)

        self.client: Client = _build(global_args)
        self.case_id = args['<case-id>']

        logger.info(f"Finding report IDs for case: {str(self.case_id)}")
        case_ = self.get_case()

        if 'reports' not in case_:
            logger.info(f"No reports available for case {self.case_id}. Try again later.")
        else:
            logger.info(f"Downloading report for case {self.case_id}")
            self.client.get_report(case_, "output")
            logger.success("Report download complete. Check in ./output folder")


def main():
    if len(sys.argv) == 1:
        sys.argv.append('help')
    python_version = ".".join(map(str, sys.version_info[:3]))
    assert sys.version_info >= (3, 6), _die(f"This tool requires Python >=3.6. Found {python_version}")
    try:
        _dispatch()
    except KeyboardInterrupt:
        pass
