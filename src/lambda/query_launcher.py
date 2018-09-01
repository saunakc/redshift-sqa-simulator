#!/usr/bin/env python

from __future__ import print_function

# Copyright 2016-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
# http://aws.amazon.com/apache2.0/
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

import sys
import boto3
import pg8000
import datetime
import random

ssl = True

debug = True

##################
    
def run_command(cursor, statement):
    if debug:
        print("Running Statement: %s" % statement)
        
    return cursor.execute(statement)

def lambda_handler(event, context):
    host = event['Host']
    port = event['Port']
    database = event['Database']
    user = event['User']
    password = event['Password']
    
    s3_bucket_name = "awspsa-redshift-lab"
    thread_num = 'THREAD%d' % random.randint(1, 1000000)
    print('Thread num %s' %thread_num)
    
    try:
        query_random = random.randint(1, 4)
        s3_object_key = 'scripts/%s/demo-query.sql' %query_random
        
        s3 = boto3.resource('s3')
        obj = s3.Object(s3_bucket_name, s3_object_key)
        query_str = obj.get()['Body'].read().decode('utf-8')  % thread_num
        print(query_str)
	  
    except:
        print('Reading from s3 failed: exception %s' % sys.exc_info()[1])

    pg8000.paramstyle = "qmark"

    try:
        if debug:
            print('Connect to Redshift: %s' % host)
        conn = pg8000.connect(database=database, user=user, password=password, host=host, port=port, ssl=ssl)
    except:
        print('Redshift Connection Failed: exception %s' % sys.exc_info()[1])
        return 'Failed'

    if debug:
        print('Succesfully Connected Redshift Cluster')
    cursor = conn.cursor()
    
    str_session_cache = 'SET enable_result_cache_for_session TO OFF;'
    run_command(cursor, str_session_cache)
    
    start = datetime.datetime.now()
    print('Starttime of query: %s' % start.strftime('%Y-%m-%dT%H:%M:%S'))
    
    run_command(cursor, query_str)
    #result = cursor.fetchall()
    end = datetime.datetime.now()
    print('Endtime of query: %s' % end.strftime('%Y-%m-%dT%H:%M:%S'))
    delta = end - start
    print('Time taken to execute: %s ' % delta)
    
    cursor.close()
    conn.close()
    return 'Finished'

if __name__ == "__main__":
    lambda_handler(sys.argv[0], None)
