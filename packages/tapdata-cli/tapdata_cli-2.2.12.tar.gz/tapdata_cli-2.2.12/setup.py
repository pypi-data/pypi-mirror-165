# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tapdata_cli']

package_data = \
{'': ['*'], 'tapdata_cli': ['startup/*']}

install_requires = \
['PyYAML==5.4.1',
 'allure-pytest>=2.9.45,<3.0.0',
 'asyncio==3.4.3',
 'atomicwrites==1.4.0',
 'attrs==21.2.0',
 'certifi==2020.12.5',
 'chardet==4.0.0',
 'colorama==0.4.4',
 'colorlog==5.0.1',
 'idna==2.10',
 'iniconfig==1.1.1',
 'javascripthon>=0.12,<0.13',
 'jupyter>=1.0.0,<2.0.0',
 'packaging==20.9',
 'pluggy==0.13.1',
 'py==1.10.0',
 'pymongo==4.1.1',
 'pyparsing==2.4.7',
 'pytest>=7.1.2,<8.0.0',
 'requests==2.25.1',
 'toml==0.10.2',
 'urllib3==1.26.4',
 'websockets==9.0.2']

setup_kwargs = {
    'name': 'tapdata-cli',
    'version': '2.2.12',
    'description': 'Tapdata Python Sdk',
    'long_description': '# Tapdata Python Sdk\n\n[中文文档地址](https://github.com/tapdata/tapdata/tree/master/tapshell/docs/Python-Sdk_zh-hans.md)\n\n## Install\n\n1. Install python 3.7, pip By Yourself.\n2. Run ```pip install tapdata_cli``` to install sdk.\n3. If you use poetry, please run ```poetry add tapdata_cli``` to install sdk.\n\n## Initial\n\n```python\nserver = "127.0.0.1:3000"\naccess_code = "3324cfdf-7d3e-4792-bd32-571638d4562f"\nfrom tapdata_cli import cli\ncli.init(server, access_code)\n```\n\n**Multi-thread concurrency is not supported**\n\nIt will send a request to the server to obtain the identity information and save it as a global variable. Therefore, after multiple init the \'server\' and \'access_code\' variable will be overwritten. \n\nFor situations where you need to use different servers and access_codes concurrently, use Python\'s multiprocess.\n\n## DataSource\n\n### Create DataSource\n\nThe SDK supports the following data source operations:\n\n- Mongo\n- Mysql\n- Postgres\n- Oracle\n- Kafka\n\nTo create MySQL/Mongo:\n\n```python\nfrom tapdata_cli import cli\n\nconnector = "mongodb"  # datasource type，mongodb mysql postgres\nmongo = cli.DataSource("mongodb", name="mongo")\nmongo.uri("mongodb://localhost:8080")  # datasource uri\nmongo.save()\n```\n\nor:\n\n```python\nfrom tapdata_cli import cli\n\nmongo = cli.DataSource("mongodb", name="mongo")\nmongo.host("localhost:27017").db("source").username("user").password("password").props("")\nmongo.type("source")  # datasource type，source -> only source，target -> only target，source_and_target -> target and source (default)\nmongo.save()  # success -> True, Failure -> False\n```\n\nTo Create Oracle database:\n\n```python\nfrom tapdata_cli import cli\n\ndatasource_name = "ds_name"  # datasource name\noracle = cli.Oracle(datasource_name)\noracle.thinType("SERVICE_NAME")  # connect type SID/SERVER_NAME (database name/service name)\noracle.host("106.55.169.3").password("Gotapd8!").port("3521").schema("TAPDATA").db("TAPDATA").username("tapdata")\noracle.save()\n```\n\nTo create Kafka datasource:\n\n```python\nfrom tapdata_cli import cli\n\ndatabase_name = "kafka_name"\nkafka = cli.Kafka(database_name)\nkafka.host("106.xx.xx.x").port("9092")\nkafka.save()\n```\n\nTo create Postgres datasource:\n\n```python\nfrom tapdata_cli import cli\n\npg = cli.Postgres("jack_postgre") \npg.host("106.55.169.3").port(5496).db("insurance").username("postgres").password("tapdata").type("source").schema("insurance")\npg.validate()\npg.save()\n```\n\n*As for Kafka/Oracle/Postgres, the creation mode is heterogeneous. In the future, a unified interface will be provided in the form of datasource, which is backward compatible and will not affect the existing version.*\n\n### DataSource List\n\n```python\nfrom tapdata_cli import cli\n\ncli.DataSource().list()\n\n# return struct\n\n{\n    "total": 94,\n    "items": [{\n        "id": "",\n        "lastUpdBy": "",\n        "name": "",\n        "config": {},\n        "connection_type": "",\n        "database_type": "",\n        "definitionScope": "",\n        "definitionVersion": "",\n        "definitionGroup": "",\n        "definitionPdkId": "",\n        ...\n    }]\n}\n```\n\n### Get datasource according to ID/name\n\n```python\nfrom tapdata_cli import cli\n\ncli.DataSource(id="")  # by id\ncli.DataSource(name="")  # by name\n```\n\n## Pipeline\n\n### A simple data migration Job\n\n```python\nfrom tapdata_cli import cli\n\n# Create datasource first\nsource = cli.DataSource("mongodb", name="source").uri("").save()\ntarget = cli.DataSource("mongodb", name="target").uri("").save()\n# create Pipeline\np = cli.Pipeline(name="example_job")\np.readFrom("source").writeTo("target")\n# start\np.start()\n# stop\np.stop()\n# delete\np.delete()\n# status\np.status()\n# get job list\ncli.Job.list()\n```\n\nJob is the underlying implementation of pipeline, so you can use job.start() like pipeline.start().\n\n```python\n# init job (get job info) by id\nfrom tapdata_cli import cli\njob = cli.Job(id="some id string")\njob.save() # success -> True, failure -> False\njob.start() # success -> True, failure -> False\n```\n\n### Data development job\n\nBefore performing data development tasks, you need to change the task type to Sync:\n\n```python\nfrom tapdata_cli import cli\n\nsource = cli.DataSource("mongodb", name="source").uri("").save()\ntarget = cli.DataSource("mongodb", name="target").uri("").save()\np = cli.Pipeline(name="")\np = p.readFrom("source.player") # source is db, player is table\np.dag.jobType = cli.JobType.sync\n```\n\nThen perform specific operations:\n\n```python\n# filter cli.FilterType.keep (keep data) / cli.FilterType.delete (delete data)\np = p.filter("id > 2", cli.FilterType.keep)\n\n# filerColumn cli.FilterType.keep (keep column) / cli.FilterType.delete (delete column)\np = p.filterColumn(["name"], cli.FilterType.delete)\n\n# rename\np = p.rename("name", "player_name")\n\n# valueMap\np = p.valueMap("position", 1) \n\n# js\np = p.js("return record;")\n\np.writeTo("target.player")  # target is db, player is table\n```\n\nmaster slave merge:\n\n```python\n# merge\np2 = cli.Pipeline(name="source_2")  # Create merged pipeline\np3 = p.merge(p2, [(\'id\', \'id\')]).writeTo("target")  # Merge pipeline\n\np3.writeTo("target.player")  # target is db, player is table\n```\n\n### Create initial_sync/cdc job\n\nBy default, all tasks created through pipeline are "full + incremental" job.\n\nYou can create a initial_sync job by:\n\n```python\nfrom tapdata_cli import cli\n\np = cli.Pipeline(name="")\np.readFrom("source").writeTo("target")\nconfig = {"type": "initial_sync"}  # initial_sync\np1 = p.config(config=config)\np1.start()\n```\n\nAs above, changing config to ` {"type": "cdc"}` can create an incremental task.\n\nAll pipeline configuration modification operations are passed in through the `pipeline.config` method through the config default parameters, and the parameters are verified.\n\nFor more configuration modification items, please see [this file](https://github.com/tapdata/tapdata/blob/master/tapshell/tapdata_cli/rules.py), get more configuration items.\n\n## API Operation\n\n### Publish Api\n\n```python\nfrom tapdata_cli import cli\ncli.Api(name="test", table="source.player").publish() # source is db, player is table\n```\n\n### Unpublish APi\n\n```python\nfrom tapdata_cli import cli\ncli.Api(name="test").unpublish()\n```\n',
    'author': 'Tapdata',
    'author_email': 'team@tapdata.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tapdata/tapdata/tree/master/tapshell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
