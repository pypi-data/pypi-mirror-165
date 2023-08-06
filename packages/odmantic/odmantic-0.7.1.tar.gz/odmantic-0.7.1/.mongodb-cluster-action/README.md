# MongoDB Cluster Action

[![Test GH Action](https://github.com/art049/mongodb-cluster-action/actions/workflows/ci.yml/badge.svg)](https://github.com/art049/mongodb-cluster-action/actions/workflows/ci.yml)

## Github Action Usage

#### Basic

```yaml
steps:
  # Create the MongoDB cluster
  - uses: art049/mongodb-cluster-action@v0
    id: mongodb-cluster-action
  # Run a CI job and pass the cluster address
  # in the MONGO_URI env variable
  - run: ./script/test
    env:
      MONGO_URI: ${{ steps.mongodb-cluster-action.outputs.connection-string }}
```

#### Specify a MongoDB server version

```yaml
steps:
  ...
  - uses: art049/mongodb-cluster-action@v0
    id: mongodb-cluster-action
    with:
      version: "3.6"
  ...
```

#### Run a replicaSet cluster

```yaml
steps:
  ...
  - uses: art049/mongodb-cluster-action@v0
    id: mongodb-cluster-action
    with:
      mode: replicaSet
  ...
```

#### Run a sharded cluster

```yaml
steps:
  ...
  - uses: art049/mongodb-cluster-action@v0
    id: mongodb-cluster-action
    with:
      mode: sharded
  ...
```

### Action details

#### Inputs

| Input     | Description                                                                                                        | Default      |
| --------- | ------------------------------------------------------------------------------------------------------------------ | ------------ |
| `version` | Specifies the MongoDB version to use. Available versions can be found [here](https://hub.docker.com/_/mongo/tags). | `latest`     |
| `mode`    | Specifies the type of cluster to create: either `standalone`, `replicaSet` or `sharded`.                           | `standalone` |

#### Outputs

| Output              | Description                                                    |
| ------------------- | -------------------------------------------------------------- |
| `connection-string` | The connection string to use to connect to the MongoDB cluster |

## Taskfile Usage

This action can also be used with [taskfile](https://taskfile.dev/).

Here are the available tasks:

- `standalone-docker`: Start a standalone MongoDB instance using a docker container

- `standalone-docker:down`: Stop the standalone instance

- `replica-compose`: Start a replica set MongoDB cluster using docker-compose

- `replica-compose:down`: Stop the replica set cluster

- `sharded-compose`: Start a sharded MongoDB cluster using docker-compose

- `sharded-compose:down`: Stop the sharded MongoDB cluster

### Integration in an existing taskfile

First add this repository as a submodule in your project:

```bash
git submodule add https://github.com/art049/mongodb-cluster-action.git .mongodb-cluster-action
```

Then you can include the taskfile in an existing one by adding the following lines:

```yaml
includes:
  mongodb:
    taskfile: ./.mongodb-cluster-action/Taskfile.yml
    dir: .mongodb-cluster-action
    optional: true
```

You can then use the mongodb cluster actions by adding the `mongodb` prefix. For example to start a standalone MongoDB instance:

```bash
task mongodb:standalone-docker
```

## Generated clusters details

### Standalone

Spawn a standalone MongoDB instance.

Server: `localhost:27017`

Connection string: `mongodb://localhost:27017/`

### Replica Set

Spawn a 3 member replicaset cluster (1 primary, 2 secondaries)

Servers:

- `172.16.17.11:27017`
- `172.16.17.12:27017`
- `172.16.17.13:27017`

Connection string: `mongodb://172.16.17.11:27017,172.16.17.12:27017,172.16.17.13:27017/?replicaSet=mongodb-action-replica-set`

### Sharded Cluster

Spawn the most simple sharded cluster as possible with 3 replicated shards.

[![](https://mermaid.ink/img/pako:eNp1ksFqwzAQRH9F7MmG2HiVUDem9JL01pN99UWO5NgQW0GRAiXk36vGK2jsdg9CDDP7BqQbHLRUUMDRiHPHPst6ZH520U6PbX-sroa9NeadYc5TfEkxTxELnme4jVmSJKyMSu2s-s-Vx9O-8mGusujSCSMzUquMZEG6mK_h2WPNa8xoZsGGgs0iiH8GqQdOMQw9kGTqgYse69BjFiA-LvhrfAoQl092HtZwkonLF9zNjBsCxOUL7uaZ-_uEFQzKDKKX_rlvP1oNtlODqqHwV6la4U62hnq8e6s7S2HVh-ytNlC04nRRKxDO6uprPEBhjVPBtO-F_z0Due7fFniYnw)](https://mermaid-js.github.io/mermaid-live-editor/edit#pako:eNp1ksFqwzAQRH9F7MmG2HiVUDem9JL01pN99UWO5NgQW0GRAiXk36vGK2jsdg9CDDP7BqQbHLRUUMDRiHPHPst6ZH520U6PbX-sroa9NeadYc5TfEkxTxELnme4jVmSJKyMSu2s-s-Vx9O-8mGusujSCSMzUquMZEG6mK_h2WPNa8xoZsGGgs0iiH8GqQdOMQw9kGTqgYse69BjFiA-LvhrfAoQl092HtZwkonLF9zNjBsCxOUL7uaZ-_uEFQzKDKKX_rlvP1oNtlODqqHwV6la4U62hnq8e6s7S2HVh-ytNlC04nRRKxDO6uprPEBhjVPBtO-F_z0Due7fFniYnw)

Servers:

- Router: `172.16.17.11:27017`
- Configuration server: `172.16.17.11:27019`
- Shard0 servers:
  - `172.16.17.20:27018`
  - `172.16.17.21:27018`
- Shard1 servers:
  - `172.16.17.30:27018`
  - `172.16.17.31:27018`
- Shard2 servers:
  - `172.16.17.40:27018`
  - `172.16.17.41:27018`

Connection string: `mongodb://172.16.17.10:27017/?retryWrites=false`

[Source](https://docs.mongodb.com/manual/core/sharded-cluster-components/#development-configuration)

**Note**: Does not work with Mongo 4.4.2 ([issue](https://jira.mongodb.org/browse/SERVER-53259))

</details>

## License

The scripts and documentation in this project are released under the [MIT License](./LICENSE)
