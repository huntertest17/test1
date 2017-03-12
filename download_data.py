import re,os,sys
import csv
import pandas as pd
import numpy as np
import datetime
import sqlite3

def constructYFURL(ticker,start_date,end_date,freq):#{{{
    start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()

    s=ticker.replace("^","%5E")

    if start_date.month-1<10:
        a="0"+str(start_date.month-1)
    else:
        a=str(start_date.month-1)
    # a represents the month portion - however the month count starts from 0
    # Also the month always has 2 digits
    b=str(start_date.day)

    c=str(start_date.year)
    # b and c represent the day and year parts of the start date
    if end_date.month - 1 < 10:
        d = "0" + str(end_date.month - 1)
    else:
        d = str(end_date.month - 1)
    # similarly we have to set up the month part for the end date
    e=str(end_date.day)

    f=str(end_date.year)
    # e and f represent the day and year parts of the end date
    g=freq
    # g represents the frequency d = daily, w= weekly, m=monthly

    # Finally let's set up the URL

    yfURL = "http://real-chart.finance.yahoo.com/table.csv?s="+s+"&a="+a+"&b="+b+"&c="+c+"&d="+d+"&e="+e+"&f="+f+"&g="+g+"&ignore=.csv"
    return yfURL

#}}}
def download(filePath,urlOfFile):#{{{
    import urllib2

    # We can just use a function from urllib2 to download a url, and save its contents to a
    # local path
    hdr = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Language':'en-US,en;q=0.8',
           'Accept-Encoding':'none',
           'Connection':'keep-alive'}


    webRequest  = urllib2.Request(urlOfFile,headers=hdr)
    #  We'll pass in a header attribute to the webRequest

    # The rest of our code will be enclosed within a try:/except: pair
    # This will act as a safety net in case we encounter some errors when
    # accessing the web urls or working with the files

    try:
        page=urllib2.urlopen(webRequest)
        # save the contents of the web request in a variable called 'content'
        # These are literally the file form the URL (i.e. what you'd get if you
        # downloaded the URL manually

        content=page.read()

        with open(filePath,"wb") as output:
            output.write(bytearray(content))

    # We are simply reading the bytes in content and writing them to our local file.
    # This way we are agnostic to what kind of file we are trying to download ie zip files , csvs,
    # excel etc

    except urllib2.HTTPError, e:
        # Let's print out the error , if any resulted
        print e.fp.read()
#}}}
def update_db_yahoo(sL):#{{{
    HD=" "*4
    dbName = 'data.db'
    conn=sqlite3.connect(dbName)
    c=conn.cursor()

    tn = datetime.datetime.now()
    te_m1 = tn.date()
    if tn.weekday()>4:
        te_m1 = te_m1 - datetime.timedelta(days=(tn.weekday()-4))
    te = te_m1
    if tn.hour<13:
        te_m1 -= datetime.timedelta(days=1)

    for symbol in sL:
        symbol = symbol.lower()
        fileName = "%s.csv" % symbol

        mk_tbl0="""
        create table %s (
        date float,
        open float,
        high float,
        low float,
        close float,
        volume float,
        adjclose float,
        unique (date)
        );
        """ % symbol
        #constraint uniq_row unique (date)

        print "%10s" % symbol,
        try: c.execute(mk_tbl0)
        except: pass

        if os.path.isfile(fileName):
            rd = csv.reader(open(fileName, 'r'), delimiter=',')
            next(rd, None) # skip header
            rL = []
            for r in rd:
                t=datetime.datetime.strptime(r[0],"%Y-%m-%d").toordinal()
                r[0] = "%d" % t  # "%04d-%02d-%02d" % (t.year,t.month,t.day)
                rL.append(tuple(r))
            c.executemany('insert or ignore into %s values (?,?,?,?,?,?,?)' % symbol, rL)
            conn.commit()

        last = "2000-01-01"
        ts = datetime.datetime.strptime(last,"%Y-%m-%d")
        if 1:
            c.execute("select max(date) from %s" % symbol)
            t = c.fetchall()[0][0]
            if not t==None:
                ts = datetime.datetime.fromordinal(int(t))
        ts = ts.date()

        if 1 and  ts.toordinal() < te_m1.toordinal():
            ts_str = "%04d-%02d-%02d" % (ts.year, ts.month, ts.day)
            te_str = "%04d-%02d-%02d" % (te.year, te.month, te.day)
            smb = re.sub("^_","^",symbol)
            print te-ts, ts_str, te_str

            url  = constructYFURL(smb,ts_str,te_str,"d")
            download(fileName, url)
            with open(fileName,'r') as f:
                rd = csv.reader(open(fileName, 'r'), delimiter=',')
            next(rd, None) # skip header
            rL = []
            for r in rd:
                t=datetime.datetime.strptime(r[0],"%Y-%m-%d").toordinal()
                r[0] = "%d" % t
                rL.append(tuple(r))
            c.executemany('insert or ignore into %s values (?,?,?,?,?,?,?)' % symbol, rL)
            conn.commit()
        else:
            print

    c.close()
    conn.close()
#}}}


s1L = """tsla amzn ibm v aapl acn afsi aig amt amtd asna axp bke bks bpi br c coh cost czr dfs dgs f fb five ges
gild gntx goog hal hlf hri ibm intc ko luk ma mcd mkl mo nflx nok
nov orcl orly otex p pfe praa prxl pzza qcom sbux
shld swks tmfgx tsla tup urbn v vfinx voo wfc wfm wrld gld fds
cmcsa jcp shld vix gs nvda gm msft
aal bac _vix _tnx spy qqq voo
"""

proL = """
fb br afsi orly ma aapl swks amt orcl otex pzza sbux gntx
amtd jnj amzn mtd payc v gild vmi fds vrsk svxy dgs vrsn gogo 
"""

fidL = """
FIUIX FSAIX FSAVX FSRBX FBIOX FSLBX FSCHX FSDCX FDCPX FSHOX
FSCPX FSVLX FDFAX FSDAX FSENX FSESX FSLEX FIDSX FSAGX FSPHX
FSHCX FSCGX FCYIX FSPCX FBSOX FDLSX FSDPX FSMEX FBMPX FSNGX
FNARX FPHAX FSRPX FSELX FSCSX FSPTX FSTCX FSRFX FSUTX FWRLX
"""

tstL = """
gm
"""

sL=tstL
sL=proL
sL=s1L
sL=fidL

sL = tstL + proL + s1L + fidL

sL = re.sub("\n"," ",sL).split()
sL = set(sL)

update_db_yahoo(sL)


