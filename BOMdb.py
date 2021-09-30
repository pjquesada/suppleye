import datetime
import sqlite3


def sql_boot(db_file):
    """
    This function creates a SQLite database to store all part information using sqlite3. Each table is created
    with rowid as the primary key. The product table is linked to the parts table by mpn, and the parts table is
    linked to the stock table by OctoPart id or octoid, as listed. The database name and location are configurable.
    """
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    curs = conn.cursor()

    create_parts_table = '''CREATE TABLE parts(
        octoid INTEGER PRIMARY KEY NOT NULL,
        mfr TEXT NOT NULL,
        mpn TEXT NOT NULL,
        avpn TEXT NOT NULL,
        inactive TEXT NOT NULL);'''
    curs.execute(create_parts_table)

    create_stock_table = '''CREATE TABLE stock(
        rowid INTEGER PRIMARY KEY AUTOINCREMENT,
        octoid INTEGER NOT NULL,
        mfr TEXT,
        seller TEXT,
        price REAL,
        total_stock INTEGER,
        lead_time TEXT,
        mpn TEXT,
        pullDate NUMBER);'''
    curs.execute(create_stock_table)

    create_product_table = '''CREATE TABLE product(
        rowid INTEGER PRIMARY KEY AUTOINCREMENT,
        octoid INTEGER NOT NULL,
        productID TEXT NOT NULL,
        boardID TEXT NOT NULL,
        mpn TEXT);'''
    curs.execute(create_product_table)

    conn.commit()
    conn.close()


def add_to_database(db_file, bom_part_info):
    """
    This function organizes part data to be stored in the database via insert query. Any duplicate information in
    the parts table is deleted. No method of adding into the product table because there needs to be a standard way
    to list product names in the file name as well as board names.
    """
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    curs = conn.cursor()
    today = datetime.date.today()
    inactive = 0
    if bom_part_info:
        to_board = []
        to_parts_table = []
        to_stock_table = []
        for avpn in bom_part_info:
            if bom_part_info[avpn]:
                for mpn in bom_part_info[avpn]:
                    if bom_part_info[avpn][mpn]:
                        for octoid in bom_part_info[avpn][mpn]:
                            if bom_part_info[avpn][mpn][octoid]:
                                for part_info in bom_part_info[avpn][mpn][octoid]:
                                    to_parts_table.append((octoid, part_info['manufacturer'], mpn, avpn, inactive))
                                    to_stock_table.append((octoid, part_info['manufacturer'], part_info['seller'],
                                                           part_info['price'], part_info['stock'],
                                                           part_info['lead'], mpn, today))
        curs.executemany("INSERT OR IGNORE INTO parts(octoid, mfr, mpn, avpn, inactive) VALUES (?, ?, ?, ?, ?);",
                         to_parts_table)
        curs.executemany("INSERT INTO stock(octoid, mfr, seller, price, total_stock, lead_time, mpn, pullDate) "
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_stock_table)
        curs.execute("DELETE FROM parts WHERE rowid NOT IN(SELECT MIN(rowid) FROM parts GROUP BY octoid, mfr, mpn)")

    conn.commit()
    conn.close()


def get_present_info_with_seller(db_file, mpn=None, octoid=None, seller=None):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    if mpn and seller:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.mpn = stock.mpn AND  parts.mfr = stock.mfr
        AND parts.mpn = '%s' AND stock.seller = '%s' 
        AND stock.pullDate = (SELECT MAX(stock.pullDate) FROM stock 
        WHERE stock.mpn = parts.mpn AND stock.mpn = '%s')  ''' % (mpn, seller, mpn)
        db_res = curs.execute(sql).fetchall()
    elif octoid and seller:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.octoid = stock.octoid AND  parts.mpn = stock.mpn
        AND parts.octoid = '%s' AND stock.seller = '%s' 
        AND stock.pullDate = (SELECT MAX(stock.pullDate) FROM stock 
        WHERE stock.mpn = parts.mpn AND stock.octoid = '%s')  ''' % (octoid, seller, octoid)
        db_res = curs.execute(sql).fetchall()
    else:
        db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'
    conn.close()

    return db_res


def get_present_info(db_file, mpn=None, octoid=None):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    if mpn:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.mpn = stock.mpn AND  parts.mfr = stock.mfr
        AND parts.mpn = '%s'
        AND stock.pullDate = (SELECT MAX(stock.pullDate) FROM stock 
        WHERE stock.mpn = parts.mpn AND stock.mpn = '%s') ''' % (mpn, mpn)
        db_res = curs.execute(sql).fetchall()
    elif octoid:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.octoid = stock.octoid AND  parts.mpn = stock.mpn
        AND parts.octoid = '%s'
        AND stock.pullDate = (SELECT MAX(stock.pullDate) FROM stock 
        WHERE stock.mpn = parts.mpn AND stock.octoid = '%s') ''' % (octoid, octoid)
        db_res = curs.execute(sql).fetchall()
    else:
        db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'
    conn.close()

    return db_res


def get_prev_info_with_seller(db_file, mpn=None, octoid=None, seller=None):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    today = datetime.date.today()
    days = datetime.timedelta(days=90)
    base_date = today - days
    if mpn and seller:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.mpn = stock.mpn AND  parts.mfr = stock.mfr
        AND parts.mpn = '%s' AND stock.pullDate = '%s' AND stock.seller = '%s' 
        GROUP BY stock.mpn, stock.mfr, stock.seller ''' % (mpn, base_date, seller)
        db_res = curs.execute(sql).fetchall()
    elif octoid and seller:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.octoid = stock.octoid AND  parts.mpn = stock.mpn
        AND parts.octoid = '%s' AND stock.pullDate = '%s' AND stock.seller = '%s' 
        GROUP BY stock.mpn, stock.mfr, stock.seller ''' % (octoid, base_date, seller)
        db_res = curs.execute(sql).fetchall()
    else:
        db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'
    conn.close()

    return db_res


def get_prev_info(db_file, mpn=None, octoid=None):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    today = datetime.date.today()
    days = datetime.timedelta(days=90)
    base_date = today - days
    if mpn:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.mpn = stock.mpn AND  parts.mfr = stock.mfr
        AND parts.mpn = '%s' AND stock.pullDate = '%s' ''' % (mpn, base_date)
        db_res = curs.execute(sql).fetchall()
    elif octoid:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.octoid = stock.octoid AND  parts.mpn = stock.mpn
        AND parts.octoid = '%s' AND stock.pullDate = '%s' ''' % (octoid, base_date)
        db_res = curs.execute(sql).fetchall()
    else:
        db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'
    conn.close()

    return db_res


def get_earliest_part_info_with_seller(db_file, mpn=None, octoid=None, seller=None):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    if mpn and seller:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate 
        FROM parts, stock 
        WHERE stock.mpn = parts.mpn AND stock.mpn = '%s' AND stock.seller = '%s' AND 
        stock.pullDate = (SELECT MIN(stock.pullDate) FROM stock 
        WHERE stock.mpn = parts.mpn AND stock.mpn = '%s') 
        GROUP BY stock.mpn, stock.mfr, stock.seller ''' % (mpn, seller, mpn)
        db_res = curs.execute(sql).fetchall()
    if octoid and seller:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate 
        FROM parts, stock 
        WHERE parts.octoid = stock.octoid AND  parts.mpn = stock.mpn AND parts.octoid = '%s' AND 
        stock.seller = '%s' AND stock.pullDate = (SELECT MIN(stock.pullDate) 
        FROM stock WHERE stock.mpn = parts.mpn AND stock.octoid = '%s') 
        GROUP BY stock.mpn, stock.mfr, stock.seller ''' % (octoid, seller, octoid)
        db_res = curs.execute(sql).fetchall()
    else:
        db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'
    conn.close()

    return db_res


def get_earliest_part_info(db_file, mpn=None, octoid=None):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    if mpn:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate 
        FROM parts, stock 
        WHERE stock.mpn = parts.mpn AND stock.mpn = '%s' AND 
        stock.pullDate = (SELECT MIN(stock.pullDate) FROM stock 
        WHERE stock.mpn = parts.mpn AND stock.mpn = '%s') 
        GROUP BY stock.mpn, stock.mfr, stock.seller ''' % (mpn, mpn)
        db_res = curs.execute(sql).fetchall()
    elif octoid:
        sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
        stock.lead_time, stock.pullDate
        FROM parts, stock
        WHERE parts.octoid = stock.octoid AND  parts.mpn = stock.mpn
        AND parts.octoid = '%s' AND stock.pullDate = (SELECT MIN(stock.pullDate) FROM stock 
        WHERE stock.mpn = parts.mpn AND stock.octoid = '%s') 
        GROUP BY stock.mpn, stock.mfr, stock.seller ''' % (octoid, octoid)
        db_res = curs.execute(sql).fetchall()
    else:
        db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'
    conn.close()

    return db_res


def get_previous_info(db_file, mpn=None, octoid=None, seller=None):
    if seller:
        db_res = get_prev_info_with_seller(db_file, mpn=mpn, octoid=octoid, seller=seller)
    else:
        db_res = get_prev_info(db_file, mpn=mpn, octoid=octoid)

    if not db_res:
        if seller:
            db_res = get_earliest_part_info_with_seller(db_file, mpn=mpn, octoid=octoid, seller=seller)
        else:
            db_res = get_earliest_part_info(db_file, mpn=mpn, octoid=octoid)

    return db_res


def get_all_db_info(db_file):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    sql = '''SELECT DISTINCT parts.avpn, parts.mpn, parts.mfr, stock.seller, stock.price, stock.total_stock, 
            stock.lead_time, stock.pullDate
            FROM parts, stock
            GROUP BY  '''
    db_res = curs.execute(sql).fetchall()
    conn.close()

    return db_res


def get_from_database(db_file, mpn=None, octoid=None, seller=None, base=False, all=False):
    """
    This function creates a SQLite query to obtain data from the database; if mpn is specified it will search for
    the part based on mpn, if octoid is specified it will search for part data based on the octoid, if base is
    provided it will search for parts from that specified date, and if all is specified it will return all parts in
    the database. In order to error handle if a part cannot be located byt its octoid it will be searched by its mpn
    and vice versa. If a part cannot be located after both attempts its information will be printed out.
    """
    if mpn:
        if not base:
            if seller:
                db_res = get_present_info_with_seller(db_file, mpn=mpn, octoid=None, seller=seller)
            else:
                db_res = get_present_info(db_file, mpn=mpn, octoid=None)
        elif base:
            db_res = get_previous_info(db_file, mpn=mpn, octoid=None, seller=seller)
        elif all:
            db_res = get_all_db_info(db_file)
        else:
            db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'
    elif octoid:
        if not base:
            if seller:
                db_res = get_present_info_with_seller(db_file, mpn=None, octoid=octoid, seller=seller)
            else:
                db_res = get_present_info(db_file, mpn=None, octoid=octoid)
        elif base:
            db_res = get_previous_info(db_file, mpn=None, octoid=octoid, seller=seller)
        elif all:
            db_res = get_all_db_info(db_file)
        else:
            db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'
    else:
        db_res = 'SQL QUERY ERROR: NOT ENOUGH INFORMATION PROVIDED'

    return db_res


def get_all_octoids_with_sellers(db_file):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    sql = '''SELECT DISTINCT stock.octoid, stock.seller FROM stock'''
    db_res = curs.execute(sql).fetchall()
    conn.close()

    return db_res