

There are three folders representing the solutions of three problems:

- Problem 1:


- Problem 2:


- Problem 3:

--> Fast retrieval cache
    * Cache value retrieved from dictionary O(n) -> 1
--> LRU cache
    * Implemented using a doubly linked list
        Insertions anywhere O(n) -> 1
        Deletion anywhere O(n) -> 1
--> Expiration 
    * Timestamp of creation or modification is stored in the dictionary, upon each retrieval expiration is 
      accessed and if the data is expired(rest of the data following is also cleared)
      - The expiration async function will only be invoked if the expired data is accessed, in other cases LRU 
        functionality of the code should clear the linked list upon need
--> Scalable
    * Distributed Cache library is available, and it has features of synchronization(upon every write),
      reload(load the data from an another instance) and expiration sync(upon finding expired data, the 
      data will be removed from all instances)
--> Fault tolerance
    * An interface to either retrieve already saved data from the filesystem or DB. This feature not part of the first 
      commit.
--> Geo-Distributed access
    - The approach I have used to integrate geo-distribution is by using static config, where the cache-api library
      helps in finding the concerned IP for the concerned region. Upon disconnection, an another prefereable is used
      instead. A co-routine works in the background to have a stable connection. This feature is not part of the first
      commit.


'''Tests'''
make test

__
Things to do -->
-> Tidy up the code
-> Asyncio lock into equation for data integrity
-> Distributed cache tests 
-> Geo-locality reference
-> Simplify code
-> wss (secure)
-> Complete documentation and comments
-> Extended readmes
-> Add log messages
-> Exception handling and seperate classes

  