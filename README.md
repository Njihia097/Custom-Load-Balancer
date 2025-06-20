# Custom-Load-Balancer
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

