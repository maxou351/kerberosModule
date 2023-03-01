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
module: kinit

short_description: Ceci est un module permettant d'encapsuler facilement l'usage de la commande kinit.

description:
    - " Le module obtient et met en cache un ticket Kerberos ticket"

options:
    principal_name:
        description:
        type: str
        required: false
    realm_name:
        description:
        type: str
        required: false
    secret_key:
        description:
        type: str
        required: false
'''

RETURN = '''
ticket:
    description: 
    type: str
    returned: always
message:
    description: Le message de sortie généré
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess

def createTicket(user_name, realm_name, secret_key):
    parameters = ['kinit','-V',]
    if user_name:
        parameters.append( '{}@{}'.format( user_name, realm_name ) )
    proc = subprocess.Popen(
        parameters, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE, 
        shell = False
    )
    output, errors = proc.communicate( secret_key.encode() )
    if proc.returncode == 0 :
        return True, 'Authentification Kerberos OK'
    else :
        return False, parsing_result( errors.decode() )

def parsing_result(output):
    return '{}'\
        .format(output)\
        .replace( '\\n', ' ')\
        .replace( '\n', ' ')

module = AnsibleModule(
    argument_spec = dict(
        user_name = dict( type='str', required=False ),
        realm_name = dict( type='str', required=False ),
        secret_key = dict( type='str', required=False )
    ),
    supports_check_mode = False
)

try: 
    r, m = createTicket( **module.params )
    if r:
        module.exit_json( 
            **{ 'ticket' : m }
        )
    else:
        module.fail_json( 
            msg = "Une erreur est survenue durant la commande kinit", 
            **{ 'ticket' : m }
        )
except Exception as err:
    module.fail_json(
        msg = "une erreur inconnue est survenue: {}".format( err ) 
    )
