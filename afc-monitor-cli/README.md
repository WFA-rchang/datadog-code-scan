# AFC Monitor CLI

## Getting Started
__AFC Monitor CLI__ is a CLI tool provides several SRE monitoring automation feature.  Following is the guideline to setup python environment and a list of some execution tips for the tool.

### Prerequisites
* Python 3

### Installation
1. Create Python virtual env
```sh
   python3 -m venv .env
```
2. Activate the virtual env
```sh
   source .env/bin/activate
```
3. Install dependencies
```sh
   pip3 install -r requirements.txt
```

### Usage
- Help
  ```sh
  $ python3 main.py
    Usage: main.py [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      proactive-monitor  Execute Proactive Monitor
  ```

- proactive-monitor  
  This command is used to get several AFC Services health status.
  * Current supported monitor
    * NRA List Status
  
  *Command example*
  ```sh
  python3 main.py proactive-monitor
  ```

### Configuration
#### Environment Variables
Description          |         Key         | Value (Example)              | Notes          |
---------------------| ------------------- | ---------------------------- | ---------------|
PostgreSQL HOST      |  DB_HOST            | localhost                    | MP DB Host     |
PostgreSQL Post      |  DB_PORT            | 5432                         | MP DB Port     |
PostgreSQL Username  |  DB_USERNAME        | postgres                     | MP DB Username |
PostgreSQL Password  |  DB_PASSWORD        |                              | MP DB Password |
PostgreSQL DB Name   |  DB_NAME            | afc_mp                       | MP DB Name     |


#### Environment Variables set in `.env.local`
For more easier environment variable setting in development, an env file `.env.local` could be placed in project root, the tool will load those variables while execution.

__.env.local:__
``` sh
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=test
DB_NAME=afc_mp
```
