from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO


class GBQ:

    # # format of bucket-object URI should be gs://bucket/object

    def __init__(self, key):
        self.key = key
        scopes = ['https://www.googleapis.com/auth/cloud-platform']
        # for full list of scopes, refer to https://cloud.google.com/storage/docs/authentication
        credentials = service_account.Credentials.from_service_account_info(self.key, scopes=scopes)
        self.service = build('bigquery', 'v2', credentials=credentials)


    def create_jobid(self, jobType, name):
        dt=datetime.today().strftime("%Y%m%d%H%M%S")
        jobId = 'jobid_'+ jobType + '_' + name + '_' + dt
        return jobId


    def list_tables(self, project_id,dataset_id):
        tables_object = self.service.tables()
        tables_list=tables_object.list(projectId=project_id, datasetId=dataset_id).execute()
        return tables_list

    def create_queryjob(self, projectId, datasetId, destination_tableId, jobType, name, query, if_exists='replace'):
        '''CAREFUL WITH DESTINATION_TABLEID. CANNOT BE EQUIVALENT TO events_(datestring) because that will
        override the existing table in bigquery!!! feed into a table with differnet prefix

        handy tip: if you accidentally overwrite, go to cloud shell and run:
        bq cp analytics_152113748.events_<date>@<unix time of when it was ok> analytics_152113748.events_<date>
        '''
        jobId = self.create_jobid(jobType=jobType, name=name)
        dt=datetime.today().strftime("%Y%m%d%H%M%S")

        if if_exists == 'append':
            write_disposition = 'WRITE_APPEND'
        elif if_exists == 'replace':
            write_disposition = 'WRITE_TRUNCATE'

        # assumes using standard SQL, not legacy SQL.
        request= {
            "configuration": {
                "query": {
                    "query": query,
                    "destinationTable": {
                        "projectId": projectId,
                        "datasetId": datasetId,
                        "tableId": destination_tableId
                    },
                    # "tableDefinitions": {
                    #
                    # },
                    # "userDefinedFunctionResources": [],
                    "createDisposition": "CREATE_IF_NEEDED",
                    "writeDisposition": write_disposition,
                    # "defaultDataset": {},
                    "priority": "INTERACTIVE", #default, other option is BATCH
                    # "useQueryCache": boolean,
                    # "maximumBillingTier": integer,
                    # "maximumBytesBilled": string,
                    "useLegacySql": "False"
                    # "parameterMode": string,
                    # "queryParameters": [],
                    # "schemaUpdateOptions": [],
                    # "timePartitioning": {},
                    # "rangePartitioning": {},
                    # "clustering": {},
                    # "destinationEncryptionConfiguration": {},
                    # "scriptOptions": {},
                    # "connectionProperties": []
                },
                "dryRun": "False",
                # "jobTimeoutMs": string,
                "labels": {
                    "jobtype": "firebase_query",
                    "date": dt
                }
            },
            "jobReference": {
                "projectId": projectId,
                "jobId": jobId
                # "location": "US"
                }
            }

        jobs_object = self.service.jobs()
        job_request=jobs_object.insert(projectId=projectId, body=request).execute()
        return jobId

    def get_jobstatus(self,projectId, jobId):
        jobs_object = self.service.jobs()
        response=jobs_object.get(projectId=projectId, jobId=jobId).execute()
        return response['status']['state']

    def create_joblog(self, projectId):
        jobs_object = self.service.jobs()
        response = jobs_object.list(projectId=projectId).execute()

        # create list of tuples for jobIds
        jobdata = []
        for job in response['jobs']:
            jobtuple = (job['jobReference']['jobId'],
                        job['state'],
                        job['statistics']['creationTime'],
                        job['statistics']['startTime'],
                        job['statistics']['endTime'],
                        job['statistics']['totalBytesProcessed'],
                        job['statistics']['query']['totalBytesBilled'])
            jobdata.append(jobtuple)

        joblog_df = pd.DataFrame(data=jobdata,
                          columns=['jobId', 'status', 'creationTime', 'startTime', 'endTime', 'totalBytesProcessed',
                                   'totalBytesBilled'])
        joblog_df['created_at']=datetime.now().strftime('%y-%m-%d')
        return joblog_df

    def create_extractjob(self, projectId, datasetId, tableId, jobType, gcs_bucket, gcs_object, gcs_fileExtension, name):
        destinationUris = f'gs://{gcs_bucket}/{gcs_object}.*' + '.' + gcs_fileExtension
        if gcs_fileExtension == 'gzip':
            compression='GZIP'
        jobId = self.create_jobid(jobType=jobType, name=name)
        dt=datetime.today().strftime("%Y%m%d%H%M%S")

        request= {
            "configuration": {
                "extract": {
                    "destinationUris": [destinationUris],
                    # "printHeader": "true", # default is true
                    # "fieldDelimiter": string, # optional, irrelevant for json
                    "destinationFormat": "NEWLINE_DELIMITED_JSON",
                    "compression": compression,
                    # "useAvroLogicalTypes": boolean, # irrelevant
                    "sourceTable": {  # https://cloud.google.com/bigquery/docs/reference/rest/v2/TableReference
                        "projectId": projectId,
                        "datasetId": datasetId,
                        "tableId": tableId
                        }
                    },
                "dryRun": False,
                 # "jobTimeoutMs": string,
                 "labels": {
                     "jobtype": "firebase_export",
                     "date": dt,
                     }
                 },
            "jobReference": {
                "projectId": projectId,
                "jobId": jobId
            }
        }

        jobs_object = self.service.jobs()
        job_request=jobs_object.insert(projectId=projectId, body=request).execute()
        return jobId

    def delete_table(self, projectId,datasetId,tableId):
        tables_object = self.service.tables()
        delete_request = tables_object.delete(projectId=projectId, datasetId=datasetId,tableId=tableId).execute()
        return delete_request