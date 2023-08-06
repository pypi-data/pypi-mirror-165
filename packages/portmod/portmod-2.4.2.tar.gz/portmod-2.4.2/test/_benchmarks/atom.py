# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import pytest

from portmodlib.atom import Atom, FQAtom, QualifiedAtom, atom_sat, version_gt


def canimport(name: str) -> bool:
    """Returns true if the given module can be imported"""
    try:
        __import__(name)
        return True
    except ModuleNotFoundError:
        return False


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
def test_atom(benchmark):
    """Test the speed of loading Atoms"""

    def test():
        Atom._CACHE = {}
        Atom("foo/bar-1.0::baz")

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
def test_qualifed_atom(benchmark):
    """Test the speed of loading Atoms"""

    def test():
        Atom._CACHE = {}
        QualifiedAtom("foo/bar-1.0::baz")

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
def test_fqatom(benchmark):
    """Test the speed of loading Atoms"""

    def test():
        Atom._CACHE = {}
        FQAtom("foo/bar-1.0::baz")

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
def test_fqatom_cached(benchmark):
    """Test the speed of loading Atoms"""

    def test():
        FQAtom("foo/bar-1.0::baz")

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
def test_cached(benchmark):
    """Test the speed of loading Atoms"""

    def test():
        Atom("foo/bar-1.0::baz")

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
def test_atom_sat_similar(benchmark):
    """Test the speed of comparing similar Atoms"""

    def test():
        atom_sat(Atom("foo/bar-1.0.0"), Atom("~foo/bar-1.0-r1"))

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
def test_atom_sat_different(benchmark):
    """Test the speed of comparing obviously different"""

    def test():
        atom_sat(Atom("foo/bar-1.0.0"), Atom("foo/baz-1.0-r1"))

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
def test_version_gt(benchmark):
    """Test the speed of loading Atoms"""

    def test():
        version_gt("1.0.0", "1.0-r1")

    benchmark(test)
