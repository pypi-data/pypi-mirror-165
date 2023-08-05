#
# This module defines Jupyter Notebook cell magic to remotely execute a shell script.
# The cell content is expected to be a complete shell script.
# Paramiko ssh client is used to establish a remote ssh connection using password passed as a parameter on the magic line.
# Once connected, the script is executed.
# The cell magic will stream output.
# 
# Usage examples: 
#
#       In: from nbrshell import exec_shell_script
#
#       In: %%exec_shell_script <user>@<host> <password>
#
#           date
#           hostname
#           id
#           ping -s www.google.com 56 10
#
# Alternatively password can be set in memory and then reused in multiple cells without specifying password on each call:
#       In: from nbrshell import pbrun_as, set_psw
#       set_psw(<password>)    
#
#       In: %%exec_shell_script <user>@<host>
#
#           date
#           hostname
#           id
#           ping -s www.google.com 56 10
#

from IPython.core.magic import (register_cell_magic, needs_local_scope)

# import common functions
from . import nbrshell_common as cmn

@register_cell_magic
def exec_shell_script(line, script):
    """
        This is a cell magic function 
        to execute cell content as a bash script on a remote host 
        
        It uses paramiko as ssh client with password authentication so that prior key setup is not needed.
        
        Parameter "line" should be in the form of "user@host [psw=<password>] [debug=True]`" 
        where "user@host" is mandatory positional parameter. 
        Password may be either positional or keyword.
        If password is not given then it is assumed to have been previously stored with nbrshell_common.set_psw(password).
        "debug" is optional keyword parameter.
        
        Examples of valid "line" formats:
            user@host psw='some_password'
            user@host psw='some_password' debug=True
            user@host pbrun_user="user2"     # when password was previoulsy set up with set_nbrshell_psw()
        
        If "debug" is given then it will print script text after performing all substitutions 
        before sending it for remote execution.
        
        Substitutions performed prior to sending script for remote execution: 
            - any Notebook variable inside curly braces.
              Therefore if any curly brace is part of the shell script, it needs to be backslash escaped.
              
            - single quotes. This is necessary because the script is sent for remote execution using below construct:
                    "echo '{script}' | pbrun su {pbrun_user} -c 'bash -s'"
              Single quotes inside "script" are substituted with "quote-bakslash-quote-quote" sequence.
              Example: "echo 'aaa'" becomes "echo '\''aaa'\''"
    """

    # parse parameters
    conn, user, host, psw, kwargs = cmn._parse_str_as_parameters(line)

    # debug default is False
    debug = kwargs.get('debug', False)
    
    #print(conn, user, host, psw, oracle_sid, debug, kwargs)
    
    # substitute notebook variables
    script1 = cmn._substitute_notebook_variables(script)
    
    # substitute single quotes
    script2 = cmn._substitute_single_quote(script1)
    
    # form pbrun script 
    cmd=f"echo '{script2}' | bash -s"
        # alternatively:
        #   cmd=f"echo $'{script2}' | bash -s"
        #       -- this sets uid to oracle, but not group
        #       -- on Solaris group can be set newgrp in the script
        #       -- but on Exadata with Oracle Linux newgrp does not change group
        #       -- therefore this syntax can not be used there
        #       -- Instead "pbrun su oracle -c 'bash -s'" is used, since it sets both uid to oracle and group to oinstall
        #
        # alternatively:
        #   cmd=(f"bash -s <<-EOF\n"
        #        f"{script2}\n"
        #         "EOF")
        #

    # print the final script for debugging
    if debug:
        print(f"Executing script on {conn}:")
        print("======== script-start ============")
        print(cmd)
        print("========= script-end =============")

    # remote execute
    cmn._remote_execute_stream_output(host, user, psw, cmd)
