#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Max MORELLI <m.morelli.ext@intradef.gouv.fr>'
}

DOCUMENTATION = '''
---
module: klist

short_description: Ceci est un module permettant d'encapsuler facilement l'usage de la commande klist.

description:
    - " Le module liste les tickets Kerberos stockés dans le cache ou bien les clefs contenues dans un keytab"

options:
    filename:
        description:
        type: str
        required: false
    verbose:
        description:
        required: false
    time:
        description:
        required: false
    encrypt_type:
        description: 
        required: false
'''

RETURN = '''
ticket_list:
    description: La liste des tickets trouvés ou l'erreur specifiée
    type: str
message:
    description: Le message de sortie généré
    type: str
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess

class Keytab:

    def __init__( self, filename, time, encrypt_type ):
        self.filename = filename
        self.time = time
        self.encrypt_type = encrypt_type    
    
    def read( self ):

        if self.filename:

            if self.filename.endswith( ".keytab" ):

                if self.check_file() :
                    return self.run_cmd()
                else:
                    return False, 'Le fichier n\'a pas pu être trouvé'

            else:
                return False, 'Le fichier n\'est pas un keytab'
        else:
            return self.run_cmd()

    def run_cmd( self ):
        proc = subprocess.Popen(
            self.get_cmd(), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        output, errors = proc.communicate()
        if proc.returncode == 0 :
            return True, self.parsing_result( output.decode() )
        else :
            return False, errors

    def get_cmd( self ):
        cmd = [ "klist" ]
        if self.encrypt_type: 
            cmd.append( "-e" )
        if self.filename: 
            cmd.append( "-k" )
            cmd.append( self.filename ) 
            if self.time: 
                cmd.append( "-t" ) 
        return cmd

    def check_file( self ):
        try:
            with open( self.filename ):
                return True
        except IOError:
            return False
    
    def parsing_result( self, output ):
        return "{}"\
            .format( output )\
            .replace( "\t","" )\
            .split( "\n" )

module = AnsibleModule(
    argument_spec = dict(
        filename = dict( type='str', required=False ),
        time = dict( type='bool', required=False ),
        encrypt_type = dict( type='bool', required=False )
    ),
    supports_check_mode = False
)

keytab = Keytab( **module.params )

try: 
    r, m = keytab.read()
    if r:
        module.exit_json( 
            **{ 'ticket_list' : m }
        )
    else:
        module.fail_json( 
            msg = "Une erreur est survenue durant la commande klist", 
            **{ 'ticket_list' : m }
        )
except Exception as err:
    module.fail_json(
        msg = "une erreur inconnue est survenue: {}".format( err ) 
    )

