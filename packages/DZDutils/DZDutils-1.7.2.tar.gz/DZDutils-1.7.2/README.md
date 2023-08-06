# DZDutils

## About

**Maintainer**: tim.bleimehl@dzd-ev.de

**Licence**: MIT

**Purpose**: Collection of homemade Python tools of the German Center for Diabetes Research

[[_TOC_]]


## Install

`pip3 install DZDutils`

or if you need the current dev version:

`pip3 install git+https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils.git`


## Modules

### DZDutils.inspect

#### object2html

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/inspect/object2html.py#L58)

Opens the webbrowser and let you inspect any object / dict with jquery jsonviewer

```python
from DZDutils.inspect import object2html
my_ultra_complex_dict = {"key":"val"}
object2html(my_ultra_complex_dict)
``` 

### DZDutils.list

#### chunks

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/list.py#L5)

Breaks up a list in shorter lists of given length

```python
from DZDutils.list import chunks
my_ultra_long_list = [1,2,3,4,5,6,7,8,9,10]
for chunk in chunks(my_ultra_long_list, 3)
    print(chunk)
```

Output:

```python
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
[10]
``` 


#### divide

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/list.py#L12)

Breaks up a list in a given amount of shorter lists

```python
from DZDutils.list import divide
my_ultra_long_list = [1,2,3,4,5,6,7,8,9,10]
for chunk in divide(my_ultra_long_list, 3)
    print(chunk)
```

Output:

```python
[1, 2, 3, 4]
[5, 6, 7]
[8, 9, 10]
``` 

### DZDutils.neo4j


#### wait_for_db_boot

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/neo4j/tools/wait_for_db_boot.py)

Wait for a neo4j to boot up. If timeout is expired it will raise the last error of the connection expception for debuging.
The argument `neo4j` must be a dict of py2neo.Graph() arguments -> https://py2neo.org/2021.1/profiles.html#individual-settings

```python
from DZDutils.neo4j import wait_for_db_boot
wait_for_db_boot(neo4j={"host": "localhost"}, timeout_sec=120)
```

#### wait_for_index_build_up

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/neo4j/tools/wait_for_index_build_up.py)

Provide a list of index names and wait for them to be online

```python
import py2neo
from DZDutils.neo4j import wait_for_index_build_up

g = py2neo.Graph()

g.run("CREATE FULLTEXT INDEX FTI_1 IF NOT EXISTS FOR (n:MyNode) ON EACH [n.my_property]")
g.run("CREATE INDEX INDEX_2 IF NOT EXISTS FOR (n:MyNode) ON EACH [n.my_property]")
g.run("CREATE FULLTEXT INDEX FTI_3 IF NOT EXISTS FOR (n:MyNode) ON EACH [n.my_property]")

wait_for_fulltextindex_build_up(graph=g,index_names=["FTI_1","INDEX_2","FTI_3"])

print("Indexes are usable now")

```

#### nodes_to_buckets_distributor

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/neo4j/tools/nodes_to_buckets_distributor.py)

Divide a bunch of nodes into multiple buckets (labels with a prefix and sequential numbering e.b. "BucketLabel1, BucketLabel2, ...")

Supply a query return nodes. Get a list of str containg the buckets label names


```python
import py2neo
from DZDutils.neo4j import nodes_to_buckets_distributor

g = py2neo.Graph()

# Create some testnodes

g.run(f"UNWIND range(1,10) as i CREATE (:MyNodeLabel)")

labels = nodes_to_buckets_distributor(
            g,
            query=f"MATCH (n:MyNodeLabel) return n",
            bucket_count=3,
            bucket_label_prefix="Bucket",
        )

print(labels)
```
Output:

`['Bucket0','Bucket1','Bucket2']`

Each of our `:MyNodeLabel`-Nodes has now applied one of the bucket labels


#### run_periodic_iterate

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/neo4j/tools/run_periodic_iterate.py)

Abstraction function for [`apoc.periodic.iterate`](https://neo4j.com/labs/apoc/4.1/overview/apoc.periodic/apoc.periodic.iterate/) with proper error handling and less of the string fumbling

```python
import py2neo
from DZDutils.neo4j import run_periodic_iterate

g = py2neo.Graph()

# Create some node per iterate
run_periodic_iterate(
        g,
        cypherIterate="UNWIND range(1,100) as i return i",
        cypherAction="CREATE (n:_TestNode) SET n.index = i",
        parallel=True,
    )

# set some props per iterate
run_periodic_iterate(
        g,
        cypherIterate="MATCH (n:_TestNode) return n",
        cypherAction="SET n.prop = 'MyVal'",
        parallel=True,
    )
```

##### Error Handling

When using `apoc.periodic.iterate` manual you have to parse the result table for errors and interpret the result if and how a query failed.


With `run_periodic_iterate` you dont have to anymore.

Lets have an example and write some faulty query

```python
import py2neo
from DZDutils.neo4j import run_periodic_iterate

g = py2neo.Graph()

# Create some node per iterate
run_periodic_iterate(
        g,
        cypherIterate="UNWIND range(1,100) as i return i",
        cypherAction="f*** ohnooo i cant write proper cypher",
        parallel=True,
    )
```

This will result in an exception: 

```
DZDutils.neo4j.Neo4jPeriodicIterateError: Error on 100 of 100 operations. ErrorMessages:

 Invalid input 'f': expected
  ","
  "CALL"
  "CREATE"
[...]
  "WITH"
  <EOF> (line 1, column 46 (offset: 45))
"UNWIND $_batch AS _batch WITH _batch.i AS i  f*** ohnooo i cant write proper cypher"
```

As wee see we get immediately feedback if and how the query failed

#### LuceneTextCleanerTools

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/neo4j/LuceneTextCleanerTools.py)

`LuceneTextCleanerTools` is a class with some functions/tools to prepare node properties to be used as input for a lucene fulltext search. 

e.g. You want to search for `(:Actor).name` in any `(:Movie).description`. In real word data you will mostly have some noise in the Actor names: 

* Some Lucene operators like "-" or "OR"
* Or maybe some generic words like "the" which will drown any meaningful results

LuceneTextCleanerTools will help you to sanitize your data.

Lets get started with a small example

```python
import py2neo
import graphio
from DZDutils.neo4j import LuceneTextCleanerTools

g = py2neo.Graph()

# lets create some testdata

actorset = graphio.NodeSet(["Actor"], ["name"])
# lets assume our actor names came from a messy source;
for actor in [
    "The",
    "The.Rock",
    "Catherine Zeta-Jones",
    "Keith OR Kevin Schultz",
    "32567221",
]:
    actorset.add_node({"name": actor})
movieset = graphio.NodeSet(["Movie"], ["name"])
for movie_name, movie_desc in [
    (
        "Hercules",
        "A movie with The Rock and other people. maybe someone is named Keith",
    ),
    (
        "The Iron Horse",
        "An old movie with the twin actors Keith and Kevin Schultz. Never seen it; 5 stars nevertheless. its old and the title is cool",
    ),
    (
        "Titanic",
        "A movie with The ship titanic and Catherine Zeta-Jones and maybe someone who is named Keith",
    ),
]:
    movieset.add_node({"name": movie_name, "desc": movie_desc})

actorset.create_index(g)
actorset.merge(g)
movieset.create_index(g)
movieset.merge(g)

# We have our test data. lets start...

# If we now would do create a fulltext index on `(:Movie).desc` and do a search by every actor name and create a relationship on every actor appearing in the description our result would be all over the place
# e.g.
#   * `Keith OR Kevin Schultz` would be connected to every movie because Keith comes up in every description. But actually we wanted to match  `Keith OR Kevin Schultz` but `OR` is an lucene operator
#   * `Catherine Zeta-Jones` would appear in no description because the Hyphen expludes anything with `Jones`
#   * `The.Rock` would appeat in no description because the data is dirty and there is a dot in his name

# lets sanitize our actor names with LuceneTextCleanerTools
txt = LuceneTextCleanerTools(g)
txt.create_sanitized_property_for_lucene_index(
    labels=["Actor"],
    property="name",
    target_property="name_clean",
    min_word_length=2,
    exlude_num_only=False,
    to_be_escape_chars=["-"],
)
# this will cast our actor names to:
# * "The.Rock" -> "The Rock"
# * "Catherine Zeta-Jones" -> "Catherine Zeta\-Jones"
# * "Keith OR Kevin Schultz" -> "Keith Kevin Schultz"

#  The new value will be writen into a new property `name_clean`. No information is lost

# optionaly, depending on what we want to do, we also can import common words in many languages

txt.import_common_words(
    top_n_words_per_language=4000, min_word_length=2, max_word_length=6
)

# we can now tag actor names that are not suitable for full text matching
txt.find_sanitized_properties_unsuitable_for_lucene_index(
    match_labels=["Actor"],
    check_property="name_clean",
    tag_with_labels=["_OmitFullTextMatch"],
    match_properties_equal_to_common_word=True,
)

# this would tag the Actors `32567221` and `the` as unsuitable. these values are obviously garbage or to common to match anything meaningful

# Now we can do our lucene full test matching on clean data :)
```

For further actions have a look at `TextIndexBucketProcessor`

#### TextIndexBucketProcessor

[code](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/neo4j/TextIndexBucketProcessor.py)

Running a [`db.index.fulltext.queryNodes`](https://neo4j.com/docs/operations-manual/current/reference/procedures/#procedure_db_index_fulltext_querynodes) is a very powerful but also expensiv query.

When running `db.index.fulltext.queryNodes` often against a lot of data it wont scale well. 

For example, in our case, finding thousand of genes (and their synonyms) in million of scientific papers will take a very long time.

The proper solution would be to run multiple queries at a time. But what if you want to generate Nodes and new Relations based on the query result?

You would end up in node locking situations and wont gain much perfomance or even run in timeouts/deadlocks (depending on your actions and/or setup)

Here is where `TextIndexBucketProcessor` can help you:

`TextIndexBucketProcessor` will seperate you data into multiple "Buckets" and do your queries and transforming-actions isolated in these buckets. 

You can now run multiple actions at a time where you usally would end up in Lock situations.

Lets have an example:
(The demodata generator source is [here](https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils/-/blob/master/DZDutils/neo4j/TextIndexBucketProcessor.py#L190))

```python
import py2neo
from DZDutils.neo4j import TextIndexBucketProcessor, create_demo_data


g = py2neo.Graph()
# lets create some testdata first.
# * We create some nodes `(:AbstractText)` nodes with long texts in the property `text`
# * We create some nodes `(:Gene)` nodes with gene IDs in the property `sid`
create_demo_data(g)
# Our goal is now to connect `(:Gene)` nodes to `(:AbstractText)` nodes when the gene sid appears in the abstracts text

# First we create an instance of TextIndexBucketProcessor with a conneciton to our database.
# `buckets_count_per_collection` defines how many isolated buckets we want to run at one time. In other words: The CPU core count we have on our database available
ti_proc = TextIndexBucketProcessor(graph=g, buckets_count_per_collection=6)

# We add a query which contains the nodes with the words we want to search for
ti_proc.set_iterate_node_collection(
    name="gene", query="MATCH (n:Gene) WHERE NOT n:_OmitMatch return n"
)

# Next we add a query which contains the nodes and property name we want to scan.
# You also replace `fulltext_index_properties` with `text_index_property` to use a CONTAINS query instead of fulltext index
ti_proc.set_text_node_collection(
    name="abstract",
    query="MATCH (n:AbstractText) return n",
    fulltext_index_properties=["text"],
)

# Now we define the action we want to apply on positive search results, set the property we search for and start our full text index search
# Mind the names of the nodes: its the name we defined in `add_iterate_node_collection` and `add_fulltext_node_collection`
ti_proc.run_text_index(
    iterate_property="sid", cypher_action="MERGE (abstract)-[r:MENTIONS]->(gene)"
)

# At the end we clean up our bucket labels
ti_proc.clean_up()
```

We now have connected genes that appear in abstracts and did that process with the use of multiple CPU cores and avoided any nodelocking.

This was 4-times faster (because of `buckets_count_per_collection=4`) as just loop throug all genes and send them one by one to `db.index.fulltext.queryNodes`


> :warning: This is a prove of concept with a very narrow scope. You can not modify the `db.index.fulltext.queryNodes`-call which makes this tool rather unflexibel atm. Expect improvements in future versions :) 
