import sys, os
import py2neo

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "../..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))

from DZDutils.neo4j import TextIndexBucketProcessor, create_demo_data


g = py2neo.Graph()
# lets create some testdata first.
# * We create some nodes `(:AbstractText)` nodes with long texts in the property `text`
# * We create some nodes `(:Gene)` nodes with gene IDs in the property `sid`
create_demo_data(g)
# Our goal is now to connect `(:Gene)` nodes to `(:AbstractText)` nodes when the gene sid appears in the abstracts text

# First we create an instance of FullTextIndexBucketMultiProcessor with a conneciton to our database.
# `buckets_count_per_collection` defines how many isolated buckets we want to run at one time. In other words: The CPU core count we have on our database available
ti_proc = TextIndexBucketProcessor(graph=g, buckets_count_per_collection=6)

# We add a query which contains the nodes with the words we want to search for
ti_proc.set_iterate_node_collection(
    name="gene", query="MATCH (n:Gene) WHERE NOT n:_OmitMatch return n"
)
ti_proc.fulltext_index_analyzer = "unicode_whitespace"
# Next we add a query which contains the nodes and property name we want to scan
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
