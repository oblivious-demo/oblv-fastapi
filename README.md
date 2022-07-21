# MPC Encalve Applications with FastAPI :rocket:

![](https://oblv.io/badge)

What we'll cover in this tutorial:
- developing with oblivious (OBLV) and fastapi
    - recieving inputs from clients
    - runtime arguments
    - outbound calls
- local testing
    - unit tests
- configuring, deploying and connecting
    - configure repo to be valid service
    - create client keys
    - deploy to enclave
    - connect to and interact with the enclave application 

## 1. Understanding OBLV Architecture for MPC :classical_building:

```mermaid
graph TD;
    subgraph client
    A[client] --- B[client proxy];
    end
    B -. secured end-to-end connection .- C[enclave proxy];
    subgraph enclave
    C --- D[enclave services];
    end
```

## 2. Attestation & Runtime Args :runner:

```mermaid
graph TD;
    a[Code] --> b[Docker Build];
    b -- Hashes for attestation determined --> c[Enclave Image Build];
    c --> d[Encalve Launch];
    d -- Runtime YAML not effecting attestation post-launch --> e[Add Runtime YAML];
    e --> f[Launch Services];
```

## 3. Outbound Calls :mega:

```mermaid
graph TD;
    a[Service] --> b[DNS Routing]
    b -- Approved FQDN 1 --> c[Outbound Socket]
    b -- Approved FQDN 2 --> d[Outbound Socket]
    b -- Approved FQDN 3 --> e[Outbound Socket]
```