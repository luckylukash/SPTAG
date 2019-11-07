 # Running your indexes on distributed servers

This guide assumes you have already generated and saved indexes using SPTAG. IF you have not done this, please follow this tutorial to learn how to generate a sample index with an image dataset. 

## Setting up a Server
In the Release folder, create a config file (e.g. serverconfig.ini). An example of the server config file is as follows:

```
[Service]
ListenAddr=0.0.0.0
ListenPort=8000
ThreadNumber=8
SocketThreadNumber=8

[QueryConfig]
DefaultMaxResultNumber=6
DefaultSeparator=,

[Index]
List=BKT

[Index_BKT]
IndexFolder=<path-to-your-index-folder>
```

Then, run the following command in the Release folder to start the server:
```
./server --mode socket --config <name-of-your-config-file>
```

Each server you set up can point to a different index - just change the IndexFolder path in your config file. 

## Setting up the Aggregator
If you wish to aggregate results from multiple servers, then use the aggregator. The client calls the aggregator, and the aggregator will aggregate results from the servers which it points to. In the Release folder, create a config file called **Aggregator.ini**. Note that this .ini file must be named Aggregator.ini, and be in root of the Release folder. 

An example of Aggregator.ini is as follows:
```
[Service]
ListenAddr=0.0.0.0
ListenPort=8100
ThreadNumber=8
SocketThreadNumber=8

[Servers]
Number=2

[Server_0]
Address=127.0.0.1
Port=8000

[Server_1]
Address=127.0.0.1
Port=8010
```

In the config file, you can specify the ports which your servers are running on. 

Then, run the following command to start the aggregator:
```
./aggregator
```

## Setting up the Client

Run the following to start the client:
```
./client --server <server-ip> --port <port-number>
```
You can use the IP address/port of your aggregator or a single server, depending on your setup. 

## Reference

For more options and information on configuring the server, aggregator and client, please refer to the following doc: https://github.com/microsoft/SPTAG/blob/master/docs/GettingStart.md
