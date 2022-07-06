import json

from sanic import Sanic, response
from asyncpg import create_pool


app = Sanic(__name__)


@app.route("/")
async def test(request):
    pool = request.app.config['pool']
    async with pool.acquire() as conn:
        sql = '''
                SELECT *  FROM rates WHERE ISO = 'USD'; 
            '''
        rows = await conn.fetch(sql)
        # return response.json({'status': 200, 'data': jsonify(rows)}, status=200)
        return response.text(json.dumps(rows, indent=4, sort_keys=True, default=str))


@app.listener('before_server_start')
async def register_db(app, loop):
    # Create a database connection pool
    conn = "postgres://{user}:{password}@{host}:{port}/{database}?sslmode=disable" \
        .format(
            user='growens',
            password='alittlebit-1729',
            host='growens-db',
            port=2345,
            database='currencies'
        )
    app.config['pool'] = await create_pool(
        dsn=conn,
        # in bytes
        min_size=10,
        # in bytes
        max_size=1000,
        # maximum query
        max_queries=50000,
        # maximum idle times
        max_inactive_connection_lifetime=300,
        loop=loop)


@app.listener('after_server_stop')
async def close_connection(app, loop):
    pool = app.config['pool']
    async with pool.acquire() as conn:
        await conn.close()


def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    list_return = []
    for r in records:
        itens = r.items()
        list_return.append({i[0]: i[1].rstrip() if type(
            i[1]) == str else i[1] for i in itens})
    return list_return


if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=8282,
            access_log=True,
            debug=True)
    # import datetime
    # import asyncio
    # import pandas as pd
    # import numpy as np
    # df = pd.read_csv(CSV_FILE, header=0)
    # # currency = USD()
    # # print(currency.get_records())
    # # print(df.columns)
    # # # world_rate_list = df.loc[:, [col for col in df.columns if col in ('Rate', 'Country', 'Reference date (CET)')]]
    # usd_selection = df.loc[df['ISO Code'] == 'USD']
    # # dkk_selection = df.loc[df['ISO Code'] == 'DKK']
    # print("USD:", usd_selection['Rate'].max(), "at", usd_selection['Reference date (CET)'].unique())
    # # print("DKK", dkk_selection['Rate'].max(), "at", dkk_selection['Reference date (CET)'].unique())
