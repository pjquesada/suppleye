import sqlite3
import alert


def get_avpns_from_db(db_file):
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    cursor = conn.cursor()
    sql = '''SELECT DISTINCT parts.avpn FROM parts '''
    db_res = cursor.execute(sql).fetchall()
    conn.close()
    print(db_res)

    return db_res


def get_avpn_parts(db_file, avpn):
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    cursor = conn.cursor()
    sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
    stock.lead_time, stock.pullDate
    FROM parts, stock
    WHERE parts.mpn = stock.mpn AND  parts.mfr = stock.mfr
    AND parts.avpn = '%s'
    AND stock.pullDate = (SELECT MAX(stock.pullDate) FROM stock 
    WHERE stock.mpn = parts.mpn AND parts.avpn = '%s') ''' % (avpn, avpn)
    db_res = cursor.execute(sql).fetchall()
    conn.close()

    return db_res


def get_mpns(avpn_parts):
    mpns = []
    for part in avpn_parts:
        if part[1] not in mpns:
            mpns.append(part[1])

    return mpns


def check_critical_stock(db_file):
    all_avpns = get_avpns_from_db(db_file)
    critical_avpns = []
    for avpn in all_avpns:
        avpn_parts = get_avpn_parts(db_file, avpn[0])
        mpns = get_mpns(avpn_parts)
        total_mpn_stock = 0
        critical_part = 0
        for mpn in mpns:
            critical_stock = 0
            part_count = 0
            for part in avpn_parts:
                if mpn == part[1]:
                    part_count += 1
                    if part[5] < 1000:
                        critical_stock += 1
            if part_count == critical_stock:
                critical_part += 1
        if critical_part == len(mpns):
            critical_avpns.append(avpn_parts)

    return critical_avpns


def critical_stock_db_check(db_file):
    get_avpns_from_db(db_file)
    critical_avpns = check_critical_stock(db_file)
    msg = 'The following part numbers have parts with critically low stock.'
    alert.alert(critical_avpns, msg, critical=True)