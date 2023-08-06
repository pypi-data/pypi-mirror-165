# MIT License
#
# Modifications Copyright (c) klaytn authors
Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest

import tests.resources
from klaytnetl.jobs.export_events_job import ExportEventsJob
from klaytnetl.jobs.exporters.events_item_exporter import events_item_exporter
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from tests.klaytnetl.job.helpers import get_web3_provider
from tests.helpers import compare_lines_ignore_order, read_file, skip_if_slow_tests_disabled

RESOURCE_GROUP = 'test_export_events_job'


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize("start_block,end_block,batch_size,resource_group,web3_provider_type", [
    (60000000, 60000001, 1, 'logs', 'mock'),
    (60000000, 60000001, 2, 'logs', 'mock'),
    skip_if_slow_tests_disabled((60000000, 60000001, 1, 'logs', 'fantrie')),
    skip_if_slow_tests_disabled((60000000, 60000001, 2, 'logs', 'fantrie'))
])
def test_export_blocks_job(tmpdir, start_block, end_block, batch_size, resource_group, web3_provider_type):
    events_output_file = str(tmpdir.join('actual_events.json'))
    block_iterator = range(start_block, end_block + 1)

    job = ExportEventsJob(
        block_iterator=block_iterator, batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(
            lambda: get_web3_provider(web3_provider_type, lambda file: read_resource(resource_group, file), batch=True)
        ),
        max_workers=5,
        item_exporter=events_item_exporter(events_output_file),
        event_hash=None
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, 'expected_events.json'), read_file(events_output_file)
    )