
#
# common functions for pbrun_* modules
#

import re

from subprocess import Popen, PIPE, STDOUT

import paramiko
from socket import gaierror
from time import sleep

_psw=""

def set_psw(psw):
    """
        Public function to store psw in a module variable.
        The stored value optionally can be used instead of supplying psw on each cell magic call
    """
    global _psw
    _psw=psw

def _parse_str_as_parameters(line):
    """
        Function to interpret cell magic "line" string as Python parameters (positional and keyword) 
        separated by spaces instead of commas
    """
    
    def _line_to_parameters(conn, psw="dummy", **kwargs):
        """
        helper function
        """
        if psw =="dummy":
            # if password not given then take it from global
            global _psw
            if _psw:
                psw=_psw
            else:
                raise Exception('Error! Password is not given.')
        
        if '@' in conn:
            user = conn.split('@')[0]
            host = conn.split('@')[1]
        else:
            raise Exception('Error! First line magic parameter should be in the form of user@host')
            
        #print(conn, user, host, psw, kwargs)
        return conn, user, host, psw, kwargs
   
    #
    # convert line from space-delimeted into comma-delimeted to mimic Python function parameter list
    #
    word_lst=line.split()
    #print(word_lst)
    # first argument is connection; surround it with quotes to make it a string parameter
    word_lst[0]='"' + word_lst[0] + '"'
    args_str=",".join(word_lst)
    #print(args_str)
    
    #
    # parse as parameters 
    #
    parse_call_str="_line_to_parameters(" + args_str + ")"
    #print(parse_call_str)
    return eval(parse_call_str)
    
def _add_oracle_env_variables(script, oracle_sid):
    """
        add Oracle environment setup to script
    """
    #script1= (f"newgrp oinstall\n"
    script1= (f"export ORACLE_SID={oracle_sid}\n"
              f'if [[ "`uname -s`" == "Linux" ]]\n'
              f"  then ORATAB=/etc/oratab\n"
              f'elif [[ "`uname -s`" == "AIX" ]]\n'
              f"  then ORATAB=/etc/oratab\n"
              f'elif [[ "`uname -s`" == "SunOS" ]]\n'
              f"  then ORATAB=/var/opt/oracle/oratab\n"
              f"fi\n"
              f"export ORACLE_HOME=`cat $ORATAB | grep $ORACLE_SID | cut -d: -f2`\n"
              f"export ORACLE_BASE=`echo $ORACLE_HOME | sed 's@/product.*$@@'`\n"
              f"PATH=$ORACLE_HOME/bin:$PATH\n"
             f"{script}")
    return script1

def _substitute_notebook_variables(script):
    """
      Substitute any Notebook variables inside not escaped curly braces.
      If curly braces were escaped with backslash then remove backslash.
      get_ipython().user_ns[] gives variable value
      
    """
    #
    # Substitute any Notebook variables inside not escaped curly braces.
    #
    ip=get_ipython()
    script1=re.sub(r"(?<=[^\\]){[^\\]*?}",
                   lambda x: ip.user_ns[x.group(0)[1:-1]],
                   script,
                   flags=re.MULTILINE)
    #
    # if curly braces were escaped with backslash then remove backslash
    #
    script2=re.sub(r"\\([{}])",
                   "\\1",
                   script1)
    return script2
   
def _substitute_single_quote(script):
    """
      Escape any single quote within script with sequence '\'' (quote-backslash-quote-quote)
      because "script" will be echo'ed in single quotes:
            echo '{script}' | pbrun su oracle -c 'bash -s'
    """
    script1=re.sub(r"'",
                   r"'\''",
                    script)
    return script1

def _remote_execute_stream_output(host, user, psw, cmd):
    #
    # establish connection
    #
    
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, 22, user, psw)
    #except (paramiko.SSHException, gaierror) as e:
    except (paramiko.SSHException, gaierror, TimeoutError) as e:
        print(f"AuthenticationException: {e}")
        ssh.close()
        return f"AuthenticationException: {e}"

    #
    # execute remote_script and stream output
    #
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    while True:
        while stdout.channel.recv_ready():
             line = stdout.readline()
             print(line.replace("\n",""), flush=True)
       
        if stdout.channel.exit_status_ready():
            lines=''.join(stdout.readlines())
            print(lines, flush=True)
            break
            
        # sleep to save on CPU
        sleep(0.2)
    #
    # append stderr after stdout
    #
    errlines=stderr.readlines()
    # remove two unexplainable errors 
    err=''.join([l for l in errlines if 'shell-init: error retrieving current directory' not in l
                                             and 'Command caught signal 15 (Terminated)' not in l])
    print(err, flush=True)
    
    ssh.close()
    
def _remote_execute_fn (host, user, psw, cmd, stderr_after_stdout=False):
    #
    # establish connection
    #
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, 22, user, psw)
    #except (paramiko.SSHException, gaierror) as e:
    except (paramiko.SSHException, gaierror, TimeoutError) as e:
        print(f"AuthenticationException: {e}")
        ssh.close()
        return f"AuthenticationException: {e}"
    #
    # execute remote_script
    #
    stdin, stdout, stderr = ssh.exec_command(cmd)

    outlines=stdout.readlines()
    out=''.join(outlines)
    
    errlines=stderr.readlines()
    # remove two unexplainable errors 
    err=''.join([l for l in errlines if 'shell-init: error retrieving current directory' not in l
                                             and 'Command caught signal 15 (Terminated)' not in l])
    ssh.close()
    
    if stderr_after_stdout:
        # append stderr after stdout
        return out+err
    else:
        return out

    # below if we want to stream output via returned generator
    # (but see how streaming is done in _remote_execute_stream_output, as it uses sleep to save on CPU)
    #while True:
    #    if stdout.channel.recv_ready():
    #        line = stdout.readline()
    #        yield line.replace("\n","")
    #
    #    if stdout.channel.exit_status_ready():
    #        if stdout.channel.recv_ready():
    #            lines=''.join(stdout.readlines())
    #            yield lines
    #        ssh.close()
    #        break
