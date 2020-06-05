#!/usr/bin/env python3
# Copyright 2020 Google LLC
#
# Licensed under the the Apache License v2.0 with LLVM Exceptions (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import glob
import json
import logging
import os
import sys
import uuid

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phabtalk.phabtalk import PhabTalk
from buildkite.utils import format_url

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', type=str, default='WARNING')
    parser.add_argument('--success', action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, format='%(levelname)-7s %(message)s')
    phabtalk = PhabTalk(os.getenv('CONDUIT_TOKEN'), 'https://reviews.llvm.org/api/', False)
    build_url = f'https://reviews.llvm.org/harbormaster/build/{os.getenv("ph_build_id")}'
    print(f'Reporting results to Phabricator build {format_url(build_url)}')
    ph_buildable_diff = os.getenv('ph_buildable_diff')
    ph_target_phid = os.getenv('ph_target_phid')
    phabtalk.update_build_status(ph_buildable_diff, ph_target_phid, False, args.success)
    bug_url = f'https://github.com/google/llvm-premerge-checks/issues/new?assignees=&labels=bug' \
              f'&template=bug_report.md&title=buildkite build {os.getenv("BUILDKITE_PIPELINE_SLUG")} ' \
              f'{os.getenv("BUILDKITE_BUILD_NUMBER")}'
    print(f'{format_url(bug_url, "report issue")}')
