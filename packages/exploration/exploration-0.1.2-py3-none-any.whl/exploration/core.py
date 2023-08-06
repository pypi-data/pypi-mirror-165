"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-3-3
- Purpose: Core types and tools for dealing with them.

This file defines the main types used for processing and storing
exploration graphs. Key types are:

- `DecisionGraph`: Represents a graph of decisions, including observed
    connections to unknown destinations.
- `Exploration`: A list of `DecisionGraph`s with position and transition
    information representing exploration over time.
"""

from typing import (
    Any, Optional, List, Set, Union, Iterable, cast, Tuple, Dict,
    TypedDict, Sequence, Collection, TypeAlias
)

import copy
import ast
import sys
import warnings
import random

from . import graphs

Decision: TypeAlias = str
"""
A type alias: decision points are defined by their names.

A decision represents a location within a decision graph where a decision
can be made about where to go, or a dead-end reached by a previous
decision. Typically, one room can have multiple decision points in it,
even though many rooms have only one. Concepts like 'room' and 'area'
that group multiple decisions together (at various scales) are handled
by the idea of a `Zone`.
"""

Transition: TypeAlias = str
"""
A type alias: transitions are defined by their names.

A transition represents a means of travel from one decision to another.
Outgoing transition names have to be unique at each decision, but not
globally.
"""


State: TypeAlias = dict
"""
A type alias: states are just dictionaries.

They can contain whatever key/value pairs are necessary to represent
exploration-relevant game state. Typical entries might include:

- `'powers'`: A set of `Power`s the player has acquired.
- `'tokens'`: A dictionary mapping `Token`s to integers representing how
    many of that token type have been acquired.
"""


Power: TypeAlias = str
"""
A type alias: powers are defined by their names.

A power represents a capability that can be used to traverse certain
transitions. These transitions should have a `Requirement` specified to
indicate which power(s) and/or token(s) can be used to traverse it.
Powers are usually permanent, but may in some cases be temporary or be
temporarily disabled. Powers might also combine (e.g., speed booster
can't be used underwater until gravity suit is acquired).
"""

Token: TypeAlias = str
"""
A type alias: tokens are defined by their type names.

A token represents an expendable item that can be used to traverse certain
transitions a limited number of times (normally once after which the
token is used up), or to permanently open certain transitions.

When a key permanently opens only one specific door, or is re-usable to
open many doors, that should be represented as a Power, not a token. Only
when there is a choice of which door to unlock (and the key is then used
up) should keys be represented as tokens.
"""

Tag: TypeAlias = str
"""
A type alias: tags are strings.

A tag is an arbitrary string attached to a decision or transition.
Meanings are left up to the map-maker, but some conventions include:

- `'random'` indicates that an edge (usually an action, i.e., a
    self-edge) is not always available, but instead has some random
    element to it (for example, a random item drop from an enemy).
    Normally, the specifics of the random mechanism are not represented
    in detail.
- `'hard'` indicates that an edge is non-trivial to navigate. An
    annotation starting with `'fail:'` can be used to name another edge
    which would be traversed instead if the player fails to navigate the
    edge (e.g., a difficult series of platforms with a pit below that
    takes you to another decision). This is of course entirely
    subjective.
- `'false'` indicates that an edge doesn't actually exist, although it
    appears to. This tag is added in the same exploration step that
    requirements are updated (normally to `ReqImpossible`) to indicate
    that although the edge appeared to be traversable, it wasn't. This
    distinguishes that case from a case where edge requirements actually
    change.
- `'error'` indicates that an edge does not actually exist, and it's
    different than `'false'` because it indicates an error on the
    player's part rather than intentional deception by the game (another
    subjective distinction). It can also be used with a colon and another
    tag to indicate that that tag was applied in error (e.g., a ledge
    thought to be too high was not actually too high). This should be
    used sparingly, because in most cases capturing the player's
    perception of the world is what's desired. This is normally applied
    in the step before an edge is removed from the graph.
- `'hidden'` indicates that an edge is non-trivial to perceive. Again
    this is subjective. `'hinted'` can be used as well to indicate that
    despite being obfuscated, there are hints that suggest the edge's
    existence.
- `'internal'` indicates that this transition joins two different parts
    of the same room, which are represented as separate decisions.
- `'created'` indicates that this transition is newly created and
    represents a change to the decision layout. Normally, when entering
    a decision point, all visible options will be listed. When
    revisiting a decision, several things can happen:
        1. You could notice a transition you hadn't noticed before.
        2. You could traverse part of the room that you couldn't before,
           observing new transitions that have always been there (this
           would be represented as an internal edge to another decision
           node).
        3. You could observe that the decision had changed due to some
           action or event, and discover a new transition that didn't
           exist previously.
    This tag distinguishes case 3 from case 1. The presence or absence
    of a `'hidden'` tag in case 1 represents whether the newly-observed
    (but not new) transition was overlooked because it was hidden or was
    just overlooked accidentally.
"""

Annotation: TypeAlias = str
"A type alias: annotations are strings."

Zone = str
"""
A type alias: A zone as part of a DecisionGraph is identified using its
name.
"""

if sys.version_info < (3, 8):
    AstStrNode = ast.Str
else:
    AstStrNode = ast.Constant
"An AST node representing a string constant (changed in version 3.8)."


class Requirement:
    """
    Represents a precondition for traversing an edge or taking an action.
    This can be any boolean expression over powers and/or tokens the
    player needs to posses, with numerical values for the number of
    tokens required. For example, if the player needs either the
    wall-break power or the wall-jump power plus a balloon token, you
    could represent that using:

        ReqAny(
            ReqPower('wall-break'),
            ReqAll(
                ReqPower('wall-jump'),
                ReqTokens('balloon', 1)
            )
        )

    The subclasses define concrete requirements.
    """
    def satisfied(self, state: State) -> bool:
        """
        This will return True if the requirement is satisfied in the
        given game state, and False otherwise.
        """
        raise NotImplementedError(
            "Requirement is an abstract class and cannot be"
            " used directly."
        )

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError(
            "Requirement is an abstract class and cannot be compared."
        )

    def asGainList(self) -> List[Union[Power, Tuple[Token, int]]]:
        """
        Transforms this `Requirement` into a list of `Power` and/or
        `Token` entries suitable for the 'gain' slot of a
        `TransitionEffects` dictionary. The requirement must be either a
        `ReqTokens`, a `ReqPower`, or a `ReqAny` which includes only
        those three types as sub-requirements. The token and power
        requirements at the leaves of the tree will be collected into a
        list for the result. Raises a `TypeError` if this requirement is
        not suitable for transformation into a gains list.

        TODO: This code should be distributed to the sub-classes...
        """
        if isinstance(self, ReqPower):
            return [self.power]
        elif isinstance(self, ReqTokens):
            return [(self.tokenType, self.cost)]
        elif isinstance(self, ReqAny):
            result = []
            for sub in self.subs:
                result.extend(sub.asGainList())
            return result
        else:
            raise TypeError(
                f"Requirement contains a '{type(self)}' which cannot be"
                f" converted into a gained power or token (only"
                f" ReqPower, ReqTokens, and ReqAny are allowed, meaning"
                f" that '|' must be used instead of '&')."
            )

    @staticmethod
    def parse(req: str) -> 'Requirement':
        """
        This static method takes a string and returns a `Requirement`
        object using a mini-language for specifying requirements. The
        language uses '|' for 'or', '&' for 'and', '*' to indicate a
        token requirement (with an integer afterwards specifying the
        number of tokens) and either a valid Python identifier or a
        quoted string to name a power or token type required. You can
        also use 'X' (without quotes) for a never-satisfied requirement,
        and 'O' (without quotes) for an always-satisfied requirement. In
        particular, 'X' can be used for transitions which are only going
        to become accessible when some event takes place, like when a
        switch is flipped. Finally, you can use '-' for negation of a
        requirement; when applied to a token this flips the sense of the
        integer from 'must have at least this many' to 'must have
        strictly less than this many'.
        """
        # Parse as Python
        try:
            root = ast.parse(req.strip(), '<requirement string>', 'eval')
        except (SyntaxError, IndentationError):
            raise ValueError(f"Could not parse requirement '{req}'.")

        if not isinstance(root, ast.Expression):
            raise ValueError(
                f"Could not parse requirement '{req}'"
                f" (result must be an expression)."
            )

        top = root.body

        if not isinstance(top, (ast.BinOp, ast.Name, AstStrNode)):
            raise ValueError(
                f"Could not parse requirement '{req}'"
                f" (result must use only '|', '&', '*', quotes, and"
                f" parentheses)."
            )

        return Requirement.convertAST(top)

    @staticmethod
    def convertAST(node: ast.expr) -> 'Requirement':
        if isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, ast.USub):
                raise ValueError(
                    f"Invalid unary operator:\n{ast.dump(node)}"
                )
            negated = Requirement.convertAST(node.operand)
            return ReqNot(negated)

        if isinstance(node, ast.BinOp):
            # Three valid ops: '|' for or, '&' for and, and '*' for
            # tokens.
            if isinstance(node.op, ast.BitOr):
                # An either-or requirement
                lhs = Requirement.convertAST(node.left)
                rhs = Requirement.convertAST(node.right)
                # We flatten or-or-or chains
                if isinstance(lhs, ReqAny):
                    lhs.subs.append(rhs)
                    return lhs
                elif isinstance(rhs, ReqAny):
                    rhs.subs.append(lhs)
                    return rhs
                else:
                    return ReqAny([lhs, rhs])

            elif isinstance(node.op, ast.BitAnd):
                # An all-of requirement
                lhs = Requirement.convertAST(node.left)
                rhs = Requirement.convertAST(node.right)
                # We flatten and-and-and chains
                if isinstance(lhs, ReqAll):
                    lhs.subs.append(rhs)
                    return lhs
                elif isinstance(rhs, ReqAll):
                    rhs.subs.append(lhs)
                    return rhs
                else:
                    return ReqAll([lhs, rhs])

            elif isinstance(node.op, ast.Mult):
                # Merge power into token name w/ count
                lhs = Requirement.convertAST(node.left)
                if isinstance(lhs, ReqPower):
                    name = lhs.power
                    negate = False
                elif (
                    isinstance(lhs, ReqNot)
                and isinstance(lhs.sub, ReqPower)
                ):
                    name = lhs.sub.power
                    negate = True
                else:
                    raise ValueError(
                        f"Invalid token name:\n{ast.dump(node.left)}"
                    )

                if sys.version_info < (3, 8):
                    if (
                        not isinstance(node.right, ast.Num)
                     or not isinstance(node.right.n, int)
                    ):
                        raise ValueError(
                            f"Invalid token count:\n{ast.dump(node.right)}"
                        )

                    n = node.right.n
                else:
                    if (
                        not isinstance(node.right, ast.Constant)
                     or not isinstance(node.right.value, int)
                    ):
                        raise ValueError(
                            f"Invalid token count:\n{ast.dump(node.right)}"
                        )

                    n = node.right.value

                if negate:
                    return ReqNot(ReqTokens(name, n))
                else:
                    return ReqTokens(name, n)

            else:
                raise ValueError(
                    f"Invalid operator type for requirement:"
                    f" {type(node.op)}"
                )

        elif isinstance(node, ast.Name):
            # variable names are interpreted as power names (with '*'
            # the bin-op level will convert to a token name).
            if node.id == 'X':
                return ReqImpossible()
            elif node.id == 'O':
                return ReqNothing()
            else:
                return ReqPower(node.id)

        elif isinstance(node, AstStrNode):
            # Quoted strings can be used to name powers that aren't
            # valid Python identifiers
            if sys.version_info < (3, 8):
                name = node.s
            else:
                name = node.value

            if not isinstance(name, str):
                raise ValueError(
                    f"Invalid value for requirement: '{name}'."
                )

            return ReqPower(name)

        else:
            raise ValueError(
                f"Invalid AST node for requirement:\n{ast.dump(node)}"
            )


class ReqAny(Requirement):
    """
    A disjunction requirement satisfied when any one of its
    sub-requirements is satisfied.
    """
    def __init__(self, subs: Iterable[Requirement]) -> None:
        self.subs = list(subs)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqAny) and other.subs == self.subs

    def __repr__(self):
        return "ReqAny(" + repr(self.subs) + ")"

    def satisfied(self, state: State) -> bool:
        """
        True as long as any one of the sub-requirements is satisfied.
        """
        return any(sub.satisfied(state) for sub in self.subs)


class ReqAll(Requirement):
    """
    A conjunction requirement satisfied when all of its sub-requirements
    are satisfied.
    """
    def __init__(self, subs: Iterable[Requirement]) -> None:
        self.subs = list(subs)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqAll) and other.subs == self.subs

    def __repr__(self):
        return "ReqAll(" + repr(self.subs) + ")"

    def satisfied(self, state: State) -> bool:
        """
        True as long as all of the sub-requirements are satisfied.
        """
        return all(sub.satisfied(state) for sub in self.subs)


class ReqNot(Requirement):
    """
    A negation requirement satisfied when its sub-requirement is NOT
    satisfied.
    """
    def __init__(self, sub: Requirement) -> None:
        self.sub = sub

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqNot) and other.sub == self.sub

    def __repr__(self):
        return "ReqNot(" + repr(self.sub) + ")"

    def satisfied(self, state: State) -> bool:
        """
        True as long as the sub-requirement is not satisfied.
        """
        return not self.sub.satisfied(state)


class ReqPower(Requirement):
    """
    A power requirement satisfied if the specified power is possessed by
    the player according to the given state.
    """
    def __init__(self, power: Power) -> None:
        self.power = power

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqPower) and other.power == self.power

    def __repr__(self):
        return "ReqPower(" + repr(self.power) + ")"

    def satisfied(self, state: State) -> bool:
        return self.power in state["powers"]


class ReqTokens(Requirement):
    """
    A token requirement satisfied if the player possesses at least a
    certain number of a given type of token.

    Note that checking the satisfaction of individual doors in a specific
    state is not enough to guarantee they're jointly traversable, since
    if a series of doors requires the same kind of token, further logic
    is needed to understand that as the tokens get used up, their
    requirements may no longer be satisfied.
    """
    def __init__(self, tokenType: Token, cost: int) -> None:
        self.tokenType = tokenType
        self.cost = cost

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, ReqTokens)
        and other.tokenType == self.tokenType
        and other.cost == self.cost
        )

    def __repr__(self):
        return f"ReqTokens({repr(self.tokenType)}, {repr(self.cost)})"

    def satisfied(self, state: State) -> bool:
        return (
            state.setdefault('tokens', {}).get(self.tokenType, 0)
         >= self.cost
        )


class ReqNothing(Requirement):
    """
    A requirement representing that something doesn't actually have a
    requirement. This requirement is always satisfied.
    """
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqNothing)

    def __repr__(self):
        return "ReqNothing()"

    def satisfied(self, state: State) -> bool:
        return True


class ReqImpossible(Requirement):
    """
    A requirement representing that something is impossible. This
    requirement is never satisfied.
    """
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqImpossible)

    def __repr__(self):
        return "ReqImpossible()"

    def satisfied(self, state: State) -> bool:
        return False


class TransitionEffects(TypedDict):
    """
    Represents the effects of a transition on the decision graph and/or
    game state. Can represent the following changes:

    - `'gain'`: a list of `Power`s or (`Token`, amount) pairs
        indicating powers and/or tokens gained.
    - `'lose'`: a list of `Power`s or (`Token`, amount) pairs
        indicating powers and/or tokens lost/spent.
    - `'alters'`: a list of (decision, transition, requirement-string)
        tuples indicating updated requirements for certain
        transitions, which can include removing requirements if None
        is used as the third element.
    - `'tags'`: a list of (decision, taglist) and/or (decision,
        transition, taglist) tuples where the taglist is a list of
        strings each starting with '+' or '-' indicating tags to
        remove or add to that decision or transition.
    - `'next'`: an optional dictionary with all of the same keys,
        including `'next'`, that will replace the original effects once
        the transition's effects have been applied. If None, the effects
        will be discarded once triggered, unless `'cycle'` is set to
        `True`, in which case the effects will remain as-is.
    - `'cycle'`: a boolean indicating whether, once these effects are
        replaced by the `'next'` effects, they should be added as
        `'next'` effects to the current final set of effects in the
        `'next'` chain. If not, once replaced they will be deleted.
    """
    gain: List[Union[Power, Tuple[Token, int]]]
    lose: List[Union[Power, Tuple[Token, int]]]
    alters: List[Tuple[Decision, Transition, Optional[str]]]
    tags: List[
        Union[
            Tuple[Decision, List[str]],
            Tuple[Decision, Transition, List[str]]
        ]
    ]
    next: Any # Support for recursive types when?
    cycle: bool


def mergeEffects(
    a: TransitionEffects,
    b: TransitionEffects
) -> TransitionEffects:
    """
    Merges two transition effects dictionaries according to the
    following rules:
    1. The `gain`, `lose`, and `alters` lists are concatenated, with the
        entries from the first effects object appearing first.
    2. For each decision or transition which includes tags
        added/removed that appears in both effects, those tag lists
        are merged (note that this may result in a tag list which
        applies and then removes a tag, or vice versa, so order
        matters).
    3. The `next` values are merged recursively.
    4. If either effect cycles, the merged effect will too.

    Note that because the next/cycle fields cannot be easily merged,
    this will distort complex effects!

    TODO: Truly modular effects system...
    """
    result: TransitionEffects = {
        'gain': a['gain'] + b['gain'],
        'lose': a['lose'] + b['lose'],
        'alters': a['alters'] + b['alters'],
        'tags': [],
        'next': None,
        'cycle': a['cycle'] or b['cycle']
    }

    # Merge tags: first map tags of b, then add those to spots in a
    bTagMap: Dict[
        Union[Decision, Tuple[Decision, Transition]],
        List[str]
    ] = {}
    for tagIt in b['tags']:
        if len(tagIt) == 2:
            tagIt = cast(Tuple[Decision, List[str]], tagIt)
            bTagMap[tagIt[0]] = tagIt[1]
        else: # length must be 3
            tagIt = cast(Tuple[Decision, Transition, List[str]], tagIt)
            bTagMap[tagIt[0:2]] = tagIt[2]

    # Track what we've seen so we can add extras
    seen: Set[Union[Decision, Tuple[Decision, Transition]]] = set()
    for tagIt in a['tags']:
        if len(tagIt) == 2:
            tagIt = cast(Tuple[Decision, List[str]], tagIt)
            if tagIt[0] in bTagMap:
                result['tags'].append(
                    (tagIt[0], tagIt[1] + bTagMap[tagIt[0]])
                )
                seen.add(tagIt[0])
        else: # length must be 3
            tagIt = cast(Tuple[Decision, Transition, List[str]], tagIt)
            if tagIt[0:2] in bTagMap:
                result['tags'].append(
                    (tagIt[0], tagIt[1], tagIt[2] + bTagMap[tagIt[0:2]])
                )
                seen.add(tagIt[0:2])

    # Add leftovers that don't need merging
    for key in bTagMap:
        if key not in seen:
            if isinstance(key, tuple):
                result['tags'].append((key[0], key[1], bTagMap[key]))
            else:
                result['tags'].append((key, bTagMap[key]))

    # Merge next fields recursively, or take unique next
    if a['next'] is None:
        result['next'] = b['next']
    elif b['next'] is None:
        result['next'] = a['next']
    else:
        result['next'] = mergeEffects(a['next'], b['next'])

    return result


def effects(
    gain: Optional[List[Union[Power, Tuple[Token, int]]]] = None,
    lose: Optional[List[Union[Power, Tuple[Token, int]]]] = None,
    alters: Optional[
        List[Tuple[Decision, Transition, Optional[str]]]
    ] = None,
    tags: Optional[List[Union[
        Tuple[Decision, List[str]],
        Tuple[Decision, Transition, List[str]]
    ]]] = None,
    next: Optional[TransitionEffects] = None,
    cycle: bool = False
) -> TransitionEffects:
    """
    Factory for transition effects which includes default values so you
    can just specify effect types that are relevant to a particular
    situation.
    """
    if gain is None:
        gain = []

    if lose is None:
        lose = []

    if alters is None:
        alters = []

    if tags is None:
        tags = []

    return {
        'gain': gain,
        'lose': lose,
        'alters': alters,
        'tags': tags,
        'next': next,
        'cycle': cycle
    }


class TransitionProperties(TypedDict):
    """
    Represents bundled properties of a transition, including a
    requirement, effects, tags, and/or annotations. Does not include the
    reciprocal. Has the following slots:

    - `'requirement'`: The requirement for the transition. This is
        always a `Requirement`, although it might be `ReqNothing` if
        nothing special is required.
    - `'effects'`: The effects of the transition.
    - `'tags'`: Any tags applied to the transition.
    - `'annotations'`: A list of annotations applied to the transition.
    """
    requirement: Requirement
    effects: TransitionEffects
    tags: Set[Tag]
    annotations: List[Annotation]


def mergeProperties(
    a: Optional[TransitionProperties],
    b: Optional[TransitionProperties]
) -> TransitionProperties:
    """
    Merges two sets of transition properties, following these rules:

    1. Tags and annotations are combined. Annotations from the
        second property set are ordered after those from the first.
    2. If one of the transitions has a `ReqNothing` instance as its
        requirement, we use the other requirement. If both have
        complex requirements, we create a new `ReqAll` which
        combines them as the requirement.
    3. The effects are merged using `mergeEffects`. Note that this can
        seriously change how effects operate (TODO: Fix that)

    If either transition is `None`, then a deep copy of the other is
    returned. If both are `None`, then an empty transition properties
    dictionary is returned, with `ReqNothing` as the requirement, no
    effects, no tags, and no annotations.
    """
    if a is None:
        if b is None:
            return {
                "requirement": ReqNothing(),
                "effects": effects(),
                "tags": set(),
                "annotations": []
            }
        else:
            return copy.deepcopy(b)
    elif b is None:
        return copy.deepcopy(a)
    # implicitly neither a or b is None below

    result: TransitionProperties = {
        "requirement": ReqNothing(),
        "effects": mergeEffects(a["effects"], b["effects"]),
        "tags": a["tags"] | b["tags"],
        "annotations": a["annotations"] + b["annotations"],
    }

    if a["requirement"] == ReqNothing():
        result["requirement"] = b["requirement"]
    elif b["requirement"] == ReqNothing():
        result["requirement"] = a["requirement"]
    else:
        result["requirement"] = ReqAll(
            [a["requirement"], b["requirement"]]
        )

    return result


RANDOM_NAME_SUFFIXES = False
"""
Causes `uniqueName` to use random suffixes instead of sequential ones,
which is more efficient when many name collisions are expected but which
makes things harder to test and debug. False by default.
"""


def uniqueName(base: str, existing: Collection) -> str:
    """
    Finds a unique name relative to a collection of existing names,
    using the given base name, plus a unique suffix if that base name is
    among the existing names. If the base name isn't among the existing
    names, just returns the base name. The suffix consists of a period
    followed by a number, and the lowest unused number is used every
    time. This does lead to poor performance in cases where many
    collisions are expected; you can set `RANDOM_NAME_SUFFIXES` to True
    to use a random suffix instead.

    Note that if the base name already has a numerical suffix, that
    suffix will be changed instead of adding another one.
    """
    # Short-circuit if we're already unique
    if base not in existing:
        return base

    # Ensure a digit suffix
    if (
        '.' not in base
     or not base.split('.')[-1].isdigit()
    ):
        base += '.1'

    # Find the split point for the suffix
    # This will be the index after the '.'
    splitPoint = len(base) - list(reversed(base)).index('.')
    if not RANDOM_NAME_SUFFIXES:
        suffix = int(base[splitPoint:])

    while base in existing:
        if RANDOM_NAME_SUFFIXES:
            base = base[:splitPoint] + str(random.randint(0, 1000000))
        else:
            suffix += 1
            base = base[:splitPoint] + str(suffix)

    return base


class DecisionGraph(graphs.UniqueExitsGraph[Decision, Transition]):
    """
    Represents a view of the world as a topological graph at a moment in
    time. It derives from `networkx.MultiDiGraph`.

    Each node (a `Decision`) represents a place in the world where there
    are multiple opportunities for travel/action, or a dead end where
    you must turn around and go back; typically this is a single room in
    a game, but sometimes one room has multiple decision points. Edges
    (`Transition`s) represent choices that can be made to travel to
    other decision points (e.g., taking the left door), or when they are
    self-edges, they represent actions that can be taken within a
    location that affect the world or the game state.

    Each `Transition` includes a `TransitionEffects` dictionary
    indicating the effects that it has. Other effects of the transition
    that are not simple enough to be included in this format may be
    represented in an `Exploration` by changing the graph in the next step
    to reflect further effects of a transition.

    In addition to normal transitions between decisions, a
    `DecisionGraph` can represent potential transitions which lead to
    unknown destinations. These are represented by adding decisions with
    the `'unknown'` tag (whose names where not specified begin with
    `'_u.'`) with a separate unknown decision for each transition
    (although where it's known that two transitions lead to the same
    unknown region, this can be represented as well).

    Both nodes and edges can have `Annotation`s associated with them that
    include extra details about the explorer's perception of the
    situation. They can also have `Tag`s, which represent specific
    categories a transition or decision falls into.

    Nodes can also be part of one or more `Zones`, and zones can also be
    part of other zones, allowing for a hierarchical description of the
    underlying space.
    """
    def __init__(self) -> None:
        super().__init__()
        self.zones = {}
        self.unknownCount = 0

    def decisionActions(self, decision: Decision) -> Set[Transition]:
        """
        Retrieves the set of self-edges at a decision. Editing the set
        will not affect the graph.
        """
        return set(self.edges[decision, decision])

    def getTransitionProperties(
        self,
        decision: Decision,
        transition: Transition
    ) -> TransitionProperties:
        """
        Returns a dictionary containing transition properties for the
        specified transition from the specified decision. The properties
        included are:

        - 'requirement': The requirement for the transition.
        - 'effects': Any effects of the transition.
        - 'tags': Any tags applied to the transition.
        - 'annotations': Any annotations on the transition.

        The reciprocal of the transition is not included.
        """
        return {
            'requirement':
                self.getTransitionRequirement(decision, transition),
            'effects': self.getTransitionEffects(decision, transition),
            'tags': self.transitionTags(decision, transition),
            'annotations': self.transitionAnnotations(decision, transition)
        }

    def setTransitionProperties(
        self,
        decision: Decision,
        transition: Transition,
        requirement: Optional[Requirement] = None,
        effects: Optional[TransitionEffects] = None,
        tags: Optional[Set[Tag]] = None,
        annotations: Optional[List[Annotation]] = None
    ) -> None:
        """
        Sets one or more transition properties all at once. Can be used
        to set the requirement, effects, tags, and/or annotations. Old
        values are overwritten, although if `None`s are provided (or
        arguments are omitted), corresponding properties are not updated.

        To add tags or annotations to existing tags/annotations instead
        of replacing them, use `tagTransition` or `annotateTransition`
        instead.
        """
        if requirement is not None:
            self.setTransitionRequirement(decision, transition, requirement)
        if effects is not None:
            self.setTransitionEffects(decision, transition, effects)
        if tags is not None:
            dest = self.destination(decision, transition)
            self.edges[decision, dest, transition]['tags'] = tags
        if annotations is not None:
            dest = self.destination(decision, transition)
            self.edges[decision, dest, transition]['ann'] = annotations

    def getTransitionRequirement(
        self,
        decision: Decision,
        transition: Transition
    ) -> Requirement:
        """
        Returns the `Requirement` for accessing a specific transition at
        a specific decision. For transitions which don't have
        requirements, returns a `ReqNothing` instance.
        """
        dest = self.destination(decision, transition)

        info = self.edges[decision, dest, transition]

        return info.get('requires', ReqNothing())

    def setTransitionRequirement(
        self,
        decision: Decision,
        transition: Transition,
        requirement: Union[Requirement, str, None]
    ) -> None:
        """
        Sets the `Requirement` for accessing a specific transition at
        a specific decision. Raises a `KeyError` if the decision or
        transition does not exist.

        Deletes the requirement if `None` is given as the requirement;
        if a string is provided, converts it into a `Requirement` using
        `Requirement.parse`. Does not raise an error if deletion is
        requested for a non-existent requirement, and silently
        overwrites any previous requirement.
        """
        dest = self.destination(decision, transition)

        info = self.edges[decision, dest, transition]

        if isinstance(requirement, str):
            requirement = Requirement.parse(requirement)

        if requirement is None:
            try:
                del info['requires']
            except KeyError:
                pass
        else:
            if not isinstance(requirement, Requirement):
                raise TypeError(
                    f"Invalid requirement type: {type(requirement)}"
                )

            info['requires'] = requirement

    def getTransitionEffects(
        self,
        decision: Decision,
        transition: Transition
    ) -> TransitionEffects:
        """
        Retrieves the effects of a transition.

        A `KeyError` is raised if the specified decision/transition
        combination doesn't exist.
        """
        dest = self.destination(decision, transition)

        info = self.edges[decision, dest, transition]

        # Making this explicit allows type-checking it
        default: TransitionEffects = effects()

        return info.get('effects', default)

    def setTransitionEffects(
        self,
        decision: Decision,
        transition: Transition,
        effects: TransitionEffects
    ) -> None:
        """
        Replaces the transition effects for the given transition at the
        given decision. Any previous effects are discarded. See
        `TransitionEffects` for the structure of these. Note that for
        this method, a string can be given in place of a `Requirement`
        and it will be converted using `Requirement.parse`. If `None` is
        given as the requirement, the requirement will not be changed,
        to remove the requirement, explicitly provide a `ReqNothing`
        instance as the `requires` value.

        A `KeyError` is raised if the specified decision/transition
        combination doesn't exist.
        """
        dest = self.destination(decision, transition)

        info = self.edges[decision, dest, transition]

        info['effects'] = effects

    def addAction(
        self,
        decision: Decision,
        action: Transition,
        requires: Union[Requirement, str, None] = None,
        effects: Optional[TransitionEffects] = None
    ) -> None:
        """
        Adds the given action as a possibility at the given decision. An
        action is just a self-edge, which can have requirements like any
        edge, and which can have effects like any edge.
        The optional arguments are given to `setTransitionRequirement`
        and `setTransitionEffects`; see those functions for descriptions
        of what they mean.

        Raises a `KeyError` if a transition with the given name already
        exists at the given decision.
        """
        self.add_edge(decision, decision, action)
        self.setTransitionRequirement(decision, action, requires)
        if effects is not None:
            self.setTransitionEffects(decision, action, effects)

    def tagDecision(
        self,
        decision: Decision,
        tagOrTags: Union[Tag, Set[Tag]]
    ) -> None:
        """
        Adds a tag (or many tags from a set of tags) to a decision.
        """
        if isinstance(tagOrTags, Tag):
            tagOrTags = {tagOrTags}

        tagsAlready = self.nodes[decision].setdefault('tags', set())
        for tag in tagOrTags:
            tagsAlready.add(tag)

    def untagDecision(self, decision: Decision, tag: Tag) -> bool:
        """
        Removes a tag from a decision. Returns `True` if the tag was
        present and got removed, or `False` if the tag wasn't present.
        """
        target = self.nodes[decision]['tags']
        try:
            target.remove(tag)
            return True
        except KeyError:
            return False

    def decisionTags(self, decision: Decision) -> Set[Tag]:
        """
        Returns the set of tags for a decision. Edits will be applied to
        the graph.
        """
        return self.nodes[decision]['tags']

    def annotateDecision(
        self,
        decision: Decision,
        annotationOrAnnotations: Union[Annotation, Sequence[Annotation]]
    ) -> None:
        """
        Adds an annotation to a decision's annotations list.
        """
        if isinstance(annotationOrAnnotations, Annotation):
            annotationOrAnnotations = [annotationOrAnnotations]
        self.nodes[decision]['ann'].extend(annotationOrAnnotations)

    def decisionAnnotations(self, decision: Decision) -> List[Annotation]:
        """
        Returns the list of annotations for the specified decision.
        Modifying the list affects the graph.
        """
        return self.nodes[decision]['ann']

    def tagTransition(
        self,
        decision: Decision,
        transition: Transition,
        tagOrTags: Union[Tag, Set[Tag]]
    ) -> None:
        """
        Adds a tag (or each tag from a set) to a transition coming out of
        a specific decision.
        """
        dest = self.destination(decision, transition)
        if isinstance(tagOrTags, Tag):
            tagOrTags = {tagOrTags}

        tagsAlready = self.edges[decision, dest, transition].setdefault(
            'tags',
            set()
        )
        for tag in tagOrTags:
            tagsAlready.add(tag)

    def untagTransition(
        self,
        decision: Decision,
        transition: Transition,
        tagOrTags: Union[Tag, Set[Tag]]
    ) -> None:
        """
        Removes a tag (or each tag in a set) from a transition coming out
        of a specific decision. Raises a `KeyError` if (one of) the
        specified tag(s) is not currently applied to the specified
        transition.
        """
        dest = self.destination(decision, transition)
        if isinstance(tagOrTags, Tag):
            tagOrTags = {tagOrTags}

        tagsAlready = self.edges[decision, dest, transition].setdefault(
            'tags',
            set()
        )
        for tag in tagOrTags:
            tagsAlready.remove(tag)

    def transitionTags(
        self,
        decision: Decision,
        transition: Transition
    ) -> Set[Tag]:
        """
        Returns the set of tags for a transition. Edits will be applied
        to the graph.
        """
        dest = self.destination(decision, transition)
        return self.edges[decision, dest, transition]['tags']

    def annotateTransition(
        self,
        decision: Decision,
        transition: Transition,
        annotations: Union[Annotation, Sequence[Annotation]]
    ) -> None:
        """
        Adds an annotation (or a sequence of annotations) to a
        transition's annotations list.
        """
        dest = self.destination(decision, transition)
        if isinstance(annotations, Annotation):
            annotations = [annotations]
        self.edges[decision, dest, transition]['ann'].extend(annotations)

    def transitionAnnotations(
        self,
        decision: Decision,
        transition: Transition
    ) -> List[Annotation]:
        """
        Returns the annotation list for a specific transition at a
        specific decision. Editing the list affects the graph.
        """
        dest = self.destination(decision, transition)
        return self.edges[decision, dest, transition]['ann']

    def createZone(self, zone: Zone) -> None:
        """
        Creates an empty zone with the given name. Raises a `ValueError`
        if that zone name is already in use.

        TODO: TESTS
        """
        if zone in self.zones:
            raise ValueError(f"Zone '{zone}' already exists.")
        self.zones[zone] = (set(), set())

    def hasZone(self, zone: Zone) -> bool:
        """
        Returns `True` if the specified zone exists; `False` otherwise.

        TODO: TESTS
        """
        return zone in self.zones

    def deleteZone(self, zone: Zone) -> Tuple[Set[Decision], Set[Zone]]:
        """
        Deletes the specified zone, returning a pair containing the set
        of decisions that had been in that zone followed by the set of
        sub-zones of that zone. Raises a `ValueError` if the zone in
        question does not exist.

        TODO: TESTS
        """
        if not self.hasZone(zone):
            raise ValueError(
                f"Cannot delete zone '{zone}': it does not exist."
            )
        result = self.zones[zone]
        del self.zones[zone]
        return result

    def addDecisionToZone(
        self,
        decision: Decision,
        zone: Zone
    ) -> None:
        "Adds a decision to a zone, creating the zone if necessary."
        self.zones.setdefault(zone, (set(), set()))[0].add(decision)

    def removeDecisionFromZone(
        self,
        decision: Decision,
        zone: Zone
    ) -> bool:
        """
        Removes a decision from a zone if it had been in it, returning
        True if that decision had been in that zone, and False if it was
        not in that zone, including if that zone didn't exist.

        TODO: TESTS
        """
        try:
            self.zones.get(zone, (set(), None))[0].remove(decision)
            return True
        except KeyError:
            return False

    def addZoneToZone(
        self,
        addIt: Zone,
        addTo: Zone
    ) -> None:
        """
        Adds a zone to another zone. Note that creating recursive zone
        structures may cause errors. Creates the zone to be added to if
        it doesn't exist, and creates the zone being added as an empty
        zone if it didn't exist.

        TODO: TESTS
        """
        self.zones.setdefault(addTo, (set(), set()))[1].add(addIt)
        if addIt not in self.zones:
            self.zones[addIt] = (set(), set())

    def removeZoneFromZone(
        self,
        removeIt: Zone,
        removeFrom: Zone
    ) -> bool:
        """
        Removes a zone from a zone if it had been in it, returning True
        if that zone had been in that zone, and False if it was not in
        that zone, including if that zone did not exist.

        TODO: TESTS
        """
        try:
            self.zones.get(
                removeFrom,
                (None, set())
            )[1].remove(removeIt)
            return True
        except KeyError:
            return False

    def allDecisionsInZone(self, zone: Zone) -> Optional[Set[Decision]]:
        """
        Returns a set containing all decisions in the given zone,
        including those included via sub-zones. Returns `None` for a
        zone that has not been created.

        TODO: TESTS
        """
        result = set()
        if not self.hasZone(zone):
            return None
        included, subZones = self.zones[zone]
        result |= included
        for subZone in subZones:
            result |= self.allDecisionsInZone(subZone)

        return result

    def zoneEdges(self, zone: Zone) -> Tuple[
        Set[Tuple[Decision, Transition]],
        Set[Tuple[Decision, Transition]]
    ]:
        """
        Given a zone to look at, finds all of the transitions which go
        out of and into that zone, ignoring internal transitions between
        decisions in the zone. This includes all decisions in sub-zones.

        Returns `None` if the target zone doesn't exist.

        TODO: TESTS
        """
        interior = self.allDecisionsInZone(zone)
        if interior is None:
            return None

        # TODO: HERE

    def getReciprocal(
        self,
        decision: Decision,
        transition: Transition
    ) -> Optional[Transition]:
        """
        Returns the reciprocal edge for the specified transition from the
        specified decision (see `setReciprocal`). Returns
        `None` if no reciprocal has been established for that
        transition, or if that decision or transition does not exist.
        """
        dest = self.getDestination(decision, transition)
        if dest is not None:
            return self.edges[decision, dest, transition].get("reciprocal")
        else:
            return None

    def setReciprocal(
        self,
        decision: Decision,
        transition: Transition,
        reciprocal: Optional[Transition],
        setBoth: bool = True,
        cleanup: bool = True
    ) -> None:
        """
        Sets the 'reciprocal' transition for a particular transition from
        a particular decision, and removes the reciprocal property from
        any old reciprocal transition.

        Raises a `KeyError` if the specified decision or transition does
        not exist.

        Raises a `ValueError` if the reciprocal transition does not
        exist, or if it does exist but does not lead back to the
        decision the transition came from.

        If `setBoth` is True (the default) then the transition which is
        being identified as a reciprocal will also have its reciprocal
        property set, pointing back to the primary transition being
        modified, and any old reciprocal of that transition will have its
        reciprocal set to None. If you want to create a situation with
        non-exclusive reciprocals, use `setBoth=False`.

        If `cleanup` is True (the default) then abandoned reciprocal
        transitions (for both edges if `setBoth` was true) have their
        reciprocal properties removed. Set `cleanup` to false if you want
        to retain them, although this will result in non-exclusive
        reciprocal relationships.

        If the `reciprocal` value is None, this deletes the reciprocal
        value entirely, and if `setBoth` is true, it does this for the
        previous reciprocal edge as well. No error is raised in this case
        when there was not already a reciprocal to delete. No
        `ValueError`s will be raised in this case either.

        Note that one should remove a reciprocal relationship before
        redirecting either edge of the pair in a way that gives it a new
        reciprocal, since otherwise, a later attempt to remove the
        reciprocal with `setBoth` set to True (the default) will end up
        deleting the reciprocal information from the other edge that was
        already modified. There is no way to reliably detect and avoid
        this, because two different decisions could (and often do in
        practice) have transitions with identical names, meaning that the
        reciprocal value will still be the same, but it will indicate a
        different edge in virtue of the destination of the edge changing.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('G')
        >>> g.addDecision('H')
        >>> g.addDecision('I')
        >>> g.addTransition('G', 'up', 'H', 'down')
        >>> g.addTransition('G', 'next', 'H', 'prev')
        >>> g.addTransition('H', 'next', 'I', 'prev')
        >>> g.addTransition('H', 'return', 'G')
        >>> g.setReciprocal('G', 'up', 'next') # Error w/ destinations
        Traceback (most recent call last):
        ...
        ValueError...
        >>> g.setReciprocal('G', 'up', 'none') # Doesn't exist
        Traceback (most recent call last):
        ...
        ValueError...
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') is None
        True
        >>> g.setReciprocal('G', 'up', 'return')
        >>> g.getReciprocal('G', 'up')
        'return'
        >>> g.getReciprocal('H', 'down') is None
        True
        >>> g.getReciprocal('H', 'return')
        'up'
        >>> g.setReciprocal('H', 'return', None) # remove the reciprocal
        >>> g.getReciprocal('G', 'up') is None
        True
        >>> g.getReciprocal('H', 'down') is None
        True
        >>> g.getReciprocal('H', 'return') is None
        True
        >>> g.setReciprocal('G', 'up', 'down', setBoth=False) # one-way
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down') is None
        True
        >>> g.getReciprocal('H', 'return') is None
        True
        >>> g.setReciprocal('H', 'return', 'up', setBoth=False) # non-symmetric
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down') is None
        True
        >>> g.getReciprocal('H', 'return')
        'up'
        >>> g.setReciprocal('H', 'down', 'up') # setBoth not needed
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') # unchanged
        'up'
        >>> g.setReciprocal('G', 'up', 'return', cleanup=False) # no cleanup
        >>> g.getReciprocal('G', 'up')
        'return'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') # unchanged
        'up'
        >>> # Cleanup only applies to reciprocal if setBoth is true
        >>> g.setReciprocal('H', 'down', 'up', setBoth=False)
        >>> g.getReciprocal('G', 'up')
        'return'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') # not cleaned up w/out setBoth
        'up'
        >>> g.setReciprocal('H', 'down', 'up') # with cleanup and setBoth
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') is None # cleaned up
        True
        """
        dest = self.destination(decision, transition) # possible KeyError
        if reciprocal is None:
            rDest = None
        else:
            rDest = self.getDestination(dest, reciprocal)

        # Set or delete reciprocal property
        if reciprocal is None:
            # Delete the property
            old = self.edges[decision, dest, transition].pop('reciprocal')
            if setBoth and self.getDestination(dest, old) is not None:
                # Note this happens even if rDest is != destination!
                del self.edges[dest, decision, old]['reciprocal']
        else:
            # Set the property, checking for errors first
            if rDest is None:
                raise ValueError(
                    f"Reciprocal transition '{reciprocal}' for"
                    f" transition '{transition}' from decision"
                    f" '{decision}' does not exist in decision"
                    f" '{dest}'."
                )

            if rDest != decision:
                raise ValueError(
                    f"Reciprocal transition '{reciprocal}' from"
                    f" decision '{dest}' does not lead back to decision"
                    f" '{decision}'."
                )

            eProps = self.edges[decision, dest, transition]
            abandoned = eProps.get('reciprocal')
            eProps['reciprocal'] = reciprocal
            if cleanup and abandoned not in (None, reciprocal):
                del self.edges[dest, decision, abandoned]['reciprocal']

            if setBoth:
                rProps = self.edges[dest, decision, reciprocal]
                revAbandoned = rProps.get('reciprocal')
                rProps['reciprocal'] = transition
                # Sever old reciprocal relationship
                if cleanup and revAbandoned not in (None, transition):
                    raProps = self.edges[decision, dest, revAbandoned]
                    del raProps['reciprocal']

    def isUnknown(self, decision: Decision) -> bool:
        """
        Returns True if the specified decision is an 'unknown' decision
        (i.e., if has the 'unknown' tag) and False otherwise. These
        decisions represent unknown territory rather than a real visited
        part of the graph, although their names may be known already and
        some of their properties may be known.
        """
        return 'unknown' in self.decisionTags(decision)

    def addDecision(
        self,
        name: Decision,
        tags: Optional[Set[Tag]] = None,
        annotations: Optional[List[Annotation]] = None
    ) -> None:
        """
        Adds a decision to the graph, without any transitions yet. Each
        decision needs a unique name. A set of tags and/or a list of
        annotations (strings in both cases) may be provided.

        Raises a ValueError if a decision with the provided name already
        exists (decision names must be unique).
        """
        # Defaults
        if tags is None:
            tags = set()
        if annotations is None:
            annotations = []

        # Error checking
        if name in self:
            raise ValueError(
                f"Cannot add decision '{name}': That decision already"
                f" exists."
            )

        # Add the decision
        self.add_node(name, tags=tags, ann=annotations)

    def addTransition(
        self,
        fromDecision: Decision,
        name: Transition,
        toDecision: Decision,
        revName: Optional[Transition] = None,
        tags: Optional[Set[Tag]] = None,
        annotations: Optional[List[Annotation]] = None,
        revTags: Optional[Set[Tag]] = None,
        revAnnotations: Optional[List[Annotation]] = None,
        requires: Union[Requirement, str, None] = None,
        effects: Optional[TransitionEffects] = None,
        revRequires: Union[Requirement, str, None] = None,
        revEffects: Optional[TransitionEffects] = None
    ) -> None:
        """
        Adds a transition connecting two decisions. The name of each
        decision is required, as is a name for the transition. If a
        `revName` is provided, a reciprocal edge will be added in the
        opposite direction using that name; by default only the specified
        edge is added. A `KeyError` will be raised if the `revName`
        matches the name of an existing edge at the destination decision.

        Both decisions must already exist, or a `ValueError` will be
        raised.

        A set of tags and/or a list of annotations (strings in both
        cases) may be provided. Tags and/or annotations for the reverse
        edge may also be specified if one is being added.

        The `requires`, `effects`, `revRequires`, and `revEffects`
        arguments specify requirements and/or effects of the new outgoing
        and reciprocal edges.
        """
        # Defaults
        if tags is None:
            tags = set()
        if annotations is None:
            annotations = []
        if revTags is None:
            revTags = set()
        if revAnnotations is None:
            revAnnotations = []

        # Error checking
        if fromDecision not in self:
            raise ValueError(
                f"Cannot add a transition from '{fromDecision}' to"
                f" '{toDecision}': '{fromDecision}' does not exist."
            )

        if toDecision not in self:
            raise ValueError(
                f"Cannot add a transition from '{fromDecision}' to"
                f" '{toDecision}': '{toDecision}' does not exist."
            )

        # Note: have to check this first so we don't add the forward edge
        # and then error out after a side effect!
        if (
            revName is not None
        and self.getDestination(toDecision, revName) is not None
        ):
            raise KeyError(
                f"Cannot add a transition from '{fromDecision}' to"
                f" '{toDecision}' with reciprocal edge '{revName}':"
                f" '{revName}' is already used as an edge name at"
                f" '{toDecision}'."
            )

        # Add the edge
        self.add_edge(
            fromDecision,
            toDecision,
            key=name,
            tags=tags,
            ann=annotations
        )
        self.setTransitionRequirement(fromDecision, name, requires)
        if effects is not None:
            self.setTransitionEffects(fromDecision, name, effects)
        if revName is not None:
            # Add the reciprocal edge
            self.add_edge(
                toDecision,
                fromDecision,
                key=revName,
                tags=revTags,
                ann=revAnnotations
            )
            self.setReciprocal(fromDecision, name, revName)
            self.setTransitionRequirement(toDecision, revName, revRequires)
            if revEffects is not None:
                self.setTransitionEffects(toDecision, revName, revEffects)

    def removeTransition(
        self,
        fromDecision: Decision,
        transition: Transition,
        removeReciprocal=False
    ) -> Union[
        TransitionProperties,
        Tuple[TransitionProperties, TransitionProperties]
    ]:
        """
        Removes a transition. If `removeReciprocal` is true (False is the
        default) any reciprocal transition will also be removed (but no
        error will occur if there wasn't a reciprocal).

        For each removed transition, *every* transition that targeted
        that transition as its reciprocal will have its reciprocal set to
        `None`, to avoid leaving any invalid reciprocal values.

        Raises a `KeyError` if either the target decision or the target
        transition does not exist.

        Returns a transition properties dictionary with the properties
        of the removed transition, or if `removeReciprocal` is true,
        returns a pair of such dictionaries for the target transition
        and its reciprocal.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        >>> g.addDecision('B')
        >>> g.addTransition('A', 'up', 'B', 'down', tags={'wide'})
        >>> g.addTransition('A', 'in', 'B', 'out') # we won't touch this
        >>> g.addTransition('A', 'next', 'B')
        >>> g.setReciprocal('A', 'next', 'down', setBoth=False)
        >>> p = g.removeTransition('A', 'up')
        >>> p['tags']
        {'wide'}
        >>> g.destinationsFrom('A')
        {'in': 'B', 'next': 'B'}
        >>> g.destinationsFrom('B')
        {'down': 'A', 'out': 'A'}
        >>> g.getReciprocal('B', 'down') is None
        True
        >>> g.getReciprocal('A', 'next') # Asymmetrical left over
        'down'
        >>> g.getReciprocal('A', 'in') # not affected
        'out'
        >>> g.getReciprocal('B', 'out') # not affected
        'in'
        >>> # Now with removeReciprocal set to True
        >>> g.addTransition('A', 'up', 'B') # add this back in
        >>> g.setReciprocal('A', 'up', 'down') # sets both
        >>> p = g.removeTransition('A', 'up', removeReciprocal=True)
        >>> g.destinationsFrom('A')
        {'in': 'B', 'next': 'B'}
        >>> g.destinationsFrom('B')
        {'out': 'A'}
        >>> g.getReciprocal('A', 'next') is None
        True
        >>> g.getReciprocal('A', 'in') # not affected
        'out'
        >>> g.getReciprocal('B', 'out') # not affected
        'in'
        >>> g.removeTransition('A', 'none')
        Traceback (most recent call last):
        ...
        KeyError...
        >>> g.removeTransition('Z', 'nope')
        Traceback (most recent call last):
        ...
        KeyError...
        """
        # raises if either is missing:
        destination = self.destination(fromDecision, transition)
        reciprocal = self.getReciprocal(fromDecision, transition)

        # Get dictionaries of parallel & antiparallel edges to be
        # checked for invalid reciprocals after removing edges
        # Note: these will update live as we remove edges
        allAntiparallel = self[destination][fromDecision]
        allParallel = self[fromDecision][destination]

        # Remove the target edge
        fProps = self.getTransitionProperties(fromDecision, transition)
        self.remove_edge(fromDecision, destination, transition)

        # Clean up any dangling reciprocal values
        for tProps in allAntiparallel.values():
            if tProps.get('reciprocal') == transition:
                del tProps['reciprocal']

        # Remove the reciprocal if requested
        if removeReciprocal and reciprocal is not None:
            rProps = self.getTransitionProperties(destination, reciprocal)
            self.remove_edge(destination, fromDecision, reciprocal)

            # Clean up any dangling reciprocal values
            for tProps in allParallel.values():
                if tProps.get('reciprocal') == reciprocal:
                    del tProps['reciprocal']

            return (fProps, rProps)
        else:
            return fProps

    def addUnexploredEdge(
        self,
        fromDecision: Decision,
        name: Transition,
        destinationName: Optional[Decision] = None,
        reciprocal: Optional[Transition] = 'return',
        tags: Optional[Set[Tag]] = None,
        annotations: Optional[List[Annotation]] = None,
        revTags: Optional[Set[Tag]] = None,
        revAnnotations: Optional[List[Annotation]] = None,
        requires: Union[Requirement, str, None] = None,
        effects: Optional[TransitionEffects] = None,
        revRequires: Union[Requirement, str, None] = None,
        revEffects: Optional[TransitionEffects] = None
    ) -> Decision:
        """
        Adds a transition connecting to a new decision named `'_u.-n-'`
        where '-n-' is the number of unknown decisions (named or not)
        that have ever been created in this graph (or using the
        specified destination name if one is provided). This represents
        a transition to an unknown destination. Also adds a reciprocal
        transition in the reverse direction, unless `reciprocal` is set
        to `None`. The reciprocal will use provided name (default is
        'return').

        The name of the decision that was created is returned.

        A `KeyError` will be raised if the starting decision does not
        exist, if it exists but already has a transition with the given
        name, or if a decision with the specified destination name
        already exists (won't happen when using an automatic name).

        Lists of tags and/or annotations (strings in both cases) may be
        provided. These may also be provided for the reciprocal edge.
        The created node will always be tagged with `'unknown'`.

        Similarly, requirements and/or effects for either edge may be
        provided.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        >>> g.addUnexploredEdge('A', 'up')
        '_u.0'
        >>> g.addUnexploredEdge('A', 'right', 'B')
        'B'
        >>> g.addUnexploredEdge('A', 'down', None, 'up')
        '_u.2'
        >>> g.addUnexploredEdge(
        ...    '_u.0',
        ...    'beyond',
        ...    tags={'fast'},
        ...    revTags={'slow'},
        ...    annotations=['comment'],
        ...    revAnnotations=['one', 'two'],
        ...    requires=ReqPower('dash'),
        ...    revRequires=ReqPower('super dash'),
        ...    effects=effects(gain=['super dash']),
        ...    revEffects=effects(lose=['super dash'])
        ... )
        '_u.3'
        >>> g.transitionTags('_u.0', 'beyond')
        {'fast'}
        >>> g.transitionAnnotations('_u.0', 'beyond')
        ['comment']
        >>> g.getTransitionRequirement('_u.0', 'beyond')
        ReqPower('dash')
        >>> e = g.getTransitionEffects('_u.0', 'beyond')
        >>> e == effects(gain=['super dash'])
        True
        >>> g.transitionTags('_u.3', 'return')
        {'slow'}
        >>> g.transitionAnnotations('_u.3', 'return')
        ['one', 'two']
        >>> g.getTransitionRequirement('_u.3', 'return')
        ReqPower('super dash')
        >>> e = g.getTransitionEffects('_u.3', 'return')
        >>> e == effects(lose=['super dash'])
        True
        """
        # Defaults
        if tags is None:
            tags = set()
        if annotations is None:
            annotations = []
        if revTags is None:
            revTags = set()
        if revAnnotations is None:
            revAnnotations = []

        # Error checking
        if fromDecision not in self:
            raise KeyError(
                f"Cannot add a new unexplored edge '{name}' to"
                f" '{fromDecision}': That decision does not exist."
            )

        if name in self.destinationsFrom(fromDecision):
            raise KeyError(
                f"Cannot add a new edge '{name}': '{fromDecision}'"
                f" already has an outgoing edge with that name."
            )

        if destinationName in self:
            raise KeyError(
                f"Cannot add a new unexplored node '{destinationName}':"
                f" A decision with that name already exists.\n(Leave"
                f" destinationName as None to use an automatic name.)"
            )

        # Create the new unexplored decision and add the edge
        if destinationName is None:
            toName = '_u.' + str(self.unknownCount)
        else:
            toName = destinationName
        self.unknownCount += 1
        self.addDecision(toName, tags={'unknown'}, annotations=[])
        self.addTransition(
            fromDecision,
            name,
            toName,
            tags=tags,
            annotations=annotations
        )
        self.setTransitionRequirement(fromDecision, name, requires)
        if effects is not None:
            self.setTransitionEffects(fromDecision, name, effects)

        # Create the reciprocal edge
        if reciprocal is not None:
            self.addTransition(
                toName,
                reciprocal,
                fromDecision,
                tags=revTags,
                annotations=revAnnotations
            )
            self.setTransitionRequirement(toName, reciprocal, revRequires)
            if revEffects is not None:
                self.setTransitionEffects(toName, reciprocal, revEffects)
            # Set as a reciprocal
            self.setReciprocal(fromDecision, name, reciprocal)

        # Return name of destination
        return toName

    def retargetTransition(
        self,
        fromDecision: Decision,
        transition: Transition,
        newDestination: Decision,
        swapReciprocal=True,
        errorOnNameColision=True
    ) -> Optional[Transition]:
        """
        Given a particular destination and a transition at that
        destination, changes that transition so that it goes to the
        specified new destination instead of wherever it was connected
        to before. If the new destination is the same as the old one, no
        changes are made.

        If `swapReciprocal` is set to True (the default) then any
        reciprocal edge at the old destination will be deleted, and a
        new reciprocal edge from the new destination with equivalent
        properties to the original reciprocal will be created, pointing
        to the origin of the specified transition. If `swapReciprocal`
        is set to False, then the reciprocal relationship with any old
        reciprocal edge will be removed, but the old reciprocal edge
        will not be changed.

        Note that if `errorOnNameColision` is True (the default), then
        if the reciprocal transition has the same name as a transition
        which already exists at the new destination node, a `ValueError`
        will be thrown. However, if it is set to False, the reciprocal
        transition will be renamed with a suffix to avoid any possible
        name collisions. Either way, the name of the reciprocal
        transition (possibly just changed) will be returned, or None if
        there was no reciprocal transition.

        ## Example

        >>> g = DecisionGraph()
        >>> for fr, to, nm in [
        ...     ('A', 'B', 'up'),
        ...     ('A', 'B', 'up2'),
        ...     ('B', 'A', 'down'),
        ...     ('B', 'B', 'self'),
        ...     ('B', 'C', 'next'),
        ...     ('C', 'B', 'prev')
        ... ]:
        ...     if fr not in g:
        ...        g.addDecision(fr)
        ...     if to not in g:
        ...         g.addDecision(to)
        ...     g.addTransition(fr, nm, to)
        >>> g.setReciprocal('A', 'up', 'down')
        >>> g.setReciprocal('B', 'next', 'prev')
        >>> g.destination('A', 'up')
        'B'
        >>> g.destination('B', 'down')
        'A'
        >>> g.retargetTransition('A', 'up', 'C')
        'down'
        >>> g.destination('A', 'up')
        'C'
        >>> g.getDestination('B', 'down') is None
        True
        >>> g.destination('C', 'down')
        'A'
        >>> g.addTransition('A', 'next', 'B')
        >>> g.addTransition('B', 'prev', 'A')
        >>> g.setReciprocal('A', 'next', 'prev')
        >>> # Can't swap a reciprocal in a way that would collide names
        >>> g.getReciprocal('C', 'prev')
        'next'
        >>> g.retargetTransition('C', 'prev', 'A')
        Traceback (most recent call last):
        ...
        ValueError...
        >>> g.retargetTransition('C', 'prev', 'A', swapReciprocal=False)
        'next'
        >>> g.destination('C', 'prev')
        'A'
        >>> g.destination('A', 'next') # not changed
        'B'
        >>> # Reciprocal relationship is severed:
        >>> g.getReciprocal('C', 'prev') is None
        True
        >>> g.getReciprocal('B', 'next') is None
        True
        >>> # Swap back so we can do another demo
        >>> g.retargetTransition('C', 'prev', 'B', swapReciprocal=False)
        >>> # Note return value was None here because there was no reciprocal
        >>> g.setReciprocal('C', 'prev', 'next')
        >>> # Swap reciprocal by renaming it
        >>> g.retargetTransition('C', 'prev', 'A', errorOnNameColision=False)
        'next.1'
        >>> g.getReciprocal('C', 'prev')
        'next.1'
        >>> g.destination('C', 'prev')
        'A'
        >>> g.destination('A', 'next.1')
        'C'
        >>> g.destination('A', 'next')
        'B'
        >>> # Note names are the same but these are from different nodes
        >>> g.getReciprocal('A', 'next')
        'prev'
        >>> g.getReciprocal('A', 'next.1')
        'prev'
        """
        # Figure out the old destination of the transition we're swapping
        oldDestination = self.destination(fromDecision, transition)
        reciprocal = self.getReciprocal(fromDecision, transition)

        # If thew new destination is the same, we don't do anything!
        if oldDestination == newDestination:
            return reciprocal

        # First figure out reciprocal business so we can error out
        # without making changes if we need to
        if swapReciprocal and reciprocal is not None:
            reciprocal = self.rebaseTransition(
                oldDestination,
                reciprocal,
                newDestination,
                swapReciprocal=False,
                errorOnNameColision=errorOnNameColision
            )

        # Handle the forward transition...
        # Find the transition properties
        tProps = self.getTransitionProperties(fromDecision, transition)

        # Delete the edge
        self.removeEdgeByKey(fromDecision, transition)

        # Add the new edge
        self.addTransition(fromDecision, transition, newDestination)

        # Reapply the transition properties
        self.setTransitionProperties(fromDecision, transition, **tProps)

        # Handle the reciprocal transition if there is one...
        if reciprocal is not None:
            if not swapReciprocal:
                # Then sever the relationship, but only if that edge
                # still exists (we might be in the middle of a rebase)
                check = self.getDestination(oldDestination, reciprocal)
                if check is not None:
                    self.setReciprocal(
                        oldDestination,
                        reciprocal,
                        None,
                        setBoth=False # Other transition was deleted already
                    )
            else:
                # Establish new reciprocal relationship
                self.setReciprocal(
                    fromDecision,
                    transition,
                    reciprocal
                )

        return reciprocal

    def rebaseTransition(
        self,
        fromDecision: Decision,
        transition: Transition,
        newBase: Decision,
        swapReciprocal=True,
        errorOnNameColision=True
    ) -> Transition:
        """
        Given a particular destination and a transition at that
        destination, changes that transition's origin to a new base
        decision. If the new source is the same as the old one, no
        changes are made.

        If `swapReciprocal` is set to True (the default) then any
        reciprocal edge at the destination will be retargeted to point
        to the new source so that it can remain a reciprocal. If
        `swapReciprocal` is set to False, then the reciprocal
        relationship with any old reciprocal edge will be removed, but
        the old reciprocal edge will not be otherwise changed.

        Note that if `errorOnNameColision` is True (the default), then
        if the transition has the same name as a transition which
        already exists at the new source node, a `ValueError` will be
        thrown. However, if it is set to False, the transition will be
        renamed with a suffix to avoid any possible name collisions.
        Either way, the (possibly new) name of the transition that was
        rebased will be returned.

        ## Example

        >>> g = DecisionGraph()
        >>> for fr, to, nm in [
        ...     ('A', 'B', 'up'),
        ...     ('A', 'B', 'up2'),
        ...     ('B', 'A', 'down'),
        ...     ('B', 'B', 'self'),
        ...     ('B', 'C', 'next'),
        ...     ('C', 'B', 'prev')
        ... ]:
        ...     if fr not in g:
        ...        g.addDecision(fr)
        ...     if to not in g:
        ...         g.addDecision(to)
        ...     g.addTransition(fr, nm, to)
        >>> g.setReciprocal('A', 'up', 'down')
        >>> g.setReciprocal('B', 'next', 'prev')
        >>> g.destination('A', 'up')
        'B'
        >>> g.destination('B', 'down')
        'A'
        >>> g.rebaseTransition('B', 'down', 'C')
        'down'
        >>> g.destination('A', 'up')
        'C'
        >>> g.getDestination('B', 'down') is None
        True
        >>> g.destination('C', 'down')
        'A'
        >>> g.addTransition('A', 'next', 'B')
        >>> g.addTransition('B', 'prev', 'A')
        >>> g.setReciprocal('A', 'next', 'prev')
        >>> # Can't rebase in a way that would collide names
        >>> g.rebaseTransition('B', 'next', 'A')
        Traceback (most recent call last):
        ...
        ValueError...
        >>> g.rebaseTransition('B', 'next', 'A', errorOnNameColision=False)
        'next.1'
        >>> g.destination('C', 'prev')
        'A'
        >>> g.destination('A', 'next') # not changed
        'B'
        >>> # Collision is avoided by renaming
        >>> g.destination('A', 'next.1')
        'C'
        >>> # Swap without reciprocal
        >>> g.getReciprocal('A', 'next.1')
        'prev'
        >>> g.getReciprocal('C', 'prev')
        'next.1'
        >>> g.rebaseTransition('A', 'next.1', 'B', swapReciprocal=False)
        'next.1'
        >>> g.getReciprocal('C', 'prev') is None
        True
        >>> g.destination('C', 'prev')
        'A'
        >>> g.getDestination('A', 'next.1') is None
        True
        >>> g.destination('A', 'next')
        'B'
        >>> g.destination('B', 'next.1')
        'C'
        >>> g.getReciprocal('B', 'next.1') is None
        True
        >>> # Rebase in a way that creates a self-edge
        >>> g.rebaseTransition('A', 'next', 'B')
        'next'
        >>> g.getDestination('A', 'next') is None
        True
        >>> g.destination('B', 'next')
        'B'
        >>> g.destination('B', 'prev') # swapped as a reciprocal
        'B'
        >>> g.getReciprocal('B', 'next') # still reciprocals
        'prev'
        >>> g.getReciprocal('B', 'prev')
        'next'
        >>> # And rebasing of a self-edge also works
        >>> g.rebaseTransition('B', 'prev', 'A')
        'prev'
        >>> g.destination('A', 'prev')
        'B'
        >>> g.destination('B', 'next')
        'A'
        >>> g.getReciprocal('B', 'next') # still reciprocals
        'prev'
        >>> g.getReciprocal('A', 'prev')
        'next'
        >>> # We've effectively reversed this edge/reciprocal pair
        >>> # by rebasing twice
        """
        # If thew new base is the same, we don't do anything!
        if newBase == fromDecision:
            return transition

        # First figure out reciprocal business so we can swap it later
        # without making changes if we need to
        destination = self.destination(fromDecision, transition)
        reciprocal = self.getReciprocal(fromDecision, transition)
        # Check for an already-deleted reciprocal
        if (
            reciprocal is not None
        and self.getDestination(destination, reciprocal) is None
        ):
            reciprocal = None

        # Handle the base swap...
        # Find the transition properties
        tProps = self.getTransitionProperties(fromDecision, transition)

        # Check for a collision
        targetDestinations = self.destinationsFrom(newBase)
        collision = transition in targetDestinations
        if collision:
            if errorOnNameColision:
                raise ValueError(
                    f"Cannot rebase transition '{transition}' from"
                    f" '{fromDecision}': it would be a duplicate"
                    f" transition name at the new base decision"
                    f" '{newBase}'."
                )
            else:
                # Figure out a good fresh name
                newName = uniqueName(
                    transition,
                    targetDestinations
                )
        else:
            newName = transition

        # Delete the edge
        self.removeEdgeByKey(fromDecision, transition)

        # Add the new edge
        self.addTransition(newBase, newName, destination)

        # Reapply the transition properties
        self.setTransitionProperties(newBase, newName, **tProps)

        # Handle the reciprocal transition if there is one...
        if reciprocal is not None:
            if not swapReciprocal:
                # Then sever the relationship
                self.setReciprocal(
                    destination,
                    reciprocal,
                    None,
                    setBoth=False # Other transition was deleted already
                )
            else:
                # Otherwise swap the reciprocal edge
                self.retargetTransition(
                    destination,
                    reciprocal,
                    newBase,
                    swapReciprocal=False
                )

                # And establish a new reciprocal relationship
                self.setReciprocal(
                    newBase,
                    newName,
                    reciprocal
                )

        # Return the new name in case it was changed
        return newName

    def mergeDecisions(
        self,
        merge: Decision,
        mergeInto: Decision,
        errorOnNameColision=True
    ) -> Dict[Transition, Transition]:
        """
        Merges two decisions, deleting the first after transferring all
        of its incoming and outgoing edges to target the second one,
        whose name is retained. If either decision does not exist, a
        `KeyError` will be raised. If `merge` and `mergeInto` are the
        same, then nothing will be changed.

        Unless `errorOnNameColision` is set to False, a `ValueError`
        will be raised if the two decisions have outgoing transitions
        with the same name. If `errorOnNameColision` is set to False,
        then such edges will be renamed using a suffix to avoid name
        collisions, with edges connected to the second decision
        retaining their original names and edges that were connected to
        the first decision getting renamed.

        The tags and annotations of the merged decision are added to the
        tags and annotations of the merge target. If this is undesired
        behavior, clear the tags/annotations of the merged decision
        before the merge.

        Returns a dictionary mapping each original transition name to
        its new name in cases where transitions get renamed; this will
        be empty when no re-naming occurs, including when
        `errorOnNameColision` is True. If there were any transitions
        connecting the nodes that were merged, these become self-edges
        of the merged node (and may be renamed if necessary).
        Note that all renamed transitions were originally based on the
        first (merged) node, since transitions of the second (merge
        target) node are not renamed.

        ## Example

        >>> g = DecisionGraph()
        >>> for fr, to, nm in [
        ...     ('A', 'B', 'up'),
        ...     ('A', 'B', 'up2'),
        ...     ('B', 'A', 'down'),
        ...     ('B', 'B', 'self'),
        ...     ('B', 'C', 'next'),
        ...     ('C', 'B', 'prev'),
        ...     ('A', 'C', 'right')
        ... ]:
        ...     if fr not in g:
        ...        g.addDecision(fr)
        ...     if to not in g:
        ...         g.addDecision(to)
        ...     g.addTransition(fr, nm, to)
        >>> g.setReciprocal('A', 'up', 'down')
        >>> g.setReciprocal('B', 'next', 'prev')
        >>> g.mergeDecisions('C', 'B')
        {}
        >>> g.destinationsFrom('A')
        {'up': 'B', 'up2': 'B', 'right': 'B'}
        >>> g.destinationsFrom('B')
        {'down': 'A', 'self': 'B', 'prev': 'B', 'next': 'B'}
        >>> 'C' in g
        False
        >>> g.mergeDecisions('A', 'A') # does nothing
        {}
        >>> # Can't merge non-existent decision
        >>> g.mergeDecisions('A', 'Z')
        Traceback (most recent call last):
        ...
        KeyError...
        >>> g.mergeDecisions('Z', 'A')
        Traceback (most recent call last):
        ...
        KeyError...
        >>> # Can't merge decisions w/ shared edge names
        >>> g.addDecision('D')
        >>> g.addTransition('D', 'next', 'A')
        >>> g.addTransition('A', 'prev', 'D')
        >>> g.setReciprocal('D', 'next', 'prev')
        >>> g.mergeDecisions('D', 'B') # both have a 'next' transition
        Traceback (most recent call last):
        ...
        ValueError...
        >>> # Auto-rename colliding edges
        >>> g.mergeDecisions('D', 'B', errorOnNameColision=False)
        {'next': 'next.1'}
        >>> g.destination('B', 'next') # merge target unchanged
        'B'
        >>> g.destination('B', 'next.1') # merged decision name changed
        'A'
        >>> g.destination('B', 'prev') # name unchanged (no collision)
        'B'
        >>> g.getReciprocal('B', 'next') # unchanged (from B)
        'prev'
        >>> g.getReciprocal('B', 'next.1') # from A
        'prev'
        >>> g.getReciprocal('A', 'prev') # from B
        'next.1'

        ## Folding four nodes into a 2-node loop

        >>> g = DecisionGraph()
        >>> g.addDecision('X')
        >>> g.addDecision('Y')
        >>> g.addTransition('X', 'next', 'Y', 'prev')
        >>> g.addDecision('preX')
        >>> g.addDecision('postY')
        >>> g.addTransition('preX', 'next', 'X', 'prev')
        >>> g.addTransition('Y', 'next', 'postY', 'prev')
        >>> g.mergeDecisions('preX', 'Y', errorOnNameColision=False)
        {'next': 'next.1'}
        >>> g.destinationsFrom('X')
        {'next': 'Y', 'prev': 'Y'}
        >>> g.destinationsFrom('Y')
        {'prev': 'X', 'next': 'postY', 'next.1': 'X'}
        >>> 'preX' in g
        False
        >>> g.destinationsFrom('postY')
        {'prev': 'Y'}
        >>> g.mergeDecisions('postY', 'X', errorOnNameColision=False)
        {'prev': 'prev.1'}
        >>> g.destinationsFrom('X')
        {'next': 'Y', 'prev': 'Y', 'prev.1': 'Y'}
        >>> g.destinationsFrom('Y') # order 'cause of 'next' re-target
        {'prev': 'X', 'next.1': 'X', 'next': 'X'}
        >>> 'preX' in g
        False
        >>> 'postY' in g
        False
        >>> # Reciprocals are tangled...
        >>> g.getReciprocal('X', 'prev')
        'next.1'
        >>> g.getReciprocal('X', 'prev.1')
        'next'
        >>> g.getReciprocal('Y', 'next')
        'prev.1'
        >>> g.getReciprocal('Y', 'next.1')
        'prev'
        >>> # Note: one merge cannot handle both extra transitions
        >>> # because their reciprocals are crossed (e.g., prev.1 <-> next)
        >>> # (It would merge both edges but the result would retain
        >>> # 'next.1' instead of retaining 'next'.)
        >>> g.mergeTransitions('X', 'prev.1', 'prev', mergeReciprocal=False)
        >>> g.mergeTransitions('Y', 'next.1', 'next', mergeReciprocal=True)
        >>> g.destinationsFrom('X')
        {'next': 'Y', 'prev': 'Y'}
        >>> g.destinationsFrom('Y')
        {'prev': 'X', 'next': 'X'}
        >>> # Reciprocals were salvaged in second merger
        >>> g.getReciprocal('X', 'prev')
        'next'
        >>> g.getReciprocal('Y', 'next')
        'prev'
        """
        # Create our result as an empty dictionary
        result: Dict[Transition, Transition] = {}

        # Short-circuit if the two decisions are the same
        if merge == mergeInto:
            return result

        # KeyErrors from here if either decision doesn't exist
        allNewOutgoing = set(self.destinationsFrom(merge))
        allOldOutgoing = set(self.destinationsFrom(mergeInto))
        # Find colliding transition names
        collisions = allNewOutgoing & allOldOutgoing
        if len(collisions) > 0 and errorOnNameColision:
            raise ValueError(
                f"Cannot merge decision '{merge}' into decision"
                f" '{mergeInto}': the decisions share {len(collisions)}"
                f" transition names: {collisions}\n(Note that"
                f" errorOnNameColision was set to True, set it to False"
                f" to allow the operation by renaming half of those"
                f" transitions.)"
            )

        # First, swap all incoming edges, along with their reciprocals
        # This will include self-edges, which will be retargeted and
        # whose reciprocals will be rebased in the process, leading to
        # the possibility of a missing edge during the loop
        for source, incoming in self.allEdgesTo(merge):
            # Skip this edge if it was already swapped away because it's
            # a self-loop with a reciprocal whose reciprocal was
            # processed earlier in the loop
            if incoming not in self.destinationsFrom(source):
                continue

            # Find corresponding outgoing edge
            outgoing = self.getReciprocal(source, incoming)

            # Swap both edges to new destination
            newOutgoing = self.retargetTransition(
                source,
                incoming,
                mergeInto,
                swapReciprocal=True,
                errorOnNameColision=False # collisions were detected above
            )
            # Add to our result if the name of the reciprocal was
            # changed
            if (
                outgoing is not None
            and newOutgoing is not None
            and outgoing != newOutgoing
            ):
                result[outgoing] = newOutgoing

        # Next, swap any remaining outgoing edges (which didn't have
        # reciprocals, or they'd already be swapped, unless they were
        # self-edges previously). Note that in this loop, there can't be
        # any self-edges remaining, although there might be connections
        # between the merging nodes that need to become self-edges
        # because they used to be a self-edge that was half-retargeted
        # by the previous loop.
        # Note: a copy is used here to avoid iterating over a changing
        # dictionary
        for stillOutgoing in copy.copy(self.destinationsFrom(merge)):
            newOutgoing = self.rebaseTransition(
                merge,
                stillOutgoing,
                mergeInto,
                swapReciprocal=True,
                errorOnNameColision=False # collisions were detected above
            )
            if stillOutgoing != newOutgoing:
                result[stillOutgoing] = newOutgoing

        # At this point, there shouldn't be any remaining incoming or
        # outgoing edges!
        assert self.degree(merge) == 0

        # Merge tags & annotations
        # Note that these operations affect the underlying graph
        destTags = self.decisionTags(mergeInto)
        destTags |= self.decisionTags(merge)
        self.decisionAnnotations(mergeInto).extend(
            self.decisionAnnotations(merge)
        )

        # Delete the old node
        self.remove_node(merge)

        return result

    def renameDecision(
        self,
        decision: Decision,
        newName: Decision
    ):
        """
        Renames a decision. Note that this actually merges the old
        decision into a newly-created decision, so it both requires a
        substantial amount of work and might invalidate some of the
        active data structures like tag or annotation views.

        Raises a `KeyError` if a decision using the new name already
        exists.
        """
        if newName in self:
            raise KeyError(
                f"Can't rename '{decision}' as '{newName}' because a"
                f" decision with that name already exists."
            )
        self.addDecision(newName, tags=set(), annotations=[])
        self.mergeDecisions(decision, newName)

    def mergeTransitions(
        self,
        fromDecision: Decision,
        merge: Transition,
        mergeInto: Transition,
        mergeReciprocal=True
    ) -> None:
        """
        Given a decision and two transitions that start at that decision,
        merges the first transition into the second transition, combining
        their transition properties (using `mergeProperties`) and
        deleting the first transition. By default any reciprocal of the
        first transition is also merged into the reciprocal of the
        second, although you can set `mergeReciprocal` to `False` to
        disable this in which case the old reciprocal will lose its
        reciprocal relationship, even if the transition that was merged
        into does not have a reciprocal.

        If the two names provided are the same, nothing will happen.

        If the two transitions do not share the same destination, they
        cannot be merged, and a `ValueError` will result. Use
        `retargetTransition` beforehand to ensure that they do if you
        want to merge transitions with different destinations.

        A `KeyError` will result if the decision or either transition
        does not exist.

        If merging reciprocal properties was requested and the first
        transition does not have a reciprocal, then no reciprocal
        properties change. However, if the second transition does not
        have a reciprocal and the first does, the first transition's
        reciprocal will be set to the reciprocal of the second
        transition, and that transition will not be deleted as usual.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        >>> g.addDecision('B')
        >>> g.addTransition('A', 'up', 'B')
        >>> g.addTransition('B', 'down', 'A')
        >>> g.setReciprocal('A', 'up', 'down')
        >>> # Merging a transition with no reciprocal
        >>> g.addTransition('A', 'up2', 'B')
        >>> g.mergeTransitions('A', 'up2', 'up')
        >>> g.getDestination('A', 'up2') is None
        True
        >>> g.getDestination('A', 'up')
        'B'
        >>> # Merging a transition with a reciprocal & tags
        >>> g.addTransition('A', 'up2', 'B')
        >>> g.addTransition('B', 'down2', 'A')
        >>> g.setReciprocal('A', 'up2', 'down2')
        >>> g.tagTransition('A', 'up2', 'one')
        >>> g.tagTransition('B', 'down2', 'two')
        >>> g.mergeTransitions('B', 'down2', 'down')
        >>> g.getDestination('A', 'up2') is None
        True
        >>> g.getDestination('A', 'up')
        'B'
        >>> g.getDestination('B', 'down2') is None
        True
        >>> g.getDestination('B', 'down')
        'A'
        >>> # Merging requirements uses ReqAll (i.e., 'and' logic)
        >>> g.addTransition('A', 'up2', 'B')
        >>> g.setTransitionProperties('A', 'up2', requirement=ReqPower('dash'))
        >>> g.setTransitionProperties('A', 'up', requirement=ReqPower('slide'))
        >>> g.mergeTransitions('A', 'up2', 'up')
        >>> g.getDestination('A', 'up2') is None
        True
        >>> repr(g.getTransitionRequirement('A', 'up'))
        "ReqAll([ReqPower('dash'), ReqPower('slide')])"
        >>> # Errors if destinations differ, or if something is missing
        >>> g.mergeTransitions('A', 'down', 'up')
        Traceback (most recent call last):
        ...
        KeyError...
        >>> g.mergeTransitions('Z', 'one', 'two')
        Traceback (most recent call last):
        ...
        KeyError...
        >>> g.addDecision('C')
        >>> g.addTransition('A', 'down', 'C')
        >>> g.mergeTransitions('A', 'down', 'up')
        Traceback (most recent call last):
        ...
        ValueError...
        >>> # Merging a reciprocal onto an edge that doesn't have one
        >>> g.addTransition('A', 'down2', 'C')
        >>> g.addTransition('C', 'up2', 'A')
        >>> g.setReciprocal('A', 'down2', 'up2')
        >>> g.tagTransition('C', 'up2', 'narrow')
        >>> g.getReciprocal('A', 'down') is None
        True
        >>> g.mergeTransitions('A', 'down2', 'down')
        >>> g.getDestination('A', 'down2') is None
        True
        >>> g.getDestination('A', 'down')
        'C'
        >>> g.getDestination('C', 'up2')
        'A'
        >>> g.getReciprocal('A', 'down')
        'up2'
        >>> g.getReciprocal('C', 'up2')
        'down'
        >>> g.transitionTags('C', 'up2')
        {'narrow'}
        >>> # Merging without a reciprocal
        >>> g.addTransition('C', 'up', 'A')
        >>> g.mergeTransitions('C', 'up2', 'up', mergeReciprocal=False)
        >>> g.getDestination('C', 'up2') is None
        True
        >>> g.getDestination('C', 'up')
        'A'
        >>> g.transitionTags('C', 'up') # tag gets merged
        {'narrow'}
        >>> g.getDestination('A', 'down')
        'C'
        >>> g.getReciprocal('A', 'down') is None
        True
        >>> g.getReciprocal('C', 'up') is None
        True
        >>> # Merging w/ normal reciprocals
        >>> g.addDecision('D')
        >>> g.addDecision('E')
        >>> g.addTransition('D', 'up', 'E', 'return')
        >>> g.addTransition('E', 'down', 'D')
        >>> g.mergeTransitions('E', 'return', 'down')
        >>> g.getDestination('D', 'up')
        'E'
        >>> g.getDestination('E', 'down')
        'D'
        >>> g.getDestination('E', 'return') is None
        True
        >>> g.getReciprocal('D', 'up')
        'down'
        >>> g.getReciprocal('E', 'down')
        'up'
        >>> # Merging w/ weird reciprocals
        >>> g.addTransition('E', 'return', 'D')
        >>> g.setReciprocal('E', 'return', 'up', setBoth=False)
        >>> g.getReciprocal('D', 'up')
        'down'
        >>> g.getReciprocal('E', 'down')
        'up'
        >>> g.getReciprocal('E', 'return') # shared
        'up'
        >>> g.mergeTransitions('E', 'return', 'down')
        >>> g.getDestination('D', 'up')
        'E'
        >>> g.getDestination('E', 'down')
        'D'
        >>> g.getDestination('E', 'return') is None
        True
        >>> g.getReciprocal('D', 'up')
        'down'
        >>> g.getReciprocal('E', 'down')
        'up'
        """
        # Short-circuit in the no-op case
        if merge == mergeInto:
            return

        # These lines will raise a KeyError if needed
        dest1 = self.destination(fromDecision, merge)
        dest2 = self.destination(fromDecision, mergeInto)

        if dest1 != dest2:
            raise ValueError(
                f"Cannot merge transition '{merge}' into transition"
                f" '{mergeInto}' from decision '{fromDecision}' because"
                f" their destinations are different ('{dest1}' and"
                f" '{dest2}').\nNote: you can use `retargetTransition`"
                f" to change the destination of a transition."
            )

        # Find and the transition properties
        props1 = self.getTransitionProperties(fromDecision, merge)
        props2 = self.getTransitionProperties(fromDecision, mergeInto)
        merged = mergeProperties(props1, props2)
        # Note that this doesn't change the reciprocal:
        self.setTransitionProperties(fromDecision, mergeInto, **merged)

        # Merge the reciprocal properties if requested
        # Get reciprocal to merge into
        reciprocal = self.getReciprocal(fromDecision, mergeInto)
        # Get reciprocal that needs cleaning up
        altReciprocal = self.getReciprocal(fromDecision, merge)
        # If the reciprocal to be merged actually already was the
        # reciprocal to merge into, there's nothing to do here
        if altReciprocal != reciprocal:
            if not mergeReciprocal:
                # In this case, we sever the reciprocal relationship if
                # there is a reciprocal
                if altReciprocal is not None:
                    self.setReciprocal(dest1, altReciprocal, None)
                    # By default setBoth takes care of the other half
            else:
                # In this case, we try to merge reciprocals
                # If altReciprocal is None, we don't need to do anything
                if altReciprocal is not None:
                    # Was there already a reciprocal or not?
                    if reciprocal is None:
                        # altReciprocal becomes the new reciprocal and is
                        # not deleted
                        self.setReciprocal(
                            fromDecision,
                            mergeInto,
                            altReciprocal
                        )
                    else:
                        # merge reciprocal properties
                        props1 = self.getTransitionProperties(
                            dest1,
                            altReciprocal
                        )
                        props2 = self.getTransitionProperties(
                            dest2,
                            reciprocal
                        )
                        merged = mergeProperties(props1, props2)
                        self.setTransitionProperties(
                            dest1,
                            reciprocal,
                            **merged
                        )

                        # delete the old reciprocal transition
                        self.remove_edge(dest1, fromDecision, altReciprocal)

        # Delete the old transition (reciprocal deletion/severance is
        # handled above if necessary)
        self.remove_edge(fromDecision, dest1, merge)

    def replaceUnexplored(
        self,
        fromDecision: Decision,
        transition: Transition,
        connectTo: Optional[Decision] = None,
        revName: Optional[Transition] = None,
        requirement: Optional[Requirement] = None,
        applyEffects: Optional[TransitionEffects] = None,
        tags: Optional[Set[Tag]] = None,
        annotations: Optional[List[Annotation]] = None,
        revRequires: Union[Requirement, str, None] = None,
        revEffects: Optional[TransitionEffects] = None,
        revTags: Optional[Set[Tag]] = None,
        revAnnotations: Optional[List[Annotation]] = None,
        decisionTags: Optional[Set[Tag]] = None,
        decisionAnnotations: Optional[List[Annotation]] = None
    ) -> Tuple[
        Dict[Transition, Transition],
        Dict[Transition, Transition]
    ]:
        """
        Given a decision and an edge name in that decision, where the
        named edge leads to an unexplored decision, replaces the
        unexplored decision on the other end of that edge with either a
        new decision using the given `connectTo` name, or if a decision
        using that name already exists, with that decision. If a
        `revName` is provided, a reciprocal edge will be added using
        that name connecting the `connectTo` decision back to the
        original decision. If this transition already exists, it must
        also point to an unexplored node, which will also be merged into
        the fromDecision node.

        If `connectTo` is not given (or is set to `None` explicitly)
        then the name of the unknown decision will not be changed,
        unless that name has the form `'_u.-n-'` where `-n-` is a
        positive integer (i.e., the form given to automatically-named
        unknown nodes). In that case, the name will be changed to
        `'_x.-n-'` using the same number, or a higher number if that
        name is already taken. In any case, the `'unknown'` tag will be
        removed from the decision.

        Any additional edges pointing to or from the unknown node(s)
        being replaced will also be re-targeted at the now-discovered
        known destination(s). These edges will retain their reciprocal
        names, or if this would cause a name clash, they will be renamed
        with a suffix (see `retargetTransition`).

        The return value is a pair of dictionaries mapping old names to
        new ones that just includes the names which were changed. The
        first dictionary contains renamed transitions that are outgoing
        from the new destination node (which used to be outgoing from
        the unexplored node). The second dictionary contains renamed
        transitions that are outgoing from the source node (which used
        to be outgoing from the unexplored node attached to the
        reciprocal transition; if there was no reciprocal transition
        specified then this will always be an empty dictionary).

        A `ValueError` will be raised if the destination of the specified
        transition is not an unknown decision (see `isUnknown`), or if
        the `connectTo`'s `revName` transition does not lead to an
        unknown decision (it's okay if this second transition doesn't
        exist). A `ValueError` will also be raised if the unknown
        destination decision already has an outgoing transition with the
        specified `revName` which does not lead back to the
        `fromDecision`.

        The transition properties (requirement and/or effects) of the
        replaced transition will be copied over to the new transition.
        Transition properties from the reciprocal transition will also
        be copied for the newly created reciprocal edge. Properties for
        any additional edges to/from the unknown node will also be
        copied.

        Also, any transition properties on existing forward or reciprocal
        edges from the destination node with the indicated reverse name
        will be merged with those from the target transition. Note that
        this merging process may introduce corruption of complex
        transition effects. TODO: Fix that!

        Any tags and annotations are added to copied tags/annotations,
        but specified requirements, and/or effects will replace previous
        requirements/effects, rather than being added to them.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        >>> g.addUnexploredEdge('A', 'up')
        '_u.0'
        >>> g.destination('A', 'up')
        '_u.0'
        >>> g.destination('_u.0', 'return')
        'A'
        >>> g.replaceUnexplored('A', 'up', 'B', 'down')
        ({}, {})
        >>> g.destination('A', 'up')
        'B'
        >>> g.destination('B', 'down')
        'A'
        >>> g.getDestination('B', 'return') is None
        True
        >>> '_u.0' in g
        False
        >>> # Two unexplored edges to the same node:
        >>> g.addDecision('C')
        >>> g.addTransition('B', 'next', 'C')
        >>> g.addTransition('C', 'prev', 'B')
        >>> g.setReciprocal('B', 'next', 'prev')
        >>> g.addUnexploredEdge('A', 'next', 'D', 'prev')
        'D'
        >>> g.addTransition('C', 'down', 'D')
        >>> g.addTransition('D', 'up', 'C')
        >>> g.setReciprocal('C', 'down', 'up')
        >>> g.replaceUnexplored('C', 'down')
        ({}, {})
        >>> g.destination('C', 'down')
        'D'
        >>> g.destination('A', 'next')
        'D'
        >>> g.destinationsFrom('D')
        {'prev': 'A', 'up': 'C'}
        >>> g.decisionTags('D')
        set()
        >>> # An unexplored transition which turns out to connect to a
        >>> # known decision, with name collisions
        >>> g.addUnexploredEdge('D', 'next', reciprocal='prev')
        '_u.2'
        >>> g.tagDecision('_u.2', 'wet')
        >>> g.addUnexploredEdge('B', 'next', reciprocal='prev') # edge taken
        Traceback (most recent call last):
        ...
        KeyError...
        >>> g.addUnexploredEdge('A', 'prev', reciprocal='next')
        '_u.3'
        >>> g.tagDecision('_u.3', 'dry')
        >>> # Add transitions that will collide when merged
        >>> g.addUnexploredEdge('_u.2', 'up') # collides with A/up
        '_u.4'
        >>> g.addUnexploredEdge('_u.3', 'prev') # collides with D/prev
        '_u.5'
        >>> g.replaceUnexplored('A', 'prev', 'D', 'next') # two decisions gone
        ({'prev': 'prev.1'}, {'up': 'up.1'})
        >>> g.destination('A', 'prev')
        'D'
        >>> g.destination('D', 'next')
        'A'
        >>> # Note that further unexplored structures are NOT merged
        >>> # even if they match against existing structures...
        >>> g.destination('A', 'up.1')
        '_u.4'
        >>> g.destination('D', 'prev.1')
        '_u.5'
        >>> '_u.2' in g
        False
        >>> '_u.3' in g
        False
        >>> g.decisionTags('D') # tags are merged
        {'dry'}
        >>> g.decisionTags('A')
        {'wet'}
        >>> # Auto-renaming an anonymous unexplored node
        >>> g.addUnexploredEdge('B', 'out')
        '_u.6'
        >>> g.replaceUnexplored('B', 'out')
        ({}, {})
        >>> '_u.6' in g
        False
        >>> g.destination('B', 'out')
        '_x.6'
        >>> g.destination('_x.6', 'return')
        'B'
        """

        if tags is None:
            tags = set()
        if annotations is None:
            annotations = []
        if revTags is None:
            revTags = set()
        if revAnnotations is None:
            revAnnotations = []
        if decisionTags is None:
            decisionTags = set()
        if decisionAnnotations is None:
            decisionAnnotations = []

        # Figure out destination decision
        oldUnknown = self.destination(fromDecision, transition)

        # Check that it's unknown
        if not self.isUnknown(oldUnknown):
            raise ValueError(
                f"Transition '{transition}' from '{fromDecision}' does"
                f" not lead to an unexplored decision (it leads to"
                f" '{oldUnknown}')."
            )

        # Check that the old unknown doesn't have a reciprocal edge that
        # would collide with the specified return edge
        if revName is not None:
            revFromUnknown = self.getDestination(oldUnknown, revName)
            if revFromUnknown not in (None, fromDecision):
                raise ValueError(
                    f"Transition '{revName}' from '{oldUnknown}' exists"
                    f" and does not lead back to '{fromDecision}' (it"
                    f" leads to '{revFromUnknown}')."
                )

        # If connectTo name wasn't specified, use current name of
        # unknown node unless it's a default name
        if connectTo is None:
            if (
                oldUnknown.startswith('_u.')
            and oldUnknown[3:].isdigit()
            ):
                connectTo = uniqueName('_x.' + oldUnknown[3:], self)
            else:
                connectTo = oldUnknown

        # Apply any new tags or annotations, or create a new node
        if connectTo in self:
            # Before applying tags, check if we need to error out
            # because of a reciprocal edge that points to a known
            # destination:
            if revName is not None:
                otherOldUnknown = self.getDestination(connectTo, revName)
                if (
                    otherOldUnknown is not None
                and not self.isUnknown(otherOldUnknown)
                ):
                    raise ValueError(
                        f"Reciprocal transition '{revName}' from"
                        f" '{connectTo}' does not lead to an unexplored"
                        f" decision (it leads to '{otherOldUnknown}')."
                    )
            self.tagDecision(connectTo, decisionTags)
            self.annotateDecision(connectTo, decisionAnnotations)
        else:
            self.addDecision(
                connectTo,
                tags=decisionTags,
                annotations=decisionAnnotations
            )
            # In this case there can't be an other old unknown
            otherOldUnknown = None

        # Remember old reciprocal edge for future merging in case
        # it's not revName
        oldReciprocal = self.getReciprocal(fromDecision, transition)

        # First, merge the old unknown with the connectTo node...
        destRenames = self.mergeDecisions(
            oldUnknown,
            connectTo,
            errorOnNameColision=False
        )
        sourceRenames = {} # empty for now

        # Remove the 'unknown' tag transferred during the merge
        self.untagDecision(connectTo, "unknown")

        # Next, if there is a reciprocal name specified, we do more...
        if revName is not None:
            # Figure out what kind of merging needs to happen
            if otherOldUnknown is None and revFromUnknown is None:
                # Just create the desired reciprocal transition, which
                # we know does not already exist
                self.addTransition(connectTo, revName, fromDecision)
                self.setReciprocal(fromDecision, transition, revName)
                otherOldReciprocal = None
            elif otherOldUnknown is not None:
                otherOldReciprocal = self.getReciprocal(connectTo, revName)
                # we need to merge otherOldUnknown into our fromDecision
                sourceRenames = self.mergeDecisions(
                    otherOldUnknown,
                    fromDecision,
                    errorOnNameColision=False
                )
                # Remove the 'unknown' tag transferred during the merge
                self.untagDecision(fromDecision, "unknown")
            # no need for else...
            # Only other possibility is that otherOldUnknown is None
            # and revFromUnknown is not None, in which case the revName
            # transition already exists and points to fromDecision; it
            # could not have been renamed during the merge because
            # otherOldUnknown was None.

            # Now we might need to merge some transitions:
            # - Any reciprocal of the target transition should be merged
            #   with revName (if it was already revName, that's a
            #   no-op).
            # - Any reciprocal of the revName transition from the target
            #   node (leading to otherOldUnknown) should be merged with
            #   the target transition, even if it shared a name and was
            #   renamed as a result.
            # - If revName was renamed during the initial merge, those
            #   transitions should be merged.

            # Merge old reciprocal into revName
            if oldReciprocal is not None:
                oldRev = destRenames.get(oldReciprocal, oldReciprocal)
                if self.getDestination(connectTo, oldRev) is not None:
                    # Note that we don't want to auto-merge the reciprocal,
                    # which is the target transition
                    self.mergeTransitions(
                        connectTo,
                        oldRev,
                        revName,
                        mergeReciprocal=False
                    )
                    # Remove it from the renames map
                    if oldReciprocal in destRenames:
                        del destRenames[oldReciprocal]

            # Merge revName reciprocal from otherOldUnknown
            if otherOldReciprocal is not None:
                otherOldRev = sourceRenames.get(
                    otherOldReciprocal,
                    otherOldReciprocal
                )
                # Note that the reciprocal is revName, which we don't
                # need to merge
                self.mergeTransitions(
                    fromDecision,
                    otherOldRev,
                    transition,
                    mergeReciprocal=False
                )
                # Remove it from the renames map
                if otherOldReciprocal in sourceRenames:
                    del sourceRenames[otherOldReciprocal]

            # Merge any renamed revName onto revName
            if revName in destRenames:
                extraRev = destRenames[revName]
                self.mergeTransitions(
                    connectTo,
                    extraRev,
                    revName,
                    mergeReciprocal=False
                )
                # Remove it from the renames map
                del destRenames[revName]

        # Accumulate new tags & annotations for the transitions
        self.tagTransition(fromDecision, transition, tags)
        self.annotateTransition(fromDecision, transition, annotations)

        if revName is not None:
            self.tagTransition(connectTo, revName, revTags)
            self.annotateTransition(connectTo, revName, revAnnotations)

        # Override copied requirement/effects for the transitions
        if requirement is not None:
            self.setTransitionRequirement(
                fromDecision,
                transition,
                requirement
            )
        if applyEffects is not None:
            self.setTransitionEffects(
                fromDecision,
                transition,
                applyEffects
            )

        if revName is not None:
            if revRequires is not None:
                self.setTransitionRequirement(
                    connectTo,
                    revName,
                    revRequires
                )
            if revEffects is not None:
                self.setTransitionEffects(
                    connectTo,
                    revName,
                    revEffects
                )

        # Return our final rename dictionaries
        return (destRenames, sourceRenames)

    def addEnding(
        self,
        fromDecision: Decision,
        name: Decision,
        tags: Optional[Set[Tag]] = None,
        annotations: Optional[List[Annotation]] = None,
        endTags: Optional[Set[Tag]] = None,
        endAnnotations: Optional[List[Annotation]] = None,
        requires: Union[Requirement, str, None] = None,
        effects: Optional[TransitionEffects] = None
    ) -> None:
        """
        Adds an edge labeled `'_e:-name-'` where '-name-' is the provided
        name, connecting to a new (or existing) decision named
        `'_e:-name-'` (same as the edge). This represents a transition to
        a game-end state. No reciprocal edge is added, but tags may be
        applied to the added transition and/or the ending room. The new
        transition and decision are both automatically tagged with
        'ending'.

        The starting decision must already exist, and must not already
        have a transition with the transition name, or a `ValueError`
        will be raised. Note that this means that ending names should not
        overlap with common transition names, since they may need to be
        used from multiple decisions in the graph; the '_e:' prefix
        should help with this.

        Requirements and/or effects if provided will be applied to the
        transition.
        """
        # Defaults
        if tags is None:
            tags = set()
        if annotations is None:
            annotations = []
        if endTags is None:
            endTags = set()
        if endAnnotations is None:
            endAnnotations = []

        tags.add("ending")
        endTags.add("ending")

        namePlus = '_e:' + name

        # Error checking
        if fromDecision not in self:
            raise ValueError(
                f"Cannot add a new ending transition '{name}' to"
                f" '{fromDecision}': That decision does not exist."
            )

        if namePlus in self.destinationsFrom(fromDecision):
            raise ValueError(
                f"Cannot add a new ending edge '{name}':"
                f" '{fromDecision}' already has an outgoing edge named"
                f" '{namePlus}'."
            )

        # Create or new ending decision if we need to
        if namePlus not in self:
            self.addDecision(
                namePlus,
                tags=endTags,
                annotations=endAnnotations
            )
        else:
            # Or tag/annotate the existing decision
            self.tagDecision(namePlus, endTags)
            self.annotateDecision(namePlus, endAnnotations)

        # Add the edge
        self.addTransition(
            fromDecision,
            namePlus,
            namePlus,
            tags=tags,
            annotations=annotations
        )
        self.setTransitionRequirement(fromDecision, namePlus, requires)
        if effects is not None:
            self.setTransitionEffects(fromDecision, namePlus, effects)


class TransitionBlockedWarning(Warning):
    """
    An warning type for indicating that a transition which has been
    requested does not have its requirements satisfied by the current
    game state.
    """
    pass


class Exploration:
    """
    A list of `DecisionGraph`s representing exploration over time, with
    specific positions for each step and transitions into them
    specified. Each decision graph represents a new state of the world
    (and/or new knowledge about a persisting state of the world), and the
    transition between graphs indicates which edge was followed, or what
    event happened to cause update(s). Depending on the resolution, it
    could represent a close record of every decision made or a more
    coarse set of snapshots from gameplay with more time in between.
    """
    def __init__(self) -> None:
        self.graphs: List[DecisionGraph] = []
        self.positions: List[Decision] = []
        self.states: List[State] = []
        self.transitions: List[Transition] = []
        # The transition at index i indicates the transition followed
        # (from the decision in the positions list at index i) or the
        # action taken that leads to the graph and position at index i + 1.
        # Normally, if there are n graphs, there will be n - 1
        # transitions listed.

    def __len__(self) -> int:
        """
        The 'length' of an exploration is the number of steps.
        """
        return len(self.graphs)

    def graphAtStep(self, n: int) -> DecisionGraph:
        """
        Returns the `DecisionGraph` at the given step index. Raises an
        `IndexError` if the step index is out of bounds (see `__len__`).
        """
        return self.graphs[n]

    def getGraphAtStep(self, n: int) -> Optional[DecisionGraph]:
        """
        Like `graphAtStep` but returns None instead of raising an error
        if there is no graph at that step.
        """
        try:
            return self.graphAtStep(n)
        except IndexError:
            return None

    def positionAtStep(self, n: int) -> Decision:
        """
        Returns the position at the given step index. Raises an `IndexError`
        if the step index is out of bounds (see `__len__`).
        """
        return self.positions[n]

    def getPositionAtStep(self, n: int) -> Optional[Decision]:
        """
        Like `positionAtStep` but returns None instead of raising
        an error if there is no position at that step.
        """
        try:
            return self.positionAtStep(n)
        except IndexError:
            return None

    def stateAtStep(self, n: int) -> State:
        """
        Returns the game state at the specified step. Raises an
        `IndexError` if the step value is out-of-bounds.
        """
        return self.states[n]

    def getStateAtStep(self, n: int) -> Optional[State]:
        """
        Like `stateAtStep` but returns None instead of raising
        an error if there is no transition at that step.
        """
        try:
            return self.stateAtStep(n)
        except IndexError:
            return None

    def transitionAtStep(self, n: int) -> Optional[Transition]:
        """
        Returns the transition taken from the situation at the given step
        index to the next situation (a `Transition` indicating which exit
        or action was taken). Raises an `IndexError` if the step index is
        out of bounds (see `__len__`), but returns `None` for the last
        step, which will not have a transition yet.
        """
        # Negative indices need an offset
        if n < 0:
            if n == -1 and len(self.graphs) > 0:
                transition = None
            else:
                transition = self.transitions[n + 1]
        # Positive indices just allow for None if we go one over
        else:
            if n == len(self.transitions) and len(self.graphs) > 0:
                transition = None
            else:
                # IndexError here for inappropriate indices
                transition = self.transitions[n]

        return transition

    def getTransitionAtStep(
        self,
        n: int
    ) -> Optional[Transition]:
        """
        Like `transitionAtStep` but returns None instead of raising
        an error if there is no transition at that step.
        """
        try:
            return self.transitionAtStep(n)
        except IndexError:
            return None

    def situationAtStep(
        self,
        n: int
    ) -> Tuple[DecisionGraph, Decision, State, Optional[Transition]]:
        """
        Returns a 4-tuple containing the graph (a `DecisionGraph`), the
        position (a `Decision`), the state (a `State`), and the
        transition taken (either a `Transition` or None) at the
        specified step. For the last step, the transition will be None.
        Raises an `IndexError` if asked for a step that's out-of-range.
        """

        return (
            self.graphs[n],
            self.positions[n],
            self.states[n],
            self.transitionAtStep(n)
        )

    def getSituationAtStep(
        self,
        n: int
    ) -> Optional[
        Tuple[DecisionGraph, Decision, State, Optional[Transition]]
    ]:
        """
        Like `situationAtStep` but returns None instead of raising an
        error if there is no situation at that step.
        """
        try:
            return self.situationAtStep(n)
        except IndexError:
            return None

    def currentGraph(self) -> DecisionGraph:
        """
        Returns the current graph, or raises an `IndexError` if there
        are no graphs yet.
        """
        return self.graphAtStep(-1)

    def getCurrentGraph(self) -> Optional[DecisionGraph]:
        "Like `currentGraph`, but returns None if there are no graphs."
        return self.getGraphAtStep(-1)

    def currentPosition(self) -> Decision:
        """
        Returns the current position, or raises an `IndexError` if there
        are no positions yet.
        """
        return self.positionAtStep(-1)

    def getCurrentPosition(self) -> Optional[Decision]:
        """
        Like `currentPosition` but returns None if there is no position.
        """
        return self.getPositionAtStep(-1)

    def currentState(self) -> State:
        """
        Returns the current game state, or raises an `IndexError` if
        there are no states yet.
        """
        return self.stateAtStep(-1)

    def getCurrentState(self) -> Optional[State]:
        "Like `getCurrentState` but returns None if there is no state."
        return self.getStateAtStep(-1)

    def currentSituation(
        self
    ) -> Tuple[DecisionGraph, Decision, State, Optional[Transition]]:
        """
        Returns a 4-tuple containing the current graph, the current
        position, the current game state, and None representing the
        current transition, which doesn't exist yet.
        """
        return self.situationAtStep(-1)

    def getCurrentSituation(
        self
    ) -> Optional[
        Tuple[DecisionGraph, Decision, State, Optional[Transition]]
    ]:
        """
        Like `currentSituation` but returns None if there is no current
        situation.
        """
        return self.getSituationAtStep(-1)

    def gainPowerNow(self, power: Power) -> None:
        """
        Modifies the current game state to add the specified `Power` to
        the player's capabilities. No changes are made to the current
        graph.
        """
        self.currentState().setdefault('powers', set()).add(power)

    def losePowerNow(self, power: Power) -> None:
        """
        Modifies the current game state to remove the specified `Power`
        from the player's capabilities. Does nothing if the player
        doesn't already have that power.
        """
        try:
            self.currentState().setdefault('powers', set()).remove(power)
        except KeyError:
            pass

    def adjustTokensNow(self, tokenType: Token, amount: int) -> None:
        """
        Modifies the current game state to add the specified number of
        `Token`s of the given type to the player's tokens. No changes are
        made to the current graph. Reduce the number of tokens by
        supplying a negative amount.
        """
        state = self.currentState()
        tokens = state.setdefault('tokens', {})
        tokens[tokenType] = tokens.get(tokenType, 0) + amount

    def updateRequirementNow(
        self,
        decision: Decision,
        transition: Transition,
        requirement: Union[Requirement, str, None]
    ) -> None:
        """
        Updates the requirement for a specific transition in a specific
        decision. If a `Requirement` object is given, that will be used;
        if a string is given, it will be turned into a `Requirement`
        using `Requirement.parse`. If `None` is given, the requirement
        for that edge will be removed.
        """
        if requirement is None:
            requirement = ReqNothing()
        self.currentGraph().setTransitionRequirement(
            decision,
            transition,
            requirement
        )

    def traversableAtStep(
        self,
        step: int,
        decision: Decision,
        transition: Transition
    ) -> bool:
        """
        Returns True if the specified transition from the specified
        decision had its requirement satisfied by the game state at the
        specified step. Raises an `IndexError` if the specified step
        doesn't exist, and a `KeyError` if the decision or transition
        specified does not exist in the `DecisionGraph` at that step.
        """
        graph = self.graphAtStep(step)
        req = graph.getTransitionRequirement(decision, transition)
        return req.satisfied(self.stateAtStep(step))

    def traversableNow(
        self,
        decision: Decision,
        transition: Transition
    ) -> bool:
        """
        Returns True if the specified transition from the specified
        decision has its requirement satisfied by the current game
        state. Raises an `IndexError` if there are no game states yet.
        """
        return self.traversableAtStep(-1, decision, transition)

    def applyEffectsNow(
        self,
        effects: TransitionEffects
    ) -> None:
        """
        Applies the specified effects to the current graph, without
        creating a new exploration step.

        A `ValueError` will be raised if one of the specified tag changes
        doesn't start with either '+' or '-'. Removal of non-applied
        tags is silently ignored however, as is the loss of non-possessed
        powers.
        """
        now = self.currentGraph()

        for gain in effects.get('gain', set()):
            if isinstance(gain, str):
                self.gainPowerNow(gain)
            else:
                tokens, amount = gain
                self.adjustTokensNow(tokens, amount)

        for lose in effects.get('lose', set()):
            if isinstance(lose, str):
                self.losePowerNow(lose)
            else:
                tokens, amount = lose
                self.adjustTokensNow(tokens, -amount)

        for decision, transition, req in effects.get('alters', []):
            now.setTransitionRequirement(decision, transition, req)

        for entry in effects.get('tags', []):
            if len(entry) == 2:
                entry = cast(Tuple[Decision, List[Tag]], entry)
                tagDecision, taglist = entry
                for tagChange in taglist:
                    action = tagChange[0]
                    theTag = tagChange[1:]
                    if action == '+':
                        now.tagDecision(tagDecision, theTag)
                    elif action == '-':
                        now.untagDecision(tagDecision, theTag)
                    else:
                        raise ValueError(
                            f"Invalid taglist entry '{tagChange}'"
                            f" (didn't start with either '+' or '-')."
                        )
            else: # length must be 3
                entry = cast(Tuple[Decision, Transition, List[Tag]], entry)
                decision, transition, taglist = entry
                for tagChange in taglist:
                    action = tagChange[0]
                    theTag = tagChange[1:]
                    if action == '+':
                        now.tagTransition(decision, transition, theTag)
                    elif action == '-':
                        try:
                            now.untagTransition(decision, transition, theTag)
                        except KeyError:
                            pass
                    else:
                        raise ValueError(
                            f"Invalid taglist entry '{tagChange}'"
                            f" (didn't start with either '+' or '-')."
                        )

    def applyTransitionEffectsNow(
        self,
        decision: Decision,
        transition: Transition,
        step: int = -1
    ) -> None:
        """
        Applies the effects of the specified transition from the
        specified decision to the current graph and state. By default,
        these effects are read from the transition information in the
        current graph, but specifying a non-default `step` value will
        cause the effects to be read from the graph at a different step.
        The effects in the current graph will be updated based on the
        `'next'` entry of the effects object applied.

        Raises an `IndexError` if the specified step doesn't exist, or a
        `KeyError` if the decision or transition specified doesn't exist
        in the graph at the specified step.

        This function does not check whether any requirements for the
        specified transition are satisfied.
        """
        then = self.graphAtStep(step)
        effects = then.getTransitionEffects(decision, transition)
        self.applyEffectsNow(effects)

    def start(
        self,
        decisionName: Decision,
        connectionNames: Iterable[Transition],
        startState: Dict[str, Any] = None
    ) -> None:
        """
        Creates a new initial graph, and places one decision in that
        graph with the given name and with connections to unknown nodes
        for each of the connection names provided. These connections are
        set up without any properties or effects.

        Raises a `ValueError` if the exploration isn't empty.
        """
        if len(self.graphs) > 0:
            raise ValueError(
                "Cannot start an exploration which already has graphs in"
                " it."
            )

        if startState is None:
            startState = {}

        first = DecisionGraph()
        first.addDecision(decisionName)
        for connection in connectionNames:
            first.addUnexploredEdge(decisionName, connection)

        # Add the graph to our graphs list and set our starting position
        self.graphs.append(first)
        self.positions.append(decisionName)
        self.states.append(startState)

        # Transitions remains empty for now

    def explore(
        self,
        transition: Transition,
        destination: Decision,
        connectionNames: Iterable[Transition],
        reciprocal: Optional[Transition] = None
    ) -> None:
        """
        Adds a new graph to the exploration graph representing the
        traversal of the specified transition from the current position,
        and updates the current position to be the new decision added.
        The transition must have been pointing to an unexplored region,
        which will be replaced by a new decision with the given name.
        That decision will have each of the given connections added to
        it (pointing to new unexplored regions). If a reciprocal name is
        specified, the reciprocal transition will be renamed using that
        name, or created with that name if it didn't already exist. If
        reciprocal is left as `None` (the default) then no change will be
        made to the reciprocal transition, and it will not be created if
        it doesn't exist.

        An `IndexError` will be raised if there aren't any existing
        graphs, and a `KeyError` will be raised if the current position
        is invalid or if the listed transition does not exist at the
        current position. A `ValueError` will be raised if the specified
        transition does not lead to an unknown region, or if the
        specified destination already exists, and a
        `TransitionBlockedWarning` will be issued if the specified
        transition is not traversable given the current game state (but
        in that last case the step will still be taken).

        The reciprocal may not be one of the listed new connections to
        create (because they will all be created pointing to unknown
        regions).

        To create a decision with multiple connections back to explored
        space, leave those connections out of the `connectionNames`
        argument, and add them manually afterwards by modifying the
        result of `currentGraph`.
        """
        here = self.currentPosition()
        if not self.traversableNow(here, transition):
            warnings.warn(
                (
                    f"The requirements for transition '{transition}'"
                    f" from decision '{here}' are not met at step"
                    f" {len(self)}."
                ),
                TransitionBlockedWarning
            )

        now = copy.deepcopy(self.currentGraph())
        current = copy.deepcopy(self.currentState())

        if destination in now:
            raise ValueError(
                f"Cannot explore to decision '{destination}' because it"
                f" already exists (use `returnTo` when revisiting a"
                f" previous decision)."
            )

        now.replaceUnexplored(
            here,
            transition,
            destination,
            reciprocal
        )

        for outgoing in connectionNames:
            now.addUnexploredEdge(destination, outgoing)

        # Grow our state-list variables
        self.graphs.append(now)
        self.transitions.append(transition)
        self.positions.append(destination)
        self.states.append(current)

        # Pick up state effects of the transition
        self.applyTransitionEffectsNow(here, transition)
        # Note: we apply the transition effects from the copied + updated
        # graph, not from the previous-step graph. This shouldn't make
        # any difference, since we just copied the graph.

    def returnTo(
        self,
        transition: Transition,
        destination: Decision,
        reciprocal: Optional[Transition] = None
    ) -> None:
        """
        Adds a new graph to the exploration that replaces the given
        transition at the current position (which must lead to an unknown
        node, or a `ValueError` will result). The new transition will
        connect back to the specified destination, which must already
        exist (or a different `ValueError` will be raised).

        If a `reciprocal` transition is specified, that transition must
        either not already exist in the destination decision or lead to
        an unknown region; it will be replaced (or added) as an edge
        leading back to the current position.

        A `TransitionBlockedWarning` will be issued if the requirements
        for the transition are not met, but the step will still be taken.
        """
        # Get current position and graph
        now = copy.deepcopy(self.currentGraph())
        here = self.currentPosition()
        state = copy.deepcopy(self.currentState())

        if not self.traversableNow(here, transition):
            warnings.warn(
                (
                    f"The requirements for transition '{transition}'"
                    f" from decision '{here}' are not met at step"
                    f" {len(self)}."
                ),
                TransitionBlockedWarning
            )

        if destination not in now:
            raise ValueError(
                f"Cannot return to decision '{destination}' because it"
                f" does not yet exist (use `explore` when visiting a new"
                f" decision)."
            )

        # Replace with connection to existing destination
        now.replaceUnexplored(
            here,
            transition,
            destination,
            reciprocal
        )

        # Grow our state-list variables
        self.graphs.append(now)
        self.transitions.append(transition)
        self.positions.append(destination)
        self.states.append(state)

        # Apply transition effects
        self.applyTransitionEffectsNow(here, transition)

    def takeAction(
        self,
        action: Transition,
        requires: Union[Requirement, str, None] = None,
        effects: Optional[TransitionEffects] = None
    ) -> None:
        """
        Adds a new graph to the exploration based on taking the given
        action, which must be a self-transition in the graph. If the
        action does not already exist in the graph, it will be created;
        either way the requirements and effects of the action will be
        updated to match any specified here, and those are the
        requirements/effects that will count. The optional arguments
        specify a requirement and/or effect for the action.

        Issues a `TransitionBlockedWarning` if the current game state
        doesn't satisfy the requirements for the action.
        """
        here = self.currentPosition()
        now = copy.deepcopy(self.currentGraph())
        state = copy.deepcopy(self.currentState())
        # If the action doesn't already exist, we create it in the new
        # graph (e.g, if there's a hidden cutscene trigger).
        if now.getDestination(here, action) is None:
            now.addAction(here, action, requires, effects)
        else:
            # Otherwise, just update the transition effects (before the
            # action is taken)
            now.setTransitionRequirement(here, action, requires)
            if effects is not None:
                now.setTransitionEffects(here, action, effects)

        # Note: can't use traversableNow here, because if we just added
        # the action, it won't appear in the current graph yet
        # (self.graph.append happens below, and must happen after this).
        req = now.getTransitionRequirement(here, action)
        if not req.satisfied(self.currentState()):
            warnings.warn(
                (
                    f"The requirements for action '{action}' in"
                    f" decision '{here}' are not met in the game state"
                    f" at step {len(self)}."
                ),
                TransitionBlockedWarning
            )

        self.graphs.append(now)
        self.transitions.append(action)
        self.positions.append(self.currentPosition())
        self.states.append(state)

        self.applyTransitionEffectsNow(here, action)

    def retrace(
        self,
        transition: Transition,
    ) -> None:
        """
        Adds a new graph to the exploration based on taking the given
        transition, which must already exist and which must not lead to
        an unknown region.

        Issues a `TransitionBlockedWarning` if the current game state
        doesn't satisfy the requirements for the transition.

        A `ValueError` is raised if the specified transition does not yet
        exist or leads to an unknown area.
        """
        here = self.currentPosition()
        now = copy.deepcopy(self.currentGraph())
        state = copy.deepcopy(self.currentState())
        # If the action doesn't already exist, we create it in the new
        # graph (e.g, if there's a hidden cutscene trigger).
        dest = now.getDestination(here, transition)
        if dest is None:
            raise ValueError(
                f"Cannot retrace transition '{transition}' from"
                f" decision '{here}' because it does not yet exist."
            )

        # TODO: Check for tag on destination, not edge!
        if 'unknown' in now.transitionTags(here, transition):
            raise ValueError(
                f"Cannot retrace transition '{transition}' from"
                f" decision '{here}' because it leads to an unknown"
                f" decision.\nUse `Exploration.explore` and provide"
                f" destination decision details instead."
            )

        if not self.traversableNow(here, transition):
            warnings.warn(
                (
                    f"The requirements for transition '{transition}' in"
                    f" decision '{here}' are not met in the game state"
                    f" at step {len(self)}."
                ),
                TransitionBlockedWarning
            )

        self.graphs.append(now)
        self.transitions.append(transition)
        self.positions.append(dest)
        self.states.append(state)

        self.applyTransitionEffectsNow(here, transition)

    def warp(
        self,
        destination: Decision,
        message: str = "",
        effects: Optional[TransitionEffects] = None
    ) -> None:
        """
        Adds a new graph to the exploration that's a copy of the current
        graph, listing the transition as '~~:' plus the specified message
        (or just '~~' if the message is an empty string). That transition
        string must NOT be a valid transition in the current room.

        If the destination is the same as the current position, the
        transition prefix (or content) will be '..' instead of '~~'.

        The position is set to the specified destination, and if effects
        are specified they are applied.

        A `ValueError` is raised if the specified transition name
        already exists.

        A `KeyError` is raised if the specified destination does not
        exist.
        """
        here = self.currentPosition()
        now = copy.deepcopy(self.currentGraph())
        state = copy.deepcopy(self.currentState())

        if destination not in now:
            raise KeyError(
                f"Warp destination '{destination}' does not exist."
            )

        prefix = '~~'
        if here == destination:
            prefix = '..'

        if message == '':
            tName = prefix
        else:
            tName = prefix + ':' + message

        # If the transition already exists, it's not a valid warp
        # message.
        dest = now.getDestination(here, tName)
        if dest is not None:
            raise ValueError(
                f"Cannot use '{message}' as a warp message because"
                f" transition '{tName}' exists at decision '{here}'."
            )

        self.graphs.append(now)
        self.transitions.append(tName)
        self.positions.append(destination)
        self.states.append(state)

        if effects is not None:
            self.applyEffectsNow(effects)

    def wait(
        self,
        message: str = "",
        effects: Optional[TransitionEffects] = None
    ) -> None:
        """
        Adds a warp which leaves the player in the same position. If
        effects are specified, they are applied.

        A `ValueError` is raised if the message implies a transition name
        which already exists (this is unlikely).
        """
        here = self.currentPosition()
        self.warp(here, message, effects)
