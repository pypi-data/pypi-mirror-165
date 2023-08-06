import py2neo
import urllib
import graphio
from typing import List, Dict
from DZDutils.neo4j import run_periodic_iterate


class LuceneTextCleanerTools:
    """
    Prepare node property to be suitable for lucene textsearch
    and some extra tools
    Maintainer: Tim Bleimehl
    """

    common_word_labels: List[str] = ["_Word", "_WordCommon"]

    # http://corpus.leeds.ac.uk/frqc/
    word_list_url = {
        "en": "http://corpus.leeds.ac.uk/frqc/internet-en-forms.num",
        "de": "http://corpus.leeds.ac.uk/frqc/internet-de-forms.num",
        "ru": "http://corpus.leeds.ac.uk/frqc/internet-ru-forms.num",
        "chi": "http://corpus.leeds.ac.uk/frqc/internet-zh.num",
        "es": "http://corpus.leeds.ac.uk/frqc/internet-es.num",
        "fr": "http://corpus.leeds.ac.uk/frqc/internet-fr-forms.num",
    }

    def __init__(self, graph: py2neo.Graph):
        self.graph = graph

    def create_sanitized_property_for_lucene_index(
        self,
        labels: List[str],
        property: str,
        target_property: str = None,
        min_word_length: int = 2,
        max_word_length: int = None,
        min_total_length: int = None,
        max_total_length: int = None,
        min_word_count: int = None,
        max_word_count: int = None,
        exclude_num_only: bool = False,
        exclude_num_only_smaller_as: int = None,
        to_be_escape_chars: List[str] = None,
        to_be_removed_chars: List[str] = [
            "!",
            "#",
            "$",
            "%",
            "<",
            ">",
            ".",
            ",",
            "/",
        ],
        escape_character: str = "\\",
        batchSize: int = 10000,
        to_lower: bool = False,
    ):
        """
        Clean/sanitize a certain property for proper textindex matching. We do:
            * (optional) escape a custom a list of chars
            * remove Lucence operators
            * replace "\", '"' and "'" char with space
            * (optional) replace ["!","#","$","%","<",">", ".", ","] with space
            * (optional) remove words shorter as n chars
            * remove whitespaces (expect space)
            * trim double, multi spaces
            * trim trailing, leading spaces
            * (optional) replace values not passing min_word_count or max_word_count with ''
            * optional lower all cases

        and add the result to a new property. If `target_property` is none it defaults to f"{property}_clean"
        """
        escape_placeholder_prefix = "_E_S_C_"
        if target_property is None:
            target_property = f"{property}_clean"
        # init/start cypher action string
        cypher_action = f"SET n.{target_property} = n.{property}"
        cypher_action = fr"""{cypher_action}
            SET n.{target_property} = replace(n.{target_property},'\\\\',' ')
            SET n.{target_property} = replace(n.{target_property},'\"',' ')
            SET n.{target_property} = replace(n.{target_property},'\\'',' ')
        """
        # handle escape chars. we replace them by an indexed placeholder word. when we do wordmatching some lines later they will not trigger any word boundaries
        # at the end we will cast them back to escaped version of them
        if to_be_escape_chars:
            to_be_escapced_chars_indexed = {}
            for index, char in enumerate(to_be_escape_chars):
                to_be_escapced_chars_indexed[
                    f"{escape_placeholder_prefix}{index}"
                ] = char
                cypher_action = f"""{cypher_action}
                SET n.{target_property} = replace(n.{target_property},'{char}','{escape_placeholder_prefix}{index}')
                """
        if to_be_removed_chars:
            for char in to_be_removed_chars:
                cypher_action = f"""{cypher_action}
                SET n.{target_property} = replace(n.{target_property},'{char}',' ')
                """

        # remove lucene operators
        cypher_action = f"""{cypher_action}
            SET n.{target_property} = apoc.text.regreplace(n.{target_property},'[\/\(\)\+\-\|\:\?\*\~\[\]\{{\}}\:\^\&]|(?:^|\W)AND(?:$|\W)|(?:^|\W)NOT(?:$|\W)',' ')
            """
        if min_word_length > 1:
            cypher_action = fr"""{cypher_action}
            SET n.{target_property} = apoc.text.regreplace(n.{target_property},'\\\\b\w{{1,{min_word_length-1}}}\\\\b',' ')
            """
        if max_word_length:
            cypher_action = fr"""{cypher_action}
            SET n.{target_property} = apoc.text.regreplace(n.{target_property},'\\\\b\w{{{max_word_length+1},}}\\\\b',' ')
            """
        if exclude_num_only:
            cypher_action = fr"""{cypher_action}
            SET n.{target_property} = apoc.text.regreplace(n.{target_property},'\\\\b\d+\\\\b',' ')
            """
        if exclude_num_only_smaller_as:
            cypher_action = f"""{cypher_action}
            SET n.{target_property} = CASE WHEN size(apoc.text.regreplace(n.{target_property},'[0-9]','')) = 0 THEN CASE WHEN toInteger(n.{target_property}) >= {exclude_num_only_smaller_as} THEN n.{target_property} ELSE '' END ELSE n.{target_property} END
            """
        # as remove any double/multi spaces
        cypher_action = f"""{cypher_action}
                        SET n.{target_property} = apoc.text.regreplace(n.{target_property},'[^\S ]+|([ ]{{2,}})',' ')"""
        # remove the placeholder for to be escaped chars and replace them by escpaed version of the actual char
        if to_be_escape_chars:
            for placeholder, char in to_be_escapced_chars_indexed.items():
                cypher_action = f"""{cypher_action}
                SET n.{target_property} = replace(n.{target_property},'{placeholder}','{escape_character}{char}')
                """
        cypher_action = f"""{cypher_action}
            SET n.{target_property} = trim(n.{target_property})
            """
        if to_lower:
            cypher_action = f"""{cypher_action}
                SET n.{target_property} = toLower(n.{target_property})
                """

        if min_word_count:
            cypher_action = f"""{cypher_action}
            SET n.{target_property} = CASE WHEN size(split(n.{target_property},' ')) >= {min_word_count} THEN n.{target_property} ELSE '' END
            """
        if max_word_count:
            cypher_action = f"""{cypher_action}
            SET n.{target_property} = CASE WHEN size(split(n.{target_property},' ')) <= {max_word_count} THEN n.{target_property} ELSE '' END
            """
        if min_total_length:
            cypher_action = fr"""{cypher_action}
            SET n.{target_property} = CASE WHEN size(replace(n.{target_property},'\\\\','')) >= {min_total_length} THEN n.{target_property} ELSE '' END
            """
        if max_total_length:
            cypher_action = fr"""{cypher_action}
            SET n.{target_property} = CASE WHEN size(replace(n.{target_property},'\\\\','')) <= {max_total_length} THEN n.{target_property} ELSE '' END
            """

        run_periodic_iterate(
            self.graph,
            cypherIterate=f"match (n:{':'.join(labels)}) return n",
            cypherAction=cypher_action,
            batchSize=batchSize,
            parallel=True,
        )

    def find_sanitized_properties_unsuitable_for_lucene_index(
        self,
        match_labels: List[str],
        check_property: str,
        tag_with_labels: List[str] = None,
        delete_node_instead_of_tagging: bool = False,
        match_properties_equal_to_common_word=False,
    ):
        if delete_node_instead_of_tagging:
            # delete action
            cypherAction = f"WITH n WHERE trim(n.{check_property}) = '' OR n.{check_property} is null DELETE n"
        else:
            # tag action
            if tag_with_labels:
                cypherAction = f"WITH n WHERE trim(n.{check_property}) = '' OR n.{check_property} is null SET n:{':'.join(tag_with_labels)}"
            else:
                raise ValueError(
                    f"No tagging labels supplied. Provide at least a list with one label name to 'tag_with_labels'. Got: {tag_with_labels}"
                )
        run_periodic_iterate(
            self.graph,
            cypherIterate=f"MATCH (n:{':'.join(match_labels)}) return n",
            cypherAction=cypherAction,
            parallel=False,
            batchSize=10000,
        )
        """ old variant. to be deleted
        if match_properties_equal_to_common_word:
            if delete_node_instead_of_tagging:
                # delete action
                cypherAction = f"WITH w MATCH (n:{':'.join(match_labels)}) WHERE n.{check_property} = w.word DELETE n"
            else:
                # tag action
                cypherAction = f"WITH w MATCH (n:{':'.join(match_labels)}) WHERE NOT n:{':'.join(tag_with_labels)} AND n.{check_property} = w.word SET n:_LikeCommonWord:{':'.join(tag_with_labels)}"
            run_periodic_iterate(
                self.graph,
                cypherIterate=f"MATCH (w:{':'.join(self.common_word_labels)}) return w",
                cypherAction=cypherAction,
                parallel=False,
                batchSize=1000
            )
        """
        if match_properties_equal_to_common_word:
            if delete_node_instead_of_tagging:
                # delete action
                cypherAction = f"WITH n MATCH (w:{':'.join(self.common_word_labels)}) WHERE n.{check_property} = w.word DELETE n"
            else:
                # tag action
                cypherAction = f"WITH n MATCH (w:{':'.join(self.common_word_labels)}) WHERE n.{check_property} = w.word SET n:_LikeCommonWord:{':'.join(tag_with_labels)}"
            run_periodic_iterate(
                self.graph,
                cypherIterate=f"MATCH (n:{':'.join(match_labels)}) WHERE NOT n:{':'.join(tag_with_labels)} return n",
                cypherAction=cypherAction,
                parallel=True,
                batchSize=10000,
            )

    def import_common_words(
        self,
        top_n_words_per_language=5000,
        min_word_length: int = 2,
        max_word_length: int = 8,
        to_lower: bool = False,
        addional_words: Dict[str, List] = None,
    ):
        """Import top used word for common languages (see TextCleanerTools.word_list_url for the source urls)

        Args:
            top_n_words_per_language (int, optional): Only import the top "n" common words per language. Defaults to 4000. max 20000. Defaults to 5000.
            min_word_length (int, optional): [description]. Defaults to 2.
            max_word_length (int, optional): [description]. Defaults to 8.
            to_lower (bool, optional): [description]. Defaults to False.
            addional_words (Dict[str, List], optional): Extra words per langage e.g. `{"en":["stop","stuff"],"de":["Dochjanein"]}`. Defaults to None.

        Returns:
            [type]: [description]
        """
        word_set = graphio.NodeSet(
            labels=self.common_word_labels, merge_keys=["word", "language"]
        )
        for lang, word_list_url in self.word_list_url.items():
            for index, line in enumerate(urllib.request.urlopen(word_list_url)):
                if index > 3:
                    word: str = line.decode("utf-8").split(" ", 2)[2].strip()
                    word_set.add_node(
                        {
                            "word": word.lower() if to_lower else word,
                            "language": lang,
                            "ranking": index - 3,
                        }
                    )
                if index == top_n_words_per_language + 3:
                    break
        if addional_words:
            for lang, words in addional_words.items():
                for word in words:
                    word_set.add_node(
                        {
                            "word": word.lower() if to_lower else word,
                            "language": lang,
                            "ranking": "customword",
                        }
                    )

        word_set.create_index(self.graph)
        word_set.merge(self.graph)
        # remove garbage
        self.create_sanitized_property_for_lucene_index(
            labels=self.common_word_labels,
            property="word",
            target_property="word_clean",
            min_word_length=min_word_length,
            max_word_length=max_word_length,
        )
        self.find_sanitized_properties_unsuitable_for_lucene_index(
            match_labels=self.common_word_labels,
            check_property="word_clean",
            delete_node_instead_of_tagging=True,
        )
        # remove temporary property
        run_periodic_iterate(
            graph=self.graph,
            cypherIterate=f"MATCH (n:{':'.join(self.common_word_labels)}) return n",
            cypherAction="REMOVE n.word_clean",
            parallel=True,
        )
