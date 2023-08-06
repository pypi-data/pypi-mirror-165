import py2neo
from typing import Dict, List, Callable


class Neo4jPeriodicIterateError(Exception):
    pass


def python_dict_to_java_map_str(dict_: Dict):
    map_items_str = []
    for key, val in dict_.items():
        map_items_str.append(f"{key}:{val}")
    return f"{{{':'.join(map_items_str)}}}"


def run_periodic_iterate(
    graph: py2neo.Graph,
    cypherIterate: str,
    cypherAction: str,
    batchSize: int = None,
    parallel: bool = None,
    retries: int = None,
    batchMode: str = None,
    params: Dict = None,
    concurrency: int = None,
    failedParams: int = None,
    planner: str = None,
    _ignore_erros: bool = False,
    _only_return_query: bool = False,
    _log_status_func: Callable = None,
):

    """
    https://neo4j.com/labs/apoc/4.1/overview/apoc.periodic/apoc.periodic.iterate/
    """
    args = locals()
    config_map = []
    for conf_key, conf_val in args.items():
        if conf_val and conf_key not in [
            "graph",
            "cypherIterate",
            "cypherAction",
            "_ignore_erros",
            "_only_return_query",
            "_log_status_func",
        ]:
            if isinstance(conf_val, bool):
                conf_val = str(conf_val)
            if isinstance(conf_val, dict):
                conf_val = python_dict_to_java_map_str(conf_val)
            config_map.append(f"{conf_key}:{conf_val}")
    query = f"""
    CALL apoc.periodic.iterate("{cypherIterate}","{cypherAction}",\n{{{",".join(config_map)}}}) 
    """
    if _log_status_func:
        _log_status_func(query)
    if _only_return_query:
        return query
    res = graph.run(query)
    res_data = res.to_data_frame()
    if res_data["failedOperations"][0] != 0 and not _ignore_erros:
        errors = []
        for error_msg, count in res_data["errorMessages"][0].items():
            errors.append(f"\n {error_msg}")
        raise Neo4jPeriodicIterateError(
            f'Error on {res_data["failedOperations"][0]} of {res_data["total"][0]} operations. Query: \n\n {query} \n\n ErrorMessages:\n{":".join(errors)}'
        )
    return res
