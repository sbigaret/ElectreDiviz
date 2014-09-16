"""
ElectreCrispOutrankingRelation - 
Usage:
    ElectreCrispOutrankingRelation.py -i DIR -o DIR

Options:
    -i DIR     Specify input directory. It should contain the following files:
                   alternatives.xml
                   concordance.xml
                   discordance.xml
    -o DIR     Specify output directory. Files generated as output:
                   outranking.xml
                   message.xml
    --version  Show version.
    -h --help  Show this screen.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import traceback
from functools import partial

from algorithm import *

from docopt import docopt

from common import comparisons_to_xmcda, create_messages_file, get_dirs, \
    get_error_message, get_input_data, get_linear, omega, write_xmcda, Vividict

__version__ = '0.1.0'

def main():
    try:
    
        args = docopt(__doc__, version=__version__)
        output_dir = None
        input_dir, output_dir = get_dirs(args)
        
        filenames = [
            ('method_parameters.xml', False)
        ]
        params = [
            'comparison_with'
        ]
        
        d = get_input_data(input_dir, filenames, params)
        comparison_with = d.comparison_with
        
        profilesId = None
        
        if  comparison_with == "profiles":
            filenames = [
                ('alternatives.xml', False),
                ('profiles.xml', False),
                ('concordance.xml', False),
                ('discordance.xml', False),
            ]
            params = [
                'alternatives',
                'profiles',
                'concordance',
                'discordance',
            ]
            kwargs = {'use_partials': False, 'comparison_with': comparison_with}        
            d = get_input_data(input_dir, filenames, params, **kwargs)
                
            profilesId = d.profiles
            alternativesId = d.alternatives
            concordance = d.concordance
            discordance = d.discordance
        else:
            filenames = [
                ('alternatives.xml', False),
                ('concordance.xml', False),
                ('discordance.xml', False),
            ]
            params = [
                'alternatives',
                'concordance',
                'discordance',
            ] 
            kwargs = {'use_partials': False}              
            d = get_input_data(input_dir, filenames, params, **kwargs)
            
            alternativesId = d.alternatives
            concordance = d.concordance
            discordance = d.discordance
        
        alg = algorithm(alternativesId, profilesId, concordance, discordance)
        result = alg.Run()
        
        if profilesId == None:
            comparables = (alternativesId, alternativesId)
            xmcda = comparisons_to_xmcda(result, comparables)
            write_xmcda(xmcda, os.path.join(output_dir, 'outranking.xml'))
            create_messages_file(None, ('Everything OK.',), output_dir)
        else:
            comparables = (alternativesId, profilesId)
            xmcda = comparisons_to_xmcda(result, comparables, None, with_profile = True)
            write_xmcda(xmcda, os.path.join(output_dir, 'outranking.xml'))
            create_messages_file(None, ('Everything OK.',), output_dir)
 
        return 0
    
    except Exception, err:
        err_msg = get_error_message(err)
        log_msg = traceback.format_exc()
        print(log_msg.strip())
        create_messages_file((err_msg, ), (log_msg, ), output_dir)
        return 1            
        
           

if __name__ == '__main__':
    sys.exit(main())



