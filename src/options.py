import click

from src.validation.val_spot import validate_side, validate_time_in_force, validate_recv_window, \
    validate_new_order_resp_type


def get_new_order_default_options():
    return [
        {'params': ['-sy', '--symbol'], 'attrs': {'required': True, 'type': click.types.STRING}},
        {'params': ['-si', '--side'], 'attrs': {'required': True, 'callback': validate_side,
                                                'type': click.types.STRING}},
        {'params': ['-tif', '--time_in_force'], 'attrs': {'callback': validate_time_in_force,
                                                          'type': click.types.STRING}},
        {'params': ['-q', '--quantity'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-qoq', '--quote_order_qty'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-p', '--price'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-ncoid', '--new_client_order_id'], 'attrs': {'type': click.types.STRING}},
        {'params': ['-sp', '--stop_price'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-iq', '--iceberg_qty'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-rw', '--recv_window'], 'attrs': {'default': 5000, 'show_default': True,
                                                       'callback': validate_recv_window,
                                                       'type': click.types.INT}},
        {'params': ['-nort', '--new_order_resp_type'], 'attrs': {'default': "FULL", 'show_default': True,
                                                                 'callback': validate_new_order_resp_type,
                                                                 'type': click.types.STRING}},
    ]