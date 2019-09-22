# Logs Analysis Project
## Introduction
This project is a reporting tool for a newspaper site using the database `newsdata.sql` to provide information on what kinds of articles readers like from a newspaper site.

## Getting started
### Install virtual machine
This project makes use of a Linux-based virtual machine (VM) which runs on top of your own computer. In order to install and manage the VM, the following tools are recommended:

* [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) - the software that actually runs the VM
* [Vagrant](https://www.vagrantup.com/) - the software that configures the VM and lets you share files between host computer and VM's filesystem

Once these tools are installed, you must download and unzip the VM configuration which can be found [here](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip). This will give you a directory called **FSND-Virtual-Machine**.

The unzipped directory will contain the relevant VM files. `cd` into this directory and you will find another directory called **vagrant**. `cd` into the **vagrant** directory.

### Start the virtual machine
Inside the **vagrant** subdirectory, run the command `vagrant up`. Once this is finished running, run `vagrant ssh` to log into the newly installed Linux VM.

### Install relevant packages
Ensure that python3 has been installed by running `python3 --version`.

Within your virtual machine, run the following to install the relevant packages:
* `pip3 install flask`
* `sudo apt install python3-dev postgresql postgresql-contrib python3-psycopg2 libpq-dev`
* `pip3 install psycopg2`

## Load data and create views
The relevant data can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Put this in your vagrant directory.

Load the data from the `.sql` file into database by running `psql -d news -f newsdata.sql`.

Connect to the `news` database by running `psql news`. Once connected to the `news` database, the following 3 views must be created:

1. Create the `popular_articles` view
```
create view popular_articles as 
select articles.title, count(log.path) as views 
from articles 
left join log 
on concat('/article/', articles.slug) = log.path 
group by log.path, articles.title 
order by count(log.path) desc 
limit 3;
```

2. Create the `popular_authors` view
```
create view popular_authors as
select author_slugs.name, count(log.path) as views
from (
    select authors.name, articles.slug 
    from authors left join articles 
    on authors.id = articles.author) as author_slugs 
left join log 
on concat('/article/', author_slugs.slug) = log.path 
group by author_slugs.name 
order by count(log.path) desc;
```

3. Create the `one_perc_error_days` view
```
create view one_perc_error_days as
select 
    to_char(sq.date, 'FMMonth DD, FMYYYY') as date
    , round(sq.percentage,1) as perc_errors 
from (
    select 
        date(time)
        , count(log.path) as requests
        , count(log.path) filter (where status != '200 OK') as errors
        , ((count(log.path) filter (where status != '200 OK'))::numeric / count(log.path)::numeric) * 100 as percentage
    from log 
    group by date(time)
    order by date(time) desc) as sq 
where sq.percentage > 1;
```

## Program
The program is found in the Python3 script **logsanalysis.py**. The program is a Flask app which listens for a request on `port 8000` on `localhost` (i.e. `host='0.0.0.0'`).

Once a request is received, it retrieves relevant answers to each question from pre-created views in the `news` database using the `get_ans()` function, wraps them into an HTML script and returns this to the client.

### Running the program
Once logged into Virtual Machine, `cd` to the directory containing the file **logsanalysis.py**. Run the program by running `python3 logsanalysis.py` at the command line.

## Acknowledgements
Details for **Getting Started** have been summarised from Udacity's "Installing the Virtual Machine" lesson, which can be found [here](https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0).