# knot-cli




Command Line Interface for Restknot


## What is knot-cli


Knot-cli is a command line interface to operate RESTKnot



## Usage

List of available command on knot-cli

#### Create
```
create dns (--nm=NAME) [-i]
create record (--nm NAME) (--nm-zn ZONENAME) (--type=TYPE) (--ttl TTL) (--nm-con CON) [--nm-con-ser CONSER] 
create record -f FILENAME
```

Options : 
```
-h --help                 Print usage
--nm NAME                 Set DNS/record name
-type=TYPE                Set DNS type
--ttl TTL                 Set DNS TTL 
--nm-zn ZONENAME          Set zone of new record
-i --interactive          Interactive Mode
--nm-con CON              Set content name
--nm-con-ser CONSER       Set content serial name
-f FILENAME               Create Record using YAML
```

#### List

```
ls ttl
ls type
ls record [--nm NAME]
ls dns
```

Options : 

```
--nm                        Show list of selected zone

```

#### Remove
```
rm dns (--nm NAME)
rm record [(--nm-zone=ZNNAME [--nm-record=NAME] [--type=TYPE] )]

```

<a name="Filter"></a>Options : 
```
-h --help               Print usage
--nm=NAME               DNS' name to delete
--nm-record=NAME        Filter record by record's name
--nm-zn=ZNNAME          Filter record by zone's name
```

### Login and Account
Knot-cli requires you to create an account on [portal-neo](https://portal.neo.id/). Note that before using knot-cli you have to login using

```
login
```
```
logout [-r]
```

use logout -r to remove all your data for fresh login in the future


### Creating Zone and Record

To create a new zone and records, use the following commands respectively 

```
create dns (--nm=NAME)
```
```
create record (--nm NAME) (--nm-zn ZONENAME) (--type=TYPE) (--ttl TTL) (--nm-con) [--nm-con-ser CONSER]
```
```
create record -f FILENAME
```

#### Creating Record  from YAML File

Place your yaml file in
```
~/restknot
```

and must follow this format
```yaml

"zone_name":
    "record_name_1":
        - "record_type1":
            "ttl" : "ttl_value"
            "content_name" : "content_value"
        - "record_type2":
            "ttl" : "ttl_value"
            "content_name" : "content_value"
            "content_serial" : "content_serial_value"
    "record_name_2":
        - "record_type":
            "ttl" : "ttl_value"
            .
            ...
"other_zone":
    "record_name_1":
        - "record_type2":
            .
            ...

```


```yaml
"klakla.com":
    "budak":
        - "MX":
            "ttl": "1800"
            "content": "contoh1"
            "content-serial": "contoh2"
        - "AAAA":
            "ttl": "3600"
            "content": "IPv6"
    "papah":
        - "CNAME":
            "ttl": "900"
            "content": "waduksiah"
"thepokis.com":
    "ampun":
        - "A":
            "ttl": "1800"
            "content": "test"

```


Remember to check available type and ttl before creating records, also MX and SRV record need serial content on creation. 


```
ls ttl
ls type
```



### Removing Zone and Record

```
rm dns (--nm NAME)
rm record [(--nm-zone=ZNNAME [--nm-record=NAME] [--type=TYPE] )]
```

When you're removing dns, knot-cli will give you a list of records that will also be removed and ask your confirmation.

On record removal, knot-cli will give you a list of your record based on filter (or all of your record if no filter is given). 

![knot-cli rm1](https://github.com/riszkymf/RESTKnot/blob/devel/CLI/docs/img/rm1.jpg "Record removal")

Enter index of the record that you want to remove, then knot-cli will ask for your confirmation.

![knot-cli rm2](https://github.com/riszkymf/RESTKnot/blob/devel/CLI/docs/img/rm2.jpg "Record removal 2")


