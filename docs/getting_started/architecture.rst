############
Architecture
############



.. graphviz::

   digraph architecture {
    graph[
    ];
    node[
        fontsize = "16";
    ];
    "web" [
        shape = "record"
    ];
    "worker" [
        shape = "record"
    ];
    "database" [
        shape = "record"
    ];
    "celery" [
        shape = "record"
    ];
    "reddis" [
        shape = "record"
    ];
    "elasticsearch" [
        shape = "record"
    ];
    "haystack" [
        shape = "record"
    ];

    "database" -> "web";
    "database" -> "worker";

    "web" -> "celery" -> "reddis" -> "worker";
    "web" -> "haystack" -> "elasticsearch";
   }
