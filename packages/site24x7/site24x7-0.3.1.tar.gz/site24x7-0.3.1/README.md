
## system argument requirements
```python
server            = sys.argv[1]
database          = sys.argv[2]
username          = sys.argv[3]
password          = sys.argv[4]
driverLocation    = sys.argv[5] 
query             = sys.argv[6] # EXEC sql command to execute
thisPluginName    = sys.argv[7]
```

## example input
```bash
python main.py localhost testdb sa password /usr/local/lib/python3.6/dist-packages/pyodbc/drivers/pyodbc.so "select * from testtable" testplugin
```

## what is expected query(EXEC) input and expected output?
```js
const rows = database.exec(query); 
console.log(rows);
// [(0, 'key', 'value'), (1, 'dev', 'renas'), ...rows]

const fs = require('fs');
console.log(fs.readFileSync('/tmp/testplugin.cache', 'utf8'))
// {
//     "plugin_version": "2",
//     "heartbeat_required": "true",
//     "CPU": 100,
//     "server": "localhost",
//     "database": "testdb",
//     "driverLocation": "/usr/local/lib/python3.6/dist-packages/pyodbc/drivers/pyodbc.so",
//     "query": "select * from testtable",
//     "thisPluginName": "testplugin",
//     "key": "value",
//     "dev": "renas"
// }
```

# HOW-TOs

## how to see how many plugin this server has on site24x7.com
- 48 plugins on 06
- 111 plugins on 05 # this SERVER also did not let me install 3 diffirent plugins on site24x7.com
```js
await page.goto('https://site24x7.com/plugins/');
await page.evaulate(()=>{
    return document.querySelectorAll(".cursor.ng-scope").length;
}).then(result=>{
    console.log(result);
}).catch(error=>{
    console.log(error);
}).finally(()=>{
    browser.close();
}).then(()=>{
    console.log('done');
});
```

## jenkins run command
```bash
if pip3 list | grep -F site24x7; then
    echo "site24x7 is installed"
else
    echo "site24x7 is not installed, installing it right now..."
    pip3 install site24x7 --force-reinstall
fi

server="localhost" 
database="testdb" 
username="sa" 
password="password" 
driverLocation="/usr/local/lib/python3.6/dist-packages/pyodbc/drivers/pyodbc.so"
query="""select * from testtable" 
thisPluginName="TRY6"

mkdir /opt/site24x7/monagent/plugins/$thisPluginName
touch /opt/site24x7/monagent/plugins/$thisPluginName/$thisPluginName.py

python main.py $server $database $username $password $driverLocation $query $thisPluginName
```

## how to check if site24x7_plugin_helper is installed
```bash
ls '/usr/local/lib/python3.7/dist-packages/site24x7_plugin_helper/'
```