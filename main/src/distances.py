import networkx as nx


def compute_distance_between_project(instance, profile, c1, c2):
    if c1 == c2:
        return c1.cost
    else:
        return 0


def compute_flow_distance(instance, profile, com1, com2):

    # Create a directed graph
    G = nx.DiGraph()
    # Add edges to the source
    for c1 in com1:
        G.add_edge('s', f'a_{c1}', capacity=c1.cost)

    # Add intermediate edges
    for c1 in com1:
        for c2 in com2:
            distance = compute_distance_between_project(instance, profile, c1, c2)
            G.add_edge(f'a_{c1}', f'b_{c2}', capacity=distance)

    # Add edges to the sink
    for c2 in com2:
        G.add_edge(f'b_{c2}', 't', capacity=c2.cost)


    # Compute maximum flow
    flow_value, flow_dict = nx.maximum_flow(G, 's', 't')
    # print("Max Flow:", flow_value)
    # print("Flow values on each edge:", flow_dict)

    return instance.budget_limit-flow_value

