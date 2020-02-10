

There are three folders presenting the solutions of the following three problems:

1. Problem 1:
- Wrote a program that accepts two lines as tuple arguments. Returns a boolean true on overlap. Test has been provided

2. Problem 2:
- Wrote a python object class that accepts 2 version string as a constructor arg and has a comparable function to 
  compare with same class object.

3. Problem 3:
- This was my favourite, started off with exploring different ways to store cache data. For retrieving data it 
  had to be stored in dictionary(python data-structure) with constant time retrieval, lets call it key-store. 
  But then how would you add least recently used feature to the program? That's where I started admiring 
  doubly linked list(DLL) for its O(1) additions and deletions. I had a look around at the existing doubly linked 
  list libraries out there such as pyllist, but it only provided the function to delete indexed node(for that 
  I had to remember the index) and the list length can change. So I ended writing a class for it *CacheList* in 
  cache_dlinked_list.py. Added functions for this use-case including the generic pop_from_tail, add_to_head and 
  specifically deleting a node using the node as an arg itself. We will call this DDL key-list 
- The key is stored in key-list whereas for the same key another dictionary is stored in key-store. This dictionary 
  would include the value, timestamp(when the value was accessed) and the node itself(reference in the world of objects).
- Two implementation of caches are presented in SimpleCache and DistributedCache. SimpleCache is a single instance 
  running of cache.
- Distributed cache is based on asyncio and uses websockets to connect to other neighbour instances. This mini-project enabled
  me to put my asyncio theoretical knowledge into practise(plenty of aspects to improve on). 
  - Upon every set operation, the value is set in other instances to present real time replication. 
  - Upon every get request, a synch get is executed in other instances to have consistent LRU data. 
  - Upon encountering expired data, a synch expiration call is executed on other instances to clear space.
  - A reload call has been added to the library so that an instance could reload its neighbours data on start. 
   
  
  
  
***LIBRARY FEATURES***
1. **Fast retrieval cache**
 - Cache value retrieved from dictionary O(n) -> 1


2. **LRU cache**
 - Implemented using a doubly linked list
   - Insertions anywhere O(n) -> 1
   - Deletion anywhere O(n) -> 1
   
   
3. **Expiration**
 - Timestamp of creation or modification is stored in the dictionary, upon each retrieval expiration is 
   accessed and if the data is expired(rest of the data following is also cleared)
 - The expiration async function will only be invoked if the expired data is accessed, in other cases LRU 
   functionality of the code should clear the linked list upon need
   
   
4. **Scalable**
 - Distributed Cache library is available, and it has features of synchronization(upon every write),
   reload(load the data from an another instance) and expiration sync(upon finding expired data, the 
   data will be removed from all instances)


5. **Fault tolerance**
 - An interface to either retrieve already saved data from the filesystem or data base could be added to initialize
   the cache_handler class. Currently the distributed_cache instance asks up from a neighbour for reloading cache 
  
  
6. **Geo-Distributed access**
 - If we're on cloud (we have to be on cloud for scalable distributed fault-tolerant systems) we can use something like
   AWS route-53 which provides with Geolocation routing. Something like this would enable us to choose between the resources 
   that serve our traffic based on the geographic location of users accessing the data using the DNS entry for our service.




Makefile is provided.
*Tests*
```make test```


**Things I still intend to do**
- wss (secure)
- write some more unittests and integration test (there has to be bugs)

  