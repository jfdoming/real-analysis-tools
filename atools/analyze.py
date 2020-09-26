def compute(A, split=False):
    track = {A}
    res1 = [A]
    res2 = []
    W = A
    i = 0
    while True:
        if i % 2 == 0:
            W = W.cl()
        else:
            W = W.co()
        if W in track:
            break
        track.add(W)
        res1.append(W)
        i += 1

    W = A
    i = 0
    while True:
        if i % 2 == 0:
            W = W.co()
        else:
            W = W.cl()
        if W in track:
            break
        track.add(W)
        res2.append(W)
        i += 1

    res = (res1, res2) if split else res1 + res2
    return res

def count(A, split=False):
    res = compute(A, split=split)
    if split:
        return len(res[0]), len(res[1])
    return len(res)