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
     - Result 1,2,3.
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
    Add some files and remember the hash values.
    Add a directory with some files.

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
     - GET and POST the api with "recursive" is 0/false. (1) pin add a file. (2) pin add a directory.
     - 200 code.
     - A
   * - 6
     - GET and POST with "hidden" is 1/true.
     - 200 code.
     - A
   * - 7
     - POST and GET with correct joint parameter. Eg. recursive=1&hidden=1.
     - 200 code.
     - A
   * - 8
     - POST and GET with correct joint parameter. But some of them value incorrect. Eg. recursive=directxxx&hidden=1
     - 200 code.
     - A
   * - 9
     - POST and GET with joint parameter. But some of parameter incorrect. Eg. recursive=1&hiddenxx=1
     - 200 code.
     - A

**TEST CASE: /api/v0/file/pin/ls**

`Descriptions:`
    List objects that pinned to the cluster.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.
    Add some files and remember the hash values.
    Create some different status of pin, "direct", "indirect", "recursive".

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - POST and GET without any parameter.
     - 200 code and body correct.
     - A
   * - 2
     - POST and GET with "type" and the value is "direct", "indirect", "recursive", "all" respectively.
     - 200 code and return result correct.
     - A
   * - 3
     - POST and GET with "quiet". Each bool value respectively.
     - 200 code.
     - A
   * - 4
     - POST and GET with correct joint parameter. Eg. type=direct&quiet=1.
     - 200 code.
     - A
   * - 5
     - POST and GET with correct joint parameter. But some of them value incorrect. Eg. type=directxxx&quiet=1
     - 200 code.
     - A
   * - 6
     - POST and GET with joint parameter. But some of parameter incorrect. Eg. type=direct&qxxxxuiet=1
     - 200 code.
     - A

**TEST CASE: /api/v0/file/pin/rm**

`Descriptions:`
    Remove pinned objects from the cluster.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.
    Add some files and remember the hash values.
    Create some different status of pin, "direct", "indirect", "recursive".

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - POST and GET without any parameter. http://10.10.165.11:9095/api/v0/pin/rm
     - 500 code. {"Message":"Error: bad argument"}
     - A
   * - 2
     - GET with an error hash value. http://10.10.165.11:9095/api/v0/pin/rm?arg=xxxxxx
     - 500 code. {"Message":"Error parsing CID: selected encoding not supported"}
     - A
   * - 3
     - GET with correct hash value.
     - 200 code. Then check status correct.
     - A
   * - 4
     - POST with an unpin hash.
     - 500 code. {"Message":"cannot unpin pin uncommitted to state: cid is not part of the global state"}
     - A
   * - 5
     - POST with an correct hash.
     - 200 code.
     - A
   * - 6
     - GET with recursive and correct value.
     - 200 code.
     - A
   * - 7
     - POST with recursive and incorrect value.
     - 200 code.
     - A
   * - 8
     - GET with error parameter string. Eg. recursivxxx
     - 200 code.
     - A

**TEST CASE: /api/v0/file/add**

`Descriptions:`
    Add a file or directory to cluster.
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
     - POST and GET without any parameter. http://10.10.165.11:9095/api/v0/add
     - 500 code. {"Message":"error reading request: request Content-Type isn't multipart/form-data"}
     - A
   * - 2
     - POST and GET required argument "path".
     - 200 code and add file successful. Return body correct.
     - A
   * - 3
     - POST and GET required argument "path", but file not exist.
     - Return fail message.
     - A
   * - 4
     - POST and GET a random string of "path".
     - 200 code.
     - A
   * - 5
     - POST and GET with correct value of "recursive".
     - 200 code.
     - A
   * - 6
     - POST and GET with incorrect value of "recursive".
     - 200 code.
     - A
   * - 7
     - POST and GET with correct value of "hidden".
     - 200 code.
     - A
   * - 8
     - POST and GET with incorrect value of "hidden".
     - 200 code.
     - A
   * - 9
     - GET with error parameter string. Eg. recursivxxx
     - 200 code.
     - A
   * - 10
     - POST and GET with correct joint parameter.
     - 200 code.
     - A
   * - 11
     - POST and GET with correct joint parameter. But some of them value incorrect.
     - 200 code.
     - A
   * - 12
     - POST and GET with joint parameter. But some of parameter incorrect.
     - 200 code.
     - A

**TEST CASE: /api/v0/file/get**

`Descriptions:`
    Download files from the cluster.
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
     - GET and POST without required argument.
     - 400 code.
     - A
   * - 2
     - GET and POST with correct "arg" argument.
     - 200 code and body correct.
     - A
   * - 3
     - GET and POST with correct "arg" argument but value incorrect. Eg. xxxx
     - 500 code.
     - A
   * - 4
     - GET and POST with correct "arg" argument ,value correct but not exist.Eg. QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQh
     - Timeout and error.
     - A
   * - 5
     - GET with "output" argument.
     - <>
     - M
   * - 6
     - GET with "archive" argument.
     - <>
     - M
   * - 7
     - GET with "compress" argument with correct bool value.
     - 200 code.
     - A
   * - 8
     - GET with "compress" argument with incorrect bool value.
     - 500 code.
     - A
   * - 9
     - GET with "arg", "compress" and "compress-level" arguments with correct value.
     - 200 code.
     - A
   * - 10
     - GET with "arg", "compress" and "compress-level" arguments but level value not in 1-9.
     - 500 code. {"Message":"compression level must be between 1 and 9","Code":0,"Type":"error"}
     - A
   * - 11
     - GET with "arg" and "compress-level" arguments only
     - 200 code.
     - A

**TEST CASE: /api/v0/file/ls**

`Descriptions:`
    List directory contents for Unix filesystem objects.
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
     - GET and POST without required argument.
     - 400 code.
     - A
   * - 2
     - GET and POST with correct "arg" argument and value.
     - 200 code and body correct.
     - A
   * - 3
     - GET and POST with correct "arg" argument and error value.
     - 500 code. {"Message":"invalid 'ipfs ref' path","Code":0,"Type":"error"}
     - A

**TEST CASE: /api/v0/files/cp**

`Descriptions:`
    Copy files among clusters.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.


`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET and POST without required argument.
     - 400 code.
     - A
   * - 2
     -
     -
     - A

**TEST CASE: /api/v0/files/flush**

`Descriptions:`
    Flush a given path’s data to cluster.
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
     - GET without required argument.
     - 200 code. Null body.
     - A
   * - 2
     - GET with an error uid string.
     - 200 code. Null body.
     - A
   * - 3
     - GET with "path" string which not / and not exist.
     - 200 code.
     - A
   * - 4
     - Make a directory and add a file. GET with path argument.
     - 200 code. Body correct.
     - A

**TEST CASE: /api/v0/files/ls**

`Descriptions:`
    List directories in the private mutable namespace.
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
     - GET without required argument.
     - 200 code. Eg: {"Entries":[{"Name":"suxx","Type":0,"Size":0,"Hash":""},{"Name":"suxx2","Type":0,"Size":0,"Hash":""}]}
     - A
   * - 2
     - GET with "uid" argument.
     - 200 code.
     - A
   * - 3
     - GET with "uid" but value is error.
     - 200 code.
     - A
   * - 4
     - POST with "path" argument. The value is an exist directory.
     - 200 code.<!>
     - A
   * - 5
     - POST with "path" the value is an un-exist directory.
     - 200 code.<!>
     - A

**TEST CASE: /api/v0/files/mkdir**

`Descriptions:`
    Create directories.
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
     - GET without required argument.
     - 400 code.
     - A
   * - 2
     - GET with "path" argument only.
     -
     - A
   * - 3
     - GET with "uid" argument only.
     -
     - A
   * - 4
     - POST with "path" and "uid" value.
     -
     - A

**TEST CASE: /api/v0/files/mv**

`Descriptions:`
    Move files.
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
     - GET without required argument.
     - 400 code.
     - A
   * - 2
     - GET with "source" argument only.
     - 400 code.
     - A
   * - 3
     - GET with "dest" argument only.
     - 400 code.
     - A
   * - 4
     - POST with "source" and "dest" value.
     -
     - A
   * - 5
     - GET with "uid" argument only.
     -
     - A


**TEST CASE: /api/v0/files/read**

`Descriptions:`
    Read a file in a given path.
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
     - GET without required argument.
     - 400 code.
     - A
   * - 2
     -
     -
     -


**TEST CASE: /api/v0/files/rm**

`Descriptions:`
    Remove a file.
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
     - GET without required argument.
     - 400 code.
     - A
   * - 2
     - GET method rm a directory.
     - 500 code. {"Message":"/suxx is a directory, use -r to remove directories","Code":0,"Type":"error"}
     - A
   * - 3
     - GET rm an un-exist file.
     - 500 code. {"Message":"file does not exist","Code":0,"Type":"error"}
     - A


**TEST CASE: /api/v0/files/stat**

`Descriptions:`
    Display file status.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.
    Make some directory.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 400 code.
     - A
   * - 2
     - GET with "path"(arg) with error directory value.
     - 500 code.{"Message":"file does not exist","Code":0,"Type":"error"}
     - A
   * - 3
     - GET with "path"(arg) with correct directory value.
     - 200 coed. Body correct.
     - A
   * - 4
     - GET with "format" arguments and value.
     - 200 code.
     - M

**TEST CASE: /api/v0/files/write**

`Descriptions:`
    Write to a mutable file in a given filesystem.
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
     - GET without required argument.
     - 400 code.
     - A
   * - 2
     -
     -
     -

**TEST CASE: /api/v0/name/publish**

`Descriptions:`
    Publish user context file or directory to public.
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
     -
     -
     - A

**TEST CASE: /api/v0/message/pub**

`Descriptions:`
    Publish a message to a given pubsub topic.
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
     -
     -
     - A

**TEST CASE: /api/v0/message/sub**

`Descriptions:`
    Subscribe to message to a given topic.
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
     -
     -
     - A


**TEST CASE: /version**

`Descriptions:`
    Version information.
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
     - GET and POST without any argument.
     - 200 code. Body correct.
     - A
   * - 2
     - GET and POST with "number" correct argument.
     -
     - A
   * - 3
     - GET and POST with "number" incorrect argument.
     -
     - A
   * - 4
     - GET and POST with "commit" correct argument.
     -
     - A
   * - 5
     - GET and POST with "commit" incorrect argument.
     -
     - A
   * - 6
     - GET and POST with "repo" correct argument.
     -
     - A
   * - 7
     - GET and POST with "repo" incorrect argument.
     -
     - A
   * - 8
     - GET and POST with "all" correct argument.
     -
     - A
   * - 9
     - GET and POST with "all" incorrect argument.
     -
     - A
   * - 8
     - GET and POST with joint correct argument.
     -
     - A
   * - 9
     - GET and POST with joint incorrect argument.
     -
     - A