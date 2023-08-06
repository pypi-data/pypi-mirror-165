import io
import os
import gzip
import time
import typing
import logging
import sqlite3

import arrow
import pandas
import requests

from .helpers import get_domain


class GoatPie:
    """
    'Goatcounter' analytics at your fingertips
    """

    # Base URL
    url: str = 'https://example.goatcounter.com'


    # Request headers
    headers: dict = {'Content-type': 'application/json'}


    # Database
    db: sqlite3.Connection


    # Minimum update interval (in seconds)
    interval = 1 * 60 * 60  # 1 hour


    def __init__(self, url: str, token: str, data_dir: str = '.tmp') -> None:
        """
        Creates 'GoatPie' instance

        :param url: str API token
        :param token: str API token
        :param data_dir: str Data directory

        :return: None
        """

        # Store base URL
        self.url = url

        # Add API token
        self.headers['Authorization'] = 'Bearer {}'.format(token)

        # Store data directory
        self.data_dir = data_dir

        # Create data directory (if needed)
        os.makedirs(data_dir, exist_ok=True)

        # Initialize logger
        self.logger = self.get_logger(data_dir)

        # Connect to database
        db_file = os.path.join(data_dir, 'db.sqlite')
        self.db = sqlite3.connect(db_file)

        # Populate database
        self.update()


    def fetch(self, endpoint: str, json: dict = {}) -> requests.Response:
        """
        Fetches data from 'Goatcounter' API

        :param endpoint: str API endpoint
        :param first_id: int First entry
        :param method: str HTTP method

        :return: requests.Response
        """

        # Prepare request
        # (1) Define HTTP method
        method = 'post' if endpoint == 'export' else 'get'

        # (2) Build target URL
        base = '{}/api/v0/{}'.format(self.url, endpoint)

        # Call API
        return getattr(requests, method)(base, headers=self.headers, json=json)


    def export(self, first_id: int = 0) -> int:
        """
        Triggers generation of new export

        :param first_id: int Index of first entry

        :return: int Export identifier
        :throws: Exception Something went wrong
        """

        # Call API
        response = self.fetch('export', {'start_from_hit_id': first_id})

        # Get JSON response data
        data = response.json()

        # If error occurred ..
        if 'error' in data:
            # .. report back
            raise Exception(data['error'])

        # Determine remaining API (= rate limit)
        remaining = response.headers['X-Rate-Limit-Remaining']

        # If rate limit is (about to be) exceeded ..
        if int(remaining) < 2:
            # .. wait until next reset happens
            until_reset = response.headers['X-Rate-Limit-Reset']

            # .. report back
            self.logger.info('Rate limit exceeded, waiting for reset in {} seconds ..'.format(until_reset))

            # Bide the time
            time.sleep(int(until_reset))

        return data['id']


    def status(self, idx: int) -> dict:
        """
        Checks progress of triggered export

        :param idx: int Export identifier

        :return: dict Status report
        """

        return self.fetch('export/{}'.format(idx)).json()


    def download(self, idx: int) -> str:
        """
        Initiates download of finished export

        :param idx: int Export identifier

        :return: str Exported CSV data
        :throws: Exception Invalid response code
        """

        # Fetch archive
        response = self.fetch('export/{}/download'.format(idx))

        # If status code indicates error ..
        if response.status_code not in [200, 202]:
            # .. report back
            raise Exception('{}: {}'.format(response.status_code, response.content.decode('utf-8')))

        # Unzip & stringify data
        return gzip.decompress(response.content).decode('utf-8')


    def update(self, last_update: int = 1 * 60 * 60) -> None:
        """
        Fetches analytics data & inserts it into local database

        :param last_update: int Minimum timespan since last update (in seconds)

        :return: None
        """

        # Define file containing next entry
        id_file = os.path.join(self.data_dir, '.next_idx')

        try:
            # If identifier file not present ..
            if not os.path.exists(id_file):
                # .. create it
                with open(id_file, 'w') as file:
                    file.write('0')

            # Get last modification & current time
            modified = arrow.get(os.path.getmtime(id_file))
            just_now = arrow.utcnow().to('local')

            # If time since last modification lesser than this ..
            if arrow.get(modified) > just_now.shift(seconds=-last_update):
                # .. do not update database (unless forced to)
                if last_update > 0:
                    # Get human-readable interval since last export
                    interval = arrow.get(modified).humanize()
                    feedback = interval if interval == 'just now' else 'less than {}'.format(interval)

                    # Report back
                    raise Exception('Last update was {}, skipping ..'.format(feedback))

            # Append data if database table already exists
            if_exists = 'append'

            # Attempt to ..
            try:
                # .. load identifier of next entry
                with open(id_file, 'r') as file:
                    first_id = int(file.read())

            # .. but if something goes south & table already exists ..
            except:
                # .. replace it instead of appending to it
                if_exists = 'replace'

            # Initiate data export & get export index
            idx = self.export(first_id or 0)

            # Enter indefinite loop
            while True:
                # Wait a ..
                time.sleep(1)

                # Receive export status
                status = self.status(idx)

                # Check export status
                if status['finished_at'] is None:
                    continue

                # If no new data available ..
                if status['num_rows'] == 0:
                    # .. store current time (preventing further requests)
                    timestamp = arrow.utcnow().to('local').timestamp()
                    os.utime(id_file, (timestamp, timestamp))

                    # .. report back
                    raise Exception('No new data, skipping ..')

                # Fetch string containing CSV data
                content = self.download(idx)

                # Load data into dataframe & store in database
                df = pandas.read_csv(io.StringIO(content))
                df.to_sql('data', self.db, if_exists=if_exists, index=False)

                # Update identifier of last entry
                with open(id_file, 'w') as file:
                    file.write(str(int(status['last_hit_id']) + 1))

                # Step out of the loop
                break

        except Exception as error:
            # Capture stack trace
            self.logger.exception('Something went wrong')


    def execute(self, command: str) -> pandas.DataFrame:
        """
        Executes SQL command against database

        :return: pandas.DataFrame
        :throws: Exception Something went wrong
        """

        try:
            return pandas.read_sql(command, self.db)

        except Exception as error:
            # Capture stack trace
            self.logger.exception('Something went wrong')

            # Reraise exception
            raise


    def get_referrers(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most commonly used referrers

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) No internal links
        # (3) Group by referrer
        # (4) Sort by count
        # (5) Last XY entries
        referrers = self.execute('''
            SELECT count(Referrer) as Total, Referrer
            FROM data
            WHERE Bot == 0 AND Referrer NOT LIKE "%{}%"
            GROUP BY Referrer
            ORDER BY Total DESC
            LIMIT {}
        '''.format(get_domain(self.url), limit))

        # Add percentages
        referrers['%'] = round(referrers['Total'] / referrers['Total'].sum() * 100, 1)

        return referrers


    def get_pages(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most commonly visited pages

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by path
        # (3) Sort by count
        # (4) Last XY entries
        pages = self.execute('''
            SELECT count("2Path") as Total, "2Path" as Page
            FROM data
            WHERE Bot == 0
            GROUP BY Page
            ORDER BY Total DESC
            LIMIT {}
        '''.format(limit))

        # Add percentages
        pages['%'] = round(pages['Total'] / pages['Total'].sum() * 100, 1)

        return pages


    def get_browsers(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most commonly used browsers

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by browser
        # (3) Sort by count
        # (4) Last XY entries
        browsers = self.execute('''
            SELECT count(Browser) as Total, Browser
            FROM data
            WHERE Bot == 0
            GROUP BY Browser
            ORDER BY Total DESC
            LIMIT {}
        '''.format(limit))

        # Add percentages
        browsers['%'] = round(browsers['Total'] / browsers['Total'].sum() * 100, 1)

        return browsers


    def get_systems(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most commonly used operating systems

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by system
        # (3) Sort by count
        # (4) Last XY entries
        systems = self.execute('''
            SELECT count(System) as Total, System
            FROM data
            WHERE Bot == 0
            GROUP BY System
            ORDER BY Total DESC
            LIMIT {}
        '''.format(limit))

        # Add percentages
        systems['%'] = round(systems['Total'] / systems['Total'].sum() * 100, 1)

        return systems


    def get_pageviews(self, limit: int = 14) -> pandas.DataFrame:
        """
        Provides (limited set of) pageviews (= total hits) per day

        :param limit: int Limits data to last XY days

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by day
        # (3) Last XY days
        pageviews = self.execute('''
            SELECT strftime("%Y-%m-%d", Date) as Day, count(*) as Pageviews
            FROM data
            WHERE Bot == 0
            GROUP BY Day
            ORDER BY Day DESC
            LIMIT {}
        '''.format(limit))

        return pageviews


    def get_visits(self, limit: int = 14) -> pandas.DataFrame:
        """
        Provides (limited set of) visits (= unique users) per day

        :param limit: int Limits data to last XY days

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by day
        # (3) Last XY days
        visits = self.execute('''
            SELECT strftime("%Y-%m-%d", Date) as Day, count(distinct Session) as Visits
            FROM data
            WHERE Bot == 0
            GROUP BY Day
            ORDER BY Day DESC
            LIMIT {}
        '''.format(limit))

        return visits


    # Helper functions

    def get_logger(self, log_dir: str) -> logging.Logger:
        """
        Initializes logger

        :param log_dir: str Path to logfile

        :return: logging.Logger
        """

        # Import module
        from logging.handlers import RotatingFileHandler

        # Initialize logger & set logging level
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Create handler
        handler = RotatingFileHandler(os.path.join(log_dir, 'debug.log'), maxBytes=10000)

        # Format logfile content
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

        return logger
