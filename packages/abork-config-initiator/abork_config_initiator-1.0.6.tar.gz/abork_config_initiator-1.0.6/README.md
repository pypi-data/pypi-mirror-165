

# Config Initiator

This module checks if there is a configuration file of certain format. If not a file will be created and a exception is thrown to let the user know, that those have to be populated.

## How to use

    from py_config_initiator import ConfigInitiator

    ConfigInitiator(<folderpath_to_check_for_config>).set_template(<list=|string=>).check()
