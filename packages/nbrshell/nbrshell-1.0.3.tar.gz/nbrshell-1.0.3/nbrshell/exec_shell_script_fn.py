
# import common functions
from . import nbrshell_common as cmn

def exec_shell_script_fn(conn, psw="dummy", pbrun_user="", debug=False, script="", stderr_after_stdout=False):
    """
        This is functional eqiuvalent of cell magic 'exec_shell_script', with following differences:
            - regular function with no magic decorator.
            - returns output instead of printing.
            - does not stream and will block until remote script finishes.
            - does not attempt to substitute Notebook variables inside curly braces.
              all necessary substitutions should be done by a caller.
            - parameter stderr_after_stdout controls if stderror will be appended to stdout
    """
    if ('@' not in conn):
        print('Usage: exec_shell_script_fn( user@host, [psw], [debug], [script], [stderr_after_stdout]')
        return

    if psw=="dummy":
        # get password from cmn module
        if cmn._psw:
            psw=cmn._psw
        else:
            raise Exception('Error! Password is not given.')
        
    user = conn.split('@')[0]
    host = conn.split('@')[1]

    # substitute single quotes
    script1=cmn._substitute_single_quote(script)
       
    # form pbrun script 
    cmd=f"echo '{script1}' | bash -s"
        # alternative form:
        #       cmd=(f"bash -s <<-EOF\n"
        #            f"{script1}\n"
        #             "EOF")
        # 
        # alternative form:
        #       cmd="echo $'{script1}' | bash -s"
        #       -- this sets uid to oracle, but not group
        #       -- on Solaris there is workaround of setting group with newgrp in the script
        #       -- but on Exadata with Oracle Linux newgrp does not change group
        #       -- therefore this syntax can not be used on Exadata
        #       -- Instead "echo '{script1}' | pbrun su oracle -c 'bash -s'" is used, since it sets both uid to oracle and group to oinstall
        #
        
    # print final script for debugging
    if debug:
        print(f"Executing script on {conn}:")
        print("======== script-start ============")
        print(cmd)
        print("========= script-end =============")
        
    # remote execute and return output
    return cmn._remote_execute_fn (host, user, psw, cmd, stderr_after_stdout)

    
