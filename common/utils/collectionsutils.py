from typing import Optional, Any, Dict, List, TypeVar

from common.consts import UNDEFINED


TKey = TypeVar('TKey')
TValue = TypeVar('TValue')


def with_update(dct: Dict[TKey, TValue],
                update: Dict) -> Dict[TKey, TValue]:
    dct.update(update)
    return dct


class RDict(dict):
    """
    Recursive dict
    Supports dot in keys (expects multi layer dicts)
    """

    def get(self,
            key: Any,
            default: Optional[Any] = None) -> Optional[Any]:
         if '.' not in key:
             return super().get(key, default)

         return self._rget(node=self,
                           parts=key.split('.'),
                           offset=0,
                           default=default)

    def _rget(self,
             node: Dict[str, Any],
             parts: List[str],
             offset: int,
             default: Any) -> Optional[Any]:
        """
        Recursive get
        :param node:
        :param key:
        :param parts:
        :param offset:
        :param default:
        :return:
        """
        if offset >= len(parts) - 1:
            # last key part
            return node.get(parts[-1], default)

        node = node[parts[offset]]
        return self._rget(node=node,
                          parts=parts,
                          offset=offset + 1,
                          default=default)

    def set(self,
            key: str,
            value: Optional[Any] = None):
        self._rset(node=self,
                   parts=key.split('.'),
                   offset=0,
                   value=value)

    def _rset(self,
              node: Dict[str, Any],
              parts: List[str],
              offset: int,
              value: Any):
        if offset >= len(parts) - 1:
            # last key part

            node[parts[-1]] = value
        else:
            # keep reference to original node if there's no child node with the same key part
            _node: Dict[str, Any] = node.get(parts[offset], UNDEFINED)
            if _node == UNDEFINED:
                node[parts[offset]] = {}
                _node = node[parts[offset]]

            self._rset(node=_node,
                       parts=parts,
                       offset=offset+1,
                       value=value)


def get_from_dict(dct: Dict[str, Any],
                  key: Any,
                  default: Optional[Any] = None) -> Optional[Any]:
     if '.' not in key:
         return dct.get(key, default)

     return get_from_dict_node(node=dct,
                               parts=key.split('.'),
                               offset=0,
                               default=default)


def get_from_dict_node(node: Dict[str, Any],
                       parts: List[str],
                       offset: int,
                       default: Any) -> Optional[Any]:
    """
    Recursive get
    :param node:
    :param key:
    :param parts:
    :param offset:
    :param default:
    :return:
    """
    if offset >= len(parts) - 1:
        # last key part
        return node.get(parts[-1], default)

    node = node[parts[offset]]
    return get_from_dict_node(node=node,
                              parts=parts,
                              offset=offset + 1,
                              default=default)


def set_in_dict(dct: Dict[str, Any],
                key: str,
                value: Optional[Any] = None):
    set_in_dict_node(node=dct,
                     parts=key.split('.'),
                     offset=0,
                     value=value)


def set_in_dict_node(node: Dict[str, Any],
                     parts: List[str],
                     offset: int,
                     value: Any):
    if offset >= len(parts) - 1:
        # last key part
        node[parts[-1]] = value
    else:
        # keep reference to original node if there's no child node with the same key part
        _node: Dict[str, Any] = node.get(parts[offset], UNDEFINED)
        if _node == UNDEFINED:
            node[parts[offset]] = {}
            _node = node[parts[offset]]

        set_in_dict_node(node=_node,
                         parts=parts,
                         offset=offset+1,
                         value=value)
