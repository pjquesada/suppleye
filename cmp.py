import BOMdb


def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.
    """

    return (x > y) - (x < y)


def price_cmp(db_file):
    part_list = BOMdb.get_all_octoids_with_sellers(db_file)
    price_change_arr = []
    for part in part_list:
        _octoid = int(part[0])
        _seller = part[1]
        old_part_info = BOMdb.get_from_database(db_file, octoid=_octoid, seller=_seller, base=True)
        latest_part_info = BOMdb.get_from_database(db_file, octoid=_octoid, seller=_seller, base=False)

        if latest_part_info and old_part_info:
            _curr_price = latest_part_info[0][4]
            _prev_price = old_part_info[0][4]
            compare_val = cmp(_curr_price, _prev_price)

            if compare_val == 1:
                _avpn = latest_part_info[0][0]
                _mpn = latest_part_info[0][1]
                _mfr = latest_part_info[0][2]
                _seller = latest_part_info[0][3]
                _stock = latest_part_info[0][5]
                _lead = latest_part_info[0][6]
                _pull_date = latest_part_info[0][7]
                price_change_arr.append((_avpn, _octoid, _mfr, _mpn, _seller, _prev_price, _curr_price, _stock, _lead,
                                         _pull_date))
        else:
            print('DATABASE QUERY ERROR: COULD NOT GET', _octoid, _seller)

    return price_change_arr


def stock_cmp(db_file):
    stock_change_arr = []
    part_list = BOMdb.get_all_octoids_with_sellers(db_file)
    for part in part_list:
        _octoid = int(part[0])
        _seller = part[1]
        old_part_info = BOMdb.get_from_database(db_file, octoid=_octoid, seller=_seller, base=True)
        latest_part_info = BOMdb.get_from_database(db_file, octoid=_octoid, seller=_seller, base=False)

        if latest_part_info and old_part_info:
            _curr_stock = latest_part_info[0][5]
            _prev_stock = old_part_info[0][5]
            compare_val = cmp(_curr_stock, _prev_stock)

            if compare_val == 1:
                _avpn = latest_part_info[0][0]
                _mpn = latest_part_info[0][1]
                _mfr = latest_part_info[0][2]
                _seller = latest_part_info[0][3]
                _price = latest_part_info[0][4]
                _lead = latest_part_info[0][6]
                _pull_date = latest_part_info[0][7]
                stock_change_arr.append((_avpn, _octoid, _mfr, _mpn, _seller, _price, _curr_stock, _prev_stock, _lead,
                                         _pull_date))
        else:
            print('DATABASE QUERY ERROR: COULD NOT GET', _octoid, _seller)

    return stock_change_arr


def lead_cmp(db_file):
    lead_change_arr = []
    part_list = BOMdb.get_all_octoids_with_sellers(db_file)
    for part in part_list:
        _octoid = int(part[0])
        _seller = part[1]
        old_part_info = BOMdb.get_from_database(db_file, octoid=_octoid, seller=_seller, base=True)
        latest_part_info = BOMdb.get_from_database(db_file, octoid=_octoid, seller=_seller, base=False)

        if latest_part_info and old_part_info:
            _curr_lead = latest_part_info[0][6]
            _prev_lead = old_part_info[0][6]
            compare_val = cmp(_curr_lead, _prev_lead)

            if compare_val == 1:
                _avpn = latest_part_info[0][0]
                _mpn = latest_part_info[0][1]
                _mfr = latest_part_info[0][2]
                _seller = latest_part_info[0][3]
                _price = latest_part_info[0][4]
                _stock = latest_part_info[0][5]
                _pull_date = latest_part_info[0][7]
                lead_change_arr.append((_avpn, _octoid, _mfr, _mpn, _seller, _price, _stock, _curr_lead, _prev_lead,
                                        _pull_date))
        else:
            print('DATABASE QUERY ERROR: COULD NOT GET', _octoid, _seller)

    return lead_change_arr