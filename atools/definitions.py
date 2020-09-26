class S:
    def cl(self):
        return self
    def co(self):
        return SM(X, self)
    def it(self):
        return self
    def __bool__(self):
        return True
    def __add__(self, other):
        return SU(self, other)
    def __sub__(self, other):
        return SM(self, other)
    def __mul__(self, other):
        return SI(self, other)
    def __repr__(self):
        return "<base set>"
    def __latex__(self):
        return ""

class SS(S):
    __count__ = 10298387892173
    def __init__(self):
        self.__hc__ = SS.__count__
        SS.__count__ += 1
    def __hash__(self):
        return self.__hc__

class E(SS):
    def __repr__(self):
        return "@"
    def __latex__(self):
        return "\\emptyset"
    def __bool__(self):
        return False

class X(SS):
    def __repr__(self):
        return "R"
    def __latex__(self):
        return "\\mathbb R"

class Q(SS):
    def __repr__(self):
        return "Q"
    def __latex__(self):
        return "\\mathbb Q"
    def cl(self):
        return X
    def it(self):
        return E

# These should be singletons.
E, X, Q = E(), X(), Q()

class F(S):
    def __init__(self, *v):
        self.v = frozenset(v)
    def __new__(cls, *v):
        if not v:
            return E
        return super().__new__(cls)
    def __repr__(self):
        return f"{{{', '.join(str(e) for e in self.v)}}}"
    def __latex__(self):
        return f"\\left\\{{{','.join(str(e) for e in self.v)}\\right\\}}"
    def __eq__(self, other):
        return type(self) == type(other) and self.v == other.v
    def __hash__(self):
        return hash(self.v)
    def it(self):
        return E

class I(S):
    def __init__(self,a,b,ao,bo):
        self.a = a
        self.b = b
        self.ao = ao
        self.bo = bo
    def __new__(cls, a, b, ao, bo):
        if not ao and not bo:
            if a == b:
                return F(a)
        if a >= b:
            return E
        return super().__new__(cls)
    def cl(self):
        return C(self.a,self.b)
    def co(self):
        return SM(X, self)
    def it(self):
        return U(self.a,self.b)
    def __eq__(self, other):
        return type(self) == type(other) and self.a == other.a and self.b == other.b and self.ao == other.ao and self.bo == other.bo
    def __hash__(self):
        return hash((self.a, self.b, self.ao, self.bo))
    def __repr__(self):
        return f"{'(' if self.ao else '['}{self.a}, {self.b}{')' if self.bo else ']'}"
    def __latex__(self):
        return self.__repr__()

def C(a, b):
    return I(a, b, False, False)
def U(a, b):
    return I(a, b, True, True)
def LU(a, b):
    return I(a, b, True, False)
def RU(a, b):
    return I(a, b, False, True)

class N(S):
    def __init__(self, limit):
        self.limit = limit
    def __repr__(self):
        return f"{{1/n + {self.limit}}}" if self.limit >= 0 else f"{{1/n - {-self.limit}}}"
    def __latex__(self):
        return f"\\left\\{{\\frac{{1}}{{n}} + {self.limit}\\right\\}}" if self.limit >= 0 else f"\\left\\{{\\frac{{1}}{{n}} - {-self.limit}\\right\\}}"
    def __eq(self, other):
        return type(self) == type(other) and self.limit == other.limit
    def __hash__(self):
        return hash(self.limit) ^ 13282739847
    def cl(self):
        return SU(self, F(self.limit))
    def it(self):
        return E

class SO(S):
    def __init__(self, *sets):
        if hasattr(self, "initd") and self.initd:
            return
        self.initd = True
        self.sets = frozenset(sets)
    def __repr__(self):
        return f" {self.repr_symbol} ".join(s.__repr__() if not isinstance(s, SO) else f"({s.__repr__()})" for s in self.sets)
    def __latex__(self):
        return f" {self.latex_symbol} ".join(s.__latex__() if not isinstance(s, SO) else f"({s.__latex__()})" for s in self.sets)
    def __eq__(self, other):
        return type(self) == type(other) and self.sets == other.sets
    def __hash__(self):
        return hash(self.sets)
    
    @property
    def repr_symbol(self):
        raise NotImplementedError

    @property
    def latex_symbol(self):
        raise NotImplementedError

class SM(SO):
    def __init__(self, *sets):
        if not hasattr(self, "initd") or not self.initd:
            self.s = sets[0]
            self.t = sets[1]
        super().__init__(*sets)
    def __new__(cls, *sets):
        if not sets:
            return E
        if len(sets) == 1:
            return sets[0]
        if len(sets) > 2:
            return SM(sets[0], SU(*sets[1:]))
        s = sets[0]
        t = sets[1]
        if s == t:
            return E
        if not s or not t:
            return s
        if t == X:
            return E
        if s == X and isinstance(t, SM) and t.s == X:
            return t.t
        if isinstance(s, SM):
            return SM(s.s, SU(s.t, t))
        return super().__new__(cls)

    def __repr__(self):
        return f" {self.repr_symbol} ".join(s.__repr__() if not isinstance(s, SO) else f"({s.__repr__()})" for s in [self.s, self.t])
    def __latex__(self):
        return f" {self.latex_symbol} ".join(s.__latex__() if not isinstance(s, SO) else f"({s.__latex__()})" for s in [self.s, self.t])

    def cl(self):
        return SM(self.s.cl(), self.t.it())
    def co(self):
        if self.s == X:
            return self.t
        return SM(X, self)
    def it(self):
        return SM(self.s.it(), self.t.cl())
    
    @property
    def repr_symbol(self):
        return "\\"
    @property
    def latex_symbol(self):
        return "\\setminus"

class SU(SO):
    def __init__(self, *sets):
        super().__init__(*sets)
    def __F_I__(cls, l, i):
        res = set()
        rt = i
        f = False
        for e in l.v:
            if e > i.a and e < i.b:
                continue
            if e == i.a:
                if i.ao:
                    rt = I(i.a, i.b, False, rt.bo)
                continue
            if e == i.b:
                if i.bo:
                    rt = I(i.a, i.b, rt.ao, False)
                continue
            res.add(e)
        return F(*res), rt

    def __new__(cls, *sets):
        if X in sets:
            return X
        ops = [s for s in sets if isinstance(s, SO)]
        sets = [s for s in sets if not isinstance(s, SO) and s]
        for o in ops:
            if isinstance(o, SU):
                sets += o.sets
            elif isinstance(o, SM) or isinstance(o, SI):
                sets.append(o)
        if not sets:
            return E
        rmops = [s for s in sets if isinstance(s, SO) or s == Q]
        seq = set(s for s in sets if isinstance(s, N))
        finites = [s for s in sets if isinstance(s, F)]
        finite = set()
        for f in finites:
            finite = finite.union(f.v)
        intervals = [s for s in sets if isinstance(s, I)]

        if not intervals:
            # Check for sequence overlap (assume only overlap with integers).
            rfinite = set()
            for f in finite:
                for s in seq:
                    if f != s.limit + 1:
                        rfinite.add(f)
            finite = F(*rfinite)
            if finite:
                res = super().__new__(cls)
                res.sets = frozenset((finite, *seq, *rmops))
                res.initd = True
                res.n = "U"
                return res
            res = super().__new__(cls)
            res.sets = frozenset((*seq, *rmops))
            res.initd = True
            res.n = "U"
            return res
        
        finite = F(*finite)

        for i in range(len(intervals)):
            if not finite:
                break
            finite, intervals[i] = cls.__F_I__(cls, finite, intervals[i])
        
        # Try to add sequences in.
        rseq = set()
        for s in seq:
            for i in range(len(intervals)):
                if s.limit == intervals[i].a:
                    assert s.limit + 1 <= intervals[i].b # Assume full containment of sequences for now.
                    if s.limit + 1 == intervals[i].b:
                        intervals[i].bo = False
                elif s.limit > intervals[i].a and s.limit < intervals[i].b:
                    assert s.limit + 1 <= intervals[i].b # Assume full containment of sequences for now.
                    if s.limit + 1 == intervals[i].b:
                        intervals[i].bo = False
                else:
                    assert s.limit + 1 <= intervals[i].a or s.limit >= intervals[i].b
                    if s.limit + 1 == intervals[i].a:
                        intervals[i].ao = False
                    rseq.add(s)
        
        intervals.sort(key=lambda i: i.a)
        sets = [*rseq, *rmops, finite, intervals[0]] if finite else [*rseq, *rmops, intervals[0]]
        for i in intervals[1:]:
            if sets[-1].b > i.a:
                # Overlapping intervals.
                if sets[-1].b == i.b:
                    sets[-1].bo = i.bo and sets[-1].bo
                elif sets[-1].b < i.b:
                    sets[-1].b = i.b
                    sets[-1].bo = i.bo
            elif sets[-1].b == i.a:
                if not sets[-1].bo or not i.ao:
                    sets[-1].b = i.b
                    sets[-1].bo = i.bo
                else:
                    sets.append(i)
            else:
                sets.append(i)
        if len(sets) == 1:
            return sets[0]
        res = super().__new__(cls)
        res.sets = frozenset(sets)
        res.initd = True
        res.n = "U"
        return res
        
    def cl(self):
        return SU(*(s.cl() for s in self.sets))
    
    @property
    def repr_symbol(self):
        return "\u222a"
    @property
    def latex_symbol(self):
        return "\\cup"

    def it(self):
        return SU(*(s.it() for s in self.sets))

class SI(SO):
    # Placeholder implementation for rational-interval intersection only.
    def __init__(self, *sets):
        super().__init__(*sets)
    def __new__(cls, *sets):
        if E in sets:
            return E
        sets = list(filter(lambda s: s != X, sets)) # Intersection with X should do nothing.
        if not sets:
            return E
        if len(sets) == 1:
            return sets[0]

        assert all(map(lambda s: s == Q or isinstance(s, I), sets))
        assert len(sets) == 2
        i = sets[0] if isinstance(sets[0], I) else sets[1]
        assert isinstance(i, I)
        return super().__new__(cls)
    def cl(self):
        return SI(*(s.cl() for s in self.sets))
    def it(self):
        return SI(*(s.it() for s in self.sets))
    
    @property
    def repr_symbol(self):
        return "\u2229"
    @property
    def latex_symbol(self):
        return "\\cap"