
import ast
import gurobipy as gp
from gurobipy import GRB, LinExpr
import numpy as np

# Constraint on budget
# Suma po wszystkich i p_i * c_i <= Budget

# Constrant per voter
# Suma po wszystkich projektach aprobowanych przez wyborce j jest rowna s_j


def egalitarian_ilp(votes, projects, budget, num_projects, acs):

    num_buckets = 10
    num_voters = len(votes)
    t = int(budget/num_voters)
    buckets = [int(i * t/num_buckets) for i in range(num_buckets)]
    # print(buckets)

    cp = gp.Model("guru")
    # cp.parameters.threads.set(1)

    # OBJECTIVE FUNCTION
    VARS = {}
    p_vars = []
    p_coeff = []
    for vote_id in votes:
        for bucket in buckets:
            p_coeff.append(bucket)
            # p_coeff.append(bucket*bucket)
            name = f'b_{vote_id}_{str(bucket)}'
            VARS[name] = cp.addVar(vtype=GRB.BINARY, name=name)
            p_vars.append(VARS[name])
    lin_expr = LinExpr(p_coeff, p_vars)
    cp.setObjective(lin_expr, GRB.MINIMIZE)

    # CONSTRAINT FOR TOTAL BUDGET
    p_coeff = []
    p_vars = []
    for project_id in projects:
        p_coeff.append(int(projects[project_id]['cost']))
        name = f'p_{project_id}'
        VARS[name] = cp.addVar(vtype=GRB.BINARY, name=name)
        p_vars.append(VARS[name])
    lin_expr = LinExpr(p_coeff, p_vars)
    cp.addLConstr(lhs=lin_expr,
                  sense=GRB.LESS_EQUAL,
                  rhs=budget,
                  name='c0')

    # SUM OF SPENDING PER VOTER

    for vote_id in votes:
        p_coeff = []
        p_vars = []
        vote = ast.literal_eval(votes[vote_id]['vote'])
        if type(vote) is int:
            vote = [vote]
        for project_id in vote:
            p_coeff.append(int(int(projects[str(project_id)]['cost']) / len(acs[str(project_id)])))
            name = f'p_{project_id}'
            p_vars.append(VARS[name])
        p_coeff.append(-1)
        name = f's_{vote_id}'
        VARS[name] = cp.addVar(vtype=GRB.INTEGER, name=name)
        p_vars.append(VARS[name])
        lin_expr = LinExpr(p_coeff, p_vars)
        cp.addLConstr(lhs=lin_expr,
                      sense=GRB.EQUAL,
                      rhs=0,
                      name=f'vs_{vote_id}')

    # a_l >= 0
    for vote_id in votes:
        p_coeff = 1
        name = f'a_{vote_id}'
        VARS[name] = cp.addVar(vtype=GRB.INTEGER, name=name)
        p_vars = VARS[name]
        lin_expr = LinExpr(p_coeff, p_vars)
        cp.addLConstr(lhs=lin_expr,
                      sense=GRB.GREATER_EQUAL,
                      rhs=0,
                      name=f'a_{vote_id}')

    # a_l + s_l >= t
    for vote_id in votes:
        p_coeff = [1, 1]
        p_vars = [VARS[f'a_{vote_id}'], VARS[f's_{vote_id}']]
        lin_expr = LinExpr(p_coeff, p_vars)
        cp.addLConstr(lhs=lin_expr,
                                  sense=GRB.GREATER_EQUAL,
                                  rhs=t,
                                  name=f'as_{vote_id}')

    # BUCKETS 1 to 1
    for vote_id in votes:
        p_coeff = []
        p_vars = []
        for bucket in buckets:
            p_coeff.append(1)
            p_vars.append(VARS[f'b_{vote_id}_{str(bucket)}'])
        lin_expr = LinExpr(p_coeff, p_vars)
        cp.addLConstr(lhs=lin_expr,
                      sense=GRB.EQUAL,
                      rhs=1,
                      name=f'b1_{vote_id}')
    # BUCKETS
    for vote_id in votes:
        for bucket in buckets:
            p_coeff = []
            p_vars = []
            p_coeff.append(1)
            p_vars.append(VARS[f'a_{vote_id}'])
            val = t-bucket
            p_coeff.append(val)
            p_vars.append(VARS[f'b_{vote_id}_{str(bucket)}'])
            lin_expr = LinExpr(p_coeff, p_vars)
            cp.addLConstr(lhs=lin_expr,
                          sense=GRB.LESS_EQUAL,
                          rhs=t,
                          name='c5')

    # cp.write('model.mps')
    cp.write('model.lp')

    # c.Params.mipgap = 0.001


    # SOLVE THE ILP
    # cp.set_results_stream(None)
    try:
        cp.optimize()
    except:
        print("Exception raised while solving")
        return

    for v in cp.getVars():
        print('%s %g' % (v.varName, v.x))

    print(cp.objVal)
    return cp.objVal

