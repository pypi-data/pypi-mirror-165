#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a program written by Claudia Millan
# E-mail cmncri@ibmb.csic.es

# Import libraries
# Future imports
from __future__ import print_function
from __future__ import unicode_literals

# Python Modules
from builtins import range
from future import standard_library
standard_library.install_aliases()
import configparser
import collections
import io
import os
import shutil
import sys
import time
from multiprocessing import Pool
from termcolor import colored

# Our own modules
import alixe_library as al

def main():
    command_line= False
    now = time.time()
    head1 = """
                                         ___       __       __  ___   ___  _______ 
                                        /   \     |  |     |  | \  \ /  / |   ____|
                                       /  ^  \    |  |     |  |  \  V  /  |  |__   
                                      /  /_\  \   |  |     |  |   >   <   |   __|  
                                     /  _____  \  |  `----.|  |  /  .  \  |  |____ 
                                    /__/     \__\ |_______||__| /__/ \__\ |_______|
        """

    print(colored(head1, 'cyan'))
    print("""
           Institut de Biologia Molecular de Barcelona --- Consejo Superior de Investigaciones Cientificas
                             I.B.M.B.                                            C.S.I.C.

                                                 Department of Structural Biology
                                                 Crystallographic Methods Group
                                  http://www.sbu.csic.es/research-groups/crystallographic-methods/

        In case this result is helpful, please, cite:

        ALIXE: a phase-combination tool for fragment-based molecular replacement. 
        C. Millan, E. Jimenez, A. Schuster, K. Diederichs and I. Uson.
        Acta Cryst. D76: (2020) (doi:10.1107/S205979832000056X)
        
        Combining phase information in reciprocal space for molecular replacement with partial models. 
        C. Millan, M. Sammito, I. Garcia-Ferrer, T. Goulas, G. M. Sheldrick and I. Uson.
        Acta Cryst. D71: 1931-1945 (2015) (doi:10.1107/S1399004715013127)
        
        """)
    print("Email support: ", colored("bugs-borges@ibmb.csic.es", 'blue'))
    print("\nALIXE website: ", colored("http://chango.ibmb.csic.es/alixe", 'blue'))
    print("\n")
    # Reading input from command line / bor
    if len(sys.argv) == 1:
        print("\nUsage: ")
        print("\nTo generate an example of configuration file: ALIXE.py -f name_conf.bor")
        print("\nTo run with a configuration file: ALIXE.py name_conf.bor ")
        print("\nTo run by command line:",
              "\n ALIXE.py -m mode -i input_folder or arcimboldo_bor "
              "\n optional depending on data in input_folder -d hkl_file -s pdb_symmetry"
              "\n optional -o name_output_folder"
              )
        sys.exit(0)
    elif len(sys.argv) == 2:  # then it is an ALIXE configuration file
        path_alibor = sys.argv[1]
        # Defaults are found in al.defaults_alixe
        Config = configparser.ConfigParser()
        # Read the defaults first
        Config.readfp(io.StringIO(al.defaults_alixe))
        # Now include whatever found in the user's bor file (we should validate it)
        Config.read(path_alibor)
        path_merged_bor = 'temp.bor'
        file_merged_bor = open(path_merged_bor,'w')
        Config.write(file_merged_bor)
        del file_merged_bor
        ali_confdict = al.read_confibor_alixe(path_merged_bor)
        os.remove(path_merged_bor)
    elif len(sys.argv) == 3: # check the -f
        if sys.argv[1] == '-f':
            try:
                f = open(sys.argv[2], "w")
                f.write(al.defaults_alixe)
                f.close()
            except:
                # print the traceback
                print('Some error while writing the configuration file')
                sys.exit(1)
            sys.exit(0)
    else:   # Then it must be command line
        command_line=True
        alixe_mode, alixe_input_info, hkl_filepath, path_sym, output_folder, fragment = '','','','','', ''
        for indi in range(1,len(sys.argv)):
            if sys.argv[indi] == '-m':
                alixe_mode=sys.argv[indi+1]
            if sys.argv[indi] == '-i':
                alixe_input_info=sys.argv[indi+1]
            if sys.argv[indi] == '-d':
                hkl_filepath = sys.argv[indi+1]
            if sys.argv[indi] == '-s':
                path_sym = sys.argv[indi + 1]
            if sys.argv[indi] == '-o':
                output_folder = sys.argv[indi + 1]
            if sys.argv[indi] == '-f':
                fragment = sys.argv[indi + 1]
            # add fragment option too for the postmortem
        ali_confdict = al.generate_minimal_ali_confdict_from_mode_and_input(alixe_mode, alixe_input_info,
                                                                            hkl_filepath, path_sym, output_folder, fragment)


    # Automatically set the chescat path
    if sys.platform == "darwin":
        path_chescat = os.path.join(os.path.dirname(__file__), "executables/chescat_mac")
    else:
        path_chescat = os.path.join(os.path.dirname(__file__), "executables/chescat_linux")
    ali_confdict['path_chescat'] = path_chescat


    # Validate ali_confdict
    folder_mode, ali_confdict = al.validate_confdict_alixe(ali_confdict)

    list_tuples_pools = []
    PoolTup = collections.namedtuple('PoolTup', 'key_input_info sub_clust_key sub_clust_path')
    if not folder_mode:
        # General structure, as many bors as given
        for i in range(ali_confdict['n_pools']):
            # Save the names and paths for the pools for later steps
            keyinputinfo = 'input_info_' + str(i + 1)
            sub_clust_key = 'clustpool_' + str(i + 1)
            sub_clust_path = os.path.join(ali_confdict['output_folder'], sub_clust_key)
            new_tuple = PoolTup(key_input_info=keyinputinfo, sub_clust_key=sub_clust_key, sub_clust_path=sub_clust_path)
            list_tuples_pools.append(new_tuple)
            # Read the bor file from the ARCIMBOLDO run
            config_obj_arci = configparser.ConfigParser()
            config_obj_arci.read(ali_confdict[keyinputinfo])
            # Generate the clustering folder for this particular pool
            al.check_dir_or_make_it(sub_clust_path, remove=True)
            # Get the computing info from one of them, e.g. the first (I just need one)
            if i == 0:
                # I only need the computing info to get the shelxe path, so if it is already present, I should not call this
                if 'shelxe_path' not in ali_confdict:
                    ali_confdict = al.get_computing_info_for_alixe(config_obj_arci, ali_confdict)
                ali_confdict = al.get_general_paths_for_alixe(config_obj_arci, ali_confdict)
                if 'ent_file' in ali_confdict.keys() and command_line:
                    ali_confdict['postmortem'] = True

            # NOTE CM: I am HERE, now need to modify the function of the arcirun
            # in order to prepare each folder separatedly
            al.link_file(folder_for_link=sub_clust_path, path_orifile=ali_confdict['hkl_file'],
                         name_link='reflection.hkl')
            if 'ent_file' in ali_confdict.keys() and ali_confdict['postmortem']:
                al.link_file(folder_for_link=sub_clust_path, path_orifile=ali_confdict['ent_file'],
                             name_link="final_solution.ent")
            else:
                ali_confdict['postmortem'] = False # if there is no ent file I can't do postmortem
            ali_confdict = al.get_arcirun_info_for_alixe(config_obj_arci, ali_confdict, sub_clust_path)
            ali_confdict[sub_clust_path]['compute_phs'] = False
    else:  # Folder mode, no previous info from the solutions in principle
        # General structure, as many folders as given
        for i in range(ali_confdict['n_pools']):
            keyinputinfo = 'input_info_' + str(i + 1)
            sub_clust_key = 'clustpool_' + str(i + 1)
            sub_clust_path = os.path.join(ali_confdict['output_folder'], sub_clust_key)

            # initialise the dictionary for this clustering folder
            ali_confdict[sub_clust_path]={}

            new_tuple = PoolTup(key_input_info=keyinputinfo, sub_clust_key=sub_clust_key, sub_clust_path=sub_clust_path)
            list_tuples_pools.append(new_tuple)
            al.check_dir_or_make_it(sub_clust_path, remove=True)
            # list files to understand whether PDBs only or phs files or pda or a mix
            list_input_files = os.listdir(ali_confdict[keyinputinfo])
            list_phs = []
            list_pdb = []
            for inp in list_input_files:
                fullpathinp = os.path.join(ali_confdict[keyinputinfo], inp)
                fullpathclu = os.path.join(sub_clust_path, inp)
                shutil.copy(fullpathinp, fullpathclu)
                if inp.endswith('.phs') or inp.endswith('.phi'):
                    list_phs.append(fullpathclu)
                elif inp.endswith('.pdb') or inp.endswith('.pda'):
                    list_pdb.append(fullpathclu)
            if len(list_phs) == 0:
                # Then we need to compute the phs out of the pdb files
                ali_confdict[sub_clust_path]['compute_phs'] = True
            else:
                ali_confdict[sub_clust_path]['compute_phs'] = False

            # Check that if we are going to run SHELXE we do have the required files
            if ali_confdict[sub_clust_path]['compute_phs']:
                if 'hkl_file' not in ali_confdict:
                    al.print_message_and_log("You have not provided a valid hkl file to compute the phs files out of your solutions",
                                             ali_confdict['log'], 'Error')
                    sys.exit(0)

            # We need to set the information required in folder mode that is not available, like we do in bor mode

            # Checking for postmortem analysis
            # NOTE CM: at the moment only with alixe bor mode, not in minimal case
            if 'ent_file' in ali_confdict.keys() and ali_confdict['postmortem']:
                print("\n *Info* You have an ent file, a post-mortem analysis of MPE will be performed")
                al.link_file(folder_for_link=sub_clust_path, path_orifile=ali_confdict['ent_file'],
                             name_link="final_solution.ent")
                ali_confdict['shelxe_line_alixe'] = ali_confdict['shelxe_line_alixe']+' -x'


    dictio_fragments = {}
    if not folder_mode:
        # Now, depending on the type of run in the case of ARCIMBOLDO input:
        # check if there is space in the disk for the run
        # get the files
        # change their names
        # and link them to the clustering folder
        # Again, general, as many runs as we have set
        for i, ele in enumerate(list_tuples_pools):
            keyinputinfo, sub_clust_key, sub_clust_path = ele[0], ele[1], ele[2]
            print(' * Info * Working on ',sub_clust_path )
            output_size, free = al.size_prediction(wd=ali_confdict[sub_clust_path]["wd_run"],
                                                   type_run=ali_confdict[sub_clust_path]["type_run"],
                                                   ali_confdict=ali_confdict,
                                                   folder_mode=folder_mode,
                                                   hard_limit_phs=ali_confdict['limit_sol_per_rotclu'])
            if free < output_size:
                print('\n * Warning * you do not have enough free space in disk to run ALIXE')
                sys.exit(1)
                # or activate a different minimal version
            elif free > output_size:
                print(
                    '\n * Info * Enough disk space. ALIXE will start now and for this run it will occupy about %d MB of free space \n' % (
                            output_size // 2 ** 20))

            if ali_confdict[sub_clust_path]['type_run'] == 'ARCIMBOLDO':
                print('Getting the files from the fragment ', ali_confdict['fragment'], ' of an ARCIMBOLDO_LITE run')
                dict_sorted_input = al.get_files_from_ARCIMBOLDO_for_ALIXE(wd=ali_confdict[sub_clust_path]['wd_run'],
                                                                           clust_fold=sub_clust_path,
                                                                           fragment=ali_confdict['fragment'],
                                                                           hard_limit_phs=ali_confdict[
                                                                               'limit_sol_per_rotclu'])
                list_id_rotclu = dict_sorted_input.keys()
            elif ali_confdict[sub_clust_path]['type_run'] == "BORGES":
                print('Getting the files from a BORGES run')
                fragment = 1
                dict_sorted_input = {}
                list_id_rotclu=[]
                for id_clu in os.listdir(os.path.join(ali_confdict[sub_clust_path]['wd_run'], '9_EXP')):
                    print("Getting files from rotation cluster ", id_clu)
                    list_id_rotclu.append(id_clu)
                    # NOTE CM: Only the rigid body refined solutions are taken in the case of BORGES runs (mode=9)
                    dict_sorted_input[id_clu] = al.get_files_from_9_EXP_BORGES(wd=ali_confdict[sub_clust_path]['wd_run'],
                                                                               clust_fold=sub_clust_path,
                                                                               cluster_id=id_clu, mode=9,
                                                                               hard_limit_phs=ali_confdict[
                                                                                   'limit_sol_per_rotclu'])

            print("\nCompleted linking of files in ", sub_clust_path)

            list_pdbs = al.list_files_by_extension(sub_clust_path, 'pda')
            if i == 0:
                # Getting the symmetry information and setting up the files needed
                # NOTE CM: This is just performed on the first iteration
                # NOTE CM: This means that if we ever attempt with different datasets
                # and the symmetry changes slightly we should change this
                ali_confdict['path_sym'] = list_pdbs[0]
                ali_confdict = al.generate_sym_data(ali_confdict['path_sym'], ali_confdict, sub_clust_path)

            dictio_fragments = al.fill_dictio_fragments(dictio_fragments=dictio_fragments, sub_clust_key=sub_clust_key,
                                                        sub_clust_path=sub_clust_path, list_pdbs=list_pdbs,
                                                        list_rotclu=list_id_rotclu,ali_confdict=ali_confdict)

            # Generate the list of rotation clusters that are available for clustering in the pool
            list_rot_cluster = al.get_list_rotation_clusters_from_dictio_fragments(dictio_fragments, sub_clust_key)
            ali_confdict[sub_clust_path]['list_rotation_clusters'] = list_rot_cluster

            # Save information about FOMs of fragments in a file that is readable as a table
            al.write_info_frag_from_dictio_frag(dictio_fragments=dictio_fragments, clust_fold=sub_clust_path,
                                                keypool=sub_clust_key, ali_confdict=ali_confdict)

            # If plotting option is active, prepare plots describing the solutions
            if ali_confdict['plots']:
                al.plots_info_frag(path_files=sub_clust_path, ali_confdict=ali_confdict, folder_mode=folder_mode)


    else:
        # FOLDER MODE CASE
        for i, ele in enumerate(list_tuples_pools):
            keyinputinfo, sub_clust_key, sub_clust_path = ele[0], ele[1], ele[2]
            output_size, free = al.size_prediction(wd=ali_confdict[keyinputinfo],
                                                               type_run=None,
                                                               ali_confdict=ali_confdict,
                                                               folder_mode=folder_mode,
                                                               hard_limit_phs=ali_confdict['limit_sol_per_rotclu'])

            if free < output_size:
                print('\n * Warning * you do not have enough free space in disk to run ALIXE')
                sys.exit(1)
                # or activate a different minimal version
            elif free > output_size:
                print(
                    '\n * Info * Enough disk space. ALIXE will start now and for this run it will occupy about %d MB of free space \n' % (
                            output_size // 2 ** 20))

            list_rot_cluster = ['0']  # just a dummy id, the same for all of them
            ali_confdict[sub_clust_path]['list_rotation_clusters'] = list_rot_cluster
            dictio_fragments[sub_clust_key] = {}
            if ali_confdict[sub_clust_path]['compute_phs']: # then we are sure we have pda or pdbs files
                # Check if pda or pdbs
                list_pdas = al.list_files_by_extension(sub_clust_path, 'pda')
                list_pdbs = al.list_files_by_extension(sub_clust_path, 'pdb')
                if len(list_pdbs)>0:
                    # then we need to convert those pdbs to pdas
                    al.get_pdas_for_all_pdbs(sub_clust_path)
                    list_pdbs = al.list_files_by_extension(sub_clust_path, 'pda')

                # Check if we had the path to the symmetry info defined
                if not ('path_sym' in ali_confdict) or ali_confdict['path_sym'] == '':
                    # Check cryst cards and get symmetry info
                    returncheck = al.check_cryst_cards_folder_mode(list_pdbs, 0.2)
                    if returncheck: # we can safely assume that we can extract the symmetry from any of the pdbs
                        ali_confdict['path_sym'] = list_pdbs[0]
                    else: # Then we print a warning and exit
                        print('\n *Error* The CRYST1 records from the pdb files given differ too much, please check')
                        sys.exit()
                # By now he have set it up correctly
                ali_confdict = al.generate_sym_data(ali_confdict['path_sym'], ali_confdict, sub_clust_path)
                if ('hkl_file' not in ali_confdict) or ali_confdict['hkl_file'] == '':
                    print('\n *Error* You need to provide an hkl file trough the configuration')
                    sys.exit()
                al.get_links_for_all(sub_clust_path, ali_confdict['hkl_file'][:-4],'pda', 'hkl')
                if 'ent_file' in ali_confdict.keys():
                    al.get_links_for_all(sub_clust_path, ali_confdict['ent_file'][:-4],'pda', 'ent')
                if not 'shelxe_line_alixe' in ali_confdict:
                    ali_confdict['shelxe_line_alixe'] = '-m5 -a0'
                    # al.print_message_and_log("You need to provide the keyword shelxe_line_alixe", ali_confdict['log'], 'Error')
                    # sys.exit(1)
                if not 'shelxe_path' in ali_confdict:
                    al.print_message_and_log("You need to provide the keyword shelxe_path", ali_confdict['log'], 'Error')
                    sys.exit(1)
                al.phase_all_in_folder_with_SHELXE(linea_arg=ali_confdict['shelxe_line_alixe'], dirname=sub_clust_path,
                                                   shelxe_path=ali_confdict['shelxe_path'], n_cores=ali_confdict['number_cores_parallel'],
                                                   dir_log=ali_confdict['log'],check_if_solved=False)

                # Now we could get information back from these shelxe runs
                for pdb in list_pdbs:
                    dictio_fragments[sub_clust_key][pdb[:-4]] = {'rot_cluster': None, 'llg': None, 'zscore': None,
                                                                 'initcc': None, 'efom': None, 'pseudocc': None,
                                                                 'list_MPE': None}
                # FOMs from lst files
                if ali_confdict['alixe_mode'] != 'postmortem':
                    dictio_fragments = al.get_FOMs_from_lst_files_in_folder(dictio_fragments=dictio_fragments,
                                                                            ali_confdict=ali_confdict,
                                                                            keypool=sub_clust_key,
                                                                            remove_after=True,
                                                                            write_shifted_to_ent=False)
                else:
                    dictio_fragments = al.get_FOMs_from_lst_files_in_folder(dictio_fragments=dictio_fragments,
                                                                            ali_confdict=ali_confdict,
                                                                            keypool=sub_clust_key,
                                                                            remove_after=True,
                                                                            write_shifted_to_ent=True)
                    #Note Eli: Add size prediction info in postmortem mode.
                    output_size, free, disk_space = al.size_prediction(wd=ali_confdict[sub_clust_path]["wd_run"],
                                                                       type_run=ali_confdict[sub_clust_path]["type_run"],
                                                                       ali_confdict=ali_confdict,
                                                                       folder_mode=folder_mode,
                                                                       hard_limit_phs=ali_confdict['limit_sol_per_rotclu'])


                # Save information about FOMs of fragments in a file that is readable as a table
                # TODO CM: This function must have the option to write a table without any Phaser FOM
                # al.write_info_frag_from_dictio_frag(dictio_fragments=dictio_fragments, clust_fold=sub_clust_path,
                #                                     keypool=sub_clust_key, ali_confdict=ali_confdict)
                # If plotting option is active, prepare plots describing the solutions
                # if ali_confdict['plots']:
                #     al.plots_info_frag(path_files=sub_clust_path, ali_confdict=ali_confdict, folder_mode=folder_mode)

            else: # Then they are phs and we cannot get a lot of the information, and we need to have set the symmetry
                if ('path_sym' not in ali_confdict) or ali_confdict['path_sym'] == '':
                    print('\n *Error* You need to provide a file for the symmetry path_sym trough the configuration')
                    sys.exit()
                else:
                    ali_confdict = al.generate_sym_data(ali_confdict['path_sym'], ali_confdict, sub_clust_path)
                    ali_confdict['fusedcoord'] = False #Note Eli: pda cannot be shifted if there are not pdas.



    #######################################
    # Modes of autoalixe: core algorithms #
    #######################################
    if ali_confdict['alixe_mode'] == 'fish':
        for i, ele in enumerate(list_tuples_pools):
            keyinputinfo, sub_clust_key, sub_clust_path = ele[0], ele[1], ele[2]
            dict_clust_by_rotclu = {}
            dict_clust_by_rotclu['0'] = {} # dummy id for the output
            phs_files = al.list_files_by_extension(path=sub_clust_path, extension='phs', fullpath=False)
            # Checking references
            if os.path.isdir(ali_confdict['references']):
                # Check if pda,pdbs or phs
                list_fichis = al.list_files_by_extension(path=ali_confdict['references'], extension='phs', fullpath=True)
                type_file = 'phs'
                if not list_fichis:
                    list_fichis = al.list_files_by_extension(path=ali_confdict['references'], extension='pdb', fullpath=True)
                    type_file = 'pdb'
                    if not list_fichis:
                        list_fichis = al.list_files_by_extension(path=ali_confdict['references'], extension='pda', fullpath=True)
                        type_file = 'pda'
            else:
                if os.path.exists(ali_confdict['references']): # single reference file
                    list_fichis = [ali_confdict['references']]
                    type_file = ali_confdict['references'][-3:]
            total_references = len(list_fichis)
            print('\n*****************************************************************************************')
            print('\n The number of cores available to use in the fishing parallel mode will be ',
                  ali_confdict['number_cores_parallel'])
            print('\n The number of references to attempt will be ', total_references)
            print('\n*****************************************************************************************\n\n')
            # In this case, all attempts are independent, it is totally parallel, I can run all the jobs
            list_references_names = [os.path.basename(ele)[:-4] for ele in list_fichis]
            list_pool_names = [os.path.basename(ele)[:-4] for ele in phs_files]
            list_equal_names = [ele for ele in list_references_names if ele in list_pool_names]
            if len(list_equal_names) == len(list_references_names):
                print('The references are already part of the pool, there is no need to compute anything else')
                list_references_fish = [ele + '.phs' for ele in list_references_names]
            else:
                print('The references are not part of the pool')
                for fichito in list_fichis:
                    name_fichito = os.path.basename(fichito)
                    al.link_file(sub_clust_path, fichito, name_fichito)
                    if not type_file == 'phs':
                        if type_file == 'pdb':
                            print('Reference is a pdb file')
                            al.link_file(sub_clust_path,fichito, name_fichito[:-4]+'.pda')
                        al.link_file(sub_clust_path, ali_confdict['hkl_file'], name_fichito[:-4]+'.hkl')
                        if 'ent_file' in ali_confdict.keys():
                            al.link_file(sub_clust_path, ali_confdict['ent_file'], name_fichito[:-4]+'.ent')
                if not type_file == 'phs':
                    list_basenames_pda = [os.path.basename(fichi)[:-4]+'.pda' for fichi in list_fichis]
                    al.phase_all_in_folder_with_SHELXE(linea_arg=ali_confdict['shelxe_line_alixe'],
                                                       dirname=sub_clust_path,
                                                       shelxe_path=ali_confdict['shelxe_path'],
                                                       n_cores=ali_confdict['number_cores_parallel'],
                                                       dir_log=ali_confdict['log'],
                                                       check_if_solved=False,
                                                       subset=list_basenames_pda)
                list_references_fish = [os.path.basename(fichi)[:-4]+'.phs' for fichi in list_fichis]

            phs_files.sort()
            dict_clust_by_rotclu = al.ALIXE_fishing(ali_confdict=ali_confdict, dict_clust_by_rotclu=dict_clust_by_rotclu,
                                                 rotclu='0', list_phs_rotclu=phs_files,
                                                 reference_files=list_references_fish, clust_fold=sub_clust_path)

            bitten = al.process_fishing_ALIXE(dict_clust_by_rotclu, '0', sub_clust_path, ali_confdict)

            # Expand with SHELXE if the user selected this option
            if ali_confdict['expansions'] and bitten:
                # NOTE CM this function filters the single solutions for expansion, but I think I should made that optional
                # so that single solutions are also attempted
                al.perform_SHELXE_expansions_from_dictio_cluster(dict_clust_by_rotclu,
                                                                 ali_confdict, sub_clust_path, sort=False)

    elif ali_confdict['alixe_mode'] == 'monomer' or ali_confdict['alixe_mode'] == 'multimer':

        for i, ele in enumerate(list_tuples_pools):
            keyinputinfo, sub_clust_key, sub_clust_path = ele[0], ele[1], ele[2]

            # Prepare the input to perform phase clustering inside each rotation cluster
            sizerotclu = len(list_rot_cluster)

            # NOTE CM: This block is required for ARCIMBOLDO_LITE runs only I think (well, for runs with more than 1 frag)
            # NOTE CM: Maybe it can be moved to a function
            new_list_rot_cluster = []
            for i, ele in enumerate(list_rot_cluster):
                list_clu = ele.split('_')
                list_clu = [int(ele) for ele in list_clu]
                list_clu = sorted(list_clu)
                list_clu = [str(ele) for ele in list_clu]
                new_list_rot_cluster.append('_'.join(list_clu))

            # Prepare for saving the output
            dict_clust_by_rotclu = {}  # final dictionary to save the resulting ALIXE clusters

            # Iteration for clustering within each rotation cluster
            for indx, rotclu in enumerate(new_list_rot_cluster):

                print('\n************************************************************************************************')
                print('\n We are processing rotation cluster ', rotclu, ' which is the ', indx + 1, ' out of ', sizerotclu)
                print(
                    '\n************************************************************************************************\n\n')
                if not folder_mode:
                    list_phs_full = [dict_sorted_input[str(rotclu)][i] for i in range(len(dict_sorted_input[str(rotclu)]))]
                    list_phs_rotclu = al.sort_list_phs_rotclu_by_FOM(list_phs_full=list_phs_full,
                                                                     fom_sorting=ali_confdict['fom_sorting'],
                                                                     dictio_fragments=dictio_fragments,
                                                                     keypool=sub_clust_key)
                else:
                    list_phs_rotclu = al.list_files_by_extension(sub_clust_path, 'phs')

                dict_clust_by_rotclu = al.ALIXE_clustering_on_a_set(ali_confdict, dict_clust_by_rotclu, rotclu,
                                                                    list_phs_rotclu,
                                                                    sub_clust_path, tolerance='first')

            # write the output in table format
            al.prepare_output_tables_clustering_alixe(dict_clust_by_rotclu, ali_confdict, sub_clust_path, sub_clust_key,
                                                      dictio_fragments, folder_mode)
            # write the output in pkl format to retrieve it later on
            al.prepare_pickle_clustering_alixe(dict_clust_by_rotclu, sub_clust_path, sub_clust_key)

            # If plotting option is active, prepare plots describing the clustering
            if ali_confdict['plots']:
                path_info_clust = os.path.join(sub_clust_path, sub_clust_key + "_info_clust_table")
                al.plots_info_clust(path_info_clust=path_info_clust, ali_confdict=ali_confdict,
                                    folder_mode=folder_mode)


            # Now we need to either proceed to the second step or finish

            if ali_confdict['alixe_mode'] == 'multimer':
                if not folder_mode:
                    list_input_clust = al.get_clusters_from_dict_clust_by_rotclu(dict_clust_by_rotclu,with_fom=True)
                else:
                    list_input_clust = al.get_clusters_from_dict_clust_by_rotclu(dict_clust_by_rotclu,with_fom=False)
                # NOTE CM. Do I need the full path really?
                #list_input_clust = [ os.path.join(sub_clust_path,ele) for ele in list_input_clust]
                if len(list_input_clust) > 1:
                    dict_clust_second_round = {}
                    dict_clust_second_round = al.ALIXE_clustering_on_a_set(ali_confdict, dict_clust_second_round, 'R2',
                                                                        list_input_clust,
                                                                        sub_clust_path, tolerance='second')
                    # write the output in table format
                    # NOTE CM: filter single set to False
                    al.prepare_output_tables_clustering_alixe_second_round(dict_clust_second_round, ali_confdict,
                                                                           sub_clust_path, sub_clust_key,folder_mode)

                    # TODO: If plotting option is active, prepare plots describing the clustering
                    # Current function would need changes
                    #if ali_confdict['plots']:
                    #    al.plots_info_clust(path_files=sub_clust_path, postmortem=ali_confdict['postmortem'],
                    #                        folder_mode=folder_mode)

                    # Check before whether there is something to expand
                    filtered_list = [os.path.join(sub_clust_path, key) for key in
                                     dict_clust_second_round['R2'].keys()
                                     if dict_clust_second_round['R2'][key]['n_phs'] > 1]
                    if ali_confdict['expansions'] and len(filtered_list)>=1:
                        al.perform_SHELXE_expansions_from_dictio_cluster(dict_clust_second_round,
                                                                          ali_confdict, sub_clust_path, sort=False)

                else:
                    print('\n *Info* There was only a single cluster formed in monomer mode)')
                    print('\n *Info* Multimer mode will not proceed')
            else: # Then is monomer, check if expansions and otherwise exit
                if ali_confdict['expansions']:
                    if not folder_mode:
                        al.perform_SHELXE_expansions_from_dictio_cluster(dict_clust_by_rotclu, ali_confdict, sub_clust_path,
                                                                         sort=True)
                    else:
                        al.perform_SHELXE_expansions_from_dictio_cluster(dict_clust_by_rotclu, ali_confdict, sub_clust_path,
                                                                         sort=False)

    elif ali_confdict['alixe_mode'] == 'cc_analysis':
        for i, ele in enumerate(list_tuples_pools):
            keyinputinfo, sub_clust_key, sub_clust_path = ele[0], ele[1], ele[2]

            phs_files = al.list_files_by_extension(path=sub_clust_path, extension='phs', fullpath=False)
            if not phs_files:
                print('\n There were not phs files found, trying to get phi files')
                phs_files = al.list_files_by_extension(path=sub_clust_path, extension='phi', fullpath=False)
            table_cc_names = open(os.path.join(sub_clust_path, 'corresp_names_ccfiles.txt'), 'w')
            dict_cc_names = {}
            list_ls_to_process = []
            for i, phs1 in enumerate(phs_files):
                table_cc_names.write(str(i + 1) + '\t' + os.path.basename(phs1) + '\n')
                dict_cc_names[os.path.basename(phs1)] = str(i + 1)
                if i < len(phs_files) - 1:
                    path_ls = os.path.join(sub_clust_path, "ref" + str(i + 1) + '.ls')
                    if not os.path.exists(os.path.join(sub_clust_path, path_ls[:-3] + ".pda")):
                        try:
                            os.link(ali_confdict['path_sym'], os.path.join(sub_clust_path, path_ls[:-3] + ".pda"))
                        except:
                            shutil.copyfile(ali_confdict['path_sym'], os.path.join(sub_clust_path, path_ls[:-3] + ".pda"))
                    lsfile = open(path_ls, 'w')
                    for j in range(i, len(phs_files)):
                        # print '   And including ',phs_files[j]
                        phs_namefile = os.path.basename(phs_files[j])
                        lsfile.write(phs_namefile + '\n')
                    del lsfile
                    list_ls_to_process.append((os.path.basename(path_ls), j - i + 1, os.path.basename(phs1)))
            del table_cc_names

            # start your parallel workers at the beginning of your script
            pool = Pool(int(ali_confdict['number_cores_parallel']))
            print('\n\n Opening the pool with ', ali_confdict['number_cores_parallel'], ' workers')

            # prepare the iterable with the arguments
            list_args = []
            for op, tuplels in enumerate(list_ls_to_process):
                namels = tuplels[0]
                phs_in_ls = tuplels[1]
                phs_ref = tuplels[2]
                list_args.append((namels[:-3], sub_clust_path, ali_confdict['path_chescat'],
                                 ali_confdict['resolution_merging'], 1, 100, 1, ali_confdict['origin_search'],
                                 ali_confdict['weight'], ali_confdict['oricheck'], ali_confdict['map_cc'], True))

            # execute a computation(s) in parallel
            pool.map(al.call_chescat_for_clustering_global, list_args)

            # turn off your parallel workers at the end of your script
            print('Closing the pool')
            pool.close()

            input_for_ccanalysis = open(os.path.join(sub_clust_path, 'alixecc.dat'), 'w')
            info_relations = open(os.path.join(sub_clust_path, 'global_table.dat'), 'w')
            info_relations.write('%-35s %-35s %-12s %-12s %-12s %-12s %-12s %-12s \n' % (
                'File1', 'File2', 'mapCC', 'wMPD', 'diffwMPD', 'shiftX', 'shiftY', 'shiftZ'))

            for op, tuplels in enumerate(list_ls_to_process):
                namels = tuplels[0]
                phs_in_ls = tuplels[1]
                phs_ref = tuplels[2]
                output_path = os.path.join(sub_clust_path, namels[:-3] + '.out')
                list_dictio_results = al.process_chescat_output_multiseed(output_path, 1, phs_in_ls, 1)
                dictio_result = {}
                list_remove = []
                dictio_result, list_remove, clubool = al.process_list_dictio_results_to_global(list_dictio_results,
                                                                                               dictio_result,
                                                                                               list_remove,
                                                                                               namels[:-3],
                                                                                               sub_clust_path,
                                                                                               keep_phi_key=True)
                # Note: in this case, there is only one cycle so dictio_result first and last entries are the same
                ref_id = dict_cc_names[phs_ref]
                for keyphi in dictio_result.keys():
                    keyphs = os.path.basename(keyphi)[:-8]+'.phs'
                    comp_id = dict_cc_names[keyphs]
                    comp_name = os.path.basename(keyphi)
                    if ref_id == comp_id:
                        continue
                    mapcc_scaled1 = (dictio_result[keyphi][0][2][keyphs]['mapcc_first']) / 100
                    wmpd = dictio_result[keyphi][0][2][keyphs]['wMPE_first']
                    diffwmpd = dictio_result[keyphi][0][2][keyphs]['diff_wMPE_first']
                    shiftx = dictio_result[keyphi][0][2][keyphs]['shift_first'][0]
                    shifty = dictio_result[keyphi][0][2][keyphs]['shift_first'][1]
                    shiftz = dictio_result[keyphi][0][2][keyphs]['shift_first'][2]
                    input_for_ccanalysis.write('\t' + str(ref_id) + '\t' + str(comp_id) + '\t' + str(mapcc_scaled1) + '\n')
                    info_relations.write('%-35s %-35s %-12s %-12s %-12s %-12s %-12s %-12s \n' % (
                        phs_ref, comp_name, mapcc_scaled1, wmpd, diffwmpd, shiftx, shifty, shiftz))
            del input_for_ccanalysis
            del info_relations
            # Remove the phi files resulting from this mode
            phi_to_remove = al.list_files_by_extension(sub_clust_path, 'phi')
            phi_to_remove = [ele for ele in phi_to_remove if (os.path.basename(ele)).startswith('ref')]
            for phi in phi_to_remove:  # Remove all the files with ref, not only the phi
                try:
                    os.remove(phi)
                    os.remove(phi[:-4] + '.ls')
                    os.remove(phi[:-4] + '.pda')
                    # At the moment I keep them just to be able to check if everything is OK.
                    # os.remove(phi[:-4]+'.out')
                except:
                    pass

    # Print final time and close log file before finishing
    new_now = time.time()
    final_string = '\nTotal time spent in running autoalixe is ' + str((new_now - now)) + ' seconds , or ' + str(
        (new_now - now) / 60) + ' minutes \n Command line used was ' + " ".join(sys.argv)
    al.print_message_and_log(final_string,ali_confdict['log'],'Info')

if __name__ == "__main__":
    main()
