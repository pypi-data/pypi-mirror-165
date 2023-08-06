import py2neo
import uuid
import threading
import time
from typing import Dict, List
from DZDutils.neo4j import (
    nodes_to_buckets_distributor,
    run_periodic_iterate,
    wait_for_index_build_up,
)

# TODO: Check if text index is used with toString https://neo4j.com/docs/cypher-manual/4.4/query-tuning/indexes/#administration-indexes-node-text-index-example
class TextIndexBucketProcessor:
    _iterate_bucket_prefix: str = "_Bucket_mp_iter_"
    text_bucket_prefix: str = "_Bucket_mp_ft_"
    batchSize: int = 500
    _pre_neo4j_4_4_no_index: bool = False
    # call db.index.fulltext.listAvailableAnalyzers
    fulltext_index_analyzer: str = None

    def __init__(self, graph: py2neo.Graph, buckets_count_per_collection: int = 8):
        self.graph = graph
        self.id = uuid.uuid4().hex[:6]
        self.buckets_count_per_collection: int = buckets_count_per_collection
        self.bucket_text_index_names: Dict[str, str] = {}
        self.text_collection_property: str = None
        self.iterate_collection_buckets: List[str] = None
        self.text_collection_buckets = None

    def set_iterate_node_collection(self, name: str, query: str):
        if self.iterate_collection_buckets:
            # This instance was already set with another text node collection and is propaly reused. lets clean up the stuff from previous runs
            self._clean_up_iterate_buckets()
        self.iterate_collection_buckets: List[str] = nodes_to_buckets_distributor(
            self.graph,
            query,
            bucket_count=self.buckets_count_per_collection,
            bucket_label_prefix=f"{self._iterate_bucket_prefix}{self.id}_",
        )
        self.iterate_collection_name = name

    def set_text_node_collection(
        self,
        name: str,
        query: str,
        fulltext_index_properties: List[str] = None,
        text_index_property: str = None,
    ):
        if fulltext_index_properties and text_index_property:
            raise ValueError(
                "'fulltext_index_properties'  and 'text_index_property' are both provided. Only either one can be provided."
            )
        elif not fulltext_index_properties and not text_index_property:
            raise ValueError(
                "No 'fulltext_index_properties' and no 'text_index_property' provided. One of these param sneed to be provided."
            )

        if self.text_collection_buckets:
            # This instance was already set with another text node collection and is propaly reused. lets clean up the stuff from previous runs
            self._clean_up_text_buckets()
            self.text_collection_property = None
        self.text_collection_buckets = nodes_to_buckets_distributor(
            self.graph,
            query,
            bucket_count=self.buckets_count_per_collection,
            bucket_label_prefix=f"{self.text_bucket_prefix}{self.id}_",
        )
        self.text_collection_name = name
        if fulltext_index_properties:
            self._create_fulltext_index_buckets(fulltext_index_properties)
        if text_index_property:
            self.text_collection_property = text_index_property
            self._create_text_index_buckets(text_index_property)

    def _create_text_index_buckets(self, property: str):
        for bucket_label in self.text_collection_buckets:
            ti_name: str = f"{bucket_label}_ti"
            q = f"CREATE TEXT INDEX {ti_name} FOR (n:{bucket_label}) ON (n.{property})"
            if not self._pre_neo4j_4_4_no_index:
                self.graph.run(q)
            self.bucket_text_index_names[bucket_label] = ti_name
        if not self._pre_neo4j_4_4_no_index:
            wait_for_index_build_up(
                self.graph, list(self.bucket_text_index_names.values())
            )

    def _create_fulltext_index_buckets(self, properties: List[str]):
        for bucket_label in self.text_collection_buckets:

            options = ""
            if self.fulltext_index_analyzer:
                options = f" OPTIONS {{indexConfig: {{`fulltext.analyzer`: '{self.fulltext_index_analyzer}'}}}}"
            fti_name: str = f"{bucket_label}_FTI"
            q = f'CREATE FULLTEXT INDEX  {fti_name} FOR (n:{bucket_label}) ON EACH [{",".join(["n." + prop for prop in properties])}] {options}'
            self.graph.run(q)
            self.bucket_text_index_names[bucket_label] = fti_name
        wait_for_index_build_up(
            self.graph,
            list(self.bucket_text_index_names.values()),
            log_status_func=None,
        )

    def clean_up(self, clean_orphean_full_text_index: bool = False):
        self._clean_up_iterate_buckets()
        self._clean_up_text_buckets()
        if clean_orphean_full_text_index:
            self._clean_up_orphean_buckets_and_indexes()

    def _clean_up_iterate_buckets(self):
        for bucket_label in self.iterate_collection_buckets:
            run_periodic_iterate(
                self.graph,
                cypherIterate=f"MATCH (n:{bucket_label}) return n",
                cypherAction=f"REMOVE n:{bucket_label}",
                parallel=True,
            )

    def _clean_up_text_buckets(self):
        for bucket_label, index_name in self.bucket_text_index_names.items():
            q = f"DROP INDEX {index_name}"
            self.graph.run(q)
        for bucket_label in self.text_collection_buckets:
            run_periodic_iterate(
                self.graph,
                cypherIterate=f"MATCH (n:{bucket_label}) return n",
                cypherAction=f"REMOVE n:{bucket_label}",
                parallel=True,
            )

    def _clean_up_orphean_buckets_and_indexes(self):
        # delete indexes
        indexes = self.graph.run("SHOW INDEXES YIELD type, name").to_data_frame()
        if not indexes.empty:
            for index_name in indexes["name"].to_list():
                if index_name.startswith(self.text_bucket_prefix):
                    self.graph.run(f"DROP INDEX {index_name}")
        # delete labels
        labels: List[str] = (
            self.graph.run("call db.labels()").to_data_frame()["label"].tolist()
        )
        for label in labels:
            if label.startswith(self.text_bucket_prefix) or label.startswith(
                self._iterate_bucket_prefix
            ):
                run_periodic_iterate(
                    self.graph,
                    cypherIterate=f"MATCH (n:{label}) return n",
                    cypherAction=f"REMOVE n:{label}",
                    parallel=True,
                )

    @classmethod
    def _run_periodic_iterate_thread(cls, params: Dict):
        run_periodic_iterate(concurrency=1, parallel=True, **params)

    def run_text_index(
        self,
        iterate_property,
        cypher_action,
    ):
        query_params_per_iter_bucket: Dict[str, List[Dict]] = {}
        # exmaple cypher_action
        # cypher_action = f"MERGE (source_col)<-[r:HAS_GENE]-(target_col)"

        # Collect query params
        for text_index_bucket_label in self.text_collection_buckets:
            bucket_text_index_name = self.bucket_text_index_names[
                text_index_bucket_label
            ]
            for iterate_bucket in self.iterate_collection_buckets:
                match_query = f"MATCH ({self.iterate_collection_name}:{iterate_bucket}) return {self.iterate_collection_name}"

                if self.text_collection_property:
                    # text query via 'CONTAINS'
                    ti_query = f"""MATCH ({self.text_collection_name}:{text_index_bucket_label}) WHERE {self.text_collection_name}.{self.text_collection_property} CONTAINS toString({self.iterate_collection_name}.{iterate_property}) """
                else:
                    # Fulltext query via db.index.fulltext.queryNodes
                    ti_query = f"""call db.index.fulltext.queryNodes('{bucket_text_index_name}', '\\"' + {self.iterate_collection_name}.{iterate_property} + '\\"') yield node as {self.text_collection_name},score"""
                action_query = f"{ti_query} {cypher_action}"
                if not iterate_bucket in query_params_per_iter_bucket:
                    query_params_per_iter_bucket[iterate_bucket] = []
                query_params_per_iter_bucket[iterate_bucket].append(
                    dict(
                        graph=self.graph,
                        cypherIterate=match_query,
                        cypherAction=action_query,
                        batchSize=self.batchSize,
                    )
                )

        # Run queries parallel
        for bucket_name, querie_params in query_params_per_iter_bucket.items():
            # todo: refactor with pool executor https://realpython.com/intro-to-python-threading/#using-a-threadpoolexecutor
            threads = []
            for query_param in querie_params:
                t = threading.Thread(
                    target=self._run_periodic_iterate_thread, args=(query_param,)
                )
                threads.append(t)
                t.start()
            for t in threads:
                t.join()


def create_demo_data(g: py2neo.Graph):
    # create test nodes
    import graphio

    list_of_genes = [
        "A2M",
        "ABL1",
        "ACE2",
        "ACE212",
        "ACE2232fw",
        "CACNA1A",
        "CHEK2",
        "CREBBP",
        "CTNNB1",
        "EEF1E1",
        "EP300",
    ]
    nodeset = graphio.NodeSet(["Gene", "TestGenes"], merge_keys=["sid"])
    for gene in list_of_genes:
        nodeset.add_node(properties={"sid": gene})
    nodeset.create_index(g)
    nodeset.merge(g)

    abstract_texts = [
        "Lorem A2M ipsum ABL1 dolor ACE2-232.fw sit amet, consetetur CACNA1A sadipscing elitr, sed EP300 diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, EP300 consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum CHEK2 dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, CTNNB1 sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    ]
    nodeset = graphio.NodeSet(["AbstractText", "TestAbstractText"], merge_keys=["text"])
    for text in abstract_texts:
        nodeset.add_node(properties={"text": text})
    nodeset.create_index(g)
    nodeset.merge(g)
