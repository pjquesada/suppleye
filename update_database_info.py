import datetime
import json
import sqlite3
import octoqueries


def get_octoid_from_db(db_file):
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    cursor = conn.cursor()
    sql = '''SELECT DISTINCT parts.avpn, parts.octoid, parts.mpn FROM parts '''
    db_res = cursor.execute(sql).fetchall()
    conn.close()
    print(db_res)

    return db_res


def get_id_list(all_parts):
    """
    This function is used to create a list of OctoPart ids to use for a query as demonstrated in the OctoPart API
    Getting started guide example Python Client.
    """
    id_list = []
    for part in all_parts:
        octoid = part[1]
        id_list.append(octoid)

    return id_list


def query_database_parts(client, all_parts):
    id_list = get_id_list(all_parts)
    resp = octoqueries.octoid_query(client, id_list)

    return resp


def get_avpn_key(mpn, octoid, all_parts):
    avpn_key = None
    for part in all_parts:
        if mpn == part[2]:
            if octoid == part[1]:
                avpn_key = part[0]
                break

    return avpn_key


def store_part_info(resp, database_parts_dict):
    resp_list = json.loads(resp)
    seller_description = 'N/A'
    _approved_distributors = ['Digi-Key', 'Mouser', 'Arrow', 'Avnet']
    if resp_list['data']:
        for part in resp_list['data']['parts']:
            if part['sellers']:
                _octoid = int(part['id'])
                _mpn = part['mpn']
                _mfr = part['manufacturer']['name']
                for seller in part['sellers']:
                    total_seller_inventory = 0
                    seller_prices = []
                    seller_lead_times = []
                    if seller['company']['name'] in _approved_distributors:
                        _seller_name = seller['company']['name']
                        for offer in seller['offers']:
                            if offer['inventory_level'] is not None:
                                total_seller_inventory += offer['inventory_level']
                            if offer['prices']:
                                seller_prices.append(offer['prices'][0]['price'])
                            if offer['factory_lead_days'] is not None:
                                if offer['factory_lead_days'] is str:
                                    seller_lead_times.append(9999)
                                else:
                                    seller_lead_times.append(offer['factory_lead_days'])
                            else:
                                seller_lead_times.append(9999)
                        if len(seller_prices) == 0:
                            seller_avg_price = 0
                        else:
                            seller_avg_price = round(((sum(seller_prices)) / (len(seller_prices))), 3)
                        low_lead_time = min(seller_lead_times)
                        if part['short_description']:
                            seller_description = part['short_description']
                        part_dict_data = {'manufacturer': _mfr, 'seller': _seller_name, 'price': seller_avg_price,
                                          'stock': total_seller_inventory, 'lead': low_lead_time,
                                          'description': seller_description}
                        for avpn in database_parts_dict:
                            if _mpn in database_parts_dict[avpn].keys():
                                if database_parts_dict[avpn][_mpn]:
                                    if _octoid in database_parts_dict[avpn][_mpn].keys():
                                        database_parts_dict[avpn][_mpn][_octoid].append(part_dict_data)
                                        break

    return database_parts_dict


def get_query_info(client, all_parts):
    database_parts_dict = {}
    for part in all_parts:
        _avpn = part[0]
        _octoid = part[1]
        _mpn = part[2]
        if _avpn in database_parts_dict.keys():
            if _mpn in database_parts_dict[_avpn].keys():
                if _octoid not in database_parts_dict[_avpn][_mpn].keys():
                    database_parts_dict[_avpn][_mpn][_octoid] = []
            else:
                database_parts_dict[_avpn][_mpn] = {}
                database_parts_dict[_avpn][_mpn][_octoid] = []
        else:
            database_parts_dict[_avpn] = {}
            database_parts_dict[_avpn][_mpn] = {}
            database_parts_dict[_avpn][_mpn][_octoid] = []
    resp = query_database_parts(client, all_parts)
    store_part_info(resp, database_parts_dict)

    return database_parts_dict


def add_parts_to_database(db_file, database_parts_dict):
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    cursor = conn.cursor()
    today = datetime.date.today()
    inactive = 0
    to_parts_table = []
    to_stock_table = []
    for avpn in database_parts_dict:
        for mpn in database_parts_dict[avpn]:
            for octoid in database_parts_dict[avpn][mpn]:
                for part in database_parts_dict[avpn][mpn][octoid]:
                    to_parts_table.append((octoid, part['manufacturer'], mpn, avpn, inactive))
                    to_stock_table.append((octoid, part['manufacturer'], part['seller'], part['price'],
                                           part['stock'], part['lead'], mpn, today))
    cursor.executemany("INSERT OR IGNORE INTO parts(octoid, mfr, mpn, avpn, inactive) VALUES (?, ?, ?, ?, ?);",
                       to_parts_table)
    cursor.executemany("INSERT INTO stock(octoid, mfr, seller, price, total_stock, lead_time, mpn, pullDate) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_stock_table)
    cursor.execute("DELETE FROM parts WHERE rowid NOT IN(SELECT MIN(rowid) FROM parts GROUP BY octoid, mfr, mpn)")

    conn.commit()
    conn.close()


def update_db_info(client, db_file):
    all_parts = get_octoid_from_db(db_file)
    database_parts_info = get_query_info(client, all_parts)
    add_parts_to_database(db_file, database_parts_info)