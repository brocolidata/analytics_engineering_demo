![dbt+postgres](https://www.entechlog.com/images/blog/data/configure-dbt-for-postgres/01_hu42dc3e98dc978ed7da922474cdf63e17_32874_e42c87427412a5022aa4353ff1a512af.webp)
# analytics_engineering_demo
A Postgres + dbt setup for demonstration purposes

## Prerequisites
- **Docker** (started) and docker-compose (just install Docker for Desktop if you are on laptop) 
- **VS Code** + VS Code extension [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) 


## Quickstart
1. Clone repo
2. Duplicate the `.env.example` , rename it to `.env` and replace dummy values with yours
3. Click on *Open a Remote Window* button (left-down corner) & select **Reopen in Container**
4. Wait while your Development Environment is being built (it may take some time)
5. See [Inform dbt project](src/inform_risks/README.md) to start using the project.

## Project structure
```
.
├── .devcontainer              
│   └── devcontainer.json      # Dev Container settings
├── .env                       # Secret environment variables (filled)
├── .env.example               # Example of secret environment variables
├── Dockerfile                  # Docker Image settings
├── README.md                
├── docker-compose.yml         # Docker Container settings
├── requirements.txt           # Python dependencies
├── source_data                # Data folder (source data)
│   └── inform_trends.parquet
└── src
    ├── extract_load.py        # Extract/Load python script
    ├── inform_risks           # dbt project folder
    │   ├── .gitignore
    │   ├── README.md
    │   ├── dbt_packages       # dbt packages
    │   ├── dbt_project.yml    # dbt project settings
    │   ├── logs               # dbt logs
    │   ├── macros             # dbt macros
    │   ├── models             # dbt models
    │   ├── packages.yml       # dbt dependencies
    │   ├── seeds              # dbt static data
    │   └── target             # Where dbt store compiled code
    └── profiles
        └── profiles.yml        # dbt connection profile to the database
```