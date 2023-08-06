'''
 #####
#     #  ####   ####  #   ##   #      #      #   #
#       #    # #    # #  #  #  #      #       # #
 #####  #    # #      # #    # #      #        #
      # #    # #      # ###### #      #        #
#     # #    # #    # # #    # #      #        #
 #####   ####   ####  # #    # ###### ######   #

######
#     # ###### ##### ###### #####  #    # # #    # ###### #####
#     # #        #   #      #    # ##  ## # ##   # #      #    #
#     # #####    #   #####  #    # # ## # # # #  # #####  #    #
#     # #        #   #      #####  #    # # #  # # #      #    #
#     # #        #   #      #   #  #    # # #   ## #      #    #
######  ######   #   ###### #    # #    # # #    # ###### #####
'''

import io
import boto3
import botocore
import pandas as pd
from sdutilities.logger import SDLogger

"""
This module contains the AWSClient class and its related functions.
"""


class AWSClient(object):
    """
    Class provides functionality for interfacing with AWS.

    Creates AWS session and provides functionality for interacting
    with the data through Python.  Also utilizes the SDLogger class.

    Attributes:
        _logger (SDLogger): Access the SDLogger object from the
            sdutilities.SDLogger class.
        session (Session): Session object from the boto3 Session class.
    """

    def __init__(self, profile_name=None, log_level=None, log_file=True,
                 file_log_level=None, log_file_prefix=None):
        """
        Constructor

        Args:
            profile_name (String, optional): ~/.aws/credentials profile
            log_level (String, optional): One of
                ['DEBUG', 'INFO', 'WARNING', 'ERROR'].
            log_file (bool, optional): Flag to output a log file
                (Defaults to True).
            file_log_level (String, optional): One of
                ['DEBUG', 'INFO', 'WARNING', 'ERROR'].
            log_file_prefix(String, optional): Set prefix of log file name.

            NOTE: See SDLogger documentation for more information about the
                  parameters and functions associated with this class.
        """

        self.session = boto3.Session(profile_name=profile_name)

        self._logger = SDLogger(log_level, log_file, file_log_level,
                                log_file_prefix)

    def get_available_iam_roles(self):
        """Returns a list of all available IAM Roles

        Returns:
            roles (List of Strings): Available IAM Roles
        """
        iam_client = self.session.client('iam')
        roles = [r['RoleName'] for r in iam_client.list_roles()['Roles']]
        return roles

    def get_iam_role_credentials(self, client_name=None,
                                 role_name=None):
        """Returns AWS credentials for the IAM Role

        Args:
            boto3_session (Session): Session object from Boto3.
            client_name (String, optional): Client IAM Role to assume
            role_name (String, optional): IAM Role to assume

        Returns:
            credentials (Dict of Strings): IAM Role AWS Credentials
        """
        sts_client = self.session.client('sts')
        account = sts_client.get_caller_identity().get('Account')
        self._logger.debug(f"AWS Account Number: {account}")
        if(client_name is not None):
            role_name = f"SDAC-IAMRole-DL-Client-{client_name}"
        try:
            assumed_role_object = sts_client.assume_role(
                RoleArn=f"arn:aws:iam::{account}:role/{role_name}",
                RoleSessionName="AssumedRoleSession")
            credentials = assumed_role_object['Credentials']
            return credentials
        except botocore.exceptions.ClientError:
            self._logger.error(f"Could not assume IAM Role {role_name}")
            self._logger.info(
                "IAM Roles can be found with get_available_iam_roles()")
            self._logger.info(
                "Some IAM Roles are unavailable due to permissions")

    def build_s3_client(self, client_name=None, role_name=None):
        """Builds a boto3 S3 client

        Args:
            client_name (String, optional): Client IAM Role to assume
            role_name (String, optional): IAM Role to assume
        """
        if(client_name or role_name):
            self._logger.info("Gathering AWS credentials")
            credentials = self.get_iam_role_credentials(
                client_name=client_name, role_name=role_name)
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
            )
        else:
            self.s3_client = self.session.client('s3')

    def get_s3_data(self, client_name, file_id, dtype_dict=None):
        """Returns client IDW dataframes from S3

        Args:
            client_name (String): Client code for desired IDWs
            file_id (String): Job ID for desired IDWs or partial URI for TU files (SRG and CM)

        Returns:
            food_idw_df (DataFrame): Food IDWs for client/job_id
            hr_idw_df (DataFrame): Health Resource IDWs for client/job_id
            OR
            srg_df (DataFrame): TU SRG table for client/irb
            cm_df (DataFrame): TU CM table for client/irb
        """
        
        # grabs .aws/credentials information to be able to access client s3 files
        self.build_s3_client(client_name=client_name)
        # if given a partial uri, grab a TU return file else grab IDW file

        if '/' in file_id:
            # construct uri
            tu_prefix = (f'aqueduct/client_databases/{client_name}/' + file_id)
            
            self._logger.info("Searching for TU file " + tu_prefix)
            
            tu_key = None
            
            try:
                # grab key/file location to see if you can see the file/ the file exists
                tu_key = self.s3_client.list_objects(
                    Bucket='sdac-s3-use1-datalake',
                    Prefix=tu_prefix)['Contents'][0]['Key']
                self._logger.info(f"TU file {tu_key} found")
                
            except:
                self._logger.error(
                    "Couldn't find a TU file associated with that client and uri")
                return
            
            if 'append' in file_id:
                # getting file data in bytes to be able to read into a df
                srg_csv = self.s3_client.get_object(
                    Bucket='sdac-s3-use1-datalake', Key=tu_key)
                # grab dtypes for how to read columns in srg file from individual_risk_pipeline/lib/tu_cols.json
                cols = dtype_dict
                # create TU srg df
                srg_df = pd.read_csv(
                    io.StringIO(
                        srg_csv['Body'].read().decode('utf-8')),
                    low_memory=False,
                    dtype=dict(zip(cols['request'] + cols['srg'], ([str] * 17) + (['Int64'] * len(cols['srg'])))))
                return srg_df
            
            else:
                # getting file data in bytes to be able to read into a df
                cm_csv = self.s3_client.get_object(
                    Bucket='sdac-s3-use1-datalake', Key=tu_key)
                # grab dtypes for how to read columns in cm file from individual_risk_pipeline/lib/tu_cols.json
                cols = dtype_dict
                # create TU cm df
                cm_df = pd.read_csv(
                    io.StringIO(
                        cm_csv['Body'].read().decode('utf-8')),
                    low_memory=False, sep='|',
                    dtype=dict(zip(cols['request'] + cols['cm_int'] + cols['cm_str'],
                                   ([str] * 17) + (['Int64'] * len(cols['cm_int']) + ([str] * len(cols['cm_str']))))))
                return cm_df
           
        else:

            food_idw_prefix = (
                f'aqueduct/client_databases/{client_name}/jobs/{file_id}/' +
                'analytics/idw/idw_classification=food_idw/part'
            )
            food_idw_key = None

            self._logger.info("Searching for Food IDW file.")
            try:
                food_idw_key = self.s3_client.list_objects(
                    Bucket='sdac-s3-use1-datalake',
                    Prefix=food_idw_prefix)['Contents'][0]['Key']
                self._logger.info("Food IDW key found.")
            except:
                self._logger.error(
                    "Couldn't find IDW files associated with that client/job_id")
                return
            food_idw_csv = self.s3_client.get_object(
                Bucket='sdac-s3-use1-datalake', Key=food_idw_key)
            food_idw_df = pd.read_csv(io.StringIO(
                food_idw_csv['Body'].read().decode('utf-8'))
            )
            self._logger.info("Food IDW file loaded")

            health_resource_idw_prefix = (
                f'aqueduct/client_databases/{client_name}/jobs/{file_id}/' +
                'analytics/idw/idw_classification=health_resource_idw/part'
            )
            health_resource_idw_key = None
            self._logger.info("Searching for Health Resources IDW file.")
            try:
                health_resource_idw_key = self.s3_client.list_objects(
                    Bucket='sdac-s3-use1-datalake',
                    Prefix=health_resource_idw_prefix)['Contents'][0]['Key']
                self._logger.info("Health Resources IDW key found.")
            except:
                self._logger.error(
                    "Couldn't find IDW files associated with that client/job_id")
                return
            health_resource_idw_csv = self.s3_client.get_object(
                Bucket='sdac-s3-use1-datalake', Key=health_resource_idw_key)
            hr_idw_df = pd.read_csv(io.StringIO(
                health_resource_idw_csv['Body'].read().decode('utf-8'))
            )
            self._logger.info("Health Resources IDW file loaded.")

            return (food_idw_df, hr_idw_df)

    def load_s3_idws(self, client_db, client_name, job_id,
                     table_suffix='eng_idw_person',
                     schema='social_transformed'):
        """Loads IDWs from S3 client locations into client postgres databases

        Args:
            client_db (DataLink): Connection to client database
            client_name (String): Client code for IDWs
            job_id (String): Job ID for IDWs
            table_suffix (String, Optionals): Suffix to be used in database table names
            schema (String, Optionals): Schema to write tables to on client databases
        """
        food_idw_df, hr_idw_df = self.get_s3_data(client_name, job_id)
        self._logger.info("Writing IDWs to Client Database")
        client_db.upsert(food_idw_df, f'food_{table_suffix}', schema,
                         constraint_cols=['sd_uuid'],
                         owner=f'sd_{client_name}_phi_datascience')
        client_db.upsert(hr_idw_df, f'health_resources_{table_suffix}', schema,
                         constraint_cols=['sd_uuid'],
                         owner=f'sd_{client_name}_phi_datascience')
