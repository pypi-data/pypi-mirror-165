#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate a yWorks Graph Widget """


from yfiles_jupyter_graphs import GraphWidget

from baseblock import BaseObject

from yworks_helper.core.svc import KeyByLabelLoader


class GenerateGraphWidget(BaseObject):
    """ Generate a yWorks Graph Widget """

    def __init__(self):
        """
        Created:
            18-Aug-2022
            craigtrim@gmail.com
            *   design principles specified in
                https://github.com/craigtrim/yworks-helper/issues/1
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                d_nodes: dict,
                edges: list = None,
                directed: bool = True) -> GraphWidget:
        """ Create a Graph Widget

        Args:
            d_nodes (dict): the node input
            Sample Input:
                {
                    "john smith": {
                        "alpha": 22
                    },
                    "jane smith": {
                        "alpha": 233,
                        "beta": 400
                    }
                }
            edges (list, optional): the edge input
            Sample Input:
               [
                    {
                        'start': 'john smith',
                        'end': 'jane smith',
                        'label': 'knows'
                    }
                ]            
            directed (bool, optional): indicate if this is a directed graph. Defaults to True.

        Returns:
            GraphWidget: an instantiated GraphWidget
        """

        d_result = KeyByLabelLoader().process(
            d_nodes=d_nodes, edges=edges)

        w = GraphWidget()
        w.nodes = d_result['nodes']

        w.edges = d_result['edges']
        w.directed = directed

        return w
