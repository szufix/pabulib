import networkx as nx


def get_reverse_approval(instance, profile):
    reverse_approvals = {c: set() for c in instance}
    for i, vote in enumerate(profile):
        for c in vote:
            reverse_approvals[c].add(i)
    return reverse_approvals


def discrete_distance_between_projects(instance, profile, reverse_approvals, c1, c2):
    if c1 == c2:
        return 0
    else:
        return 1


def jaccard_distance_between_projects(instance, profile, reverse_approvals, c1, c2):

        ra1 = reverse_approvals[c1]
        ra2 = reverse_approvals[c2]

        if len(ra1.union(ra2)) != 0:
                return 1 - len(ra1.intersection(ra2)) / len(ra1.union(ra2))

        return 1


def compute_distance_between_projects(instance, profile, c1, c2, reverse_approvals, distance_id):

    if distance_id == 'discrete':
        return discrete_distance_between_projects(instance, profile, reverse_approvals, c1, c2)
    elif distance_id == 'jaccard':
        return jaccard_distance_between_projects(instance, profile, reverse_approvals, c1, c2)


def sum_cost(com):
    return sum([c.cost for c in com])


def compute_flow_distance(instance, profile, com1, com2, distance_id):

    demand = max(sum_cost(com1), sum_cost(com2))
    reverse_approvals = get_reverse_approval(instance, profile)

    # Create a directed graph
    G = nx.DiGraph()

    # Add edges to the source
    for c1 in com1:
        G.add_edge('s', f'a_{c1}', capacity=c1.cost, weight=0)

    # Add edges to the sink
    for c2 in com2:
        G.add_edge(f'b_{c2}', 't', capacity=c2.cost, weight=0)

    # Add intermediate edges
    for c1 in com1:
        for c2 in com2:
            distance = compute_distance_between_projects(instance, profile, c1, c2,
                                                         reverse_approvals, distance_id=distance_id)
            G.add_edge(f'a_{c1}', f'b_{c2}', capacity=min(c1.cost, c2.cost), weight=distance)

    # Add direct edge from source to sink
    G.add_edge('s', 't', capacity=demand, weight=1)

    # Set demand/supply values
    G.nodes['s']['demand'] = -demand
    G.nodes['t']['demand'] = demand

    # Compute minimum-cost max flow
    flow_cost, flow_dict = nx.network_simplex(G)

    # return flow_cost
    return float(flow_cost/demand)

