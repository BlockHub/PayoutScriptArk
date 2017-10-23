# A Collection of Random Tips

*  Want to develop on windows and access a node through this script? Use an SSH
   tunnel:
   http://realprogrammers.com/how_to/set_up_an_ssh_tunnel_with_putty.html
   
*  Having trouble connecting to a database on your local machine? You can edit
   `/etc/postgresql/9.5/main/pg_hba.conf` and replace `md5` by `trust`.  Beware
   that now anyone can access your database and change its contents, so make
   sure to either not share the access, or if you are more experienced, make a
   new user with only `SELECT` privileges. See the Postgresql documentation for
   more info; an in-depth discussion is out of scope here.
