# This sampling code was copied from the smt package by M. A. Bouhlel and J. T. Hwang and N. Bartoli and R. Lafage and
# J. Morlier and J. R. R. A. Martins, A Python surrogate modeling framework with derivatives. Advances in Engineering
# Software, 2019, 102662
# https://doi.org/10.1016/j.advengsoft.2019.03.005
# https://smt.readthedocs.io/en/latest/

from abc import ABCMeta, abstractmethod

import numpy as np
from pyDOE2 import lhs
from scipy.spatial.distance import pdist, cdist

FLOAT = "float_type"
INT = "int_type"
ORD = "ord_type"
ENUM = "enum_type"

#######################################


def ensure_2d_array(array, name):
    if not isinstance(array, np.ndarray):
        raise ValueError("{} must be a NumPy array".format(name))

    array = np.atleast_2d(array.T).T

    if len(array.shape) != 2:
        raise ValueError("{} must have a rank of 1 or 2".format(name))

    return array


def check_support(sm, name, fail=False):
    if not sm.supports[name] or fail:
        class_name = sm.__class__.__name__
        raise NotImplementedError("{} does not support {}".format(class_name, name))


def check_nx(nx, x):
    if x.shape[1] != nx:
        if nx == 1:
            raise ValueError("x should have shape [:, 1] or [:]")
        else:
            raise ValueError("x should have shape [:, {}] and not {}".format(nx, x.shape))


#######################################


def bisect_left(*args, **kwargs):  # real signature unknown
    """
    Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, i points just
    before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    pass


#######################################


def take_closest_number(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


def take_closest_in_list(myList, x):
    vfunc = np.vectorize(take_closest_number, excluded=["myList"])
    return vfunc(myList=myList, myNumber=x)


#######################################


class OptionsDictionary(object):
    """
    Generalization of the dictionary that allows for declaring keys.

    Attributes
    ----------
    _dict : dict
        Dictionary of option values keyed by option names.
    _declared_entries : dict
        Dictionary of declared entries.
    """

    def __init__(self):
        self._dict = {}
        self._declared_entries = {}

    def clone(self):
        """
        Return a clone of this object.

        Returns
        -------
        OptionsDictionary
            Deep-copied clone.
        """
        clone = self.__class__()
        clone._dict = dict(self._dict)
        clone._declared_entries = dict(self._declared_entries)
        return clone

    def __getitem__(self, name):
        """
        Get an option that was previously declared and optionally set.

        Arguments
        ---------
        name : str
            The name of the option.

        Returns
        -------
        object
            Value of the option.
        """
        return self._dict[name]

    def __setitem__(self, name, value):
        """
        Set an option that was previously declared.

        The value argument must be valid, which means it must satisfy the following:
        1. If values and not types was given when declaring, value must be in values.
        2. If types and not values was given when declaring, type(value) must be in types.
        3. If values and types were given when declaring, either of the above must be true.

        Arguments
        ---------
        name : str
            The name of the option.
        value : object
            The value to set.
        """
        assert name in self._declared_entries, "Option %s has not been declared" % name
        self._assert_valid(name, value)
        self._dict[name] = value

    def __contains__(self, key):
        return key in self._dict

    def is_declared(self, key):
        return key in self._declared_entries

    def _assert_valid(self, name, value):
        values = self._declared_entries[name]["values"]
        types = self._declared_entries[name]["types"]

        if values is not None and types is not None:
            assert value in values or isinstance(
                value, types
            ), "Option %s: value and type of %s are both invalid - " % (
                name,
                value,
            ) + "value must be %s or type must be %s" % (
                values,
                types,
            )
        elif values is not None:
            assert value in values, "Option %s: value %s is invalid - must be %s" % (name, value, values,)
        elif types is not None:
            assert isinstance(value, types), "Option %s: type of %s is invalid - must be %s" % (name, value, types)

    def update(self, dict_):
        """
        Loop over and set all the entries in the given dictionary into self.

        Arguments
        ---------
        dict_ : dict
            The given dictionary. All keys must have been declared.
        """
        for name in dict_:
            self[name] = dict_[name]

    def declare(self, name, default=None, values=None, types=None, desc=""):
        """
        Declare an option.

        The value of the option must satisfy the following:
        1. If values and not types was given when declaring, value must be in values.
        2. If types and not values was given when declaring, type(value) must be in types.
        3. If values and types were given when declaring, either of the above must be true.

        Arguments
        ---------
        name : str
            Name of the option.
        default : object
            Optional default value that must be valid under the above 3 conditions.
        values : list
            Optional list of acceptable option values.
        types : type or list of types
            Optional list of acceptable option types.
        desc : str
            Optional description of the option.
        """
        self._declared_entries[name] = {
            "values": values,
            "types": types,
            "default": default,
            "desc": desc,
        }

        if default is not None:
            self._assert_valid(name, default)

        self._dict[name] = default


#######################################


class SamplingMethod(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        """
        Constructor where values of options can be passed in.

        For the list of options, see the documentation for the problem being used.

        Parameters
        ----------
        **kwargs : named arguments
            Set of options that can be optionally set; each option must have been declared.

        Examples
        --------
        >>> import numpy as np
        >>> from smt.sampling_methods import Random
        >>> sampling = Random(xlimits=np.arange(2).reshape((1, 2)))
        """
        self.options = OptionsDictionary()
        self.options.declare(
            "xlimits",
            types=np.ndarray,
            desc="The interval of the domain in each dimension with shape nx x 2 (required)",
        )
        self._initialize()
        self.options.update(kwargs)

    def _initialize(self) -> None:
        """
        Implemented by sampling methods to declare options (optional).

        Examples
        --------
        self.options.declare('option_name', default_value, types=(bool, int), desc='description')
        """
        pass

    def __call__(self, nt: int) -> np.ndarray:
        """
        Compute the requested number of sampling points.

        The number of dimensions (nx) is determined based on `xlimits.shape[0]`.

        Arguments
        ---------
        nt : int
            Number of points requested.

        Returns
        -------
        ndarray[nt, nx]
            The sampling locations in the input space.
        """
        return self._compute(nt)

    @abstractmethod
    def _compute(self, nt: int) -> np.ndarray:
        """
        Implemented by sampling methods to compute the requested number of sampling points.

        The number of dimensions (nx) is determined based on `xlimits.shape[0]`.

        Arguments
        ---------
        nt : int
            Number of points requested.

        Returns
        -------
        ndarray[nt, nx]
            The sampling locations in the input space.
        """
        raise Exception("This sampling method has not been implemented correctly")


#######################################


def check_xspec_consistency(xtypes, xlimits):
    if len(xlimits) != len(xtypes):
        raise ValueError(
            "number of x limits ({}) do not"
            "correspond to number of specified types ({})".format(len(xlimits), len(xtypes))
        )

    for i, xtyp in enumerate(xtypes):
        if (not isinstance(xtyp, tuple)) and len(xlimits[i]) != 2:
            if xtyp == ORD and isinstance(xlimits[i][0], str):
                listint = list(map(float, xlimits[i]))
                sortedlistint = sorted(listint)
                if not np.array_equal(sortedlistint, listint):
                    raise ValueError(
                        "Unsorted x limits ({}) for variable type {} (index={})".format(xlimits[i], xtyp, i)
                    )

            else:
                raise ValueError("Bad x limits ({}) for variable type {} (index={})".format(xlimits[i], xtyp, i))
        if xtyp == INT:
            if not isinstance(xlimits[i][0], str):
                xtyp = ORD
                xtypes[i] = ORD
            else:
                raise ValueError("INT do not work with list of ordered values, use ORD instead")
        if xtyp != FLOAT and xtyp != ORD and (not isinstance(xtyp, tuple) or xtyp[0] != ENUM):
            raise ValueError("Bad type specification {}".format(xtyp))

        if isinstance(xtyp, tuple) and len(xlimits[i]) != xtyp[1]:
            raise ValueError(
                "Bad x limits and x types specs not consistent. "
                "Got a categorical type with {} levels "
                "while x limits contains {} values (index={})".format(xtyp[1], len(xlimits[i]), i)
            )


def _raise_value_error(xtyp):
    raise ValueError("Bad xtype specification: " "should be FLOAT, ORD or (ENUM, n), got {}".format(xtyp))


def compute_unfolded_dimension(xtypes):
    """
    Returns x dimension (int) taking into account  unfolded categorical features
    """
    res = 0
    for xtyp in xtypes:
        if xtyp == FLOAT or xtyp == ORD:
            res += 1
        elif isinstance(xtyp, tuple) and xtyp[0] == ENUM:
            res += xtyp[1]
        else:
            _raise_value_error(xtyp)
    return res


def unfold_xlimits_with_continuous_limits(xtypes, xlimits, categorical_kernel=None):
    """
    Expand xlimits to add continuous dimensions for enumerate x features
    Each level of an enumerate gives a new continuous dimension in [0, 1].
    Each integer dimensions are relaxed continuously.

    Parameters
    ----------
    xtypes: x types list
        x type specification
    xlimits : list
        bounds of each original dimension (bounds of enumerates being the list of levels).

    Returns
    -------
    np.ndarray [nx continuous, 2]
        bounds of the each dimension where limits for enumerates (ENUM)
        are expanded ([0, 1] for each level).
    """
    # Continuous optimization : do nothing
    xlims = []
    for i, xtyp in enumerate(xtypes):
        if xtyp == FLOAT or xtyp == ORD:
            k = xlimits[i][0]
            if xtyp == ORD and (not isinstance(xlimits[i][0], int)):
                listint = list(map(float, xlimits[i]))
                listint = [listint[0], listint[-1]]
                xlims.append(listint)
            else:
                xlims.append(xlimits[i])
        elif isinstance(xtyp, tuple) and xtyp[0] == ENUM:
            if xtyp[1] == len(xlimits[i]):
                if categorical_kernel is None:
                    xlims.extend(xtyp[1] * [[0, 1]])
                else:
                    listint = list(map(float, [0, len(xlimits[i])]))
                    listint = [listint[0], listint[-1]]
                    xlims.append(listint)
            else:
                raise ValueError(
                    "Bad xlimits for categorical var[{}] "
                    "should have {} categories, got only {} in {}".format(i, xtyp[1], len(xlimits[i]), xlimits[i])
                )
        else:
            _raise_value_error(xtyp)
    return np.array(xlims).astype(float)


def cast_to_discrete_values(xtypes, xlimits, categorical_kernel, x):
    """
    see MixedIntegerContext.cast_to_discrete_values
    """
    ret = ensure_2d_array(x, "x").copy()
    x_col = 0
    for i, xtyp in enumerate(xtypes):
        if xtyp == FLOAT:
            x_col += 1
            continue
        elif xtyp == ORD:
            if isinstance(xlimits[i][0], str):
                listint = list(map(float, xlimits[i]))
                ret[:, x_col] = take_closest_in_list(listint, ret[:, x_col])
            else:
                ret[:, x_col] = np.round(ret[:, x_col])
            x_col += 1
        elif isinstance(xtyp, tuple) and xtyp[0] == ENUM:
            if categorical_kernel is None:
                # Categorial : The biggest level is selected.
                xenum = ret[:, x_col : x_col + xtyp[1]]
                maxx = np.max(xenum, axis=1).reshape((-1, 1))
                mask = xenum < maxx
                xenum[mask] = 0
                xenum[~mask] = 1
                x_col = x_col + xtyp[1]
            else:
                ret[:, x_col] = np.round(ret[:, x_col])
                x_col += 1
        else:
            _raise_value_error(xtyp)
    return ret


def fold_with_enum_index(xtypes, x, categorical_kernel=None):
    """
    see MixedIntegerContext.fold_with_enum_index
    """
    x = np.atleast_2d(x)
    xfold = np.zeros((x.shape[0], len(xtypes)))
    unfold_index = 0
    for i, xtyp in enumerate(xtypes):
        if xtyp == FLOAT or xtyp == ORD:
            xfold[:, i] = x[:, unfold_index]
            unfold_index += 1
        elif isinstance(xtyp, tuple) and xtyp[0] == ENUM:
            index = np.argmax(x[:, unfold_index : unfold_index + xtyp[1]], axis=1)
            xfold[:, i] = index
            unfold_index += xtyp[1]
        else:
            _raise_value_error(xtyp)
    return xfold


def unfold_with_enum_mask(xtypes, x):
    """
    see MixedIntegerContext.unfold_with_enum_mask
    """
    x = np.atleast_2d(x)
    xunfold = np.zeros((x.shape[0], compute_unfolded_dimension(xtypes)))
    unfold_index = 0
    for i, xtyp in enumerate(xtypes):
        if xtyp == FLOAT or xtyp == ORD:
            xunfold[:, unfold_index] = x[:, i]
            unfold_index += 1
        elif isinstance(xtyp, tuple) and xtyp[0] == ENUM:
            enum_slice = xunfold[:, unfold_index : unfold_index + xtyp[1]]
            for row in range(x.shape[0]):
                enum_slice[row, x[row, i].astype(int)] = 1
            unfold_index += xtyp[1]
        else:
            _raise_value_error(xtyp)
    return xunfold


def cast_to_enum_value(xlimits, x_col, enum_indexes):
    """
    see MixedIntegerContext.cast_to_enum_value
    """
    return [xlimits[x_col][index] for index in enum_indexes]


def cast_to_mixed_integer(xtypes, xlimits, x):
    """
    see MixedIntegerContext.cast_to_mixed_integer
    """
    res = []
    for i, xtyp in enumerate(xtypes):
        xi = x[i]
        if xtyp == FLOAT:
            res.append(xi)
        elif xtyp == ORD:
            res.append(int(xi))
        elif isinstance(xtyp, tuple) and xtyp[0] == ENUM:
            res.append(xlimits[i][int(xi)])
        else:
            _raise_value_error(xtyp)
    return res


class MixedIntegerSamplingMethod(SamplingMethod):
    """
    Sampling method decorator that takes an SMT continuous sampling method and
    cast values according x types specification to implement a sampling method
    handling integer (ORD) or categorical (ENUM) features
    """

    def __init__(self, xtypes, xlimits, sampling_method_class, **kwargs):
        """
        Parameters
        ----------
        xtypes: x types list
            x types specification
        xlimits: array-like
            bounds of x features
        sampling_method_class: class name
            SMT sampling method class
        kwargs: options of the given sampling method
            options used to instanciate the SMT sampling method
            with the additional 'output_in_folded_space' boolean option
            specifying if doe output should be in folded space (enum indexes)
            or not (enum masks)
        """
        super()
        check_xspec_consistency(xtypes, xlimits)
        self._xtypes = xtypes
        self._xlimits = xlimits
        self._unfolded_xlimits = unfold_xlimits_with_continuous_limits(self._xtypes, xlimits)
        self._output_in_folded_space = kwargs.get("output_in_folded_space", True)
        kwargs.pop("output_in_folded_space", None)
        self._sampling_method = sampling_method_class(xlimits=self._unfolded_xlimits, **kwargs)

    def _compute(self, nt):
        doe = self._sampling_method(nt)
        unfold_xdoe = cast_to_discrete_values(self._xtypes, self._xlimits, None, doe)
        if self._output_in_folded_space:
            return fold_with_enum_index(self._xtypes, unfold_xdoe)
        else:
            return unfold_xdoe

    def __call__(self, nt):
        return self._compute(nt)


#######################################


class ScaledSamplingMethod(SamplingMethod):
    """This class describes an sample method which generates samples in the unit hypercube.

    The __call__ method does scale the generated samples accordingly to the defined xlimits.
    """

    def __call__(self, nt: int) -> np.ndarray:
        """
        Compute the requested number of sampling points.

        The number of dimensions (nx) is determined based on `xlimits.shape[0]`.

        Arguments
        ---------
        nt : int
            Number of points requested.

        Returns
        -------
        ndarray[nt, nx]
            The sampling locations in the input space.
        """
        return _scale_to_xlimits(self._compute(nt), self.options["xlimits"])

    @abstractmethod
    def _compute(self, nt: int) -> np.ndarray:
        """
        Implemented by sampling methods to compute the requested number of sampling points.

        The number of dimensions (nx) is determined based on `xlimits.shape[0]`.

        Arguments
        ---------
        nt : int
            Number of points requested.

        Returns
        -------
        ndarray[nt, nx]
            The sampling locations in the unit hypercube.
        """
        raise Exception("This sampling method has not been implemented correctly")


def _scale_to_xlimits(samples: np.ndarray, xlimits: np.ndarray) -> np.ndarray:
    """Scales the samples from the unit hypercube to the specified limits.

    Parameters
    ----------
    samples : np.ndarray
        The samples with coordinates in [0,1]
    xlimits : np.ndarray
        The xlimits

    Returns
    -------
    np.ndarray
        The scaled samples.
    """
    nx = xlimits.shape[0]
    for kx in range(nx):
        samples[:, kx] = xlimits[kx, 0] + samples[:, kx] * (xlimits[kx, 1] - xlimits[kx, 0])
    return samples


#######################################


class Random(ScaledSamplingMethod):
    def _compute(self, nt):
        """
        Implemented by sampling methods to compute the requested number of sampling points.

        The number of dimensions (nx) is determined based on `xlimits.shape[0]`.

        Arguments
        ---------
        nt : int
            Number of points requested.

        Returns
        -------
        ndarray[nt, nx]
            The sampling locations in the unit hypercube.
        """
        xlimits = self.options["xlimits"]
        nx = xlimits.shape[0]
        return np.random.rand(nt, nx)


#######################################


class LHS(ScaledSamplingMethod):
    def _initialize(self):
        self.options.declare(
            "criterion",
            "c",
            values=["center", "maximin", "centermaximin", "correlation", "c", "m", "cm", "corr", "ese",],
            types=str,
            desc="criterion used to construct the LHS design "
            + "c, m, cm and corr are abbreviation of center, maximin, centermaximin and correlation, respectively",
        )
        self.options.declare(
            "random_state",
            types=(type(None), int, np.random.RandomState),
            desc="Numpy RandomState object or seed number which controls random draws",
        )

    def _compute(self, nt):
        """
        Implemented by sampling methods to compute the requested number of sampling points.

        The number of dimensions (nx) is determined based on `xlimits.shape[0]`.

        Arguments
        ---------
        nt : int
            Number of points requested.

        Returns
        -------
        ndarray[nt, nx]
            The sampling locations in the unit hypercube.
        """
        xlimits = self.options["xlimits"]
        nx = xlimits.shape[0]

        if isinstance(self.options["random_state"], np.random.RandomState):
            self.random_state = self.options["random_state"]
        elif isinstance(self.options["random_state"], int):
            self.random_state = np.random.RandomState(self.options["random_state"])
        else:
            self.random_state = np.random.RandomState()

        if self.options["criterion"] != "ese":
            return lhs(nx, samples=nt, criterion=self.options["criterion"], random_state=self.random_state,)
        elif self.options["criterion"] == "ese":
            return self._ese(nx, nt)

    def _maximinESE(
        self, X, T0=None, outer_loop=None, inner_loop=None, J=20, tol=1e-3, p=10, return_hist=False, fixed_index=[],
    ):
        """

        Returns an optimized design starting from design X. For more information,
        see R. Jin, W. Chen and A. Sudjianto (2005):
        An efficient algorithm for constructing optimal design of computer
        experiments. Journal of Statistical Planning and Inference, 134:268-287.


        Parameters
        ----------

        X : array
            The design to be optimized

        T0 : double, optional
        Initial temperature of the algorithm.
        If set to None, a standard temperature is used.

        outer_loop : integer, optional
        The number of iterations of the outer loop. If None, set to
        min(1.5*dimension of LHS, 30)

        inner_loop : integer, optional
        The number of iterations of the inner loop. If None, set to
        min(20*dimension of LHS, 100)

        J : integer, optional
        Number of replications of the plan in the inner loop. Default to 20

        tol : double, optional
        Tolerance for modification of Temperature T. Default to 0.001

        p : integer, optional
        Power used in the calculation of the PhiP criterion. Default to 10

        return_hist : boolean, optional
        If set to True, the function returns information about the behaviour of
        temperature, PhiP criterion and probability of acceptance during the
        process of optimization. Default to False


        Returns
        ------

        X_best : array
        The optimized design

        hist : dictionnary
        If return_hist is set to True, returns a dictionnary containing the phiP
        ('PhiP') criterion, the temperature ('T') and the probability of
        acceptance ('proba') during the optimization.

        """

        # Initialize parameters if not defined
        if T0 is None:
            T0 = 0.005 * self._PhiP(X, p=p)
        if inner_loop is None:
            inner_loop = min(20 * X.shape[1], 100)
        if outer_loop is None:
            outer_loop = min(int(1.5 * X.shape[1]), 30)

        T = T0
        X_ = X[:]  # copy of initial plan
        X_best = X_[:]
        d = X.shape[1]
        PhiP_ = self._PhiP(X_best, p=p)
        PhiP_best = PhiP_

        hist_T = list()
        hist_proba = list()
        hist_PhiP = list()
        hist_PhiP.append(PhiP_best)

        # Outer loop
        for z in range(outer_loop):
            PhiP_oldbest = PhiP_best
            n_acpt = 0
            n_imp = 0

            # Inner loop
            for i in range(inner_loop):

                modulo = (i + 1) % d
                l_X = list()
                l_PhiP = list()

                # Build J different plans with a single exchange procedure
                # See description of PhiP_exchange procedure
                for j in range(J):
                    l_X.append(X_.copy())
                    l_PhiP.append(self._PhiP_exchange(l_X[j], k=modulo, PhiP_=PhiP_, p=p, fixed_index=fixed_index))

                l_PhiP = np.asarray(l_PhiP)
                k = np.argmin(l_PhiP)
                PhiP_try = l_PhiP[k]

                # Threshold of acceptance
                if PhiP_try - PhiP_ <= T * self.random_state.rand(1)[0]:
                    PhiP_ = PhiP_try
                    n_acpt = n_acpt + 1
                    X_ = l_X[k]

                    # Best plan retained
                    if PhiP_ < PhiP_best:
                        X_best = X_
                        PhiP_best = PhiP_
                        n_imp = n_imp + 1

                hist_PhiP.append(PhiP_best)

            p_accpt = float(n_acpt) / inner_loop  # probability of acceptance
            p_imp = float(n_imp) / inner_loop  # probability of improvement

            hist_T.extend(inner_loop * [T])
            hist_proba.extend(inner_loop * [p_accpt])

            if PhiP_best - PhiP_oldbest < tol:
                # flag_imp = 1
                if p_accpt >= 0.1 and p_imp < p_accpt:
                    T = 0.8 * T
                elif p_accpt >= 0.1 and p_imp == p_accpt:
                    pass
                else:
                    T = T / 0.8
            else:
                # flag_imp = 0
                if p_accpt <= 0.1:
                    T = T / 0.7
                else:
                    T = 0.9 * T

        hist = {"PhiP": hist_PhiP, "T": hist_T, "proba": hist_proba}

        if return_hist:
            return X_best, hist
        else:
            return X_best

    def _PhiP(self, X, p=10):
        """
        Calculates the PhiP criterion of the design X with power p.

        X : array_like
        The design where to calculate PhiP
        p : integer
        The power used for the calculation of PhiP (default to 10)
        """

        return ((pdist(X) ** (-p)).sum()) ** (1.0 / p)

    def _PhiP_exchange(self, X, k, PhiP_, p, fixed_index):
        """
        Modifies X with a single exchange algorithm and calculates the corresponding
        PhiP criterion. Internal use.
        Optimized calculation of the PhiP criterion. For more information, see:
        R. Jin, W. Chen and A. Sudjianto (2005):
        An efficient algorithm for constructing optimal design of computer
        experiments. Journal of Statistical Planning and Inference, 134:268-287.

        Parameters
        ----------

        X : array_like
        The initial design (will be modified during procedure)

        k : integer
        The column where the exchange is proceeded

        PhiP_ : double
        The PhiP criterion of the initial design X

        p : integer
        The power used for the calculation of PhiP


        Returns
        ------

        res : double
        The PhiP criterion of the modified design X

        """

        # Choose two (different) random rows to perform the exchange
        i1 = self.random_state.randint(X.shape[0])
        while i1 in fixed_index:
            i1 = self.random_state.randint(X.shape[0])

        i2 = self.random_state.randint(X.shape[0])
        while i2 == i1 or i2 in fixed_index:
            i2 = self.random_state.randint(X.shape[0])

        X_ = np.delete(X, [i1, i2], axis=0)

        dist1 = cdist([X[i1, :]], X_)
        dist2 = cdist([X[i2, :]], X_)
        d1 = np.sqrt(dist1 ** 2 + (X[i2, k] - X_[:, k]) ** 2 - (X[i1, k] - X_[:, k]) ** 2)
        d2 = np.sqrt(dist2 ** 2 - (X[i2, k] - X_[:, k]) ** 2 + (X[i1, k] - X_[:, k]) ** 2)

        res = (PhiP_ ** p + (d1 ** (-p) - dist1 ** (-p) + d2 ** (-p) - dist2 ** (-p)).sum()) ** (1.0 / p)
        X[i1, k], X[i2, k] = X[i2, k], X[i1, k]

        return res

    def _ese(self, dim, nt, fixed_index=[], P0=[]):
        """
        Parameters
        ----------

        fixed_index : list
            When running an "ese" optimization, we can fix the indexes of
            the points that we do not want to modify

        """
        # Parameters of maximinESE procedure
        if len(fixed_index) == 0:
            P0 = lhs(dim, nt, criterion=None, random_state=self.random_state)
        else:
            P0 = P0
            self.random_state = np.random.RandomState()
        J = 20
        outer_loop = min(int(1.5 * dim), 30)
        inner_loop = min(20 * dim, 100)

        D0 = pdist(P0)
        R0 = np.corrcoef(P0)
        corr0 = np.max(np.abs(R0[R0 != 1]))
        phip0 = self._PhiP(P0)

        P, historic = self._maximinESE(
            P0,
            outer_loop=outer_loop,
            inner_loop=inner_loop,
            J=J,
            tol=1e-3,
            p=10,
            return_hist=True,
            fixed_index=fixed_index,
        )
        return P

    def expand_lhs(self, x, n_points, method="basic"):
        """
        Given a Latin Hypercube Sample (LHS) "x", returns an expanded LHS
        by adding "n_points" new points.

        Parameters
        ----------
        x : array
            Initial LHS.
        n_points : integer
            Number of points that are to be added to the expanded LHS.
        method : str, optional
            Methodoly for the construction of the expanded LHS.
            The default is "basic". The other option is "ese" to use the
            ese optimization

        Returns
        -------
        x_new : array
            Expanded LHS.

        """

        xlimits = self.options["xlimits"]

        new_num = len(x) + n_points
        if new_num % len(x) != 0:
            print(
                "WARNING: The added number of points is not a "
                "multiple of the initial number of points."
                "Thus, it cannot be ensured that the output is an LHS."
            )

        # Evenly spaced intervals with the final dimension of the LHS
        intervals = []
        for i in range(len(xlimits)):
            intervals.append(np.linspace(xlimits[i][0], xlimits[i][1], new_num + 1))

        # Creates a subspace with the rows and columns that have no points
        # in the new space
        subspace_limits = [[]] * len(xlimits)
        subspace_bool = []
        for i in range(len(xlimits)):
            subspace_limits[i] = []

            subspace_bool.append(
                [
                    [intervals[i][j] < x[kk][i] < intervals[i][j + 1] for kk in range(len(x))]
                    for j in range(len(intervals[i]) - 1)
                ]
            )

            [
                subspace_limits[i].append([intervals[i][ii], intervals[i][ii + 1]])
                for ii in range(len(subspace_bool[i]))
                if not (True in subspace_bool[i][ii])
            ]

        # Sampling of the new subspace
        sampling_new = LHS(xlimits=np.array([[0.0, 1.0]] * len(xlimits)))
        x_subspace = sampling_new(n_points)

        column_index = 0
        sorted_arr = x_subspace[x_subspace[:, column_index].argsort()]

        for j in range(len(xlimits)):
            for i in range(len(sorted_arr)):
                sorted_arr[i, j] = subspace_limits[j][i][0] + sorted_arr[i, j] * (
                    subspace_limits[j][i][1] - subspace_limits[j][i][0]
                )

        H = np.zeros_like(sorted_arr)
        for j in range(len(xlimits)):
            order = np.random.permutation(len(sorted_arr))
            H[:, j] = sorted_arr[order, j]

        x_new = np.concatenate((x, H), axis=0)

        if method == "ese":
            # Sampling of the new subspace
            sampling_new = LHS(xlimits=xlimits, criterion="ese")
            x_new = sampling_new._ese(len(x_new), len(x_new), fixed_index=np.arange(0, len(x), 1), P0=x_new)

        return x_new


#######################################
