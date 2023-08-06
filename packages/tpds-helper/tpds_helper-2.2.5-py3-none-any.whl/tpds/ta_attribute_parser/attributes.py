from tpds.ta_attribute_parser import *
import re


def get_handle_property(value, d):
    """
    Function will invoke handle property api based on the handle class
    Ex :
    -->get_private_properties(value)
    -->get_public_properties(value)
    """
    func = "get_" + d["handle_class"].split(" ")[0].lower() + "_properties (value)"
    return {"Property": eval(func)}


def decode_attribute(attr):
    # Dict hold the decoded attribute informations
    attr_info = {}
    # handle_properties holds the bit length info of attribute fields
    # Don't remove reserved fields in below list
    handle_properties = [
        ('handle_class', 3),
        ('key_type', 4),
        ('alg_mode', 1),
        ('handle_property', 16),
        ('usage_key', 8),
        ('write_key', 8),
        ('read_key', 8),
        ('usage_perm', 2),
        ('write_perm', 2),
        ('read_perm', 2),
        ('delete_perm', 2),
        ('use_count', 2),
        ('reserved_58', 1),
        ('exportable', 1),
        ('lockable', 1),
        ('access_limit', 2),
        ('reserved_62', 1)
    ]

    name = 0
    bit_length = 1

    attr_bin = str_to_bin(attr)
    for field in handle_properties:
        bits = attr_bin[-abs(field[bit_length]):]
        attr_bin = attr_bin[:-abs(field[bit_length])]
        # Alg mode and handle_property function need key type info
        if field[name] == "alg_mode" or field[name] == "handle_property":
            value = bits
            func = 'get_' + field[name] + '(value, attr_info)'
        else:
            value = int(bits, 2)
            func = 'get_' + field[name] + '(value)'
        attr_info.update({field[name]: eval(func)})

    return attr_info


def attribute_info(val):
    attr_info = decode_attribute(val)
    key_property = re.sub(
                        r'[\[{}\]\']', '',
                        str(attr_info.get('handle_property')))
    attr_list = []
    attr_list.append(
                    f'{attr_info.get("handle_class")}, '
                    f'{attr_info.get("key_type")}, '
                    f'{attr_info.get("alg_mode")}, '
                    f'Exportable:{attr_info.get("exportable")}, '
                    f'Lockable:{attr_info.get("lockable")}, '
                    f'Access limit:{attr_info.get("access_limit")}'
                    )
    attr_list.append(
                    f'Key Permission : '
                    f' Usage:{attr_info.get("usage_perm")}, '
                    f'Write:{attr_info.get("write_perm")}, '
                    f' Read:{attr_info.get("read_perm")}, '
                    f'Delete:{attr_info.get("delete_perm")}')
    usage_key = ''
    if attr_info.get("usage_perm") == 'Rights':
        usage_key = f'Usage Rights:{attr_info.get("usage_key")}, '
    elif attr_info.get("usage_perm") == 'Auth':
        handle = hex(0x8000 | int(attr_info.get("usage_key"), base=16))
        usage_key = f'Usage Auth Handle:{handle}, '

    write_key = ''
    if attr_info.get("write_perm") == 'Rights':
        write_key = f'Write Rights:{attr_info.get("write_key")}, '
    elif attr_info.get("write_perm") == 'Auth':
        handle = hex(0x8000 | int(attr_info.get("write_key"), base=16))
        write_key = f'Write Auth Handle:{handle}, '

    read_key = ''
    if attr_info.get("read_perm") == 'Rights':
        read_key = f'Read Rights:{attr_info.get("read_key")}, '
    elif attr_info.get("read_perm") == 'Auth':
        handle = hex(0x8000 | int(attr_info.get("read_key"), base=16))
        read_key = f'Read Auth Handle:{handle}, '
    if usage_key != '' or read_key != '' or write_key != '':
        attr_list.append('Key Handles : ' + usage_key+write_key+read_key)
    attr_list.append(f'{key_property}')

    return(attr_list)
