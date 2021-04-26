import click

from .validation.val_spot import validate_side
from .validation.val_spot import validate_time_in_force
from .validation.val_spot import validate_recv_window
from .validation.val_spot import validate_new_order_resp_type


def get_new_order_default_options():
    return [
        {'-sy': True, '--symbol': True, 'attrs': {'required': True, 'type': click.types.STRING}},
        {'-si': True, '--side': True, 'attrs': {'required': True, 'callback': validate_side,
                                                'type': click.types.STRING}},
        {'-tif': True, '--time_in_force': True, 'attrs': {'callback': validate_time_in_force,
                                                          'type': click.types.STRING}},
        {'-q': True, '--quantity': True, 'attrs': {'type': click.types.FLOAT}},
        {'-qoq': True, '--quote_order_qty': True, 'attrs': {'type': click.types.FLOAT}},
        {'-p': True, '--price': True, 'attrs': {'type': click.types.FLOAT}},
        {'-ncoid': True, '--new_client_order_id': True, 'attrs': {'type': click.types.STRING}},
        {'-sp': True, '--stop_price': True, 'attrs': {'type': click.types.FLOAT}},
        {'-iq': True, '--iceberg_qty': True, 'attrs': {'type': click.types.FLOAT}},
        {'-rw': True, '--recv_window': True, 'attrs': {'default': 5000, 'show_default': True,
                                                       'callback': validate_recv_window,
                                                       'type': click.types.INT}},
        {'-nort': True, '--new_order_resp_type': True, 'attrs': {'default': "FULL", 'show_default': True,
                                                                 'callback': validate_new_order_resp_type,
                                                                 'type': click.types.STRING}},
    ]