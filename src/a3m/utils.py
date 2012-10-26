"""
Created on Sep 13, 2011

"""
from django.utils.safestring import mark_safe
import math

def get_query_string(p, new_params=None, remove=None):
    """
    Add and remove query parameters. From `django.contrib.admin`.
    """
    if new_params is None: new_params = {}
    if remove is None: remove = []
    for r in remove:
        for k in p.keys():
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if k in p and v is None:
            del p[k]
        elif v is not None:
            p[k] = v
    return mark_safe('?' + '&amp;'.join([u'%s=%s' % (k, v) for k, v in p.items()]).replace(' ', '%20'))

def string_to_dict(string):
    """
    Usage::
    
        {{ url|thumbnail:"width=10,height=20" }}
        {{ url|thumbnail:"width=10" }}
        {{ url|thumbnail:"height=20" }}
    """
    kwargs = {}
    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '': continue
            kw, val = arg.split('=', 1)
            kwargs[kw] = val
    return kwargs

def string_to_list(string):
    """
    Usage::
    
        {{ url|thumbnail:"width,height" }}
    """
    args = []
    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '': continue
            args.append(arg)
    return args

def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]

def interweave_strings(a, b, from_a=1, from_b=1):
    """
    Interweave strings a and b repeatedly taking from_a characters from a and from_b chars from b
    @param a:
    @param b:
    @param from_a:
    @param from_b:
    """
    split_a = split_len(a, from_a)
    split_b = split_len(b, from_b)
    longer, shorter = (split_a, split_b) if len(split_a) > len(split_b) else (split_b, split_a)
    result = []
    shorter = shorter * (len(longer) / max(len(shorter),1) + 1)
    for i, bit in enumerate(longer):
        result.append(bit)
        result.append(shorter[i])
    return "".join(result)
