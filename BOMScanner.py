import json
import csv
import re
import cmp
import alert
import octoqueries
import BOMdb
import GraphQLClient
import update_database_info
import get_critical_stock


def get_info_string(file_path):
    """
    This function is used to extract and format a string from the mpns extracted from the BOM file to be used for
    a query.
    """
    info_arr = []
    pattern = re.compile(pattern=r'\d{1,3}\x09\d{3}-\d{4}\x09[a-zA-Z0-9-\,\.\/\x20]+')
    with open(file_path) as fh:
        for line in fh:
            rev = pattern.findall(string=line)
            if 0 < len(rev):
                for item in rev:
                    index = rev.index(item)
                    rev[index] = rev[index].replace("\t", ' ')
                    rev = item.split()
                info_arr.append(rev)

    return info_arr


def dict_init(file_path):
    bom_part_info = {}
    info_arr = get_info_string(file_path)
    for line in info_arr:
        _avpn = line[1]
        _mpn = line[2]
        if _avpn not in bom_part_info:
            bom_part_info[_avpn] = {}
        if _mpn not in bom_part_info[_avpn]:
            bom_part_info[_avpn][_mpn] = None

    return bom_part_info


def get_mpn_from_file(file_path):
    mpn_list = []
    pattern = re.compile(pattern=r'\d{1,3}\x09\d{3}-\d{4}\x09[a-zA-Z0-9-\,\.\/\x20]+')
    with open(file_path) as fh:
        for line in fh:
            rev = pattern.findall(string=line)
            if 0 < len(rev):
                for item in rev:
                    index = rev.index(item)
                    rev[index] = rev[index].replace("\t", ' ')
                    rev = item.split()
                mpn_list.append(rev[2])

    return mpn_list


def id_parser(client, file_path):
    """
    This function parses and stores the API data on each part into its corresponding Part class. The json object
    is converted into a dictionary using the json python module function loads() in order to be parsed.
    """
    mpn_list = get_mpn_from_file(file_path)
    resp = octoqueries.mpn_query(client, mpn_list)
    resp_list = json.loads(resp)
    bom_part_info = dict_init(file_path)
    if resp_list['data']:
        for part_result in resp_list['data']['multi_match']:
            _avpn_key = 0
            if part_result['hits'] > 1:
                for part in part_result['parts']:
                    for avpn in bom_part_info:
                        if part['mpn'] in bom_part_info[avpn]:
                            if not bom_part_info[avpn][part['mpn']]:
                                _avpn_key = avpn
            else:
                for avpn in bom_part_info:
                    if part_result['parts']:
                        if part_result['parts'][0]['mpn'] in bom_part_info[avpn].keys():
                            _avpn_key = avpn
                            break
            for part in part_result['parts']:
                if part['id'] is None:
                    octoid = 'N/A'
                else:
                    octoid = part['id']
                if part['mpn'] is None:
                    mpn = 'N/A'
                else:
                    mpn = part['mpn']
                if _avpn_key != 0:
                    if mpn not in bom_part_info[_avpn_key]:
                        bom_part_info[_avpn_key][mpn] = {}
                        bom_part_info[_avpn_key][mpn][octoid] = []
                    if bom_part_info[_avpn_key][mpn] is None:
                        bom_part_info[_avpn_key][mpn] = {}
                        bom_part_info[_avpn_key][mpn][octoid] = []
                    if mpn in bom_part_info[_avpn_key]:
                        if octoid not in bom_part_info[_avpn_key][mpn]:
                            bom_part_info[_avpn_key][mpn][octoid] = []

    return bom_part_info


def get_id_list(bom_part_info):
    """
    This function is used to create a list of OctoPart ids to use for a query as demonstrated in the OctoPart API
    Getting started guide example Python Client.
    """
    id_list = []
    for avpn in bom_part_info:
        for mpn in bom_part_info[avpn]:
            if bom_part_info[avpn][mpn]:
                for octoid in bom_part_info[avpn][mpn]:
                    id_list.append(octoid)

    return id_list


def mpn_avpn_match(mpn, octoid, bom_part_info):
    avpn_key = None
    for avpn in bom_part_info:
        if bom_part_info[avpn]:
            if mpn in bom_part_info[avpn]:
                if bom_part_info[avpn][mpn]:
                    if octoid in bom_part_info[avpn][mpn]:
                        avpn_key = avpn
    return avpn_key


def info_parser(client, file_path):
    bom_part_info = id_parser(client, file_path)
    id_list = get_id_list(bom_part_info)
    resp = octoqueries.octoid_query(client, id_list)
    part_info = []
    _approved_distributors = ['Digi-Key', 'Mouser', 'Arrow', 'Avnet']
    resp_list = json.loads(resp)
    if resp_list['data']:
        for part in resp_list['data']['parts']:
            if part['sellers']:
                _octoid = part['id']
                _mpn = part['mpn']
                _mfr = part['manufacturer']['name']
                _avpn = mpn_avpn_match(_mpn, _octoid, bom_part_info)
                for seller in part['sellers']:
                    total_seller_inventory = 0
                    seller_prices = []
                    seller_lead_times = []
                    seller_description = 'N/A'
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
                        seller_avg_price = round(((sum(seller_prices)) / (len(seller_prices))), 3)
                        low_lead_time = min(seller_lead_times)
                        if part['short_description']:
                            seller_description = part['short_description']
                        part_dict_data = {'manufacturer': _mfr, 'seller': _seller_name, 'price': seller_avg_price,
                                          'stock': total_seller_inventory, 'lead': low_lead_time,
                                          'description': seller_description}
                        bom_part_info[_avpn][_mpn][_octoid].append(part_dict_data)

    return bom_part_info


def path_to_name(file_path):
    """ This function extracts the name of the file from the file path."""
    try:
        found = re.search('OCTODraft/(.+?).BOM', file_path).group(1)
    except AttributeError:
        print('Name not extracted')
        found = 'NONAME'
    return found


def to_csv(name, mparts):  # direct to sqlite
    """
    This function creates a csv file from the part information stored in the dictionary of part classes to be used
    for sending email alerts.
    """
    csv_file_name = "%s_CSV.csv" % name
    with open(csv_file_name, mode='w') as csv_file:
        fieldnames = ['AVPN', 'OCTO-ID', 'MFR', 'MPN', 'QTY', 'PRICE', 'STOCK', 'DESCRIPTION']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for i in mparts:
            temp = mparts[i]
            for val in temp.octoid:
                pos_num = temp.octoid.index(val)

                _avpn = temp.avpn
                _id = temp.octoid[pos_num]
                _mfr = temp.mfr[pos_num]
                _mpn = temp.mpn[pos_num]
                _qty = temp.qty
                _price = temp.avg_price[pos_num]
                _stock = temp.stock
                _desc = temp.description[pos_num]

            writer.writerow({'AVPN': _avpn, 'OCTO-ID': _id, 'MFR': _mfr, 'MPN': _mpn,
                             'QTY': _qty, 'PRICE': _price, 'STOCK': _stock, 'DESCRIPTION': _desc})

    return csv_file


def check_database(db_file):
    """
    This function uses the prviously defined compare function and get_from_database function to look up previous
    part data and compare it with current part data. If the compare function returns a specififc output it will send
    an alert with its corresponding alert message and subject field.
    """
    price_change_parts = cmp.price_cmp(db_file)
    stock_change_parts = cmp.stock_cmp(db_file)
    lead_time_change_parts = cmp.lead_cmp(db_file)

    if price_change_parts:
        price_msg = 'The price for the following item(s) has increased.'
        alert.alert(price_change_parts, price_msg, price=True)
    if stock_change_parts:
        stock_msg = 'The stock quantity of the following item(s) had decreased.'
        alert.alert(price_change_parts, stock_msg, stock=True)
    if lead_time_change_parts:
        lead_msg = 'The lead time for the following item(s) has increased'
        alert.alert(price_change_parts, lead_msg, lead=True)


if __name__ == '__main__':
    client = GraphQLClient.GraphQLClient('https://octopart.com/api/v4/endpoint')
    client.inject_token('OCTOPART API KEY')
    bom_file_path = r'BILL OF MATERIALS CSV FILE LOCATION'
    db_file = r"DATABASE FILE LOCATION"
    print('START \n')

    bom_part_info = info_parser(client, bom_file_path)
    '''BOMdb.sql_boot(db_file) creates database at file location'''
    # BOMdb.sql_boot(db_file)
    BOMdb.add_to_database(db_file, bom_part_info)
    check_database(db_file)

    print('\nDONE')

"""                  BOMscanner.py ©                 """
"""     Created By Pablo J. Quesada August 2021      """
