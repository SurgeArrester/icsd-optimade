<div align="center" style="padding: 2em;">
<span style="padding: 1em">
<img height="70px" align="center" src="https://matsci.org/uploads/default/original/2X/b/bd2f59b3bf14fb046b74538750699d7da4c19ac1.svg">
</span>
</div>

# <div align="center">ICSD OPTIMADE API</div>

This repo contains prototyping work for creating an [OPTIMADE
API](https://optimade.org) for searching and accessing structures
from the [Inorganic Crystal Structure Database (ICSD)](https://icsd.fiz-karlsruhe.de).

The structures are accessed via the [ICSD REST API 
](https://icsd.fiz-karlsruhe.de/api) and cast to the
OPTIMADE format; the
[`optimade-maker`](https://github.com/materialscloud-org/optimade-maker/) and
[`optimade-python-tools`](https://github.com/Materials-Consortia/optimade-python-tools/)
are then used to launch a local OPTIMADE API.

## Installation

After cloning this repository and using some appropriate method of creating a virtual environment (current recommendation is [`uv`](https://github.com/astral-sh/uv)), this package can be installed with

```shell
git clone git@github.com:datalab-industries/icsd-optimade
cd icsd-optimade
uv sync 
```

or

```shell
git clone git@github.com:datalab-industries/icsd-optimade
cd icsd-optimade
pip install .
```

> [!IMPORTANT]  
>  Any attempts to use ICSD data will additionally require a valid ICSD license
>  with login details provided at runtime.

## Usage

### Ingesting ICSD data

The CSD can be ingested into the OPTIMADE format using the `icsd-ingest` entrypoint:

```shell
icsd-ingest
```

This will use multiple processes (controlled by `--num-processes`) to ingest the
local copy of the CSD database in chunks of size `--chunk-size` until the target
`--num-structures` has been reached (defaults to the entire CSD).
Each batch will be written to an [OPTIMADE JSONLines file](https://github.com/Materials-Consortia/OPTIMADE/pull/531),
and combined into a single JSONLines file on completion, with name
`<--run-name>-optimade.jsonl`.

### Creating an OPTIMADE API

The `icsd-serve` entrypoint provides a thin wrapper around the
[`optimade-maker`](https://github.com/materialscloud-org/optimade-maker/) tool,
and bundles the simple configuration required to launch a local OPTIMADE API
with a simple in-memory database (if `--mongo-uri` is provided, a real MongoDB
backend will be used).
Just provide the path to your combined OPTIMADE JSONLines file:

```shell
icsd-serve <path-to-optimade-jsonl>
```

You should now be able to try out some queries locally, either in the browser or
with a tool like `curl`:

```shell
curl http://localhost:5000/structures?filter=elements HAS "C"
```

## Containerized version

For ease of deployment, as containerised version of the ingestion pipeline is available.

> [!IMPORTANT]
> You should verify that your license agreement allows for any kind of deployment outside of your private network; it likely does not.

```shell
docker build --secret id=env,src=.env -t icsd-optimade .
```

For development, you may prefer to use the bake definitions in
`docker-bake.hcl` to build and tag the relevant build stages.

## Contributing and Getting Help

All development of this package (bug reports, suggestions, feedback and pull requests) occurs in the [csd-optimade GitHub repository](https://github.com/datalab-industries/csd-optimade).
Contribution guidelines and tips for getting help can be found in the [contributing notes](CONTRIBUTING.md).


## Funding

This project was developed by [datalab industries ltd.](https://datalab.industries), on behalf of the UK's [Physical Sciences Data Infrastructure (PSDI)](https://psdi.ac.uk).

<div align="center">
<a href="https://psdi.ac.uk"><img src='https://github.com/user-attachments/assets/19d8a74d-f3d0-4825-8a71-4eba1b6392de' width=400/></a>
</div>
