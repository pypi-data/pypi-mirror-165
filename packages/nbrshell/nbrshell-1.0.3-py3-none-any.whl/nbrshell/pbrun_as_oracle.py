'''
    This module defines Jupyter Notebook cell magic to remotely execute a shell script via pbrun as oracle account.
    The cell content is expected to be a complete shell script.
    A Remote ssh connection is established using password, passed as a parameter on the magic line.
    Once connected, the script is executed via pbrun as oracle run user.
    Normal Oracle environment variables like ORACLE_HOME etc are set up according to SID passed as a parameter.
    The pbrun infrastructure and permissions on remote server are assumed to have already been set up.
    The cell magic will stream output.
    
    Usage examples: 
    
        In: %%pbrun_as_oracle user@host oracle_sid=ORCL1
    
            date
            hostname
            id
            env | egrep "ORACLE|PATH"
    
            echo "select sysdate from dual;" | sqlplus / as sysdba
    
            sqlplus / as sysdba @/dev/stdin <<-EOF
                set echo on
                select 'aaa' from v\$instance;
            EOF
    
            ping -s www.google.com 56 10
    
    
    As regular python function. 
    The function does not stream output, i.e. output does not appear until script finishes.
    
        from pbrun_as_oracle import pbrun_as_oracle_fn
        shell_cmd="""
            date
            hostname
            id
            env | grep ORACLE
            echo "select sysdate from dual;" | sqlplus / as sysdba
            ping -s www.google.com 56 10
        """
        out=pbrun_as_oracle_fn("user@host password ORACLE_SID", shell_cmd)
'''

from IPython.core.magic import (register_cell_magic, needs_local_scope)

# import common functions
from . import nbrshell_common as cmn

@register_cell_magic
def pbrun_as_oracle(line, script):
    """
        This is a cell magic function 
        to execute cell content as a bash script on a remote host 
        after becoming oracle with pbrun and setting some common Oracle environment variables 
        (ORACLE_SID, ORACLE_HOME, PATH).
        
        It uses paramiko as ssh client with password authentication so that prior key setup is not needed.
        
        Parameter "line" should be in the form of "user@host [psw=<password>] [oracle_sid=<sid>] [debug=True]`" 
        where only 'user@host' is mandatory positional parameter. 
        Password may be either positional or keyword.
        If password is not given then it is assumed to have been stored with nbrshell_common.set_psw(password).
        Remaining parameters are optional keyword parameters.
        
        Examples of valid "line" formats:
            user@host
            user@host some_password
            user@host r'some_password'       # when password has special characters
            user@host psw='some_password'
            user@host some_password oracle_sid='DB1'
            user@host some_password oracle_sid='DB1' debug=True
            user@host debug=True
        
        If "debug" is given then it will print script text after performing all substitutions 
        before sending it for remote execution.
        
        Substitutions performed prior to sending script for remote execution: 
            - any Notebook variable inside curly braces.
              Therefore if any curly brace is part of the shell script, it needs to be backslash escaped.
              
            - single quotes. This is necessary because the script is sent for remote execution using below construct:
                    "cd /tmp; echo '{script}' | pbrun su {pbrun_user} -c 'bash -s'"
              Single quotes inside "script" are substituted with "quote-bakslash-quote-quote" sequence.
              Example: "echo 'aaa'" becomes "echo '\''aaa'\''"
    """

    # parse parameters
    conn, user, host, psw, kwargs = cmn._parse_str_as_parameters(line)
       
    # if oracle_sid was not passed then set it to "dummy_sid"
    oracle_sid = kwargs.get('oracle_sid', "dummy_sid")
    
    # debug default is False
    debug = kwargs.get('debug', False)
    
    #print(conn, user, host, psw, oracle_sid, debug, kwargs)
    
    # substitute notebook variables
    script1 = cmn._substitute_notebook_variables(script)
    
    # add oracle env variables
    script2 = cmn._add_oracle_env_variables(script1, oracle_sid)
    
    # substitute single quotes
    script3 = cmn._substitute_single_quote(script2)
    
    # form pbrun script 
    cmd=f"cd /tmp; echo '{script3}' | pbrun su oracle -c 'bash -s'"
        # alternatively:
        #   cmd=f"echo $'{script3}' | pbrun -u oracle bash -s"
        #       -- this sets uid to oracle, but not group
        #       -- on Solaris group can be set newgrp in the script
        #       -- but on Exadata with Oracle Linux newgrp does not change group
        #       -- therefore this syntax can not be used there
        #       -- Instead "pbrun su - oracle 'bash -s'" is used, since it sets both uid to oracle and group to oinstall
        #
        # alternatively:
        #   cmd=(f"pbrun -u oracle bash -s <<-EOF\n"
        #        f"{script3}\n"
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
