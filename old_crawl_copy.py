import warc
import requests
from contextlib import closing
from StringIO import StringIO
import json

def get_partial_warc_file(url, num_bytes=1024 * 10):
    """
    Download the first part of a WARC file and return a warc.WARCFile instance.

    url: the url of a gzipped WARC file
    num_bytes: the number of bytes to download. Default is 10KB

    return: warc.WARCFile instance
    """
    with closing(requests.get(url, stream=True)) as r:
        buf = StringIO(r.raw.read(num_bytes))
    return warc.WARCFile(fileobj=buf, compress=True)


urls = {
    'warc': 'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00000-ip-10-236-182-209.ec2.internal.warc.gz'
}

files = {file_type: get_partial_warc_file(url=url) for file_type, url in urls.items()}
#files = {file_type: warc.open(url) for file_type, url in urls.items()}

def get_record_with_header(warc_file, header, value):
    print 1
    for record, _, _ in warc_file.browse():
        if record.header.get(header) == value:
            return record

warc_record = get_record_with_header(
    files['warc'],
    header='WARC-Type',
    value='response'
)
print warc_record.header

print(warc_record.payload.read())
