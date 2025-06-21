# Custom-Load-Balancer
This project is part of a distributed systems lab focused on implementing a **custom load balancer** that uses **consistent hashing** to distribute client requests across a set of replicated server containers. The objective is to simulate request routing, load balancing, and fault tolerance in a containerized environment.

---


## Project Overview

The system is built around two main components:

- **Client**: Contains the custom load balancer logic and consistent hashing algorithm.
- **Server**: A simple HTTP server that responds to requests forwarded by the load balancer.

Requests are routed from the client through the load balancer, which uses consistent hashing to determine the appropriate server to handle each request. This prevents any single server from being overloaded and enables graceful failure handling.

---


## 📁 Project Structure

```
.
├── client/                        # Load balancer + hashing logic
│   ├── consistent_hash.py        # Implements consistent hash ring (Φ, H)
│   ├── load_balancer.py          # Custom load balancer that routes requests
│   ├── test_client.py            # Simulates and tests load balancing
│   ├── dockerfile                # Dockerfile for load balancer container
│   ├── requirements.txt          # Python dependencies
│   └── venv/                     # Virtual environment (excluded in .dockerignore)
│
├── server/                       # Minimal HTTP server (Task 1)
│   ├── server.py                 # Flask server with /home and /heartbeat endpoints
│   ├── Dockerfile                # Dockerfile to containerize the server
│   └── requirements.txt          # Python dependencies for the server
│
├── docker-compose.yml           # Orchestrates client and multiple server containers
└── README.md                    # Project documentation
```
---


## Objective

To design and evaluate a lightweight, hash-based load balancing mechanism that:
- Evenly distributes requests across multiple server containers
- Uses consistent hashing with virtual replicas to ensure smooth transitions when servers are added or removed
- Handles server failure scenarios gracefully

---


## Implementation Summary

- **Task 1: Server Setup**  
  Created a simple Flask server with `/home` and `/heartbeat` endpoints and containerized it using Docker.

- **Task 2: Consistent Hashing**  
  Implemented a consistent hash ring with 512 slots and 9 virtual replicas per server. Applied lab-defined formulas `Φ(i,j)` and `H(i)` for mapping virtual servers and requests respectively.

- **Task 3: Load Balancer Logic**  
  Integrated the consistent hashing module into a custom load balancer that can route HTTP requests to the correct server container based on the hash ring.

- **Task 4: Analysis**  
  The load balancer was evaluated by simulating large volumes of requests under different configurations. Performance metrics such as request distribution, scalability with varying server counts, and fault recovery were analyzed. The following section presents observations and results from these experiments.

---


## Analysis Results
The following section presents request distribution results and fault-tolerance behavior observed during simulation:

## A-1

Server 1 handled a majority of the requests and Server 2 handled basically nothing. This is likely
caused by an imbalance in the consistent hash ring.
![Picture1](https://github.com/user-attachments/assets/a4e75e31-fe3e-4427-93de-9dcb318b9e78)


## A-2

As N Increases, the average number of requests decreases until it stabilizes at N=5,6. Therefore, 
the load balancer scales well as more servers reduce the load.
![Picture2](https://github.com/user-attachments/assets/fa939bd5-b389-461a-8944-072cede9f334)

## A-3

### Endpoints

/add

![image](https://github.com/user-attachments/assets/d9515793-cb62-4c76-bf7a-5e589525b696)


/home

![image](https://github.com/user-attachments/assets/a4bffeb1-cbca-442f-88f1-f40fbbd040fb)


/rep and /rm

![image](https://github.com/user-attachments/assets/63dd648f-a66c-49b9-b8b8-d4c5d22dafed)

