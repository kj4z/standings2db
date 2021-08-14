# standings2db
Converts Wayback Machine DXCC Standings Archives to MySQL DB tables

# Quickstart Guide

1. Create your MySQL database.  I called mine "dxcc" but if you want to use a different name, update parser.py accordingly.
2. Grant access permissions.  Probably something like this.
> CREATE USER 'dxcc'@'%' IDENTIFIED BY 'password';
> GRANT ALL PRIVILEGES ON dxcc.* to 'dxcc'@'%';
> FLUSH PRIVILEGES;
3. Create a `dxcc` directory to hold downloaded PDF files.
4. Run downloader.py: `./downloader.py`
5. Run parser.py: `./parser.py`
6. Connect to MySQL and run your queries.  Here's one to get you started:
> select report_date,mode,dxcc_count,count(*) as count from dxcc_hr WHERE filename like '%USLetter%' group by dxcc_count,mode,report_date order by report_date,mode,dxcc_count desc;
> # Would pull only the records from USLetter PDFs.  Leave out the where clause to get everything.