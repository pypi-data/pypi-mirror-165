import abc
import collections
import inspect
from collections.abc import Iterable, Sequence
from typing import Tuple

import uqbar.strings

import supriya
from supriya import BinaryOperator, SignalRange, UnaryOperator
from supriya.typing import UGenInputMap

from .mixins import UGenMethodMixin


class UGenMeta(abc.ABCMeta):

    initializer_template = uqbar.strings.normalize(
        """
    def __init__(
        self,
        {parameters_indent_one}
    ):
        {base_class_name}.__init__(
            self,
            {parameters_indent_two}
            )
    """
    )

    constructor_template = uqbar.strings.normalize(
        '''
    @classmethod
    def {rate_token}(
        cls,
        {parameters_indent_one}
    ):
        """
        Constructs a {rate_name_lower}-rate ``{ugen_name}`` unit generator graph.

        Returns unit generator graph.
        """
        calculation_rate = supriya.CalculationRate.{rate_name_upper}
        {validators}
        return cls._new_expanded(
            calculation_rate=calculation_rate,
            {parameters_indent_two}
        )
    '''
    )

    rateless_constructor_template = uqbar.strings.normalize(
        '''
    @classmethod
    def new(
        cls,
        {parameters_indent_one}
    ):
        """
        Constructs a ``{ugen_name}`` unit generator graph.

        Returns unit generator graph.
        """
        {validators}
        return cls._new_expanded(
            {parameters_indent_two}
        )
    '''
    )

    def __new__(metaclass, class_name, bases, namespace):
        ordered_input_names = namespace.get("_ordered_input_names")
        unexpanded_input_names = namespace.get("_unexpanded_input_names", ())
        valid_calculation_rates = namespace.get("_valid_calculation_rates", ())
        (
            default_channel_count,
            has_settable_channel_count,
        ) = UGenMeta.get_channel_count(namespace, bases)
        if isinstance(ordered_input_names, collections.OrderedDict):
            for name in ordered_input_names:
                if name in namespace:
                    continue
                namespace[name] = UGenMeta.make_property(
                    ugen_name=class_name,
                    input_name=name,
                    unexpanded=name in unexpanded_input_names,
                )
            if "__init__" not in namespace:
                function, string = UGenMeta.make_initializer(
                    ugen_name=class_name,
                    bases=bases,
                    parameters=ordered_input_names.copy(),
                    has_calculation_rate=bool(valid_calculation_rates),
                    default_channel_count=default_channel_count,
                    has_settable_channel_count=has_settable_channel_count,
                )
                namespace["__init__"] = function
                namespace["_init_source"] = string
            constructor_rates = {}
            if valid_calculation_rates:
                for rate in valid_calculation_rates:
                    if rate.token in namespace:
                        continue
                    constructor_rates[rate.token] = rate
            elif "new" not in namespace:
                constructor_rates["new"] = None
            for name, rate in constructor_rates.items():
                function, string = UGenMeta.make_constructor(
                    ugen_name=class_name,
                    bases=bases,
                    rate=rate,
                    parameters=ordered_input_names.copy(),
                    default_channel_count=default_channel_count,
                    has_settable_channel_count=has_settable_channel_count,
                )
                namespace[name] = function
                namespace["_{}_source".format(name)] = string
        return super().__new__(metaclass, class_name, bases, namespace)

    @staticmethod
    def get_channel_count(namespace, bases):
        default_channel_count = namespace.get("_default_channel_count")
        if default_channel_count is None:
            for base in bases:
                default_channel_count = getattr(base, "_default_channel_count")
                if default_channel_count is not None:
                    break
        has_settable_channel_count = namespace.get("_has_settable_channel_count")
        if has_settable_channel_count is None:
            for base in bases:
                has_settable_channel_count = getattr(
                    base, "_has_settable_channel_count"
                )
                if has_settable_channel_count is not None:
                    break
        return default_channel_count, has_settable_channel_count

    @staticmethod
    def compile(string, object_name, ugen_name, bases):
        namespace = {"supriya": supriya}
        namespace[bases[0].__name__] = bases[0]
        source_name = "<auto-generated> {}.py".format(ugen_name)
        try:
            code = compile(string, source_name, "exec")
            exec(code, namespace, namespace)
        except Exception:
            print(string)
            raise
        return namespace[object_name]

    @staticmethod
    def make_constructor(
        ugen_name,
        bases,
        rate,
        parameters,
        default_channel_count=False,
        has_settable_channel_count=False,
    ):
        validators = ""
        if default_channel_count and has_settable_channel_count:
            parameters["channel_count"] = int(default_channel_count)
            validators = ("\n" + (" " * 4)).join(
                [
                    "if channel_count < 1:",
                    "    raise ValueError('Channel count must be greater than zero')",
                ]
            )
        parameters_indent_one = (
            "\n    ".join(
                ["{}={},".format(key, value) for key, value in parameters.items()]
            )
            .replace("=inf,", "=float('inf'),")
            .replace("=-inf,", "=float('-inf'),")
        )
        parameters_indent_two = "\n        ".join(
            ["{}={},".format(key, key) for key, value in parameters.items()]
        )
        kwargs = dict(
            parameters_indent_one=parameters_indent_one,
            parameters_indent_two=parameters_indent_two,
            ugen_name=ugen_name,
            validators=validators,
        )
        if rate is None:
            string = UGenMeta.rateless_constructor_template.format(**kwargs)
        else:
            kwargs.update(
                rate_name_lower=rate.name.lower(),
                rate_name_upper=rate.name,
                rate_token=rate.token,
            )
            string = UGenMeta.constructor_template.format(**kwargs)
        object_name = "new" if rate is None else rate.token
        function = UGenMeta.compile(string, object_name, ugen_name, bases)
        return function, string

    @staticmethod
    def make_initializer(
        ugen_name,
        bases,
        parameters,
        has_calculation_rate=True,
        default_channel_count=False,
        has_settable_channel_count=False,
    ):
        if has_calculation_rate:
            new_parameters = collections.OrderedDict([("calculation_rate", None)])
            new_parameters.update(parameters)
            parameters = new_parameters
        if default_channel_count and has_settable_channel_count:
            parameters["channel_count"] = int(default_channel_count)
        parameters_indent_one = (
            "\n    ".join(
                ["{}={},".format(key, value) for key, value in parameters.items()]
            )
            .replace("=inf,", "=float('inf'),")
            .replace("=-inf,", "=float('-inf'),")
        )
        if has_settable_channel_count:
            parameters["channel_count"] = "channel_count"
        elif default_channel_count > 1:
            parameters["channel_count"] = int(default_channel_count)
        parameters_indent_two = "\n        ".join(
            [
                "{}={},".format(key, value if key == "channel_count" else key)
                for key, value in parameters.items()
            ]
        )
        string = UGenMeta.initializer_template.format(
            base_class_name=bases[0].__name__,
            parameters_indent_one=parameters_indent_one,
            parameters_indent_two=parameters_indent_two,
        )
        function = UGenMeta.compile(string, "__init__", ugen_name, bases)
        return function, string

    @staticmethod
    def make_property(ugen_name, input_name, unexpanded=False):
        doc = uqbar.strings.normalize(
            """
        Gets ``{input_name}`` of ``{ugen_name}``.

        Returns input.
        """
        ).format(ugen_name=ugen_name, input_name=input_name)
        if unexpanded:

            def getter(object_):
                index = tuple(object_._ordered_input_names).index(input_name)
                return tuple(object_._inputs[index:])

        else:

            def getter(object_):
                index = tuple(object_._ordered_input_names).index(input_name)
                return object_._inputs[index]

        return property(fget=getter, doc=doc)


class UGen(UGenMethodMixin, metaclass=UGenMeta):
    """
    A UGen.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_inputs", "_input_names", "_special_index", "_uuid")

    _default_channel_count = 1

    _has_settable_channel_count = False

    _has_done_flag = False

    _is_input = False

    _is_output = False

    _is_pure = False

    _is_width_first = False

    _ordered_input_names: UGenInputMap = None

    _signal_range: int = SignalRange.BIPOLAR

    _unexpanded_input_names: Tuple[str, ...] = ()

    _valid_calculation_rates: Tuple[int, ...] = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, calculation_rate=None, special_index=0, **kwargs):
        import supriya.synthdefs

        calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        if self._valid_calculation_rates:
            assert calculation_rate in self._valid_calculation_rates
        self._calculation_rate = calculation_rate
        self._inputs = []
        self._input_names = []
        self._special_index = special_index
        ugenlike_prototype = (UGen, supriya.synthdefs.Parameter)
        server_id_prototype = (
            supriya.realtime.ServerObject,
            supriya.realtime.BusProxy,
            supriya.realtime.BufferProxy,
        )
        for input_name in self._ordered_input_names:
            input_value = None
            if input_name in kwargs:
                input_value = kwargs.pop(input_name)
            if isinstance(input_value, ugenlike_prototype):
                assert len(input_value) == 1
                input_value = input_value[0]
            elif isinstance(input_value, server_id_prototype):
                input_value = int(input_value)
            if self._is_unexpanded_input_name(input_name):
                if not isinstance(input_value, Sequence):
                    input_value = (input_value,)
                if isinstance(input_value, Sequence):
                    input_value = tuple(input_value)
                elif not self._is_valid_input(input_value):
                    raise ValueError(input_name, input_value)
            elif not self._is_valid_input(input_value):
                raise ValueError(input_name, input_value)
            self._configure_input(input_name, input_value)
        if kwargs:
            raise ValueError(kwargs)
        assert all(
            isinstance(_, (supriya.synthdefs.OutputProxy, float)) for _ in self.inputs
        )
        self._validate_inputs()
        self._uuid = None
        if supriya.synthdefs.SynthDefBuilder._active_builders:
            builder = supriya.synthdefs.SynthDefBuilder._active_builders[-1]
            self._uuid = builder._uuid
        self._check_inputs_share_same_uuid()
        if self._uuid is not None:
            builder._add_ugens(self)

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        """
        Gets output proxy at index `i`.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar()
            >>> ugen[0]
            SinOsc.ar()[0]

        Returns output proxy.
        """
        return self._get_output_proxy(i)

    def __len__(self):
        """
        Gets number of ugen outputs.

        Returns integer.
        """
        return getattr(self, "_channel_count", self._default_channel_count)

    def __repr__(self):
        """
        Gets interpreter representation of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar()
            >>> repr(ugen)
            'SinOsc.ar()'

        ::

            >>> ugen = supriya.ugens.WhiteNoise.kr()
            >>> repr(ugen)
            'WhiteNoise.kr()'

        ::

            >>> ugen = supriya.ugens.Rand.ir()
            >>> repr(ugen)
            'Rand.ir()'

        Returns string.
        """
        import supriya.synthdefs

        if self.calculation_rate == supriya.CalculationRate.DEMAND:
            return "{}()".format(type(self).__name__)
        calculation_abbreviations = {
            supriya.CalculationRate.AUDIO: "ar",
            supriya.CalculationRate.CONTROL: "kr",
            supriya.CalculationRate.SCALAR: "ir",
        }
        string = "{}.{}()".format(
            type(self).__name__, calculation_abbreviations[self.calculation_rate]
        )
        return string

    ### PRIVATE METHODS ###

    @staticmethod
    def _as_audio_rate_input(expr):
        import supriya.synthdefs
        import supriya.ugens

        if isinstance(expr, (int, float)):
            if expr == 0:
                return supriya.ugens.Silence.ar()
            return supriya.ugens.DC.ar(expr)
        elif isinstance(expr, (UGen, supriya.synthdefs.OutputProxy)):
            if expr.calculation_rate == supriya.CalculationRate.AUDIO:
                return expr
            return supriya.ugens.K2A.ar(source=expr)
        elif isinstance(expr, Iterable):
            return supriya.synthdefs.UGenArray(
                UGen._as_audio_rate_input(x) for x in expr
            )
        raise ValueError(expr)

    def _add_constant_input(self, name, value):
        self._inputs.append(float(value))
        self._input_names.append(name)

    def _add_ugen_input(self, name, ugen, output_index=None):
        import supriya.synthdefs

        # if isinstance(ugen, supriya.synthdefs.Parameter):
        #    output_proxy = ugen
        if isinstance(ugen, supriya.synthdefs.OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = supriya.synthdefs.OutputProxy(
                output_index=output_index, source=ugen
            )
        self._inputs.append(output_proxy)
        self._input_names.append(name)

    def _check_inputs_share_same_uuid(self):
        import supriya.synthdefs

        for input_ in self.inputs:
            if not isinstance(input_, supriya.synthdefs.OutputProxy):
                continue
            if input_.source._uuid != self._uuid:
                message = "UGen input in different scope: {!r}"
                message = message.format(input_.source)
                raise ValueError(message)

    def _check_rate_same_as_first_input_rate(self):
        import supriya.synthdefs

        first_input_rate = supriya.CalculationRate.from_expr(self.inputs[0])
        return self.calculation_rate == first_input_rate

    def _check_range_of_inputs_at_audio_rate(self, start=None, stop=None):
        import supriya.synthdefs

        if self.calculation_rate != supriya.CalculationRate.AUDIO:
            return True
        for input_ in self.inputs[start:stop]:
            calculation_rate = supriya.CalculationRate.from_expr(input_)
            if calculation_rate != supriya.CalculationRate.AUDIO:
                return False
        return True

    def _configure_input(self, name, value):
        import supriya.synthdefs

        ugen_prototype = (
            supriya.synthdefs.OutputProxy,
            supriya.synthdefs.Parameter,
            UGen,
        )
        if hasattr(value, "__float__"):
            self._add_constant_input(name, float(value))
        elif isinstance(value, ugen_prototype):
            self._add_ugen_input(name, value._get_source(), value._get_output_number())
        elif isinstance(value, Sequence):
            if name not in self._unexpanded_input_names:
                raise ValueError(name, self._unexpanded_input_names)
            for i, x in enumerate(value):
                if hasattr(x, "__float__"):
                    self._add_constant_input((name, i), float(x))
                elif isinstance(x, ugen_prototype):
                    self._add_ugen_input(
                        (name, i), x._get_source(), x._get_output_number()
                    )
                else:
                    raise Exception("{!r} {!r}".format(value, x))
        else:
            raise ValueError(f"Invalid input: {value!r}")

    @staticmethod
    def _expand_dictionary(dictionary, unexpanded_input_names=None):
        """
        Expands a dictionary into multichannel dictionaries.

        ::

            >>> dictionary = {"foo": 0, "bar": (1, 2), "baz": (3, 4, 5)}
            >>> result = supriya.synthdefs.UGen._expand_dictionary(dictionary)
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bar', 1), ('baz', 3), ('foo', 0)]
            [('bar', 2), ('baz', 4), ('foo', 0)]
            [('bar', 1), ('baz', 5), ('foo', 0)]

        ::

            >>> dictionary = {"bus": (8, 9), "source": (1, 2, 3)}
            >>> result = supriya.synthdefs.UGen._expand_dictionary(
            ...     dictionary,
            ...     unexpanded_input_names=("source",),
            ... )
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bus', 8), ('source', (1, 2, 3))]
            [('bus', 9), ('source', (1, 2, 3))]

        """
        import supriya.synthdefs

        dictionary = dictionary.copy()
        cached_unexpanded_inputs = {}
        if unexpanded_input_names is not None:
            for input_name in unexpanded_input_names:
                if input_name not in dictionary:
                    continue
                cached_unexpanded_inputs[input_name] = dictionary[input_name]
                del dictionary[input_name]
        maximum_length = 1
        result = []
        prototype = (Sequence, UGen, supriya.synthdefs.Parameter)
        for name, value in dictionary.items():
            if isinstance(value, prototype) and not isinstance(value, str):
                maximum_length = max(maximum_length, len(value))
        for i in range(maximum_length):
            result.append({})
            for name, value in dictionary.items():
                if isinstance(value, prototype) and not isinstance(value, str):
                    value = value[i % len(value)]
                    result[i][name] = value
                else:
                    result[i][name] = value
        for expanded_inputs in result:
            expanded_inputs.update(cached_unexpanded_inputs)
        return result

    def _get_done_action(self):
        import supriya.synthdefs

        if "done_action" not in self._ordered_input_names:
            return None
        return supriya.DoneAction.from_expr(int(self.done_action))

    @staticmethod
    def _get_method_for_rate(cls, calculation_rate):
        import supriya.synthdefs

        calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        if calculation_rate == supriya.CalculationRate.AUDIO:
            return cls.ar
        elif calculation_rate == supriya.CalculationRate.CONTROL:
            return cls.kr
        elif calculation_rate == supriya.CalculationRate.SCALAR:
            if hasattr(cls, "ir"):
                return cls.ir
            return cls.kr
        return cls.new

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate] * len(self)

    def _get_source(self):
        return self

    def _is_unexpanded_input_name(self, input_name):
        if self._unexpanded_input_names:
            if input_name in self._unexpanded_input_names:
                return True
        return False

    def _is_valid_input(self, input_value):
        import supriya.synthdefs

        if isinstance(input_value, supriya.synthdefs.OutputProxy):
            return True
        elif hasattr(input_value, "__float__"):
            return True
        return False

    @classmethod
    def _new_expanded(cls, special_index=0, **kwargs):
        import supriya.synthdefs

        get_signature = inspect.signature
        signature = get_signature(cls.__init__)
        input_dicts = UGen._expand_dictionary(
            kwargs, unexpanded_input_names=cls._unexpanded_input_names
        )
        ugens = []
        has_custom_special_index = "special_index" in signature.parameters
        for input_dict in input_dicts:
            if has_custom_special_index:
                ugen = cls._new_single(special_index=special_index, **input_dict)
            else:
                ugen = cls._new_single(**input_dict)
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return supriya.synthdefs.UGenArray(ugens)

    @classmethod
    def _new_single(cls, **kwargs):
        ugen = cls(**kwargs)
        return ugen

    def _optimize_graph(self, sort_bundles):
        if self._is_pure:
            self._perform_dead_code_elimination(sort_bundles)

    def _perform_dead_code_elimination(self, sort_bundles):
        sort_bundle = sort_bundles.get(self, None)
        if not sort_bundle or sort_bundle.descendants:
            return
        del sort_bundles[self]
        for antecedent in tuple(sort_bundle.antecedents):
            antecedent_bundle = sort_bundles.get(antecedent, None)
            if not antecedent_bundle:
                continue
            antecedent_bundle.descendants.remove(self)
            antecedent._optimize_graph(sort_bundles)

    def _validate_inputs(self):
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _has_done_action(self):
        return "done_action" in self._ordered_input_names

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        """
        Gets calculation-rate of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ... )
            >>> ugen.calculation_rate
            CalculationRate.AUDIO

        Returns calculation-rate.
        """
        return self._calculation_rate

    @property
    def has_done_flag(self):
        return self._has_done_flag

    @property
    def inputs(self):
        """
        Gets inputs of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ... )
            >>> for input_ in ugen.inputs:
            ...     input_
            ...
            WhiteNoise.kr()[0]
            0.5

        Returns tuple.
        """
        return tuple(self._inputs)

    @property
    def is_input_ugen(self):
        return self._is_input

    @property
    def is_output_ugen(self):
        return self._is_output

    @property
    def outputs(self):
        """
        Gets outputs of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ... )
            >>> ugen.outputs
            (CalculationRate.AUDIO,)

        Returns tuple.
        """
        return tuple(self._get_outputs())

    @property
    def signal_range(self):
        """
        Gets signal range of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar()
            >>> ugen.signal_range
            SignalRange.BIPOLAR

        A bipolar signal range indicates that the ugen generates signals above
        and below zero.

        A unipolar signal range indicates that the ugen only generates signals
        of 0 or greater.

        Returns signal range.
        """
        return self._signal_range

    @property
    def special_index(self):
        """
        Gets special index of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ... )
            >>> ugen.special_index
            0

        The `special index` of most ugens will be 0. SuperColliders's synth
        definition file format uses the special index to store the operator id
        for binary and unary operator ugens, and the parameter index of
        controls.

        Returns integer.
        """
        return self._special_index


class MultiOutUGen(UGen):
    """
    Abstract base class for ugens with multiple outputs.
    """

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(
        self, calculation_rate=None, special_index=0, channel_count=1, **kwargs
    ):
        self._channel_count = int(channel_count)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=special_index,
            **kwargs,
        )

    ### SPECIAL METHODS ###

    def __len__(self):
        """
        Gets number of ugen outputs.

        Returns integer.
        """
        return self._channel_count

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(cls, special_index=0, **kwargs):
        import supriya.synthdefs
        import supriya.ugens

        ugen = super(MultiOutUGen, cls)._new_expanded(
            special_index=special_index, **kwargs
        )
        output_proxies = []
        if isinstance(ugen, UGen):
            output_proxies.extend(ugen[:])
        else:
            for x in ugen:
                output_proxies.extend(x[:])
        if len(output_proxies) == 1:
            return output_proxies[0]
        result = supriya.synthdefs.UGenArray(output_proxies)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        """
        Gets channel count of multi-output ugen.

        Returns integer.
        """
        return self._channel_count


class PureUGen(UGen):
    """
    Abstract base class for ugens with no side-effects.

    These ugens may be optimized out of ugen graphs during SynthDef
    compilation.
    """

    ### CLASS VARIABLES ###

    _is_pure = True

    ### PRIVATE METHODS ###

    def _optimize_graph(self, sort_bundles):
        self._perform_dead_code_elimination(sort_bundles)


class PureMultiOutUGen(MultiOutUGen):
    """
    Abstract base class for multi-output ugens with no side-effects.

    These ugens may be optimized out of ugen graphs during SynthDef
    compilation.
    """

    def _optimize_graph(self, sort_bundles):
        self._perform_dead_code_elimination(sort_bundles)


class WidthFirstUGen(UGen):
    """
    Abstract base class for UGens with a width-first sort order.
    """

    ### CLASS VARIABLES ###

    _is_width_first = True

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, calculation_rate=None, special_index=0, **kwargs):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=special_index,
            **kwargs,
        )


class UnaryOpUGen(PureUGen):
    """
    A unary operator ugen, created by applying a unary operator to a ugen.

    ::

        >>> ugen = supriya.ugens.SinOsc.ar()
        >>> unary_op_ugen = abs(ugen)
        >>> unary_op_ugen
        UnaryOpUGen.ar()

    ::

        >>> unary_op_ugen.operator
        UnaryOperator.ABSOLUTE_VALUE

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("source", None)])

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, source=None, special_index=None):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            special_index=special_index,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def operator(self):
        """
        Gets operator of UnaryOpUgen.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> unary_op_ugen = -source
            >>> unary_op_ugen.operator
            UnaryOperator.NEGATIVE

        Returns unary operator.
        """
        return UnaryOperator(self.special_index)


class BinaryOpUGen(PureUGen):
    """
    A binary operator ugen, created by applying a binary operator to two
    ugens.

    ::

        >>> left_operand = supriya.ugens.SinOsc.ar()
        >>> right_operand = supriya.ugens.WhiteNoise.kr()
        >>> binary_op_ugen = left_operand * right_operand
        >>> binary_op_ugen
        BinaryOpUGen.ar()

    ::

        >>> binary_op_ugen.operator
        BinaryOperator.MULTIPLICATION

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("left", None), ("right", None)])

    ### INITIALIZER ###

    def __init__(
        self, calculation_rate=None, special_index=None, left=None, right=None
    ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=special_index,
            left=left,
            right=right,
        )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls, calculation_rate=None, special_index=None, left=None, right=None
    ):
        a = left
        b = right
        if special_index == BinaryOperator.MULTIPLICATION:
            if a == 0:
                return 0
            if b == 0:
                return 0
            if a == 1:
                return b
            if a == 1:
                return -b
            if b == 1:
                return a
            if b == -1:
                return -a
        if special_index == BinaryOperator.ADDITION:
            if a == 0:
                return b
            if b == 0:
                return a
        if special_index == BinaryOperator.SUBTRACTION:
            if a == 0:
                return -b
            if b == 0:
                return a
        if special_index == BinaryOperator.FLOAT_DIVISION:
            if b == 1:
                return a
            if b == -1:
                return -a
        ugen = cls(
            calculation_rate=calculation_rate,
            special_index=special_index,
            left=a,
            right=b,
        )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def operator(self):
        """
        Gets operator of BinaryOpUgen.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> binary_op_ugen = left / right
            >>> binary_op_ugen.operator
            BinaryOperator.FLOAT_DIVISION

        Returns binary operator.
        """
        return BinaryOperator(self.special_index)


class PseudoUGen:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError
