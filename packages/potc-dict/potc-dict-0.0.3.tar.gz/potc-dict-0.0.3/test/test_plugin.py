import pytest

from potc.testing import provement


@pytest.mark.unittest
class TestPlugin(provement()):
    def test_pretty_dict(self):
        with self.transobj_assert({'a': 1}) as (obj, name):
            assert obj == {'a': 1}
            assert name == 'pretty_dict'
        with self.transobj_assert({}) as (obj, name):
            assert obj == {}
            assert name == 'pretty_dict'
        with self.transobj_assert({1: 2}) as (obj, name):
            assert obj == {1: 2}
            assert name == 'builtin_dict'

        with self.transvars_assert({'a': {'b': 1}}) as (vars_, code):
            assert vars_ == {'a': {'b': 1}}
            assert 'dict(b=1)' in code
