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

import os
import re
import json
import pkg_resources
import pandas as pd
from census import Census, CensusException
from us import states
from sdutilities.logger import SDLogger

"""
This module contains the ACSClient class and its related functions.
"""


class ACSClient(object):
    """
    Class provides functionality for interfacing with the Census ACS data.

    Creates Census ACS connection and provides functionality for interacting
    with the data through Python.  Also utilizes the SDLogger class.

    Attributes:
        _logger (SDLogger): Access the SDLogger object from the
            sdutilities.SDLogger class.
        cxn (Census): Access the Census object from the census.Census class.
        _all_fields (DataFrame): Fields from the Census object.
        _all_states (List): List of states fips codes.
        _acs_groups (Dictionary): ACS tables and fields by category.
        _acs_samples (Dictionary): ACS tables and fields by category,
            limited to those used by SD.
    """

    def __init__(self, year=2019, dataset='acs5',
                 api_key_file='private/api.key', log_level=None,
                 log_file=True, file_log_level=None, log_file_prefix=None):
        """
        Constructor

        Args:
            year (int, optional): Year for ACS data (Defaults to 2019).
            dataset (String, optional): Dataset to request from ACS
                One of ['acs5', 'acs3', 'acs1'] (Defaults to 'acs5').
            api_key_file (String, optional): File path for api key
                (Defaults to 'private/api.key').
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
        self.dataset = dataset

        try:
            api_key = open('private/api.key', 'r').read().strip()
        except FileNotFoundError:
            raise ValueError(f'Invalid api_key_file: {api_key_file}')

        tmpcxn = Census(api_key)

        if dataset == 'acs5':
            self.cxn = tmpcxn.acs5
        elif dataset == 'acs3':
            self.cxn = tmpcxn.acs3
        elif dataset == 'acs1':
            self.cxn = tmpcxn.acs1
        else:
            self.cxn = tmpcxn.acs5

        self.set_year(year)
        self._load_category_data()

        self._all_fields = pd.DataFrame(self.cxn.fields())
        self._all_states = [st.fips for st in states.STATES]

        self._logger = SDLogger(log_level, log_file, file_log_level,
                                log_file_prefix)

    def _get_county_fips(self, state):
        """Returns a list of county fips codes for a given state.

        Args:
            state (String): Two digit state abbreviation.

        Returns:
            clist (List of Strings): List of county fips codes.
        """
        try:
            st_fips = states.lookup(state).fips
        except AttributeError:
            raise ValueError(f'{state} is not a valid state abbreviation')

        csdf = self.cxn.get('GEO_ID',
                            {'for': 'county:*', 'in': f'state:{st_fips}'})
        csdf = pd.DataFrame(csdf)
        clist = csdf.county.tolist()
        clist.sort()
        return clist

    def _get_state_str(self, state):
        """Turns a list of state abbreviations into a string of fips codes
           for use in Census API.

        Args:
            state (String or List of Strings): State abbreviations

        Returns:
            st_str (String): String of state fips codes.
        """
        if state == '*':
            st_str = state
        else:
            if not isinstance(state, list):
                state = [state]

            try:
                st_str = list(map(lambda x: states.lookup(x).fips, state))
            except AttributeError:
                raise ValueError('Invalid state abbreviation')

        return ','.join(st_str)

    def _sd_col_names(self, acs_df):
        """ Converts column names to format used in SD PostgreSQL.

        Args:
            acs_df (DataFrame): DataFrame for which to convert the
                column names.

        Returns:
            acs_df (DataFrame): DataFrame with converted column names.
        """
        regex = r'([bc][0-9a-z]*)_0*([1-9][0-9]*)e'
        sregex = r'\1e\2'
        acs_cols = acs_df.columns

        acs_cols = map(str.lower, acs_cols)
        acs_cols = [re.sub(regex, sregex, s) for s in acs_cols]

        acs_df.columns = acs_cols

        hdr = [s for s in acs_cols if re.match(r'^[bc][0-9].*', s) is None]
        var = [s for s in acs_cols if re.match(r'^[bc][0-9].*', s)]

        ord_cols = hdr + var
        acs_df = acs_df[ord_cols]
        acs_df[var] = acs_df[var].astype('float64')
        return acs_df

    def _load_category_data(self):
        """ Loads ACS table JSON reference files.
        """
        fpath = pkg_resources.resource_filename('sdutilities', 'cfg_tables/')

        with open(os.path.join(fpath, 'grp_table_cfg.json')) as json_data:
            self._acs_groups = json.load(json_data)

        with open(os.path.join(fpath, 'sample_table_cfg.json')) as json_data:
            self._acs_samples = json.load(json_data)

    def set_year(self, year):
        """Sets the year and updates the census connection.

        Args:
            year (int): Year for the ACS data.
        """
        self.year = year
        self.cxn.default_year = year
        self.cxn._switch_endpoints(year)

    def get_states(self, fields, state='*', sd_cols=False,
                   filter_territories=True):
        """Returns state level data for all provided fields.

        Args:
            fields (List of Strings): Fields to return from the ACS API.
            state (String or List of Strings, Optional): State(s) for which
                to return data (Defaults to '*').
            sd_cols (bool, Optional): Return data with SD formatted column
                names (Defaults to False).
            filter_territories (bool, Optional): Filter out US territories
                from state list (Defaults to True).

        Returns:
            df (DataFrame): DataFrame with state level data for given state(s)
                and all provided fields.
        """
        # Ensure GEO_ID is in field list for indexing df
        fields = list(set(['GEO_ID'] + fields))

        st_str = self._get_state_str(state)

        data = self.cxn.get(fields, {'for': f'state:{st_str}'})
        df = pd.DataFrame(data)

        if sd_cols:
            df = self._sd_col_names(df)
            df = df.set_index('geo_id')
        else:
            df = df.set_index('GEO_ID')

        if filter_territories:
            df = df.query('state != "72"')

        df = df.sort_values(by=['state'])
        return df

    def get_counties(self, fields, state, county='*', sd_cols=False,
                     filter_territories=True):
        """Returns county level data for given state(s) and all provided
           fields.

        Args:
            fields (List of Strings): Fields to return from ACS API.
            state (String or List of Strings): State(s) for which to return
                data.
            county (String or List of Strings, Optional): Counties for which
                to return data (Defaults to '*').
            sd_cols (bool, Optional): Return data with SD formatted column
                names (Defaults to False).
            filter_territories (bool, Optional): Filter out US territories
                from state list (Defaults to True).

        Returns:
            df (DataFrame): DataFrame with county level data for given
                state(s), counties, and all provided fields.
        """
        # Ensure GEO_ID is in field list for indexing df
        fields = list(set(['GEO_ID'] + fields))

        if state != '*':
            if not isinstance(state, list):
                state = [state]
            try:
                st_list = list(map(lambda x: states.lookup(x).fips, state))
            except AttributeError:
                raise ValueError('Invalid state abbreviation')
            state = ','.join(st_list)

        if isinstance(county, list):
            county = ','.join(county)

        data = self.cxn.state_county(fields, state_fips=state,
                                     county_fips=county)
        df = pd.DataFrame(data)

        if sd_cols:
            df = self._sd_col_names(df)
            df = df.set_index('geo_id')
        else:
            df = df.set_index('GEO_ID')

        if filter_territories:
            df = df.query('state != "72"')

        df = df.sort_values(by=['state', 'county'])
        return df

    def get_zips(self, fields, sd_cols=False, filter_territories=True):
        """Returns zip code level data for all provided fields.

        Args:
            fields (List of Strings): Fields to return from the ACS API.
            sd_cols (bool, Optional): Return data with SD formatted column
                names (Defaults to False).
            filter_territories (bool, Optional): Filter out US territories
                from state list (Defaults to True).

        Returns:
            df (DataFrame): DataFrame with zip code level data for all
                provided fields.
        """
        # Ensure GEO_ID is in field list for indexing df
        fields = list(set(['GEO_ID'] + fields))

        data = self.cxn.zipcode(fields, Census.ALL)
        df = pd.DataFrame(data)

        if sd_cols:
            df = self._sd_col_names(df)
            df = df.set_index('geo_id')
        else:
            df = df.set_index('GEO_ID')

        if filter_territories:
            df = df.query('state != "72"')

        return df

    def get_tracts(self, fields, state, county='*', sd_cols=False):
        """Returns census tract level data for given state(s), counties,
           and all provided fields.

        Args:
            fields (List of Strings): Fields to return from the ACS API.
            state (String or List of Strings): State(s) for which to return
                data.
            county (String or List of Strings, Optional): Counties for which
                to return data (Defaults to '*').
            sd_cols (bool, Optional): Return data with SD formatted column
                names (Defaults to False).

        Returns:
            df (DataFrame): DataFrame with census tract level data for given
                state(s), counties, and all provided fields.
        """
        # Ensure GEO_ID is in field list for indexing df
        fields = list(set(['GEO_ID'] + fields))

        if state != '*':
            if not isinstance(state, list):
                state = [state]
            try:
                st_list = list(map(lambda x: states.lookup(x).fips, state))
            except AttributeError:
                raise ValueError('Invalid state abbreviation')
            state = ','.join(st_list)

        if isinstance(county, list):
            county = ','.join(county)

        if state == '*':
            df = pd.DataFrame()

            for st in states.STATES:
                self._logger.info(f'  -- Getting tract-level data for \
                                 {st}: {st.fips}')
                data = self.cxn.state_county_tract(fields, state_fips=st.fips,
                                                   county_fips=county,
                                                   tract=Census.ALL)
                df = df.append(pd.DataFrame(data))
        else:
            data = self.cxn.state_county_tract(fields, state_fips=state,
                                               county_fips=county,
                                               tract=Census.ALL)
            df = pd.DataFrame(data)

        if sd_cols:
            df = self._sd_col_names(df)
            df = df.set_index('geo_id')
        else:
            df = df.set_index('GEO_ID')

        df = df.sort_values(by=['state', 'county'])
        return df

    def get_bg_tract(self, fields, state, county, blockgroup, tract,
                     sd_cols=False):
        """Returns data for a single blockgroup and all provided fields.

           Primarily used for testing individual cases.

        Args:
            fields (List of Strings): Fields to return from ACS API.
            state (String): State for which to return data.
            county (String): County for which to return data.
            blockgroup (String): Blockgroup for which to return data.
            tract (String): Census tract for which to return data.
            sd_cols (bool, Optional): Return data with SD formatted column
                names (Defaults to False).

        Returns:
            df (DataFrame): DataFrame with blockgroup level data for given
                state, county, blockgroup, and census tract, and all
                provided fields.
        """
        data = self.cxn.state_county_blockgroup(fields, state, county,
                                                blockgroup, tract)

        df = pd.DataFrame(data)
        if sd_cols:
            df = self._sd_col_names(df)
            df = df.set_index('geo_id')
        else:
            df = df.set_index('GEO_ID')

        df = df.sort_values(by=['state', 'county'])
        return df

    def get_bgs(self, fields, state, county='*', sd_cols=False):
        """Returns blockgroup level data for given state(s), counties,
           and all provided fields.

        Args:
            fields (List of Strings): Fields to return from the ACS API.
            state (String or List of Strings): State(s) for which to return
                data.
            county (String or List of Strings, Optional): Counties for which
                to return data (Defaults to '*').
            sd_cols (bool, Optional): Return data with SD formatted column
                names (Defaults to False).

        Returns:
            df (DataFrame): DataFrame with blockgroup level data for given
                state(s), counties, and all provided fields.
        """
        # Ensure GEO_ID is in field list for indexing df
        fields = list(set(['GEO_ID'] + fields))

        if state != '*':
            if not isinstance(state, list):
                state = [state]
            try:
                st_list = list(map(lambda x: states.lookup(x).fips, state))
            except AttributeError:
                raise ValueError('Invalid state abbreviation')
        else:
            st_list = self._all_states

        if not isinstance(county, list):
            if county != '*':
                county = [county]

        df = pd.DataFrame()

        for st in st_list:
            self._logger.info(f'  -- Getting block group data for {st}')

            if county == '*':
                cty_list = self._get_county_fips(st)
            else:
                cty_list = county

            for cty in cty_list:
                try:
                    data = self.cxn.get(fields,
                                        {'for': 'block group:*',
                                         'in': f'county:{cty} state:{st}'})
                    df = df.append(pd.DataFrame(data))
                except CensusException:
                    self._logger.info(f'CENSUS ERROR 1: Retrying county {cty}')
                    try:
                        data = self.cxn.get(fields,
                                            {'for': 'block group:*',
                                             'in': f'county:{cty} state:{st}'})
                        df = df.append(pd.DataFrame(data))
                    except CensusException:
                        self._logger.info(f'CENSUS ERROR 2: Retrying county \
                                          {cty}')
                        data = self.cxn.get(fields,
                                            {'for': 'block group:*',
                                             'in': f'county:{cty} state:{st}'})
                        df = df.append(pd.DataFrame(data))

        if sd_cols:
            df = self._sd_col_names(df)
            df = df.set_index('geo_id')
        else:
            df = df.set_index('GEO_ID')

        df = df.sort_values(by=['state', 'county'])
        return df

    def fields_from_regex(self, fld_re='^.*$'):
        """Returns data fields for given regular expression.

        Args:
            fld_re (String or List of Strings, Optional): Regex or list of
                 regexes for the fields desired (Defaults to all fields).

        Returns:
            fields (List): List of all data fields given regular expression,
                plus GEO_ID and NAME.
        """
        if isinstance(fld_re, list):
            fields = []
            for reg in fld_re:
                fields += list(self._all_fields.filter(regex=reg).columns)
            fields = list(set(fields))
        else:
            fields = list(self._all_fields.filter(regex=fld_re).columns)

        fields.sort()

        if not fields:
            self._logger.info(f'Warning: No data fields found matching',
                              f'the regular expression "{fld_re}"')
        fields = ['GEO_ID', 'NAME'] + fields
        return fields

    def fields_from_category(self, category='01A', samples=False):
        """Returns data fields for given ACS categories by full group or
           by samples group.

        Args:
            category (String, Optional): 2 digit code giving the ACS data
                category (Defaults to '01A').
            samples (bool, Optional): Return fields from samples group
                (Defaults to False).

        Returns:
            fields (List): List of all datafields given category, plus
                 GEO_ID and NAME.
            tbl_name (String): String of the standard SD table name.
        """
        try:
            if(samples):
                fld_re = self._acs_samples[category]['reg']
                tbl_name = self._acs_samples[category]['tbl_name']
            else:
                fld_re = self._acs_groups[category]['reg']
                tbl_name = self._acs_groups[category]['tbl_name']
        except KeyError:
            raise ValueError(f'{category} is not a valid data category.')

        fields = self.fields_from_regex(fld_re)

        return fields, tbl_name

    def get_category_list(self):
        """Returns keys for all ACS group tables.

        Returns:
            key (String): Keys for all ACS group tables.
        """
        return self._acs_groups.keys()

    def get_samples_list(self):
        """Returns keys for all ACS sample tables.

        Returns:
            key (String): Keys for all ACS sample tables.
        """
        return self._acs_samples.keys()
