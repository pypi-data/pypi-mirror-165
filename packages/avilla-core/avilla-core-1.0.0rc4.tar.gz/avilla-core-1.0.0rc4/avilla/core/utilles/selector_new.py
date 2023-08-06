from __future__ import annotations
from typing import Callable, Literal, TypeVar, Union, Protocol, runtime_checkable, Annotated, Generic

MatchRule = Literal['exact', 'exist']
Pattern = Union[str, int, Callable[[Union[str, int]], bool]]


class Selector:
    match_rule: MatchRule = 'exact'

    pattern: dict[str, Pattern]

    def __init__(self, *, match_rule: MatchRule = 'exact'):
        self.match_rule = match_rule
        self.pattern = {}
    
    def __getattr__(self, name: str):
        def wrapper(content: Pattern):
            self.pattern[name] = content
            return self
        return wrapper

    def contains(self, key: str) -> bool:
        return key in self.pattern
    
    __contains__ = contains

    def __getitem__(self, key: str) -> Pattern:
        return self.pattern[key]
    
    @property
    def constant(self) -> bool:
        return all(not callable(v) for v in self.pattern.values())

    @property
    def path(self) -> str:
        return ".".join(self.pattern.keys())

    def match(self, another: Selector) -> bool:
        if self.match_rule == 'exact':
            if self.constant:
                return another.constant and self.pattern == another.pattern
            
        elif self.match_rule == 'exist':
            return set(self.pattern.keys()).issubset(another.pattern.keys())
        else:
            raise ValueError(f'Unknown match rule: {self.match_rule}')