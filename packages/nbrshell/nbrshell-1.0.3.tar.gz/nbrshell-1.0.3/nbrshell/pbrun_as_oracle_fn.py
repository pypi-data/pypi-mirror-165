
# import common functions
from . import nbrshell_common as cmn

def pbrun_as_oracle_fn(conn, psw="dummy", oracle_sid="dummy", debug=False, script="", stderr_after_stdout=False):
    """
        This is functional eqiuvalent of cell magic 'pbrun_as_oracle', with following differences:
            - regular function with no magic decorator.
            - returns output instead of printing.
            - does not stream and will block until remote script finishes.
            - does not attempt to substitute Notebook variables inside curly braces.
              all necessary substitutions should be done by a caller.
            - parameter stderr_after_stdout controls if stderror will be appended to stdout
    """
    if ('@' not in conn) :
        print('Usage: pbrun_as_oracle_fn(user@host [psw] [oracle_sid] [debug], script, [stderr_after_stdout]')
        return

    if psw=="dummy":
        # get password from cmn module
        if cmn._psw:
            psw=cmn._psw
        else:
            raise Exception('Error! Password is not given.')
        
    user = conn.split('@')[0]
    host = conn.split('@')[1]

    # add oracle env variables
    script1=cmn._add_oracle_env_variables(script, oracle_sid)

    # substitute single quotes
    script2=cmn._substitute_single_quote(script1)
       
    # form pbrun script 
    cmd=f"cd /tmp; echo '{script2}' | pbrun su oracle -c 'bash -s'"
        # alternative form:
        #       cmd=(f"pbrun -u oracle bash -s <<-EOF\n"
        #            f"{script2}\n"
        #             "EOF")
        # 
        # alternative form:
        #       cmd="echo $'{script2}' | pbrun -u oracle bash -s"
        #       -- this sets uid to oracle, but not group
        #       -- on Solaris there is workaround of setting group with newgrp in the script
        #       -- but on Exadata with Oracle Linux newgrp does not change group
        #       -- therefore this syntax can not be used on Exadata
        #       -- Instead "echo '{script2}' | pbrun su oracle -c 'bash -s'" is used, since it sets both uid to oracle and group to oinstall
        #
        
    # print final script for debugging
    if debug:
        print(f"Executing script on {conn}:")
        print("======== script-start ============")
        print(cmd)
        print("========= script-end =============")
        
    # remote execute and return output
    return cmn._remote_execute_fn (host, user, psw, cmd, stderr_after_stdout)

    
