#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Accept Graph Data that is keyed by Label """


from uuid import uuid1


from baseblock import BaseObject


class KeyByLabelLoader(BaseObject):
    """ Accept Graph Data that is keyed by Label """

    def __init__(self):
        """
        Created:
            18-Aug-2022
            craigtrim@gmail.com
            *   design principles specified in
                https://github.com/craigtrim/yworks-helper/issues/1
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def _uuid() -> str:
        return str(uuid1()).replace('-', '_')

    def _generate_nodes(self,
                        d_nodes: dict) -> tuple:

        nodes = []
        d_map = {}

        for k in d_nodes:

            node_id = self._uuid()
            d_map[k] = node_id

            def color():
                if 'color' in d_nodes[k]:
                    return d_nodes[k]['color']
                return '17bebb'  # default

            def properties():
                d = {
                    "label": k
                }

                inner_keys = [k for k in d_nodes[k] if k not in ['color']]
                for inner_key in inner_keys:
                    d[inner_key] = d_nodes[k][inner_key]

                return d

            nodes.append({
                "id": node_id,
                "properties": properties(),
                "color": color()
            })

        return nodes, d_map

    def _generate_edges(self,
                        d_node_map: dict,
                        source_edges: list) -> dict:

        target_edges = []

        for d_source in source_edges:
            # edge_id = self._uuid()

            d_target = {
                "start": d_node_map[d_source['start']],
                "end": d_node_map[d_source['end']],
            }

            for k in [k for k in d_source.keys()
                      if k not in ['start', 'end']]:

                d_target[k] = d_source[k]

            target_edges.append(d_target)

        return target_edges

    def process(self,
                d_nodes: dict,
                edges: list = None) -> dict:

        target_nodes, d_node_map = self._generate_nodes(d_nodes)

        def target_edges() -> dict:
            if not edges:
                return {}
            return self._generate_edges(d_node_map, edges)

        return {
            'nodes': target_nodes,
            'edges': target_edges()
        }
