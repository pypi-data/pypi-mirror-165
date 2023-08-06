# Function to load machines
import re
from maquinas.regular.dfa import *
from maquinas.regular.ndfa import *
from maquinas.regular.ndfa_e import *
from maquinas.exceptions import *

re_state = re.compile(r"^\s*(?P<initial>->)?\s*(?P<state>.*[^\]])[^\]]*(?P<final>])?$")


def load_fa(string):
    """Loads a finite automata: DFA, NDFA, NDFA-e from a string"""
    header = False
    delta = {}
    for line in string.split("\n"):
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        if not header:
            sigma = _read_sigma(line)
            header = True
        else:
            origin, states = _read_row(line)
            delta[origin] = states
    type_machine = 1
    if "epsilon" in sigma:
        type_machine = 3
    if "ε" in sigma:
        type_machine = 3
    if type_machine == 1:
        for o, states in delta.items():
            for s in states:
                if len(s) > 1:
                    type_machine = 2
                    break
            if type_machine == 2:
                break
    m = _create_fa_by_type(type_machine)
    for a in sigma:
        try:
            m.add_symbol(a)
        except AlreadyExistsSymbol:
            pass
    A = set()
    for (ini, fin, q_i), states in delta.items():
        if fin:
            A.add(q_i)
        for a, state in zip(sigma, states):
            state = [s for s in state if len(s) > 0]
            if len(state) > 0:
                if type_machine == 1 and len(state) == 1:
                    m.add_transition(q_i, a, state[0], force=True)
                else:
                    m.add_transition(q_i, a, state, force=True)
        if ini:
            m.set_initial_state(q_i)
    m.set_aceptors(A)
    return m


def _create_fa_by_type(type_machine):
    if type_machine == 1:
        return DeterministicFiniteAutomaton()
    elif type_machine == 2:
        return NonDeterministicFiniteAutomaton()
    elif type_machine == 3:
        return NonDeterministicFiniteAutomaton_epsilon()


def _read_sigma(line):
    """Reads an alphabet sigma"""
    return [a.strip() for a in line.split("|") if len(a.strip()) > 0]


def _read_row(line):
    """Reads a line of a FA"""
    row = [a.strip() for a in line.split("|")]
    origin = _read_state(row[0])
    return origin, _read_states(row[1:])


def _read_state(state):
    """Reads a source state of a FA"""
    m = re_state.match(state)
    return (
        m.group("initial") != None,
        m.group("final") != None,
        m.group("state").strip(),
    )


def _read_states(states):
    """Reads a destination states of a FA"""
    return [[s.strip() for s in state.split(",")] for state in states]


def load_jflap(string, state_prefix=lambda x: f"{x}"):
    """Reads a jflap string file definition"""
    import xml.etree.ElementTree as ET

    root = ET.fromstring(string)
    type_machine = root.find("type").text

    # TODO load other type of inputs: pda, re, grammar
    if type_machine == "fa":
        m = _load_jflap_fa(root, state_prefix=state_prefix)
    return m


def _load_jflap_fa(root, state_prefix=lambda x: f"{x}"):
    """Loads a jflap string file definition"""

    type_machine = 0
    if any(t.find("read").text == None for t in root.iter("transition")):
        type_machine = 3
    else:
        trans = set()
        for e in root.findall("transition"):
            if (e.find("from").text, e.find("read").text) in trans:
                type_machine = 2
                break
        if type_machine == 0:
            type_machine = 1
    print(type_machine)
    m = _create_fa_by_type(type_machine)
    A = set()
    id2name = {}
    for e in root.iter("state"):
        if "name" in e.attrib:
            q = state_prefix(e.attrib["name"])
            id2name[e.attrib["id"]] = q
        else:
            q = state_prefix(e.attrib["id"])
            id2name[e.attrib["id"]] = q
        try:
            m.add_state(q)
        except AlreadyExistsState:
            pass
        if not e.find("initial") is None:
            m.set_initial_state(q)
        if not e.find("final") is None:
            A.add(q)
    m.set_aceptors(A)
    for e in root.iter("transition"):
        a = e.find("read").text
        if not a:
            a = "epsilon"
        else:
            try:
                m.add_symbol(a)
            except AlreadyExistsSymbol:
                pass
        q_i = id2name[e.find("from").text]
        q_f = id2name[e.find("to").text]
        if type_machine == 1:
            m.add_transition(q_i, a, q_f, force=True)
        else:
            m.add_transition(q_i, a, [q_f], force=True, update=True)

    return m
