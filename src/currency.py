"""
This metapython quick and wrong code is only an example, less of a POC, it should be made for Sanic framework
Cloud -> Kubernates
                    -> PODS docker web gui interfaaces -> Database for users
                    -> PODS docker with Sanic Framework -> Database with partition tables (not mixed currency data)
                    -> PODS docker application that control and downloads csv file and share

Monitoring: Grafana or as you wish
Scheduling: Sanic is framework for async process, no more cronjobs
"""
import datetime
import asyncio
import asyncpg
import pandas as pd
import numpy as np
from sanic import Sanic, response




CSV_PATH = '/usr/local/app/csv/'
CSV_FILE = CSV_PATH + 'daily_rates_20211228.csv'

app = Sanic(__name__)


@app.listener('before_server_start')
async def register_db(app, loop):
    # Create a database connection pool
    conn = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user='growens',
        password='growens',
        host='postgresql',
        port=5432,
        database='currencies'
    )
    app.config['pool'] = await asyncpg.create_pool(
        dsn=conn,
        min_size=10,
        max_size=10,
        max_queries=50000,
        max_inactive_connection_lifetime=300,
        loop=loop)


@app.listener('after_server_stop')
async def close_connection(app, loop):
    pool = app.config['pool']
    async with pool.acquire() as conn:
        await conn.close()


async def server(request):
    # return response.json({"test": True})
    currency = USD()
    return currency.db_connection


@app.route('/usd')
async def test(request):
    pool = request.app.config['pool']
    async with pool.acquire() as conn:
        sql = '''SELECT * FROM rates WHERE ISO = '{iso}'; '''\
            .format(request.app.iso_ccode)
        rows = await conn.fetch(sql)
        return response.text(rows)

# @app.route('/usd')
# async def usd(request):
#     df = pd.read_csv(CSV_FILE, header=0)
#     usd_selection = df.loc[df['ISO Code'] == 'USD']
#     max = "USD: {max}, at {date}" \
#                     .format(max=usd_selection['Rate'].max(),
#                             date=usd_selection['Reference date (CET)'].unique())
#     return response.text(max)


class Currency():
    """Main Class for currency"""
    main_currency_iso_code = "EU"

    def __init__(self, country=None, iso_code=None, start_datetime=None, end_datetime=None):
        self.iso_code = iso_code
        self.country = country
        self.start_datetime = start_datetime or datetime.datetime.utcnow()
        self.end_datetime = end_datetime or datetime.datetime.utcnow()
        self.db_connection = None
        try:
            self.db_connection = register_db
            values = await db_connection
            #     .fetch(
            #     'SELECT * FROM mytable WHERE id = $1',
            #     10,
            # )
            # await conn.close()

            if not self.verify_last_import():
                self.import_data()
        except Exception as e:
            return print("DB connection fault")
        else:
            print("Here I am:", self.iso_code)

        try:
            if not self.verify_import_by_date():
                self.import_data()
        except Exception as e:
            return print("DB import fault")
        else:
            print("Data imported for:", self.iso_code)

    async def db_connect(self):
        print("DB connection ready")


        # declare the connection string specifying
        # the host name database name use name
        # and password
        conn_string = "host='postgresql' dbname='growens' user='growens' password='growens'"

        # use connect function to establish the connection
        return psycopg2.connect(conn_string)

    def import_data(self):
        print(b"Imported data from csv file to db for", self.iso_code)

    def verify_import_by_date(self):
        pass

    @staticmethod
    def average_rate(self):
        """ Average Rate """
        print(b"Average Rate for", self.iso_code)

    @staticmethod
    def highest_rate(self):
        """ Highest Rate """
        print(b"Max Rate for {iso_code}", self.iso_code)

    @staticmethod
    def minimum_rate(self):
        """ Minimum Rate """
        print(b"Min Rate for", self.iso_code)


class USD(Currency):
    def __init__(self, start_datetime, end_datetime):
        super().__init__(start_datetime, end_datetime)
        self.iso_code = "USD"
        self.country = "UNITED STATES"


class DKK(Currency):
    def __init__(self, start_datetime=None, end_datetime=None):
        super().__init__(start_datetime, end_datetime)
        self.iso_code = "DKK"
        self.country = "DENMARK"


if __name__ == "__main__":
    #
    app.run(host="0.0.0.0", port=8181)

    # df = pd.read_csv(CSV_FILE, header=0)
    # print(df.columns)
    # # world_rate_list = df.loc[:, [col for col in df.columns if col in ('Rate', 'Country', 'Reference date (CET)')]]
    # usd_selection = df.loc[df['ISO Code'] == 'USD']
    # dkk_selection = df.loc[df['ISO Code'] == 'DKK']
    # print("USD:", usd_selection['Rate'].max(), "at", usd_selection['Reference date (CET)'].unique())
    # print("DKK", dkk_selection['Rate'].max(), "at", dkk_selection['Reference date (CET)'].unique())

