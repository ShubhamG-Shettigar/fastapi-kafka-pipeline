1. Kafka Connect (Understanding basic terms, tasks, workers, sink, source connectors, why it exists, when to use, examples)
Kafka Connect is a distributed framework that acts as a platform to transfer data from source to kafka or from Kafka to sink. 
We need to have a Connector Plugin (Java code that has the actual logic) + Connector Configuration File (which instantiates the plugin file with the defined configs)
Once the plugin is installed and the Config is submitted -> Connector plugin instance gets created (Similar to a Java Object)

There is no separate "Kafka Connect Cluster". Workers group together to form a "logical" cluster. Connector plugin once instantiated with the connector configs, it is installed in each of the workers.
Workers are created by us. Connector instance decides how much tasks at max can be created (tasks.max property)
Workers assign those tasks among themselves (Just like the consumer group coordinator behavior, rebalance, heartbeats, etc) and Tasks do the actual job (of data movement)

There are 3 internal topics
_connect-configs (for storing configs of workers, cleanup policy = compact)
_connect-offsets (per tasks/per partition storage (cleanup policy = compact))
_connect-status (for storing the status of the workers, (active, dead, etc))

Source vs Sink Connector
Standalone Mode (1 worker -> Used in DEV/testing)
Distributed Mode (scalability -> Used in Production)
Converters vs Serializer (Serializers are written in the codes and uses Java objects that are created inside the producer/consumer code, but for connectors, we dont know what Java object is it. Its just an external
system that reads from some source, so we use a generic converter incase of connectors)

Each source row -> Connect record (stored inside worker memory and has schema (to identify the format) and the actual data) -> AVRO converter -> Converter fetches the Schema from the Schema
Registry -> Schema id sent back -> Appended to Kafka msg along with the data -> Sent to the broker and then to the Kafka topic

End to end workflow -> Producer -> Serializer/Converter -> Schema Registry -> Broker -> Topic -> Deserializer/Converter -> Schema Registry -> Consumer 





