**TEST CASE: /id**

`Descriptions:`
    Show the cluster peers and its daemon information
    GET
    
`Preparation:`
    IPFS-cluster with some nodes.
    
`Steps:`

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1	
     - GET operation without any arguments.(1)Create session without verbose argument. http://i.storswift.com:9194/id (2)Create session without verbose argument but with other letters. http://i.storswift.com:9194/idid
     - (1)Response 200 code and body right.(2)Response 404 code.
     - A
   * - 3
     - GET method with error arguments. Create session with error arguments' strings. Eg. verbos=1.
     - Response 200 code.
     - A  
   * - 4
     - Repeat step 1, 2, 3 on another node.
     - Result 1,2, 3.
     - A

**TEST CASE: /peers**

`Descriptions:`
    List the cluster servers with open connections.
    GET method.
    
`Preparation:`
    IPFS-cluster with some nodes.
    
`Steps:`

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1
   
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1	
     - No arguments. (1) Create session without verbose argument. (2)Create session without verbose argument & with other api interface.
     - (1)Response 200 code and body right. (2)Response 404 code.
     - A
   * - 2
     - With verbose argument. (1) Create session with verbose argument and value is 0,1,true and false, respectively. (2) Create session with verbose argument and value null. (3) Create session with verbose argument and error value(non-bool). (4) Create session with verbose argument and other strings.
     - (1)Response 200 code and body right. (2)Response 200 code. (3)Response 200 code. (4)Response 200 code.
     - A
   * - 3
     - GET method with error arguments. Create session with error arguments' strings. Eg. verbos=1.
     - Response 200 code.
     - A  
   * - 4
     - Repeat step 1, 2, 3 on another node.
     - Result 1,2, 3.
     - A
     
**TEST CASE: /peers/{peerID}**

`Descriptions:`
    Remove a cluster peer from the cluster.
    DELETE
    
`Preparation:`
    IPFS-cluster with some nodes. Get each peer ID
    
`Steps:`

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1
   
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - (1) Create session without "peerID" argument. http://i.storswift.com:9194/peers (2) Create session with error "peerID" argument.http://i.storswift.com:9194/peers/xxxx (3) Create session with error log string.http://i.storswift.com:9194/peers/x (4) Convert the peerid to capital letters. Then DELETE.
     - (1) Error code. 404. (2) Error code. 400.{"code": 400,"message": "error decoding Peer ID: uvarint: buffer too small"} (3) {"code": 400, "message": "error decoding Peer ID: multihash length inconsistent:" } (4)204 code. No peer will be removed.
     - M
   * - 2
     - With correct argument and value. (1) Create session with required argument and correct value. Check peers. (2) DELETE the peerID again.(This step equal delete a peer which not exist but id is regular correct QmW8vdqrNj86rbW6RnWTUnFFD1XcHrUws3rv4GGbiNR7cx)
     - (1) 204 code and correct body. The peer be removed. (2) 204 code.
     - M
   * - 3
     - Repeat step 1, 2 on another node.
     - Result 1,2.
     - M
     
**TEST CASE: /pins**

`Descriptions:`
    List current status of pins in the cluster.
    GET
    
`Preparation:`
    IPFS-cluster with some nodes.
    
`Steps:`

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1
   
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Create session without any parameters. (1) GET when no pins. (2) GET when exist pins. (3) GET use the error api strings, eg. /pinss.
     - (1) 200 code and body is []. (2) 200 code and body correct. (3) 404 code.
     - A
   * - 2
     - Wth verbose parameter. (1) Use correct bool value. 0/1/true/false. (2) Use error value. XXX, 34, "2" and so on.
     - 200 code and body correct.
     - A
   * - 3
     - With quiet parameter. (1) Use correct bool value. (2) Use error value.
     - 200 code.
     - A
   * - 4
     - With combined parameters. Use verbose and quiet parameters with correct values. Use correct verbose value and error quiet value. Use correct quiet value and error verbose value.
     - 200 code.
     - A
   * - 5
     - Repeat step 1, 2, 3, 4 on another node.
     - Result 1-4.
     - A
     
**TEST CASE: /pins/{cid}/sync**

`Descriptions:`
    Sync local status from IPFS.
    POST
    
`Preparation:`
    IPFS-cluster with some nodes. A pins file cid.
    
`Steps:`

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1     
    
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Create session with correct cid.
     - 200 code and body correct.
     - A
   * - 2
     - Create session with incorrect cid.
     - 400 code. {"code":400,"message":"error decoding Cid: selected encoding not supported"}
     - A
   * - 3
     - Create without cid. curl -X POST http://10.10.165.11:9094/pins/sync
     - 200 code. 
     - A
   * - 4
     - On another node create session with another cid.
     - 200 code.
     - A
   * - 5  
     - Check cid string from step 1 on different node.
     - Correct.
     - M
     
**TEST CASE: /pins/{cid}/recover**

`Descriptions:`
    Recover a CID.
    POST
    
`Preparation:`
    IPFS-cluster with some nodes. A pins file cid.
    
`Steps:`     

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1     
    
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Create session with correct cid string.
     - 200 code and body correct.
     - A
   * - 2
     - Create session with incorrect cid string.
     - 400 code.
     - A
     
**TEST CASE: /pins/recover**

`Descriptions:`
    Attempt to re-pin/unpin CIDs in error state.
    POST
    
`Preparation:`
    IPFS-cluster with some nodes. A pins file cid.
    
`Steps:`     

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1     
    
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Create session without any cid string.
     - 400 code.
     - A
   * - 2
     - Create session with local=true.
     - 200 code and body correct.
     - A
   * - 3
     - Create session with local=false.
     - 400 code.
     - A
   * - 4
     - Create an error cid state. Create session with local=true then check the pins status.
     - 200 code and status correct.
     - M
     
**TEST CASE: /api/v0/uid/new**

`Descriptions:`
    Create a unique UID and peer ID pair from Hive cluster. 
    The UID can be used to identify endpoints in communication， the PeerID is a virtual IPFS peer ID.
    
`Preparation:`
    IPFS-cluster with some nodes.
    
`Steps:`     

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1 
    
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     -
     -
     -
     
**TEST CASE: /api/v0/uid/login**

`Descriptions:`
    Log in to Hive Cluster using the UID you created earlier.
    
`Preparation:`
    IPFS-cluster with some nodes.
    
`Steps:`     

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1 
    
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     -
     -
     - 
     
**TEST CASE: /api/v0/file/pin/add**

`Descriptions:`
    Pin objects in the cluster.
    GET, POST
    
`Preparation:`
    IPFS-cluster with some nodes.
    
`Steps:`     

.. list-table:: 
   :widths: 10 30 30 10
   :header-rows: 1 
    
   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET and POST the api without any parameters.
     - 500 code. {"Message": "Error parsing CID: selected encoding not supported"}
     - A
   * - 2
     - GET and POST the api with correct arg string.
     - 200 code.
     - A
   * - 3
     - GET and POST the api with another arg string which not exist but comply the hash regular.
     - 200 code and body correct.
     - A
   * - 4
     - GET and POST the api with another arg string which not exist and not comply the hash regular, eg. xxxxx.
     - 500 code. {"Message": "Error parsing CID: selected encoding not supported"}
     - A
   * - 5
     - GET and POST the api with "recursive" is 0/false.
     -
     -