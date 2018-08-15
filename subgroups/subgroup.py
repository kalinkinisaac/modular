def subgroup_action(N, sub, group):

    # Generating set of orbit representatives
    reprs = []
    for h_j in sub.reprs:
        for x_i in group.reprs:
            reprs.append((h_j * x_i) % N)

    # Constructing reduction procedure for subgroup action
    def reduced(x):
        x_i = group.reduced(x)
        h = (x * x_i.inv() % N) % N
        h_j = sub.reduced(h)
        return (h_j * x_i) % N

    return reprs, reduced
