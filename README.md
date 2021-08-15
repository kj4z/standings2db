# standings2db
Converts Wayback Machine DXCC Standings Archives to MySQL DB tables

# Quickstart Guide

1. Create your MySQL database.  I called mine "dxcc" but if you want to use a different name, update parser.py accordingly.
2. Run `mysql.sql` against your new database to create the `dxcc_hr` table.  Something like `mysql -u <user> -p -h <host> <database> < mysql.sql`
3. Grant access permissions.  Probably something like this.
> CREATE USER 'dxcc'@'%' IDENTIFIED BY 'password';
> GRANT ALL PRIVILEGES ON dxcc.* to 'dxcc'@'%';
> FLUSH PRIVILEGES;
4. Create a `dxcc` directory to hold downloaded PDF files.
5. Make sure your MySQL settings are correct in parser.py.
6. Run downloader.py: `./downloader.py`
7. Run parser.py: `./parser.py`
8. Connect to MySQL and run your queries.  Here's one to get you started:
> select report_date,mode,dxcc_count,count(*) as count from dxcc_hr WHERE filename like '%USLetter%' group by dxcc_count,mode,report_date order by report_date,mode,dxcc_count desc;
