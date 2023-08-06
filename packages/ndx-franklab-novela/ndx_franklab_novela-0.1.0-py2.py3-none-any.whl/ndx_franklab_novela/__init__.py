import os

from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location

ndx_franklab_novela_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-franklab-novela.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_franklab_novela_specpath):
    ndx_franklab_novela_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-franklab-novela.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_franklab_novela_specpath)

AssociatedFiles = get_class('AssociatedFiles', 'ndx-franklab-novela')
CameraDevice = get_class('CameraDevice', 'ndx-franklab-novela')
DataAcqDevice = get_class('DataAcqDevice', 'ndx-franklab-novela')
HeaderDevice = get_class('HeaderDevice', 'ndx-franklab-novela')
NwbElectrodeGroup = get_class('NwbElectrodeGroup', 'ndx-franklab-novela')
Probe = get_class('Probe', 'ndx-franklab-novela')
Shank = get_class('Shank', 'ndx-franklab-novela')
ShanksElectrode = get_class('ShanksElectrode', 'ndx-franklab-novela')

# define aliases to maintain backward compatibility
Probe.add_shank = Probe.add_shanks
Probe.get_shank = Probe.get_shanks
Shank.add_shanks_electrode = Shank.add_shanks_electrodes
Shank.get_shanks_electrode = Shank.get_shanks_electrodes
