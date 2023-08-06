#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from future import standard_library
standard_library.install_aliases()

from builtins import str
from builtins import input

import configparser
import io
import copy
import datetime
import getpass
import hashlib
import os
import re
import operator
import pickle
import logging
import shutil
import subprocess
import signal
import sys
import threading
import traceback
import warnings
import xml.etree.ElementTree as ET
from optparse import OptionParser
from optparse import SUPPRESS_HELP
from Bio.PDB import PDBExceptions
from Bio.PDB import *

import numpy
from termcolor import colored

import ADT
import ANOMLIB
import alixe_library as al
import arci_output
import ALEPH.aleph.core.Bioinformatics as Bioinformatics
import Data
import ALEPH.aleph.core.Grid as Grid
import Quaternions
import SELSLIB2
import ALEPH.aleph.core.SystemUtility as SystemUtility
import ARCIMBOLDO_LITE
import unitCellTools

warnings.simplefilter("ignore", PDBExceptions.PDBConstructionWarning)

"""ARCIMBOLDO-BORGES exploits libraries of folds to phase macromolecular structures. This module
contains the main program"""

#######################################################################################################
#                                              CLASSES                                                #
#######################################################################################################


class inputConfig():
    def __init__(self):
        self.list_all_attr = []

    def get_list_attr(self):
        return self.list_all_attr

    def changeAttr(self, name_keyword, value_keyword):
        """ NS, change one of the tuples of the attribute list"""
        for i,tup in enumerate(self.list_all_attr):
            if tup[0] == name_keyword:
                self.list_all_attr[i] = (name_keyword,type(value_keyword))
                break

    def __setattr__(self, name_keyword, value_keyword):
        # if self.__dict__.has_key(name_keyword):
        #     dict.__setattr__(self,name_keyword, value_keyword)
        # else:
        #     self.__dict__[name_keyword]=value_keyword
        # self.list_all_attr.append((name_keyword,type(value_keyword)))

        # NS: changed on 22 Nov 2018
        if name_keyword in self.__dict__:
            # Check the list and replace in case the type of value_keyword has changed
            self.changeAttr(name_keyword, value_keyword)

        # Now change / fill the dictionary
        self.__dict__[name_keyword] = value_keyword

    def get_value(self, name_keyword):
        try:
            return self.name_keyword
        except:
            print('Sorry, ', name_keyword, ' could not be retrieved')


#######################################################################################################
#                                            FUNCTIONS                                                #
#######################################################################################################

def startROT_NODE(datafile):
    """ Clustering of rotations in multiprocessing, in the situation where more than 8 cores are available.

    It will compute rotations for 1000 models, and then, use these first 1000 for clustering the rest in parallel
    (-j argument in ARCIMBOLDO_BORGES)

    :param datafile:
    :type datafile:
    :return:
    :rtype:
    """

    f = open(datafile, "r")
    lista_dati = pickle.load(f)
    f.close()
    os.remove(datafile)
    SELSLIB2.PATH_NEW_PHASER = lista_dati[0]
    SELSLIB2.PATH_NEW_SHELXE = lista_dati[1]
    SELSLIB2.PATH_NEW_ARCIFIRE = lista_dati[2]
    DicParameters = lista_dati[3]
    nice = lista_dati[4]
    DicGridConn = lista_dati[5]
    RotClu = lista_dati[6]
    nameJob = lista_dati[7]
    outputDicr = lista_dati[8]
    nqueue = lista_dati[9]
    laue = lista_dati[10]
    ncs = lista_dati[11]
    spaceGroup = lista_dati[12]
    ensembles = lista_dati[13]
    clusteringAlg = lista_dati[14]
    excludeLLG = lista_dati[15]
    fixed_frags = lista_dati[16]
    cell_dim = lista_dati[17]
    thresholdCompare = lista_dati[18]
    evaLLONG = lista_dati[19]
    isArcimboldo = lista_dati[20]
    tops = lista_dati[21]
    LIMIT_CLUSTER = lista_dati[22]
    applyNameFilter = lista_dati[23]
    candelete = lista_dati[24]
    giveids = lista_dati[25]
    Clusts = lista_dati[26]
    sym = lista_dati[27]
    GRID_TYPE = lista_dati[28]
    QNAME = lista_dati[29]
    FRACTION = lista_dati[30]
    PARTITION = lista_dati[31]

    make_positive_llg = lista_dati[32]

    cm = None
    if cm == None:
        if GRID_TYPE == "Condor":
            cm = Grid.condorManager()
        elif GRID_TYPE == "SGE":
            cm = Grid.SGEManager(qname=QNAME, fraction=FRACTION)
        elif GRID_TYPE == "MOAB":
            cm = Grid.MOABManager(partition=PARTITION)
        elif GRID_TYPE == "SLURM":
            if PARTITION != None and PARTITION != '':
                cm = Grid.SLURMManager(partition=PARTITION)
            else:
                cm = Grid.SLURMManager()
        elif GRID_TYPE == "TORQUE":
            FRACTION = setupbor.getint("TORQUE", "cores_per_node")
            PARALLEL_JOBS = setupbor.getint("TORQUE", "number_of_parallel_jobs")
            MAUI = setupbor.getboolean("TORQUE", "maui")
            cm = Grid.TORQUEManager(qname=QNAME, cores_per_node=FRACTION, parallel_jobs=PARALLEL_JOBS, maui=MAUI)

    if cm is not None:
        cm.setRank("kflops")
        cm.nice_user = "true"

    quate = Quaternions.Quaternions()

    merged, unmerged, convNames = SELSLIB2.evaluateFRF_clusterOnce(DicParameters=DicParameters, cm=cm, sym=sym,
                                                                   DicGridConn=DicGridConn, RotClu=RotClu,
                                                                   nameJob=nameJob,outputDicr=outputDicr, nqueue=nqueue,
                                                                   quate=quate, laue=laue, ncs=ncs,
                                                                   spaceGroup=spaceGroup,ensembles=ensembles,
                                                                   clusteringAlg=clusteringAlg,
                                                                   excludeLLG=excludeLLG, fixed_frags=fixed_frags,
                                                                   cell_dim=cell_dim, thresholdCompare=thresholdCompare,
                                                                   evaLLONG=evaLLONG, isArcimboldo=isArcimboldo,
                                                                   tops=tops, LIMIT_CLUSTER=LIMIT_CLUSTER,
                                                                   applyNameFilter=applyNameFilter, candelete=False,
                                                                   giveids=giveids, merge=Clusts,
                                                                   make_positive_llg=make_positive_llg)

    SELSLIB2.writeSumClusters(merged, outputDicr, "merged", convNames)
    SELSLIB2.writeSumClusters(unmerged, outputDicr, "unmerged", convNames)

    f = open(os.path.join(outputDicr, nameJob + "_end.txt"), "w")
    f.write("EXIT STATUS: SUCCESS")
    f.close()


def startARCIMBOLDO_BORGES(BorData, isShredder, input_bor, DicParameters={}, DicGridConn={}, cm=None, sym=None,
                           doTest=True, mtz_given="", F_given="", SIGF_given="", tNCS_bool_given="", Intensities=False, Aniso=True,
                           normfactors="", tncsfactors="", nice=0, out_phaser_given="", fneed=False,
                           startCheckQueue=False, skip_mr=False, dictio_shred_annotation=None, skip_predicted=False):
    """

    :param BorData:
    :type BorData:
    :param isShredder: indicates whether the ARCIMBOLDO-BORGES run comes from an spherical SHREDDER call
    :type isShredder: bool
    :param input_bor:
    :type input_bor:
    :param DicParameters:
    :type DicParameters:
    :param DicGridConn:
    :type DicGridConn:
    :param cm:
    :type cm:
    :param sym:
    :type sym:
    :param doTest:
    :type doTest:
    :param mtz_given:
    :type mtz_given:
    :param F_given:
    :type F_given:
    :param SIGF_given:
    :type SIGF_given:
    :param Intensities:
    :type Intensities:
    :param Aniso:
    :type Aniso:
    :param normfactors:
    :type normfactors:
    :param tncsfactors:
    :type tncsfactors:
    :param nice:
    :type nice:
    :param out_phaser_given:
    :type out_phaser_given:
    :param fneed:
    :type fneed:
    :param startCheckQueue:
    :type startCheckQueue:
    :param skip_mr:
    :type skip_mr:
    :param dictio_shred_annotation:
    :type dictio_shred_annotation:
    :return:
    :rtype:
    """

    job_type = "ARCIMBOLDO-BORGES"
    toExit = False
    shelxe_version = '10000'

    if not isShredder:
        SELSLIB2.CheckArgumentsBorFile(input_bor, job_type)
        coiled_coil, toExit = SELSLIB2.read_coiled_coil(input_bor=input_bor, job_type=job_type, toExit=toExit)
        BorData.read_file(io.StringIO(str(Data.defaults_bor)))
        BorData.read(input_bor)
    else:
        coiled_coil, toExit = SELSLIB2.read_coiled_coil(input_bor=BorData, job_type=job_type, toExit=toExit)

    model_directory = None

    allborf = io.StringIO()
    BorData.write(allborf)
    allborf.flush()
    allborf.seek(0)
    allbor = allborf.read()
    allborf.close()
    f = open("/tmp/temp.bor", "w")
    f.write(allbor)
    f.close()
    Config = configparser.ConfigParser()
    Config.read_file(open('/tmp/temp.bor'))
    os.remove("/tmp/temp.bor")

    llgdic= {}         #NS: Needed later in shelxe_cycle

    try:
        model_directory = Config.get(job_type, "library_path")
        SELSLIB2.PATH_LIBRARY = model_directory
    except:
        print(colored("FATAL", "red"), "[" + job_type + "]\n library_path: \n Is a mandatory keyword.")
        sys.exit(1)

    if not os.path.exists(os.path.abspath(model_directory)):
        print (colored("FATAL", "red"), "The path given as library_path it does not exist or it is not accessible by the user: ", getpass.getuser())
        sys.exit(1)
	
    model_directory = os.path.abspath(model_directory)

    if not os.path.isdir(model_directory):
        print(colored("FATAL", "red"), "The path given as library_path is not a directory.")
        sys.exit(1)


    conv_names_merged = []
    clu_all_merged = []
    model_file = ""
    error_lib = False
    files_error = []
    for root, subFolders, files in os.walk(model_directory):
        for fileu in files:
            pdbf = os.path.join(root, fileu)
            if pdbf.endswith(".pdb"):
                model_file = pdbf
                datos = os.path.basename(pdbf).split("_")
                if len(datos) != 3:
                    error_lib = True
                    files_error.append(pdbf)
                try:
                    s = int(datos[1])
                    z = int(datos[2][:-4])
                except:
                    error_lib = True
                    files_error.append(pdbf)

    if error_lib:
        print(colored("FATAL", "red"), "The library given in input: ", model_directory)
        print("It is not a standard BORGES library. The following files does not respect the BORGES name convention:")
        for files in files_error:
            print(files)
        sys.exit(1)

    # NOTE CM: we take these keywords here because they involve dependencies on programs that must be checked
    alixe = Config.getboolean("ARCIMBOLDO-BORGES", "alixe")
    smart_packing = Config.getboolean("ARCIMBOLDO-BORGES", "smart_packing")
    smart_packing_clashes = Config.getfloat("ARCIMBOLDO-BORGES", "smart_packing_clashes")
    mend_after_translation = Config.getboolean("ARCIMBOLDO-BORGES", "mend_after_translation")

    try:
        distribute_computing = Config.get("CONNECTION", "distribute_computing").strip().lower()
        if distribute_computing in ["multiprocessing", "supercomputer"]:
            SELSLIB2.PATH_NEW_PHASER = Config.get("LOCAL", "path_local_phaser")
            SELSLIB2.PATH_NEW_SHELXE = Config.get("LOCAL", "path_local_shelxe")
            if alixe:
                    SELSLIB2.PATH_CHESCAT = Config.get("LOCAL", "path_local_chescat")
                    if SELSLIB2.PATH_CHESCAT == '':
                        if sys.platform == "darwin":
                            SELSLIB2.PATH_CHESCAT = os.path.join(os.path.dirname(__file__),"executables/chescat_mac")
                        else:
                            SELSLIB2.PATH_CHESCAT = os.path.join(os.path.dirname(__file__),"executables/chescat_linux")
                    if not al.check_path_chescat(SELSLIB2.PATH_CHESCAT):
                        print(colored("FATAL:", "red"), "The path given for chescat: " + str(os.path.abspath(SELSLIB2.PATH_CHESCAT)) + \
                            " does not exist or it is not accessible to the user")
                        toExit = True
                    else:
                        ali_confdict = {}
                        ali_confdict['path_chescat']=SELSLIB2.PATH_CHESCAT
            if smart_packing or mend_after_translation:
                SELSLIB2.PATH_SPACK = Config.get("LOCAL", "path_local_spack")
                if SELSLIB2.PATH_SPACK == '':
                    if sys.platform == "darwin":
                        SELSLIB2.PATH_SPACK = os.path.join(os.path.dirname(__file__), "executables/spack_mac")
                    else:
                        SELSLIB2.PATH_SPACK = os.path.join(os.path.dirname(__file__), "executables/spack_linux")
                    # TO DO check_path_spack(SELSLIB2.PATH_SPACK) and exit otherwise
                    #    toExit = True)
            path_to_arciborges = os.path.abspath(__file__)
            if path_to_arciborges.endswith('.py'): # Then we need to change the default
                #arcifullpath = os.path.dirname(path_to_arciborges)
                Config.set("LOCAL", "path_local_arcimboldo",path_to_arciborges)
                SELSLIB2.PATH_NEW_ARCIFIRE = Config.get("LOCAL", "path_local_arcimboldo")
            else: # we are in ccp4, we can keep the default
                SELSLIB2.PATH_NEW_ARCIFIRE = Config.get("LOCAL", "path_local_arcimboldo")

        general_parameters, toExit = SELSLIB2.read_general_arguments(config=Config, toExit=toExit)
        current_directory, mtz, hkl, mtzP1, ent, pdbcl, seq = general_parameters

        MW , mw_warning, toExit = SELSLIB2.read_mw(config=Config, seq=seq, job_type=job_type, toExit=toExit)

        try:
            NC = Config.getint("ARCIMBOLDO-BORGES", "number_of_component") 
        except:
            toExit = SELSLIB2.error_read_integer("number_of_component")

        
        F = Config.get("ARCIMBOLDO-BORGES", "f_label")
        SIGF = Config.get("ARCIMBOLDO-BORGES", "sigf_label")
        I = Config.get("ARCIMBOLDO-BORGES", "i_label")
        SIGI =  Config.get("ARCIMBOLDO-BORGES", "sigi_label")

        if F != '' and SIGF != '':
            Intensities = False
        elif I != '' and SIGI != '':
            Intensities = True
            F = I
            SIGF = SIGI
        elif F != '' and SIGF != '' and I != '' and SIGI != '':
            print(colored("\nFATAL", "red"), "Missing label arguments in your configuration file")
            toExit = True
        else:
            print(F, SIGF, I, SIGI)
            print(colored("\nFATAL", "red"), "Label arguments in your configuration file should be set for intensities or amplitudes, not both")
            toExit = True

        nice = Config.getint("ARCIMBOLDO-BORGES", "nice")
        RMSD = Config.getfloat(job_type, "rmsd")
    except:
        print("Mandatory tags are missing:")
        print(traceback.print_exc(file=sys.stdout))
        toExit = True

    if toExit:
        sys.exit(0)

    # Datacorrect testing by CM
    #Aniso = Config.getboolean("ARCIMBOLDO-BORGES", "ANISO")
    formfactors = Config.get("ARCIMBOLDO-BORGES", "formfactors")
    datacorr = Config.get("ARCIMBOLDO-BORGES", "datacorrect")

    peaks = 75

    #NS ANOM: parsing the anomalous parameters
    ANOMDIR=os.path.normpath(os.path.abspath(os.path.join(current_directory,"ANOMFILES")))         #just a name for the moment, the directory is not created yet
    startExpAnomDic, otherAnomParamDic, initCCAnom=ANOMLIB.parseAnomalousParameters(configParserObject=Config, ANOMDIR=ANOMDIR)
    ANOMALOUS= True if initCCAnom else False                      # A master switch for Anomalous parameters
    ANOM_HARD_FILTER=otherAnomParamDic['hardFilter']            # if True: 'union' selection of solutions discarded during evaluateExpCC from 9.5EXP and 9_EXP, if False: intersection

    if os.path.exists(os.path.join(current_directory, 'temp_transfer')):
        shutil.rmtree(os.path.join(current_directory, 'temp_transfer'))
    if os.path.exists(os.path.join(current_directory, 'grid_jobs')):
        shutil.rmtree(os.path.join(current_directory, 'grid_jobs'))
    if os.path.exists(os.path.join(current_directory, 'temp')):
        shutil.rmtree(os.path.join(current_directory, 'temp'))

    # STATIC REFERENCE TO THE QUATERNION CLASS
    quate = Quaternions.Quaternions()

    # STARTING SYSTEM MANAGER
    if sym == None:
        sym = SystemUtility.SystemUtility()

    try:
        DicParameters = {}
        nameJob = Config.get("ARCIMBOLDO-BORGES", "name_job")
        nameJob = "_".join(nameJob.split())
        if len(nameJob.strip()) == 0:
            print('\nKeyword name_job is empty, setting a default name for the job...')
            nameJob = (os.path.basename(mtz))[:-4] + '_arcimboldo_borges'
        DicParameters["nameExecution"] = nameJob
    except:
        print("Mandatory tags are missing:")
        print(traceback.print_exc(file=sys.stdout))

    nameOutput = DicParameters["nameExecution"]

    if os.path.exists(os.path.join(current_directory, nameOutput + ".html")):
        os.remove(os.path.join(current_directory, nameOutput + ".html"))
    if os.path.exists(os.path.join(current_directory, nameOutput + ".xml")):
        os.remove(os.path.join(current_directory, nameOutput + ".xml"))

    setupbor = None
    if distribute_computing == "remote_grid":
        path_bor = Config.get("CONNECTION", "setup_bor_path")
        if path_bor is None or path_bor == "" or not os.path.exists(path_bor):
            print(colored(
                "ATTENTION: the path given for the setup.bor does not exist.\n Please contact your administrator",
                "red"))
            sys.exit(1)
        try:
            setupbor = configparser.ConfigParser()
            setupbor.read_file(io.StringIO(str(Data.grid_defaults_bor)))
            setupbor.read(path_bor)

            DicGridConn["username"] = setupbor.get("GRID", "remote_frontend_username")
            DicGridConn["host"] = setupbor.get("GRID", "remote_frontend_host")
            DicGridConn["port"] = setupbor.getint("GRID", "remote_frontend_port")
            DicGridConn["passkey"] = Config.get("CONNECTION", "remote_frontend_passkey")
            DicGridConn["promptA"] = (setupbor.get("GRID", "remote_frontend_prompt")).strip() + " "
            DicGridConn["isnfs"] = setupbor.getboolean("GRID", "remote_fylesystem_isnfs")
            try:
                DicGridConn["remote_submitter_username"] = setupbor.get("GRID", "remote_submitter_username")
                DicGridConn["remote_submitter_host"] = setupbor.get("GRID", "remote_submitter_host")
                DicGridConn["remote_submitter_port"] = setupbor.getint("GRID", "remote_submitter_port")
                DicGridConn["promptB"] = (setupbor.get("GRID", "remote_submitter_prompt")).strip() + " "
            except:
                pass
            DicGridConn["home_frontend_directory"] = setupbor.get("GRID", "home_frontend_directory")
            SELSLIB2.PATH_NEW_PHASER = setupbor.get("GRID", "path_remote_phaser")
            SELSLIB2.PATH_NEW_SHELXE = setupbor.get("GRID", "path_remote_shelxe")
            SELSLIB2.PATH_NEW_ARCIFIRE = setupbor.get("GRID", "path_remote_arcimboldo")
            SELSLIB2.GRID_TYPE_R = setupbor.get("GRID", "type_remote")
            if SELSLIB2.GRID_TYPE_R == "Condor":
                SELSLIB2.SHELXE_REQUIREMENTS = setupbor.get("CONDOR", "requirements_shelxe")
                SELSLIB2.PHASER_REQUIREMENTS = setupbor.get("CONDOR", "requirements_phaser")
                SELSLIB2.BORGES_REQUIREMENTS = setupbor.get("CONDOR", "requirements_borges")
                SELSLIB2.SHELXE_MEMORY = setupbor.get("CONDOR", "memory_shelxe")
                SELSLIB2.PHASER_MEMORY = setupbor.get("CONDOR", "memory_phaser")
                SELSLIB2.BORGES_MEMORY = setupbor.get("CONDOR", "memory_borges")
                if 'ccp4' in SELSLIB2.PATH_NEW_PHASER.lower():
                    SELSLIB2.PHASER_ENVIRONMENT = "LD_LIBRARY_PATH=" + SELSLIB2.PATH_NEW_PHASER.replace('bin/phaser', 'lib')
            SELSLIB2.LOCAL = False
        except:
            print(colored("ATTENTION: Some keyword in your configuration files are missing. Contact your administrator",
                          "red"))
            print("Path bor given: ", path_bor)
            print(traceback.print_exc(file=sys.stdout))
            sys.exit(1)
    elif distribute_computing == "local_grid":
        path_bor = Config.get("CONNECTION", "setup_bor_path")
        if path_bor is None or path_bor == "" or not os.path.exists(path_bor):
            print(colored(
                "ATTENTION: the path given for the setup.bor does not exist.\n Please contact your administrator",
                "red"))
            sys.exit(1)
        try:
            setupbor = configparser.ConfigParser()
            setupbor.read_file(io.StringIO(str(Data.grid_defaults_bor)))
            setupbor.read(path_bor)
            SELSLIB2.PATH_NEW_PHASER = setupbor.get("LOCAL", "path_local_phaser")
            SELSLIB2.PATH_NEW_SHELXE = setupbor.get("LOCAL", "path_local_shelxe")
            SELSLIB2.PATH_NEW_ARCIFIRE = setupbor.get("LOCAL", "path_local_arcimboldo")
            SELSLIB2.PATH_CHESCAT = setupbor.get("LOCAL", "path_local_chescat")
            if alixe:
                SELSLIB2.PATH_CHESCAT = setupbor.get("LOCAL", "path_local_chescat")
                if SELSLIB2.PATH_CHESCAT == '':
                    if sys.platform == "darwin":
                        SELSLIB2.PATH_CHESCAT = os.path.join(os.path.dirname(__file__),
                                                             "executables/chescat_mac")
                    else:
                        SELSLIB2.PATH_CHESCAT = os.path.join(os.path.dirname(__file__),
                                                             "executables/chescat_linux")
                if not al.check_path_chescat(SELSLIB2.PATH_CHESCAT):
                    print(colored("FATAL:", "red"), "The path given for chescat: " + str(os.path.abspath(SELSLIB2.PATH_CHESCAT)) + \
                        " does not exist or it is not accessible to the user")
                    toExit = True
                else:
                    ali_confdict = {}
                    ali_confdict['path_chescat'] = SELSLIB2.PATH_CHESCAT


            if smart_packing or mend_after_translation:
                SELSLIB2.PATH_SPACK = setupbor.get("LOCAL", "path_local_spack")
                if SELSLIB2.PATH_SPACK == '':
                    if sys.platform == "darwin":
                        SELSLIB2.PATH_SPACK = os.path.join(os.path.dirname(__file__), "executables/spack_mac")
                    else:
                        SELSLIB2.PATH_SPACK = os.path.join(os.path.dirname(__file__), "executables/spack_linux")
                    # TO DO check_path_spack(SELSLIB2.PATH_SPACK) and exit otherwise
                    #    toExit = True)


                    
            SELSLIB2.GRID_TYPE_L = setupbor.get("GRID", "type_local")
            if SELSLIB2.GRID_TYPE_L == "Condor":
                SELSLIB2.SHELXE_REQUIREMENTS = setupbor.get("CONDOR", "requirements_shelxe")
                SELSLIB2.PHASER_REQUIREMENTS = setupbor.get("CONDOR", "requirements_phaser")
                SELSLIB2.BORGES_REQUIREMENTS = setupbor.get("CONDOR", "requirements_borges")
                SELSLIB2.SHELXE_MEMORY = setupbor.get("CONDOR", "memory_shelxe")
                SELSLIB2.PHASER_MEMORY = setupbor.get("CONDOR", "memory_phaser")
                SELSLIB2.BORGES_MEMORY = setupbor.get("CONDOR", "memory_borges")
                if 'ccp4' in SELSLIB2.PATH_NEW_PHASER.lower():
                    SELSLIB2.PHASER_ENVIRONMENT = "LD_LIBRARY_PATH=" + SELSLIB2.PATH_NEW_PHASER.replace('bin/phaser', 'lib')
        except:
            print(colored("ATTENTION: Some keyword in your configuration files are missing. Contact your administrator",
                          "red"))
            print("Path bor given: ", path_bor)
            print(traceback.print_exc(file=sys.stdout))
            sys.exit(1)
    if distribute_computing == "supercomputer":
        # TODO: Read the list of available nodes
        path_nodes = Config.get("CONNECTION", "nodefile_path")
        if path_nodes is None or path_nodes == "" or not os.path.exists(path_nodes):
            print(colored(
                "ATTENTION: the path given for the node file does not exist.\n Please contact your administrator",
                "red"))
            sys.exit(1)
        f = open(path_nodes, "r")
        nodes_list = f.readlines()
        f.close()
        # SELSLIB2.PATH_NEW_ARCIFIRE = nodes_list[0].strip()
        # nodes_list = nodes_list[1:]

        for i in range(len(nodes_list)):
            nodes_list[i] = nodes_list[i][:-1] + "***" + str(i)
        SystemUtility.NODES = nodes_list

    # LOCKING FOR ACCESS OUTPUT FILE
    lock = threading.RLock()
    lock = threading.Condition(lock)

    if startCheckQueue:
        SystemUtility.startCheckQueue(sym, delete_check_file=False)
    
    # VARIABLES FOR REFINEMENT IN P1
    # TODO: It is important to expand directly the anis.mtz in P1 and not ask the user to give the mtzP1.
    # Remember anis.mtz should be expanded in P1 and not the original one mtz
    PERFORM_REFINEMENT_P1 = False
    if mtzP1 != None and mtzP1 != "" and mtzP1 != " ":
        PERFORM_REFINEMENT_P1 = True

    if PERFORM_REFINEMENT_P1:
        Fp1 = Config.get(job_type, "f_p1_label")
        SIGFp1 = Config.get(job_type, "sigf_p1_label")
        NCp1 = Config.getint(job_type, "number_of_component_p1")
    else:
        Fp1 = None
        SIGFp1 = None
        NCp1 = None

    # SETTING
    clusteringAlg = Config.get(job_type, "rotation_clustering_algorithm")
    excludeLLG = Config.getfloat(job_type, "exclude_llg")
    excludeZscore = Config.getfloat(job_type, "exclude_zscore")
    thresholdCompare = Config.getfloat(job_type, "threshold_algorithm")
    USE_PACKING = Config.getboolean(job_type, "use_packing")
    filtClu = Config.getboolean(job_type, "filter_clusters_after_rot")
    USE_TRANSLA = True
    USE_NMA = Config.getboolean(job_type, "NMA")
    USE_RGR = Config.get(job_type, "ROTATION_MODEL_REFINEMENT")
    if USE_RGR.lower() == "both":
        USE_RGR = 2
    elif USE_RGR.lower() == "gyre":
        USE_RGR = 1
    else:
        USE_RGR = 0
    # Check the rmsd decrease step for gyre 
    cycle_ref = Config.getint(job_type, "number_cycles_model_refinement")
    cycles_gyre = cycle_ref
    rmsd_decrease=Config.getfloat(job_type,'step_rmsd_decrease_gyre')
    if USE_RGR != 0  and cycle_ref>1:
        last_rmsd= RMSD-(float(cycle_ref-1)*rmsd_decrease)
    else:
        last_rmsd=RMSD
    if last_rmsd <=0.0:
        print('EXITING NOW... With the current parameterization, the last rmsd that will be used in the run is ' \
              '0 or smaller. Please change parameterization and rerun')
        sys.exit(0)
    USE_NMA_P1 = Config.getboolean(job_type, "NMA_P1")
    USE_OCC = Config.getboolean(job_type, "OCC")
    prioritize_occ = Config.getboolean(job_type, "prioritize_occ")
    applyNameFilter = Config.getboolean(job_type, "applyTopNameFilter")
    randomAtoms = Config.getboolean(job_type, "extend_with_random_atoms")
    SecStrElong = Config.getboolean(job_type, "extend_with_secondary_structure")
    res_rot = Config.getfloat(job_type, "resolution_rotation")
    sampl_rot = Config.getfloat(job_type, "sampling_rotation")
    res_tran = Config.getfloat(job_type, "resolution_translation")
    sampl_tran = Config.getfloat(job_type, "sampling_translation")
    res_refin = Config.getfloat(job_type, "resolution_refinement")
    RGR_SAMPL = Config.getfloat(job_type, "sampling_gyre")
    res_gyre = Config.getfloat(job_type, "resolution_gyre")
    noDMinitcc = Config.getboolean(job_type, "noDMinitcc")
    savePHS = Config.getboolean(job_type, "savePHS")
    archivingAsBigFile = Config.getboolean(job_type, "archivingAsBigFile")
    alixe = Config.getboolean(job_type, "alixe")
    alixe_mode = Config.get(job_type, "alixe_mode")
    if alixe_mode not in ['monomer', 'multimer']:
        logging.critical('\n No valid mode for ALIXE. Must be monomer or multimer')
        sys.exit(0)
    ellg_target = Config.getfloat(job_type, "ellg_target")
    phs_fom_statistics = Config.getboolean(job_type, "phs_fom_statistics")
    n_clusters = Config.getint(job_type, "n_clusters")
    prioritize_phasers = Config.getboolean(job_type, "prioritize_phasers")
    USE_TNCS = Config.getboolean(job_type, "TNCS")
    make_positive_llg = Config.getboolean(job_type, "make_positive_llg")
    #NS 
    solventContent=Config.getfloat(job_type,"solventContent") #Solvent content to use in the shelxe DM calculations --> now taken from unitcell content analysis result following the number of mol/asu
    unitCellcontentAnalysis=Config.getboolean(job_type,"unitCellcontentAnalysis")
    frf_path_directory = Config.get(job_type, "FRF_path")
    frf_path = ''
    if frf_path_directory != '' and not os.path.exists(os.path.join(current_directory, "1_FRF_Library")):
        if not os.path.exists(frf_path_directory):
            print(colored("FATAL", "red"), "The ARCIMBOLDO run: ", frf_path_directory, " doesn't exist")
            sys.exit(1)
        elif os.path.exists(os.path.join(frf_path_directory, "1_FRF_Library")):
            frf_path = os.path.join(frf_path_directory, "1_FRF_Library")
        elif os.path.exists(os.path.join(frf_path_directory,"ARCIMBOLDO_BORGES","1_FRF_Library")):
            frf_path = os.path.join(frf_path_directory,"ARCIMBOLDO_BORGES","1_FRF_Library")
        else:
            print(colored("FATAL", "red"), "The ARCIMBOLDO run doesn't have the 1_FRF_Library folder: ", frf_path_directory)
            sys.exit(1)


    fixed_model = Config.get(job_type, "fixed_model")
    if fixed_model.endswith(".pdb"):
        stry = Bioinformatics.get_structure("test", fixed_model)
        if len(stry.get_list()) <= 0:
            print(colored("FATAL", "red"), "The model pdb file: " + str(
            os.path.abspath(fixed_model)) + " is not a standard PDB file.")
            sys.exit(1)
        if not USE_PACKING:
            print('The swap model after translation option is not available without packing')
            sys.exit(1)
    else:
        fixed_model = None

    try:
        swap_model_after_translation = Config.get(job_type, "swap_model_after_translation")
        if swap_model_after_translation.endswith(".pdb"):
            stry = Bioinformatics.get_structure("test", swap_model_after_translation)
            if len(stry.get_list()) <= 0:
                print(colored("FATAL", "red"), "The model pdb file: " + str(
                os.path.abspath(swap_model_after_translation)) + " is not a standard PDB file.")
                sys.exit(1)
        else:
            swap_model_after_translation = None
    except:
        swap_model_after_translation = None


    VRMS = Config.getboolean(job_type, "VRMS")
    VRMS_GYRE = Config.getboolean(job_type, "VRMS_GYRE")
    BFAC = Config.getboolean(job_type, "BFAC")
    BULK_FSOL = Config.getfloat(job_type, "BULK_FSOL")
    BULK_BSOL = Config.getfloat(job_type, "BULK_BSOL")
    RNP_GYRE = Config.getboolean(job_type, "GIMBLE")
    PACK_TRA = Config.getboolean(job_type, "PACK_TRA")
    trim_to_polyala = Config.getboolean(job_type, "trim_to_polyala")
    BASE_SUM_FROM_WD = Config.getboolean(job_type, "BASE_SUM_FROM_WD")
    SELSLIB2.BASE_SUM_FROM_WD = BASE_SUM_FROM_WD
    solution_sorting_scheme = Config.get(job_type, "solution_sorting_scheme").upper()
    sigr = Config.getfloat(job_type, "SIGR")
    sigt = Config.getfloat(job_type, "SIGT")
    preserveChains = Config.getboolean(job_type, "GYRE_PRESERVE_CHAINS")
    CLASHES = Config.getint(job_type, "pack_clashes")
    #NS : I need sometimes to use more autotracing cycles in the end
    nAutoTracCyc = Config.getint(job_type,'nAutoTracCyc')

    #NS: change the number of autotracing cycles per bunch (number of bunches defined by nAutoTracCyc, default:1)
    nBunchAutoTracCyc=Config.getint(job_type,'nBunchAutoTracCyc')

    topFRF = Config.getint(job_type, "topFRF")
    if topFRF <= 0:
        topFRF = None
    topFTF = Config.getint(job_type, "topFTF")
    if topFTF <= 0:
        topFTF = None
    topPACK = Config.getint(job_type, "topPACK")
    if topPACK <= 0:
        topPACK = None
    topRNP = Config.getint(job_type, "topRNP")
    if topRNP <= 0:
        topRNP = None
    topExp = Config.getint(job_type, "topExp") - 1
    if topExp <= 0:
        topExp = None
    force_core = Config.getint(job_type, "force_core")
    if force_core <= 0:
        force_core = None
    force_nsol = Config.getint(job_type, "force_nsol")
    if force_nsol <= 0:
        force_nsol = None

    force_exp = Config.getboolean(job_type, "force_exp")

    if alixe:
        savePHS = True
        archivingAsBigFile = False
        # NOTE CM: Maybe change depending on one or two steps
        #prioritize_phasers = False

    if isShredder and not preserveChains: # in case we are using the communities for annotation
        if Config.getint(job_type, "number_cycles_model_refinement")>2:
            print('\n Autoconfiguring number of cycles of model refinement to 2')

    fixed_frags = 1 #for this mode is always one it will change for LEGO
    evaLLONG = False #It just works with helices and distributionCV better not use it for now

    # STARTING THE GRID MANAGER
    GRID_TYPE = ""
    QNAME = ""
    FRACTION = 1
    PARTITION = ""

    if distribute_computing == "remote_grid":
        GRID_TYPE = setupbor.get("GRID", "type_remote")
    elif distribute_computing == "local_grid":
        GRID_TYPE = setupbor.get("GRID", "type_local")

    if cm == None:
        if GRID_TYPE == "Condor":
            cm = Grid.condorManager()
        elif GRID_TYPE == "SGE":
            QNAME = setupbor.get("SGE", "qname")
            FRACTION = setupbor.getfloat("SGE", "fraction")
            cm = Grid.SGEManager(qname=QNAME, fraction=FRACTION)
        elif GRID_TYPE == "MOAB":
            PARTITION = setupbor.get("MOAB", "partition")
            # FRACTION = setupbor.getfloat("MOAB","partition")
            cm = Grid.MOABManager(partition=PARTITION)
        elif GRID_TYPE == "SLURM":
            PARTITION = setupbor.get("SLURM", "partition")
            if PARTITION != None and PARTITION != '':
                cm = Grid.SLURMManager(partition=PARTITION)
            else:
                cm = Grid.SLURMManager()
        elif GRID_TYPE == "TORQUE":
            QNAME = setupbor.get("TORQUE", "qname")
            FRACTION = setupbor.getint("TORQUE", "cores_per_node")
            PARALLEL_JOBS = setupbor.getint("TORQUE", "number_of_parallel_jobs")
            MAUI = setupbor.getboolean("TORQUE", "maui")
            cm = Grid.TORQUEManager(qname=QNAME, cores_per_node=FRACTION, parallel_jobs=PARALLEL_JOBS, maui=MAUI)

    if cm is not None:
        cm.setRank("kflops")
        cm.nice_user = "true"
        # TODO: Eliminate the SGE.py
        PATH_REMOTE_SGEPY = setupbor.get("GRID", "path_remote_sgepy")
        PATH_REMOTE_PYTHON_INTERPRETER = setupbor.get("GRID", "python_remote_interpreter")
        PATH_LOCAL_PYTHON_INTERPRETER = setupbor.get("LOCAL", "python_local_interpreter")

        if PATH_REMOTE_PYTHON_INTERPRETER.strip() in ["", None]:
            PATH_REMOTE_PYTHON_INTERPRETER = "/usr/bin/python"

        if PATH_LOCAL_PYTHON_INTERPRETER.strip() in ["", None]:
            PATH_LOCAL_PYTHON_INTERPRETER = "/usr/bin/python"

    # TEST THE SHELXE USER LINE
    try:
        linsh = Config.get(job_type, "shelxe_line")
        if linsh == None or linsh.strip() == "":
            raise Exception

        listash = linsh.split()
        for toc in range(len(listash)):
            param = listash[toc]
            if param.startswith("-a"):
                param = "-a0"
                if toc + 1 < len(listash) and not listash[toc + 1].startswith("-"):
                    listash[toc + 1] = ""
                listash[toc] = param
                break

        if os.path.exists(ent):
            listash.append("-x")

        linsh = " ".join(listash)
        shlxLinea0 = linsh
    except:
        if os.path.exists(ent):
            shlxLinea0 = "-m1 -a0 -x"
        else:
            shlxLinea0 = "-m1 -a0"


    # ANISOTROPY CORRECTION AND TESTS

    if doTest:
        anismtz, normfactors, tncsfactors, F, SIGF, spaceGroup, cell_dim, resolution, unique_refl, aniout, anierr, \
        fneed, tNCS_bool, shelxe_version, completeness = SELSLIB2.anisotropyCorrection_and_test(cm=cm, sym=sym, DicGridConn=DicGridConn,
                                                                              DicParameters=DicParameters,
                                                                              current_dir=current_directory, mtz=mtz,
                                                                              F=F, SIGF=SIGF, Intensities=Intensities,
                                                                              Aniso=Aniso, nice=nice, pda=Data.th70pdb,
                                                                              hkl=hkl, ent=ent, formfactors=formfactors,
                                                                              shelxe_line=shlxLinea0)
    else:
        mtz = mtz_given
        F = F_given
        SIGF = SIGF_given
        tNCS_bool = tNCS_bool_given
        # READING THE SPACEGROUP FROM PHASER OUT
        spaceGroup = SELSLIB2.readSpaceGroupFromOut(out_phaser_given)
        # READING THE CELL DIMENSIONS FROM PHASER OUT
        cell_dim = SELSLIB2.cellDimensionFromOut(out_phaser_given)
        # READING THE RESOLUTION FROM PHASER OUT
        resolution = SELSLIB2.resolutionFromOut(out_phaser_given)
        # READING THE NUMBER OF UNIQUE REFLECTIONS FROM PHASER OUT
        unique_refl = SELSLIB2.uniqueReflectionsFromOut(out_phaser_given)

        completeness = None


    if smart_packing or mend_after_translation:
        # At this stage we know the symmetry info from the data
        # we are composing a cryst_card to use for smart packing
        # CRYST1   36.150   36.150  308.770  90.00  90.00 120.00 P 65 2 2     12
        cell_dim_float = [ float(ele) for ele in cell_dim]
        cryst_card_arci="CRYST1%9.3f%9.3f%9.3f%7.2f%7.2f%7.2f %-11s%4s\n"%(cell_dim_float[0],cell_dim_float[1],cell_dim_float[2],
                                                                 cell_dim_float[3],cell_dim_float[4],cell_dim_float[5],
                                                                 spaceGroup, 1)


    if datacorr == 'all_phaser_steps':
        print(' We are going to compute data corrections at each Phaser run')
        Aniso = True
        readcorr = False
    elif datacorr == 'start_phaser':
        print(' We are going to compute data corrections at the beginning with Phaser and read them later')
        Aniso = False
        readcorr = True
    elif datacorr == 'none':  # data have been externally corrected, we need to take them as they are
        print('Data will be used as given in the mtz and hkl paths from GENERAL section')
        Aniso = False
        readcorr = False
    else:
        Aniso=True
        readcorr=False

    sg = Config.get(job_type, "spacegroup")
    if sg != "" and sg != " " and sg != None:
        spaceGroup = sg

    # Check spaceGroup symmetry
    print('\n Space group set to ', spaceGroup)
    dictio_space_groups=unitCellTools.get_spacegroup_dictionary()
    try:
        sg_number=int(spaceGroup)
    except:
        sg_number = unitCellTools.get_space_group_number_from_symbol(spaceGroup)
    if sg_number==None:
        print('\n Sorry, the space group given is not supported')
        sys.exit(0)
    else:
        print('\n Input space group number {} has been correctly processed'.format(sg_number))
        # Perform specific actions depending on space group
        if sg_number == 1:
            print('\n Space group is P1 ')
            print("\n * Warning * GIMBLE refinement will be equivalent to GYRE in this space group, automatically setting to False")
            RNP_GYRE = False
            if not tNCS_bool:  # If no tNCS has been found
                print('\n * Warning * Data does not appear to have tNCS, setting TNCS keyword to False')
                USE_TNCS = False
    sg_symbol=dictio_space_groups[sg_number]['symbol']
    spaceGroup=sg_symbol

    #NS ANOM checks and update the required files for experimental phasing and generates the hkl_fa and ins_fa files with SHELXC file if they don't exist
    if ANOMALOUS:
#updateAnomParamDic(hkl=None, mtz=None, current_directory=None, cell_dim=None, sg_number=1,otherAnomParamDic=None, st     artExpAnomDic=None)
        startExpAnomDic=ANOMLIB.updateAnomParamDic(hkl=hkl, mtz=mtz, current_directory=current_directory, otherAnomParamDic=otherAnomParamDic, cell_dim=cell_dim, sg_number=sg_number, startExpAnomDic=startExpAnomDic)
        delEvalDir=True             #Flag to delete the EVALUATION directory in ANOMDIR
        #solutions_filtered_out={}    #will contain the names of all the solutions to remove after evaluateExp or evaluateExp_cc functions
        #convNamesAnom={}
        savePHS=True
        if not startExpAnomDic:
            print("Error, something went wrong when trying to update the anomalous parameters, quitting now")
            sys.exit(1)

    # SHELXE LINES
    linsh, linsh_last, _ = SELSLIB2.get_shelxe_line(config=Config, job_type=job_type, resolution=resolution, seq=seq,\
                                                    coiled_coil=coiled_coil, fneed=fneed, shelxe_version=shelxe_version)

    # Set properly the shelxe_line at the config so that the html shows it
    Config.set(job_type, "shelxe_line", linsh)
    Config.set(job_type, "shelxe_line_last", linsh_last)
    
    listash = linsh.split()
    nautocyc = 0
    listash1 = linsh.split()
    listash_unbias = linsh.split()

    unbias0 = False  # NOTE AMB: unbias

    for param in listash:
        if param == ("-K999") or param == '-V':
            listash.remove(param)
            listash1.remove(param)
            linsh_last = linsh_last.replace(param, '')
            unbias0 = True
            break

    for toc in range(len(listash)):
        param = listash[toc]
        if param.startswith("-a"):
            nautocyc = int(param[2:]) + 1
            param = "-a0"
            nk = 0
            for prr in listash:
                if prr.startswith("-K"):
                    nk = int(prr[2:])
                    break
            if nk == 0:
                param1 = "-a1"
            else:
                param1 = "-a" + str(nk + 1)
                nautocyc = nautocyc - (nk + 1)

            if toc + 1 < len(listash) and not listash[toc + 1].startswith("-"):
                listash[toc + 1] = ""
                listash1[toc + 1] = ""
            listash[toc] = param
            listash1[toc] = param1
            listash_unbias[toc] = param1
            break

    #NS: bypass the number of autotracing cycles
    if nAutoTracCyc >0:
        nautocyc = nAutoTracCyc +1

    if noDMinitcc:
        for toc in range(len(listash)):
            param = listash[toc]
            if param.startswith("-m"):
                ndenscyc = int(param[2:]) + 1
                param = "-m5"
                if toc + 1 < len(listash) and not listash[toc + 1].startswith("-"):
                    listash[toc + 1] = ""
                listash[toc] = param
                break

    if os.path.exists(ent):
        listash.append("-x")
        listash1.append("-x")
        listash_unbias.append("-x")
        linsh_last = linsh_last + ' -x '

    # if '-o' in listash_unbias: #NOTE AMB: -o is incompatible with -K999 so it is removed for the unbias
    #     listash_unbias.remove('-o')

    linsh = " ".join(listash)
    shlxLinea0 = linsh
    shlxLinea1 = " ".join(listash1)
    shlxLineaLast = linsh_last
    shlxLineaUnbias = " ".join(listash_unbias)


    #NS write a Coot script for visualizing best.pdb etc
    if ANOMALOUS:
        ANOMLIB.writeCOOTscript(current_directory,spaceGroup=spaceGroup, unitCell=cell_dim)

    #NS CALCULATE PATTERSON PEAKS FROM DATA
    pattersonPeaks=None
    if ANOMALOUS:
        if nBunchAutoTracCyc == 1:
            nBunchAutoTracCyc=ANOMLIB.NBUNCH 
        if otherAnomParamDic['patterson']:
            pattersonPeaks=ANOMLIB.pattersonFromData(pathTo_hkl_file=startExpAnomDic['hkl_fa'], resolution=resolution,
                                                     spaceGroupNum=sg_number,unitCellParam=cell_dim, amplitudes=True, harker=True)
    
    #NS: CHANGING THE DEFAULT NUMBER OF AUTOTRACING CYCLES PER BUNCH (DEFAULT 1)
    if nBunchAutoTracCyc>1:
        print("\nINFO: Changing the defaut number of autotracing cycle per bunch from 1 to {}".format(nBunchAutoTracCyc))
        shlxLinea1, shlxLineaLast = SELSLIB2.changeArgInShelxeLine(shelxeLineList=(shlxLinea1, shlxLineaLast),
                                                                   argDic={'-a': nBunchAutoTracCyc})
        print("INFO: shlxLinea1, shlxLineaLast changed to {}, {}".format(shlxLinea1, shlxLineaLast))

    #NS UNIT CELL CONTENT ANALYSIS (optional)
    if unitCellcontentAnalysis or NC<=0:
        print("UNIT CELL CONTENT ANALYSIS")
        solventContent, NC= SELSLIB2.unitCellContentAnalysis(current_directory=current_directory, spaceGroup=spaceGroup,
                                                             cell_dim=cell_dim, MW=MW, resolution=resolution ,
                                                             moleculeType="protein", numberOfComponents=NC,
                                                             solventContent=solventContent)
        
        if solventContent is None or NC is None:
            print("ERROR, your solvent content or number of components is lower or equal to zero, quitting now!")
            sys.exit(1)
        #Set up the shelxe line for further steps (adding radius of the sphere of influence and solvent content)
        solvarg_re=re.compile(r"\-s[\d.]+")
        m0=solvarg_re.search(shlxLinea0)
        m1=solvarg_re.search(shlxLinea1)
        #mP=solvarg_re.search(shlxLineaP)
        mLast=solvarg_re.search(shlxLineaLast)

        if resolution>2.5:                    #NS: Arbitrary cutoff, radius of the sphere of inflence
            shlxLinea0 += " -S%s"%resolution  
            shlxLinea1 += " -S%s"%resolution
            #shlxLineaP += " -S%s"%resolution
            shlxLineaLast += " -S%s"%resolution

        #replace the solvent content if already present in the shelxe command line, add it otherwise
        if m0:
            shlxLinea0 = re.sub(solvarg_re,"-s%.2f"%solventContent, shlxLinea0)
        else:
            shlxLinea0 += " -s%.2f"%solventContent

        if m1:
            shlxLinea1 = re.sub(solvarg_re,"-s%.2f"%solventContent, shlxLinea1)
        else:
            shlxLinea1 += " -s%.2f"%solventContent

        # if mP:
        #     shlxLineaP = re.sub(solvarg_re,"-s%.2f"%solventContent, shlxLineaP)
        # else:
        #     shlxLineaP += " -s%.2f"%solventContent

        if mLast:
            shlxLineaLast = re.sub(solvarg_re,"-s%.2f"%solventContent, shlxLineaLast)
        else:
            shlxLineaLast += " -s%.2f"%solventContent

        del(m0,m1,mLast)    #Remove these variable from memory 

    # RETRIEVING THE LAUE SIMMETRY FROM THE SPACEGROUP
    laue = quate.getLaueSimmetry(spaceGroup)
    if laue == None:
        print('Some problem happened during retrieval of the laue symmetry for this space group')

    ncs = []  # handling of non crystallographic symmetry will be integrated soon

    if os.path.exists(os.path.join(current_directory, "temp")):
        shutil.rmtree(os.path.join(current_directory, "temp"))

    SystemUtility.open_connection(DicGridConn, DicParameters, cm)
    if hasattr(cm, "channel"):
        # COPY THE FULL LIBRARY and MTZ and HKL, IN THE REMOTE SERVER
        actualdi = cm.get_remote_pwd()
        print(cm.change_remote_dir(".."))
        try:
            new_model_directory = os.path.join(current_directory,
                                               os.path.basename(os.path.normpath(model_directory)) + "_" +
                                               DicParameters["nameExecution"])
            os.symlink(model_directory, new_model_directory)
            model_directory = new_model_directory
        except:
            exctype, value = sys.exc_info()[:2]
            # NOTE: If the link already exists, I still need to rename correctly the model_directory variable
            new_model_directory = os.path.join(current_directory,
                                               os.path.basename(os.path.normpath(model_directory)) + "_" +
                                               DicParameters["nameExecution"])
            model_directory = new_model_directory
            pass
        print(cm.copy_directory(model_directory, model_directory))
        print(cm.change_remote_dir(os.path.basename(os.path.normpath(model_directory))))
        cm.remote_library_path = cm.get_remote_pwd()
        print(cm.copy_local_file(mtz, os.path.basename(mtz), send_now=True))
        cm.remote_mtz_path = os.path.join(cm.remote_library_path, os.path.basename(mtz))
        print(cm.copy_local_file(hkl, os.path.basename(hkl), send_now=True))
        cm.remote_hkl_path = os.path.join(cm.remote_library_path, os.path.basename(hkl))
        print(cm.copy_local_file(tncsfactors, os.path.basename(tncsfactors), send_now=True))
        cm.remote_tncs_path = os.path.join(cm.remote_library_path, os.path.basename(tncsfactors))
        print(cm.copy_local_file(normfactors, os.path.basename(normfactors), send_now=True))
        cm.remote_norm_path = os.path.join(cm.remote_library_path, os.path.basename(normfactors))
        if os.path.exists(ent):
            print(cm.copy_local_file(ent, os.path.basename(ent), send_now=True))
            cm.remote_ent_path = os.path.join(cm.remote_library_path, os.path.basename(ent))
        if os.path.exists(seq):
            print(cm.copy_local_file(seq, os.path.basename(seq), send_now=True))
            cm.remote_seq_path = os.path.join(cm.remote_library_path, os.path.basename(seq))
        if os.path.exists(pdbcl):
            print(cm.copy_local_file(pdbcl, os.path.basename(pdbcl), send_now=True))
            cm.remote_pdbcl_path = os.path.join(cm.remote_library_path, os.path.basename(pdbcl))

        if PERFORM_REFINEMENT_P1:
            print(cm.copy_local_file(mtzP1, os.path.basename(mtzP1), send_now=True))
            cm.remote_mtzP1_path = os.path.join(cm.remote_library_path, os.path.basename(mtzP1))
        # print cm.change_remote_dir("..")
        print(cm.change_remote_dir(actualdi))

    Config.remove_section("ARCIMBOLDO")
    Config.remove_section("ARCIMBOLDO-SHREDDER")

    allborf = io.StringIO()
    Config.write(allborf)
    allborf.flush()
    allborf.seek(0)
    allbor = allborf.read()
    allborf.close()

    new_t = None

    # Hidden parameters and hard resolution limits handling
    try:
        skipResLimit = Config.getboolean("ARCIMBOLDO-BORGES", "skip_res_limit")
    except:
        print(colored("\nFATAL", "red"), "Argument skip_res_limit must be either True or False")
        sys.exit()

    
    if resolution > 2.5 and not skipResLimit and not coiled_coil:
        print(colored("ATTENTION: Your resolution is lower than 2.5 A ARCIMBOLDO_BORGES will stop now.", 'red'))
        sys.exit(0)
    elif resolution > 4.0 and not skipResLimit and coiled_coil:
        print(colored("ATTENTION: Coiled coil protocol was active but your resolution is lower than 4.0 A "
                      "ARCIMBOLDO_BORGES will stop now.", 'red'))
        sys.exit(0)

    try:
        stop_if_solved = Config.getboolean("ARCIMBOLDO-BORGES", "STOP_IF_SOLVED")
        if stop_if_solved == False:
            filtClu = False
        SELSLIB2.STOP_IF_SOLVED = stop_if_solved
    except:
        pass

    print('\n Resolution is ',resolution)
    print('\n Coiled coil is set to ',coiled_coil)
    print('\n Stop if solved is set to ',stop_if_solved)

    xml_out = os.path.join(current_directory, nameOutput + ".xml")
    xml_obj = ET.Element('borges-arcimboldo')
    ET.SubElement(xml_obj, 'data')
    ET.SubElement(xml_obj, 'configuration')
    ET.SubElement(xml_obj.find('configuration'), 'time_start').text = str(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    ET.SubElement(xml_obj.find('configuration'), 'bor_name').text = input_bor
    ET.SubElement(xml_obj.find('configuration'), 'bor_text').text = allbor
    # Remove from the html file the hidden parameters
    lines_bor = allbor.split('\n')
    allbor = ''
    for i in range(len(lines_bor)):
        if not lines_bor[i].startswith('skip_res_limit') or not lines_bor[i].startswith('stop_if_solved'):
            allbor = allbor + (lines_bor[i] + '\n')
    ET.SubElement(xml_obj.find('configuration'), 'bor_text').text = allbor
    ET.SubElement(xml_obj.find('configuration'), 'do_packing').text = str(USE_PACKING)
    ET.SubElement(xml_obj.find('configuration'), 'do_ref_p1').text = str(PERFORM_REFINEMENT_P1)
    if spaceGroup not in ["P1", "P 1"]:
        ET.SubElement(xml_obj.find('configuration'), 'do_traslation').text = str(True)
    else:
        ET.SubElement(xml_obj.find('configuration'), 'do_traslation').text = str(False)
    ET.SubElement(xml_obj.find('configuration'), 'mw_warning').text = str(mw_warning)
    if completeness is not None:
        ET.SubElement(xml_obj.find('data'), 'completeness').text = str('%.2f' % completeness)
    ET.SubElement(xml_obj.find('data'), 'spacegroup').text = str(spaceGroup)
    ET.SubElement(xml_obj.find('data'), 'cell_dim')
    ET.SubElement(xml_obj.find('data/cell_dim'), 'A').text = str('%.2f' % float(cell_dim[0]))
    ET.SubElement(xml_obj.find('data/cell_dim'), 'B').text = str('%.2f' % float(cell_dim[1]))
    ET.SubElement(xml_obj.find('data/cell_dim'), 'C').text = str('%.2f' % float(cell_dim[2]))
    ET.SubElement(xml_obj.find('data/cell_dim'), 'alpha').text = str('%.2f' % float(cell_dim[3]))
    ET.SubElement(xml_obj.find('data/cell_dim'), 'beta').text = str('%.2f' % float(cell_dim[4]))
    ET.SubElement(xml_obj.find('data/cell_dim'), 'gamma').text = str('%.2f' % float(cell_dim[5]))
    ET.SubElement(xml_obj.find('data'), 'resolution').text = str('%.2f' % resolution)
    ET.SubElement(xml_obj.find('data'), 'unique_refl').text = str('%.2f' % unique_refl)
    ET.ElementTree(xml_obj).write(xml_out)

    arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)

    # Determine the number of processes and trials that will be performed according to hardware
    if force_core != None:
        sym.PROCESSES = force_core

    if distribute_computing == "multiprocessing":
        topscalc = sym.PROCESSES * 100
    else:
        topscalc = None

    if force_nsol != None:
        topscalc = force_nsol

    # new_t.start()

    if len(os.path.split(SELSLIB2.PATH_NEW_ARCIFIRE)[0]) == 0:
        p = subprocess.Popen(["which", SELSLIB2.PATH_NEW_ARCIFIRE], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        SELSLIB2.PATH_NEW_ARCIFIRE = out.strip()

    SIZE_LIB = 0

    for root, subFolders, files in os.walk(model_directory):
        for fileu in files:
            pdbf = os.path.join(root, fileu)
            if pdbf.endswith(".pdb"):
                SIZE_LIB += 1

    CLUSTSOL = 1000
    if distribute_computing in ["supercomputer"]:
        CLUSTSOL = len(SystemUtility.NODES)

    if SIZE_LIB <= CLUSTSOL or distribute_computing not in ["multiprocessing", "supercomputer"]:
        CLUSTSOL = SIZE_LIB

    if skip_mr or skip_predicted: # NOTE CM: This option skips rotation and translation
        applyNameFilter = True
        path_rot = os.path.join(current_directory, "1_FRF_Library/")
        if not (os.path.exists(path_rot)):
            os.makedirs(path_rot)
        else:
            shutil.rmtree(path_rot)
            os.makedirs(path_rot)
        SELSLIB2.generateFakeMRSum(model_directory, "ROT", True, path_rot, "clustersNoRed")
        path_tran = os.path.join(current_directory, "./6_FTF_Library/")
        if not (os.path.exists(path_tran)):
            os.makedirs(path_tran)
        else:
            shutil.rmtree(path_tran)
            os.makedirs(path_tran)
        SELSLIB2.generateFakeMRSum(model_directory, "TRA", True, path_tran, "clustersNoRedPSol")
        SELSLIB2.generateFakeMRSum(model_directory, "TRA", True, path_tran, "clustersRed")

        if skip_predicted:
            USE_PACKING = False
            RNP_GYRE = False
            USE_RGR = False
            unbias0 =  True

            path_rbr = os.path.join(current_directory, "./8_RBR/")
            if not (os.path.exists(path_rbr)):
                os.makedirs(path_rbr)
            else:
                shutil.rmtree(path_rbr)
                os.makedirs(path_rbr)
            SELSLIB2.generateFakeMRSum(model_directory, "RBR", True, path_rbr, "clustersNoRed")
            path_exp = os.path.join(current_directory, "./9_EXP/")
            if not (os.path.exists(path_exp)):
                os.makedirs(path_exp)
            else:
                shutil.rmtree(path_exp)
                os.makedirs(path_exp)
            SELSLIB2.generateFakeSolCC(path_exp)
            
            path_exp = os.path.join(current_directory, "./9.5_EXP/")
            if not (os.path.exists(path_exp)):
                os.makedirs(path_exp)
            else:
                shutil.rmtree(path_exp)
                os.makedirs(path_exp)
            SELSLIB2.generateFakeSolCC(path_exp)

    SystemUtility.close_connection(DicGridConn,DicParameters,cm)


    #ELLG calculation
    # NOTE CM, this only makes sense to compute if this is a standalone borges not a call from shredder
    if not isShredder:
        outputDireELLG = os.path.join(current_directory, "ELLG_COMPUTATION")
        if not (os.path.exists(outputDireELLG)):
            os.makedirs(outputDireELLG)

        mrsumpath = os.path.join(current_directory, "ELLG_COMPUTATION/ellg_computation.sum")
        if not os.path.exists(mrsumpath):
            list_model_calculate_ellg = SELSLIB2.prepare_files_for_MR_ELLG_BORGES(outputDire=outputDireELLG + "/PREPARED_FILES", model_directory=model_directory)
            (nqueuetest, convNamestest) = SELSLIB2.startMR_ELLG(DicParameters=DicParameters, cm=cm, sym=sym,
                                                            nameJob="ELLG_COMPUTATION", list_solu_set=[],
                                                            list_models_calculate=list_model_calculate_ellg,
                                                            outputDire=outputDireELLG,
                                                            mtz=mtz, MW=MW, NC=NC, F=F, SIGF=SIGF,
                                                            Intensities=Intensities, Aniso=Aniso,
                                                            normfactors=normfactors, tncsfactors=tncsfactors,
                                                            spaceGroup=spaceGroup,
                                                            nice=nice, RMSD=last_rmsd, lowR=99,
                                                            highR=res_rot, ellg_target=ellg_target, datacorr=readcorr, formfactors=formfactors)

            dict_result_ellg = SELSLIB2.evaluateMR_ELLG(DicParameters, cm, DicGridConn, nameJob="ELLG_COMPUTATION",
                                                            outputDicr=outputDireELLG,
                                                            nqueue=nqueuetest, ensembles=convNamestest)
        else:
            dict_result_ellg = SELSLIB2.readMR_ELLGsum(mrsumpath)

        for model in dict_result_ellg:
            if float(dict_result_ellg[model]['ellg_current_ensemble']) > 100000:
                print (colored("\nWARNING", "yellow"), "The eLLG calculated is above 100000. You should check you asymmetric unit content specified in the bor file. Exiting now")
                sys.exit()



    if frf_path != '' and not os.path.exists(os.path.join(current_directory, "1_FRF_Library")):
        shutil.copytree(frf_path, os.path.join(current_directory, "1_FRF_Library"))

    if not os.path.exists(os.path.join(current_directory, "1_FRF_Library/clustersNoRed.sum")):
        if not os.path.exists(os.path.join(current_directory, "1_FRF_Library/clustersNoRed_" + str(CLUSTSOL) + ".sum")):

            SystemUtility.open_connection(DicGridConn, DicParameters, cm)
            (nqueue, convNames) = SELSLIB2.startFRF(DicParameters=DicParameters, cm=cm, sym=sym,
                                                    nameJob="1_FRF_LIBRARY", dir_o_liFile=model_directory,
                                                    outputDire=os.path.join(current_directory, "./1_FRF_Library/"),
                                                    mtz=mtz, MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities,
                                                    Aniso=Aniso, normfactors=normfactors, tncsfactors=tncsfactors,
                                                    nice=nice, RMSD=RMSD, lowR=99, highR=res_rot, final_rot=peaks,
                                                    save_rot=peaks, frag_fixed=fixed_frags, spaceGroup=spaceGroup,
                                                    sampl=sampl_rot, fromN=0, toN=CLUSTSOL, VRMS=VRMS, BFAC=BFAC,
                                                    BULK_FSOL=BULK_FSOL, BULK_BSOL=BULK_BSOL,formfactors=formfactors,
                                                    datacorr=readcorr)

            SystemUtility.endCheckQueue()
            CluAll, RotClu = SELSLIB2.evaluateFRF_clusterOnce(DicParameters=DicParameters, cm=cm, sym=sym,
                                                              DicGridConn=DicGridConn, RotClu=[],
                                                              nameJob="1_FRF_LIBRARY",
                                                              outputDicr=os.path.join(current_directory,
                                                                                      "./1_FRF_Library/"),
                                                              nqueue=nqueue, quate=quate, laue=laue, ncs=ncs,
                                                              spaceGroup=spaceGroup, ensembles=convNames,
                                                              clusteringAlg=clusteringAlg, excludeLLG=excludeLLG,
                                                              fixed_frags=fixed_frags, cell_dim=cell_dim,
                                                              thresholdCompare=thresholdCompare, evaLLONG=evaLLONG,
                                                              isArcimboldo=False, tops=topFRF, LIMIT_CLUSTER=None,
                                                              applyNameFilter=True, candelete=True, giveids=False,
                                                              merge=[],make_positive_llg=make_positive_llg)

            SELSLIB2.writeSumClusters(Clusters=CluAll, dirout=os.path.join(current_directory, "./1_FRF_Library/"),
                                      filename="clustersNoRed_" + str(CLUSTSOL), convNames=convNames)
        else:
            convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters=DicParameters,
                                                                               sumPath=os.path.join(current_directory,
                                                                               "./1_FRF_Library/clustersNoRed_" + str(
                                                                                CLUSTSOL) + ".sum"),table="ROTSOL")

            nqueue = len(convNames.keys())

        if distribute_computing in ["multiprocessing", "supercomputer"]:
            Clu1 = copy.deepcopy(CluAll)
            merged_list = []
            unmerged_list = []
            for sizel in range(CLUSTSOL + 1, SIZE_LIB + 1, 100):
                if not os.path.exists(os.path.join(current_directory, "1_FRF_LIBRARY/" + str(sizel) + "/merged.sum")) or not os.path.exists(os.path.join(current_directory, "1_FRF_LIBRARY/" + str(sizel) + "/unmerged.sum")):
                    (nq, convN) = SELSLIB2.startFRF(DicParameters=DicParameters, cm=cm, sym=sym,
                                                    nameJob="1_FRF_LIBRARY_" + str(sizel), dir_o_liFile=model_directory,
                                                    outputDire=os.path.join(current_directory,
                                                                            "./1_FRF_Library/" + str(sizel) + "/"),
                                                    mtz=mtz, MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities,
                                                    Aniso=Aniso, normfactors=normfactors, tncsfactors=tncsfactors,
                                                    nice=nice, RMSD=RMSD, lowR=99, highR=res_rot, final_rot=peaks,
                                                    save_rot=peaks, frag_fixed=fixed_frags, spaceGroup=spaceGroup,
                                                    sampl=sampl_rot, fromN=sizel, toN=sizel + 100, VRMS=VRMS, BFAC=BFAC,
                                                    BULK_FSOL=BULK_FSOL, BULK_BSOL=BULK_BSOL,formfactors=formfactors,
                                                    datacorr=readcorr)

                    merged_sum, unmerged_sum = SELSLIB2.evaluateFRF_MPR(DicParameters=DicParameters, GRID_TYPE=GRID_TYPE
                                                                        , QNAME=QNAME, FRACTION=FRACTION,
                                                                        PARTITION=PARTITION, cm=cm, sym=sym, nice=nice,
                                                                        DicGridConn=DicGridConn, RotClu=[],
                                                                        nameJob="1_FRF_LIBRARY" + str(sizel),
                                                                        outputDicr=os.path.join(current_directory,
                                                                                                "./1_FRF_Library/" +
                                                                                                str(sizel) + "/"),
                                                                        nqueue=nq, quate=quate, laue=laue,
                                                                        ncs=ncs, spaceGroup=spaceGroup, ensembles=convN,
                                                                        clusteringAlg=clusteringAlg,
                                                                        excludeLLG=excludeLLG, fixed_frags=fixed_frags,
                                                                        cell_dim=cell_dim,
                                                                        thresholdCompare=thresholdCompare,
                                                                        evaLLONG=evaLLONG,applyNameFilter=True,
                                                                        tops=topFRF, merge=Clu1,
                                                                        make_positive_llg=make_positive_llg)
                    SystemUtility.endCheckQueue(blocking=False)

                    merged_list.append(merged_sum)
                    unmerged_list.append(unmerged_sum)
                else:
                    merged_list.append(os.path.join(current_directory, "1_FRF_LIBRARY/" + str(sizel) + "/merged.sum"))
                    unmerged_list.append(
                        os.path.join(current_directory, "1_FRF_LIBRARY/" + str(sizel) + "/unmerged.sum"))

            SystemUtility.endCheckQueue()

            CluAll, convNames = SELSLIB2.fillClusters(DicParameters=DicParameters, CluAll=CluAll,
                                                      merged_list=merged_list, unmerged_list=unmerged_list,
                                                      convNames=convNames,quate=quate, laue=laue, ncs=ncs,
                                                      cell_dim=cell_dim, clusteringAlg=clusteringAlg,
                                                      threshold_alg=thresholdCompare)

        SELSLIB2.writeSumClusters(Clusters=CluAll, dirout=os.path.join(current_directory, "./1_FRF_Library/"),
                                  filename="clustersNoRed",convNames=convNames, RotClu=[], LIMIT_CLUSTER=None,
                                  saveMAP=False, euler_frac_zero=False)

        convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters=DicParameters,
                                                                           sumPath=os.path.join(current_directory,
                                                                           "./1_FRF_Library/clustersNoRed.sum"),
                                                                           table="ROTSOL",LIMIT_CLUSTER=None,
                                                                           skip_reading_variables=False,
                                                                           give_fixed_frags=False, euler_to_zero=False)
    else:
        convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                           os.path.join(current_directory,
                                                                                        "./1_FRF_Library/clustersNoRed.sum"),
                                                                           "ROTSOL")

        nqueue = len(convNames.keys())


    # NOTE: START POSTMORTEM ANALYSIS OF THE ROTATIONS (TEMPORARY)
    if os.path.exists(pdbcl):
        pdbcl_directory = os.path.join(current_directory, "ensemble_clustering/")
        if not (os.path.exists(pdbcl_directory)):
            os.makedirs(pdbcl_directory)
        else:
            shutil.rmtree(pdbcl_directory)
            os.makedirs(pdbcl_directory)

        shutil.copyfile(pdbcl, os.path.join(pdbcl_directory, os.path.basename(pdbcl)))

        SystemUtility.open_connection(DicGridConn, DicParameters, cm)
        (nqueue, convNames) = SELSLIB2.startFRF(DicParameters=DicParameters, cm=cm, sym=sym, nameJob="ENT_FRF",
                                                dir_o_liFile=pdbcl_directory,
                                                outputDire=os.path.join(current_directory, "./ENT_FRF/"), mtz=mtz,
                                                MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities, Aniso=Aniso,
                                                normfactors=normfactors, tncsfactors=tncsfactors, nice=nice, RMSD=RMSD,
                                                lowR=99, highR=res_rot, final_rot=peaks, save_rot=peaks,
                                                frag_fixed=fixed_frags, spaceGroup=spaceGroup, sampl=sampl_rot,
                                                VRMS=VRMS, BFAC=BFAC, BULK_FSOL=BULK_FSOL, BULK_BSOL=BULK_BSOL,
                                                formfactors=formfactors,datacorr=readcorr)

        SystemUtility.endCheckQueue()
        CluAll, RotClu = SELSLIB2.evaluateFRF_clusterOnce(DicParameters, cm, sym, DicGridConn, [], "ENT_FRF",
                                                          os.path.join(current_directory, "./ENT_FRF/"), nqueue, quate,
                                                          laue, ncs, spaceGroup, convNames, clusteringAlg, excludeLLG,
                                                          fixed_frags, cell_dim, thresholdCompare, evaLLONG,
                                                          applyNameFilter=True, tops=topFRF,make_positive_llg=make_positive_llg)

        SELSLIB2.writeSumClusters(CluAll, os.path.join(current_directory, "./ENT_FRF/"), "clustersNoRed", convNames)
        allb = []
        for root, subFolders, files in os.walk(model_directory):
            for fileu in files:
                pdbf = os.path.join(root, fileu)
                if pdbf.endswith(".pdb"):
                    nu = int((fileu.split("_")[0])[4:])
                    allb.append(nu)
        fromV = min(allb)
        toV = max(allb)
        SELSLIB2.analyzeROTclusters(DicParameters, os.path.join(current_directory, "1_FRF_Library/clustersNoRed.sum"),
                                    os.path.join(current_directory, "ENT_FRF/clustersNoRed.sum"),
                                    os.path.join(current_directory, "./ENT_FRF/"), thresholdCompare, clusteringAlg,
                                    quate, laue, ncs, convNames, cell_dim, evaLLONG, fromV, toV)
    # TEMPORANEO#######################################################################
    # NOTE: END POSTMORTEM ANALYSIS OF THE ROTATIONS

    convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters, os.path.join(current_directory, "./1_FRF_Library/clustersNoRed.sum"), "ROTSOL")

    # LIST OF CLUSTERS TO EVALUATE

    priorityClusters = SELSLIB2.writeOutputFile(lock=lock, DicParameters=DicParameters, ClusAll=CluAll,
                                                outputDir=current_directory, filename=nameOutput,
                                                mode="ARCIMBOLDO-BORGES", step="FRF", ensembles=convNames,
                                                frag_fixed=fixed_frags,filterClusters=filtClu,coiled_coil=coiled_coil)

    orderedClusters = priorityClusters
    evaluated_clusters = orderedClusters[:n_clusters]

    SELSLIB2.writeOutputFile(lock=lock, DicParameters=DicParameters, ClusAll=CluAll, outputDir=current_directory,
                             filename=nameOutput, mode="ARCIMBOLDO-BORGES", step="FRF", ensembles=convNames,
                             frag_fixed=fixed_frags, coiled_coil=coiled_coil, n_clusters=n_clusters)

    arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)

    i = 0

    limitstoclu = Config.get(job_type, "clusters")  # all or list of clusters to evaluate

    saveRMSD = RMSD

    onerun = False
    if limitstoclu != None and limitstoclu not in ["", "all"]:
        n_clusters = None
        limitstoclu = limitstoclu.split(",")
        orderedClusters = []
        onerun = True
        for cru in limitstoclu:
            orderedClusters.append(int(cru))
            print(orderedClusters)

    if prioritize_phasers:
        onerun = False
    else:
        onerun = True
 
    for step_i in range(2):
        if step_i == 0 and onerun:
            continue

        if step_i == 1 and not onerun:
            listRotaClus = []
            completernp = "RBR"
            if RNP_GYRE:
                completernp = "GIMBLE"
            for spi in orderedClusters:
                # sumPath = os.path.join(current_directory, "./7.5_PACK_Library/"+str(spi)+"/clustersRed.sum")
                if os.path.exists(
                        os.path.join(current_directory, "./8_" + completernp + "/" + str(spi) + "/clustersNoRed.sum")):
                    sumPath = os.path.join(current_directory,
                                           "./8_" + completernp + "/" + str(spi) + "/clustersNoRed.sum")
                    Clu, dicname = SELSLIB2.readClustersFromSUM(sumPath)
                    if len(dicname.keys()) > 0:
                        listRotaClus.append(
                            (len(Clu[0]["heapSolutions"].asList()), Clu[0]["heapSolutions"].pop()[1]["llg"], spi))

            listRotaClus = sorted(listRotaClus, reverse=True)
            mean_all_llg = [x[1] for x in listRotaClus]
            mean_all_llg = numpy.mean(numpy.array(mean_all_llg))
            sorting_llg = sorted(listRotaClus,key=operator.itemgetter(1),reverse=True)
            prioclusterexp = [ ele[2] for ele in sorting_llg]
            # for t in range(len(listRotaClus)):
            #     distpdb, llgclu, nclu = listRotaClus[t]
            #     prioclusterexp.append(nclu)
            orderedClusters = prioclusterexp

        for clusi in range(len(orderedClusters)):

            print("\n<====== ANALYZING CLUSTER {} ======>\n".format(clusi))
            RMSD = saveRMSD
            if n_clusters is not None and clusi > 0 and clusi >= n_clusters:
                break

            i = orderedClusters[clusi]
            topExp_run = 0
            if step_i == 0:
                topExp_run = None
            else:
                topExp_run = topExp

            unbias = unbias0
            alixe = Config.getboolean("ARCIMBOLDO-BORGES", "alixe") 
            alixe_mode = Config.get(job_type, "alixe_mode")
            fixed_frags = 1
            nfixfr = 1
            convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                               os.path.join(current_directory,
                                                                               "./1_FRF_Library/clustersNoRed.sum"),
                                                                               "ROTSOL", LIMIT_CLUSTER=i)


            #if ANOMALOUS:  # NS: Need to refilter what was filtered out before

                # NS: I need a dictionary to help me filter CluAll subsequently
                # I don't have this problem for Lite since the values in ConvName dics are directly ensembleXXblabla instead of a pdb name (because of the rename pdb option)
                #convNamesAnom.update({ensname : os.path.basename(os.path.normpath(pdbname)) for ensname, pdbname in convNames.items()})

                # if len(solutions_filtered_out.keys())==0 and os.path.exists(os.path.join(ANOMDIR,'filteredSol.json')):     #If the program has stopped, it can retrieve the filtered solutions from here
                #     solutions_filtered_out=ANOMLIB.retrieveFilteredSol(os.path.join(ANOMDIR,'filteredSol.json'))
                #     print("REMARK: retrieving filtered-out solution list (anomalous scoring) from %s"%os.path.join(ANOMDIR,'filteredSol.json'))
                    # for dic in CluAll:
                    #     for heap in list(dic['heapSolutions']):
                    #         print(heap)
                    #         print("\n\n")
                    # sys.exit(1)
                # elif str(i) not in solutions_filtered_out.keys():
                #     solutions_filtered_out[str(i)]={}    #New entry of filtered out solutions for cluster i


            threshPrevious = thresholdCompare

            cycle_ref = Config.getint(job_type, "number_cycles_model_refinement")
            if not PERFORM_REFINEMENT_P1 and not USE_RGR and not USE_NMA_P1:             # NS: seems to be the case in Borges, so the floowing will be skipped
                cycle_ref = 1
            else:
                cycle_ref += 1

            for q in range(cycle_ref):

                if q > 0:  # Any of the cycles that is not the first
                    RMSD -= rmsd_decrease  # Decrease the rmsd to use by the amount set
                    rmsd_step = rmsd_decrease
                    tid = 1  # Only one top
                    appl_tid = True  # Filter solutions by name

                    if not USE_RGR:
                        if not os.path.exists(os.path.join(current_directory, "./4_FRF_LIBRARY/" + str(i) + "/" + str(q) + "/clustersNoRed.sum")):
                            SystemUtility.open_connection(DicGridConn, DicParameters, cm)
                            (nqueue, convNames) = SELSLIB2.startFRF(DicParameters=DicParameters, cm=cm, sym=sym,
                                                                    nameJob="4_FRF_LIBRARY_" + str(i) + "_" + str(q),
                                                                    dir_o_liFile=CluAll,
                                                                    outputDire=os.path.join(current_directory,
                                                                                            "./4_FRF_LIBRARY/" + str(
                                                                                                i) + "/" + str(q)),
                                                                    mtz=mtz, MW=MW, NC=NC, F=F, SIGF=SIGF,
                                                                    Intensities=Intensities, Aniso=Aniso,
                                                                    normfactors=normfactors, tncsfactors=tncsfactors,
                                                                    nice=nice, RMSD=RMSD, lowR=99, highR=res_rot,
                                                                    final_rot=peaks, save_rot=peaks,
                                                                    frag_fixed=fixed_frags, spaceGroup=spaceGroup,
                                                                    tops=topscalc, sampl=sampl_rot, LIMIT_CLUSTER=i,
                                                                    VRMS=VRMS, BFAC=BFAC, BULK_FSOL=BULK_FSOL,
                                                                    BULK_BSOL=BULK_BSOL,formfactors=formfactors,
                                                                    datacorr=readcorr)
                            SystemUtility.endCheckQueue()

                            CluAll, RotClu = SELSLIB2.evaluateFRF_clusterOnce(DicParameters, cm, sym, DicGridConn, [],
                                                                              "4_FRF_LIBRARY_" + str(i) + "_" + str(q),
                                                                              os.path.join(current_directory,
                                                                                           "./4_FRF_LIBRARY/" + str(
                                                                                               i) + "/" + str(q) + "/"),
                                                                              nqueue, quate, laue, ncs, spaceGroup,
                                                                              convNames, clusteringAlg, excludeLLG,
                                                                              fixed_frags, cell_dim, thresholdCompare,
                                                                              evaLLONG, LIMIT_CLUSTER=i, tops=tid,
                                                                              applyNameFilter=appl_tid,
                                                                              make_positive_llg=make_positive_llg)
                            SELSLIB2.writeSumClusters(CluAll, os.path.join(current_directory,
                                                                           "./4_FRF_LIBRARY/" + str(i) + "/" + str(
                                                                               q) + "/"), "clustersRed", convNames,
                                                      LIMIT_CLUSTER=i)
                            convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(
                                                                                                   current_directory,
                                                                                                   "./4_FRF_LIBRARY/" + str(
                                                                                                       i) + "/" + str(
                                                                                                       q) + "/clustersRed.sum"),
                                                                                               "ROTSOL",
                                                                                               LIMIT_CLUSTER=i)
                            CluAll = SELSLIB2.filterAndCountClusters(CluAll, convNames, "llg", quate, laue, ncs,
                                                                     cell_dim, clusteringAlg, thresholdCompare,
                                                                     unify=True)
                            SELSLIB2.writeSumClusters(CluAll, os.path.join(current_directory,
                                                                           "./4_FRF_LIBRARY/" + str(i) + "/" + str(
                                                                               q) + "/"), "clustersNoRed", convNames,
                                                      LIMIT_CLUSTER=i)
                        else:
                            convNames, CluAll, RotClu, enc = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                              os.path.join(
                                                                                                  current_directory,
                                                                                                  "./4_FRF_LIBRARY/" + str(
                                                                                                      i) + "/" + str(
                                                                                                      q) + "/clustersNoRed.sum"),
                                                                                              "ROTSOL", LIMIT_CLUSTER=i)
                    else:  # Then we skip the 4_FRF, we want to use the previous gyred results
                        # (DicParameters,sumPath,table,LIMIT_CLUSTER=None,skip_reading_variables=False,give_fixed_frags=False)
                        convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters=DicParameters,
                                                                                           sumPath=os.path.join(
                                                                                               current_directory,
                                                                                               "./3_RGR/" + str(
                                                                                                   i) + "/" + str(
                                                                                                   q - 1) + "/clustersNoRed.sum"),
                                                                                           table="ROTSOL",
                                                                                           LIMIT_CLUSTER=i,euler_to_zero=True)
                else: #Then we are at the first cycle of gyre
                    rmsd_step = 0


                if q == cycle_ref - 1:  # We added one to cycle_ref, so this one we don't need to do it
                    if USE_RGR:
                        RMSD += rmsd_decrease
                    break

                if PERFORM_REFINEMENT_P1:
                    if not USE_NMA_P1:
                        if not os.path.exists(os.path.join(current_directory,
                                                           "./3_RBR_P1_BRF/" + str(i) + "/" + str(q) + "/models.sum")):
                            SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                            nq, conv2 = SELSLIB2.startRBRP1(DicParameters, cm, sym,
                                                            "3_RBR_P1_BRF_" + str(i) + "_" + str(q), CluAll, convNames,
                                                            os.path.join(current_directory,
                                                                         "./3_RBR_P1_BRF/" + str(i) + "/" + str(
                                                                             q) + "/"), mtzP1, MW, NCp1, Fp1, SIGFp1,
                                                            Intensities, Aniso, nice, RMSD, 99, 1.0, 1, spaceGroup,
                                                            tops=topscalc, sampl=-1, LIMIT_CLUSTER=i, VRMS=VRMS,
                                                            BFAC=BFAC, BULK_FSOL=BULK_FSOL, BULK_BSOL=BULK_BSOL,
                                                            RNP_GYRE=RNP_GYRE, formfactors=formfactors)

                            SystemUtility.endCheckQueue()
                            CluAll, convNames = SELSLIB2.evaluateRefP1(DicParameters, cm, sym, DicGridConn,
                                                                       "3_RBR_P1_BRF_" + str(i) + "_" + str(q),
                                                                       os.path.join(current_directory,
                                                                                    "./3_RBR_P1_BRF/" + str(
                                                                                        i) + "/" + str(q) + "/"), True,
                                                                       quate, conv2, convNames, LIMIT_CLUSTER=i)
                        else:
                            asd, convie = SELSLIB2.readRefFromSUM(os.path.join(current_directory,
                                                                               "./3_RBR_P1_BRF/" + str(i) + "/" + str(
                                                                                   q) + "/models.sum"))
                            nuovoCon = {}
                            for key in convNames.keys():
                                if os.path.basename(convNames[key]) in convie:
                                    nuovoCon[key] = convie[os.path.basename(convNames[key])]
                            convNames = nuovoCon
                            convie = None
                        CluAll = os.path.join(current_directory, "./3_RBR_P1_BRF/" + str(i) + "/" + str(q) + "/")
                    else:
                        if not os.path.exists(
                                os.path.join(current_directory, "./3_NMA_P1/" + str(i) + "/" + str(q) + "/")):
                            SystemUtility.open_connection(DicGridConn, DicParameters, cm)
                            nqueue15, convNames = SELSLIB2.startNMAFromClusters(DicParameters=DicParameters, cm=cm,
                                                                                sym=sym, ClusAll=CluAll,
                                                                                ensembles=convNames,
                                                                                nameJob="3_NMA_P1_" + str(
                                                                                    i) + "_" + str(q),
                                                                                outputDire=os.path.join(
                                                                                    current_directory,
                                                                                    "./3_NMA_P1/" + str(i) + "/" + str(
                                                                                        q) + "/"), mtz=mtz, MW=MW,
                                                                                NC=NC, F=F, SIGF=SIGF,
                                                                                Intensities=Intensities, Aniso=Aniso,
                                                                                normfactors=normfactor,
                                                                                tncsfactors=tncsfactors, nice=nice,
                                                                                RMSD=RMSD, lowR=99, highR=res_clu,
                                                                                final_rot=peaks, save_rot=peaks,
                                                                                frag_fixed=fixed_frags,
                                                                                spaceGroup=spaceGroup, tops=topscalc,
                                                                                sampl=res_sampl, VRMS=VRMS, BFAC=BFAC,
                                                                                BULK_FSOL=BULK_FSOL,
                                                                                BULK_BSOL=BULK_BSOL,
                                                                                formfactors=formfactors)

                            SystemUtility.endCheckQueue()
                            SELSLIB2.evaluateNMA(DicParameters, cm, sym, DicGridConn,
                                                 "3_NMA_P1_" + str(i) + "_" + str(q), os.path.join(current_directory,
                                                                                                   "./3_NMA_P1/" + str(
                                                                                                       i) + "/" + str(
                                                                                                       q) + "/"), i,
                                                 nqueue15, convNames)
                        if not os.path.exists(
                                os.path.join(current_directory, "./3_EXP_P1/" + str(i) + "/" + str(q) + "/solCC.sum")):
                            SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                            (nqueue14, convNames_4) = SELSLIB2.startExpansion(cm=cm, sym=sym, nameJob="3_EXP_P1" + str(i) + "_" + str(q),
                                                                              outputDire=os.path.join(current_directory,"./3_EXP_P1/" + str(i) + "/" + str(q) + "/"),
                                                                              hkl=hkl, ent=ent, nice=nice, cell_dim=cell_dim, spaceGroup=spaceGroup,
                                                                              shlxLine=shlxLinea0, dirBase="./3_NMA_P1/" + str(i) + "/" + str(q) + "/", initCCAnom=initCCAnom,**startExpAnomDic)

                            SystemUtility.endCheckQueue()
                            if ANOMALOUS:
                                try:
                                    shutil.rmtree(os.path.join(ANOMDIR, "EVALUATION"))
                                except:
                                    pass


                                #Get the llg and zscore for all solutions:
                                #convNamesAnom.update(ConvNames)
                                llgdic= ANOMLIB.llgdic(convNames, CluAll)

                                CC_Val3, eliminatedSol = SELSLIB2.evaluateExp_CC(DicParameters, cm, sym, DicGridConn,
                                                                  "3_EXP_P1" + str(i) + "_" + str(q),
                                                                  os.path.join(current_directory,
                                                                               "./3_EXP/" + str(i) + "/" + str(q) + "/"),
                                                                  nqueue14, convNames_4, savePHS=savePHS,
                                                                  archivingAsBigFile=archivingAsBigFile,
                                                                  phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim, anomDic=startExpAnomDic, pattersonPeaks=pattersonPeaks, isBORGES=True, llgdic=llgdic)
                                # Filter out the eliminated solutions from the heap list
                                # if "3_EXP_P1" not in solutions_filtered_out[str(i)] or os.path.exists(os.path.join(ANOMDIR,'filteredSol.json')):
                                #     solutions_filtered_out[str(i)]["3_EXP_P1"] = []

                                # solutions_filtered_out[str(i)]["3_EXP_P1"] +=  eliminatedSol                                    
                                # if len(solutions_filtered_out[str(i)]["3_EXP_P1"])>0:
                                #     ANOMLIB.saveFilteredSol(os.path.join(ANOMDIR,'filteredSol.json'),solutions_filtered_out)
                            else:
                                CC_Val3 = SELSLIB2.evaluateExp_CC(DicParameters, cm, sym, DicGridConn,
                                                                  "3_EXP_P1" + str(i) + "_" + str(q),
                                                                  os.path.join(current_directory,
                                                                               "./3_EXP/" + str(i) + "/" + str(q) + "/"),
                                                                  nqueue14, convNames_4, savePHS=savePHS,
                                                                  archivingAsBigFile=archivingAsBigFile,
                                                                  phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim)                                
                            # SystemUtility.close_connection(DicGridConn,DicParameters,cm)
                        else:
                            CC_Val3, con4 = SELSLIB2.readCCValFromSUM(
                                os.path.join(current_directory, "./3_EXP_P1/" + str(i) + "/" + str(q) + "/solCC.sum"))
                        # TODO: Continue... We should do something with CC_Val3 like take the top for each pdb and put it in the convNames
                        CluAll = os.path.join(current_directory, "./3_EXP_P1/" + str(i) + "/" + str(q) + "/")
                elif USE_RGR:
                    if not os.path.exists(os.path.join(current_directory,"./3_RGR/"+str(i)+"/"+str(q)+"/models.sum")):
                        if q > 0:
                            convNames,CluAll,RotClu,encn = SELSLIB2.readClustersFromSUMToDB(DicParameters=DicParameters,
                                                                                            sumPath=os.path.join(
                                                                                                current_directory,
                                                                                                "./3_RGR/"+str(i)+"/"+
                                                                                                str(q-1)+
                                                                                                "/clustersNoRed.sum"),
                                                                                            table="ROTSOL",
                                                                                            LIMIT_CLUSTER=i,
                                                                                            euler_to_zero=True)
                        else:
                            convNames,CluAll,RotClu,encn = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                            os.path.join(
                                                                                                current_directory,
                                                                                                "./1_FRF_Library/clustersNoRed.sum")
                                                                                            ,"ROTSOL",LIMIT_CLUSTER=i)

                        if isShredder and dictio_shred_annotation != {}:
                            ndir = 0
                            count_models = 0
                            path_models_original = os.path.split(convNames[list(convNames.keys())[0]])[0]
                            list_models = [os.path.join(path_models_original,index)
                                           for index in os.listdir(path_models_original) if index.endswith('.pdb')]
                            models_last_directory = len(list_models) % SELSLIB2.NUMBER_OF_FILES_PER_DIRECTORY
                            if models_last_directory!=0:
                                number_directories = (len(list_models) // SELSLIB2.NUMBER_OF_FILES_PER_DIRECTORY) + 1
                            else:
                                number_directories = (len(list_models) // SELSLIB2.NUMBER_OF_FILES_PER_DIRECTORY)
                            for n in range(ndir,number_directories):
                                if n==number_directories-1 and models_last_directory!=0:  # last group, not 1000 files
                                    sub_list_models = list_models[count_models:count_models+models_last_directory]
                                    count_models = count_models + models_last_directory
                                else:
                                    sub_list_models = list_models[count_models:count_models+1000]
                                    count_models = count_models + 1000
                                new_path_models = os.path.join(current_directory, '2_GROUPING/' + str(i) + "/" + str(q)
                                                               +  "/" + str(n) + "/")
                                try:
                                    os.makedirs(new_path_models)
                                except:
                                    shutil.rmtree(new_path_models)
                                    os.makedirs(new_path_models)
                                if q == 0:
                                    print('Using the first group of annotation levels on ',new_path_models)
                                    Bioinformatics.modify_chains_according_to_shredder_annotation(pdb=sub_list_models,
                                                                                  dictio_annotation=dictio_shred_annotation,
                                                                                  annotation_level='first_ref_cycle_group',
                                                                                  output_path=new_path_models)

                                    for key in convNames.keys():
                                        if convNames[key] not in sub_list_models:
                                            continue
                                        original_path = convNames[key]
                                        convNames[key] = os.path.join(new_path_models, os.path.basename(original_path))
                                elif q==1:
                                    print('Using the second group of annotation levels on ',new_path_models)
                                    Bioinformatics.modify_chains_according_to_shredder_annotation(pdb=sub_list_models,
                                                                                  dictio_annotation=dictio_shred_annotation,
                                                                                  annotation_level='second_ref_cycle_group',
                                                                                  output_path=new_path_models)
			    
                                    for key in convNames.keys():
                                        if convNames[key] not in sub_list_models:
                                            continue
                                        original_path=convNames[key]
                                        convNames[key]=os.path.join(new_path_models,os.path.basename(original_path))
                                    
                                elif q==2:
                                    print('Using the third group of annotation levels on ', new_path_models)
                                    Bioinformatics.modify_chains_according_to_shredder_annotation(pdb=sub_list_models,
                                                                                  dictio_annotation=dictio_shred_annotation,
                                                                                  annotation_level='third_ref_cycle_group',
                                                                                  output_path=new_path_models)
				    
                                    for key in convNames.keys():
                                        if convNames[key] not in sub_list_models:
                                            continue
                                        original_path=convNames[key]
                                        convNames[key]=os.path.join(new_path_models,os.path.basename(original_path))
                        
                        SystemUtility.open_connection(DicGridConn,DicParameters,cm)


                        nq,convNames = SELSLIB2.startRGR(DicParameters=DicParameters,cm=cm,sym=sym,
                                                         nameJob="3_RGR_"+str(i)+"_"+str(q),ClusAll=CluAll,
                                                         ensembles=convNames,
                                                         outputDire=os.path.join(current_directory,"./3_RGR/"+str(i)+
                                                                                 "/"+str(q)+"/"),mtz=mtz,MW=MW,NC=NC,
                                                         F=F,SIGF=SIGF,Intensities=Intensities,Aniso=Aniso,
                                                         normfactors=normfactors,tncsfactors=tncsfactors,nice=nice,
                                                         RMSD=RMSD,lowR=99,highR=res_gyre,frag_fixed=1,
                                                         spaceGroup=spaceGroup,save_rot=peaks,tops=topscalc,
                                                         sampl=RGR_SAMPL,USE_TNCS=USE_TNCS,LIMIT_CLUSTER=i,isOMIT=False,
                                                         VRMS=VRMS_GYRE, BFAC=BFAC, BULK_FSOL=BULK_FSOL,
                                                         BULK_BSOL=BULK_BSOL, sigr=sigr, sigt=sigt,
                                                         preserveChains=preserveChains,formfactors=formfactors,
                                                         datacorr=readcorr, trim_to_polyala=trim_to_polyala)
			
                        SystemUtility.endCheckQueue()
                        convNames, CluAll = SELSLIB2.evaluateRGR(DicParameters=DicParameters, cm=cm, sym=sym,
                                                                 DicGridConn=DicGridConn,
                                                                 nameJob="3_RGR_" + str(i) + "_" + str(q),
                                                                 outputDicr=os.path.join(current_directory,
                                                                                         "./3_RGR/" + str(
                                                                                             i) + "/" + str(q) + "/"),
                                                                 maintainOrigCoord=False, cell_dim=cell_dim, quate=quate,
                                                                 convNames=convNames, models_directory=model_directory,
                                                                 ensembles=convNames, LIMIT_CLUSTER=i, isOMIT=False,
                                                                 ent=ent)

                        if USE_RGR == 2 and q == cycle_ref - 2:  # SELECT Both gyre and no gyre for FTF
                            convNames_1FRF, CluAll_1FRF, RotClu_1FRF, encn_1FRF = SELSLIB2.readClustersFromSUMToDB(
                                DicParameters, os.path.join(current_directory, "./1_FRF_Library/clustersNoRed.sum"),
                                "ROTSOL", LIMIT_CLUSTER=i)

                            SELSLIB2.getTheTOPNOfEachCluster(DicParameters=DicParameters, frag_fixed=fixed_frags,
                                                             dirout=os.path.join(current_directory,
                                                                                 "./3_RGR/" + str(i) + "/" + str(
                                                                                     q) + "/"), mode="matrix",
                                                             quate=quate, ClusAll=CluAll_1FRF, convNames=convNames_1FRF,
                                                             ntop=None, writePDB=True, performTranslation=True,
                                                             elongatingModel=None, createSimmetry=False,
                                                             cell_dim=cell_dim, laue=laue, ncs=ncs, modeTra="frac",
                                                             LIMIT_CLUSTER=i, renameWithConvNames=True,
                                                             sufixSolPos=False, appendToName="nogyre")

                            convNames_1FRF, CluAll_1FRF, RotClu_1FRF, encn_1FRF = SELSLIB2.readClustersFromSUMToDB(
                                DicParameters, os.path.join(current_directory, "./1_FRF_Library/clustersNoRed.sum"),
                                "ROTSOL", LIMIT_CLUSTER=i)

                            for key in convNames_1FRF.keys():
                                nuovoc = os.path.basename(convNames_1FRF[key])
                                nuovoc = nuovoc.split("_")[0] + "nogyre_" + nuovoc.split("_")[1] + "_" + \
                                         nuovoc.split("_")[2]
                                nuovoc = os.path.join(
                                    os.path.join(current_directory, "./3_RGR/" + str(i) + "/" + str(q) + "/"), nuovoc)
                                convNames[key + "nogyre"] = nuovoc

                            CluAll = SELSLIB2.mergeRotClusterObjects(CluAll_1FRF, CluAll, suffix="nogyre",reset_euler="both")


                        SELSLIB2.writeSumClusters(CluAll, os.path.join(current_directory,
                                                                       "./3_RGR/" + str(i) + "/" + str(q) + "/"),
                                                  "clustersNoRed", convNames, LIMIT_CLUSTER=i)
                    
                    else:
                        # returns list asd, with one dictionary per solution containing FOMs, and a convNames (convie)
                        asd, convie = SELSLIB2.readRefFromSUM(
                            os.path.join(current_directory, "./3_RGR/" + str(i) + "/" + str(q) + "/models.sum"))
                        nuovoCon = {}
                        for key in convNames.keys():
                            if os.path.basename(convNames[key]) in convie:
                                nuovoCon[key] = convie[os.path.basename(convNames[key])]
                        convNames = nuovoCon
                        convie = None
                    CluAll = os.path.join(current_directory, "./3_RGR/" + str(i) + "/" + str(q) + "/")
                    # print "After cycle gyre...."
                    # for key in convNames.keys():
                    #    print key,convNames[key]

            SELSLIB2.writeOutputFile(lock, DicParameters, CluAll, current_directory, nameOutput, "ARCIMBOLDO-BORGES",
                                     "TABLE", convNames, fixed_frags, LIMIT_CLUSTER=i,coiled_coil=coiled_coil)
            arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)

            thresholdCompare = threshPrevious

            # This is the part of the code just before all the translation steps'
            # From these step on, we do not want to change anymore the rmsd of the fragments before running phaser'
            rmsd_step=0


            if spaceGroup not in ["P1", "P 1"] or USE_TNCS:
                if not os.path.exists(
                        os.path.join(current_directory, "./6_FTF_Library/" + str(i) + "/clustersNoRedPSol.sum")):
                    SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                    nqueue6 = SELSLIB2.startFTF(DicParameters=DicParameters, cm=cm, sym=sym,
                                                nameJob="6_FTF_Library_" + str(i), ClusAll=CluAll, ensembles=convNames,
                                                outputDire=os.path.join(current_directory,
                                                                        "./6_FTF_Library/" + str(i) + "/"), mtz=mtz,
                                                MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities, Aniso=Aniso,
                                                normfactors=normfactors, tncsfactors=tncsfactors, nice=nice, RMSD=RMSD,
                                                lowR=99, highR=res_tran, final_tra=peaks, save_tra=peaks,
                                                frag_fixed=fixed_frags, spaceGroup=spaceGroup, cutoff_pack=CLASHES,
                                                sampl=sampl_tran, USE_TNCS=USE_TNCS, LIMIT_CLUSTER=i, tops=topscalc,
                                                VRMS=VRMS, BFAC=BFAC, BULK_FSOL=BULK_FSOL, BULK_BSOL=BULK_BSOL,
                                                PACK_TRA=PACK_TRA,formfactors=formfactors,datacorr=readcorr)

                    SystemUtility.endCheckQueue()
                    CluAll, convNames, nfixfr = SELSLIB2.evaluateFTF(DicParameters, cm, sym, DicGridConn,
                                                                     "6_FTF_Library_" + str(i),
                                                                     os.path.join(current_directory,
                                                                     "./6_FTF_Library/" + str(i) + "/"),
                                                                     nqueue6, convNames, excludeZscore, fixed_frags,
                                                                     quate, "TRA", laue, ncs, clusteringAlg, cell_dim,
                                                                     thresholdCompare, evaLLONG, LIMIT_CLUSTER=i,
                                                                     applyNameFilter=applyNameFilter, tops=topFTF,
                                                                     giveids=not applyNameFilter,
                                                                     make_positive_llg=make_positive_llg)

                    if nfixfr == None or nfixfr <= 0:
                        nfixfr = 1

                    SELSLIB2.writeSumClusters(CluAll,
                                              os.path.join(current_directory, "./6_FTF_Library/" + str(i) + "/"),
                                              "clustersRed", convNames, LIMIT_CLUSTER=i)
                    convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                       os.path.join(current_directory,
                                                                                                    "./6_FTF_Library/" + str(
                                                                                                        i) + "/clustersRed.sum"),
                                                                                       "ROTSOL", LIMIT_CLUSTER=i)

                    if applyNameFilter:
                        CluAll = SELSLIB2.filterAndCountClusters(CluAll, convNames, "zscore", quate, laue, ncs,
                                                                 cell_dim, clusteringAlg, thresholdCompare, unify=True)
                        SELSLIB2.writeSumClusters(CluAll,
                                                  os.path.join(current_directory, "./6_FTF_Library/" + str(i) + "/"),
                                                  "clustersNoRed", convNames, LIMIT_CLUSTER=i)

                    SELSLIB2.writeSumClusters(CluAll,
                                              os.path.join(current_directory, "./6_FTF_Library/" + str(i) + "/"),
                                              "clustersNoRedPSol", convNames, LIMIT_CLUSTER=i)
                    convNames, CluAll, RotClu, encn = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                       os.path.join(current_directory,
                                                                                                    "./6_FTF_Library/" + str(
                                                                                                        i) + "/clustersNoRedPSol.sum"),
                                                                                       "ROTSOL", LIMIT_CLUSTER=i)
                else:
                    convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(
                                                                                                   current_directory,
                                                                                                   "./6_FTF_Library/" + str(
                                                                                                       i) + "/clustersNoRedPSol.sum"),
                                                                                               "ROTSOL",
                                                                                               LIMIT_CLUSTER=i,
                                                                                               give_fixed_frags=True)

                SELSLIB2.writeOutputFile(lock, DicParameters, CluAll, current_directory, nameOutput,
                                         "ARCIMBOLDO-BORGES", "FTF", convNames, fixed_frags, LIMIT_CLUSTER=i,coiled_coil=coiled_coil)
                arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)
            else:
                SELSLIB2.writeOutputFile(lock, DicParameters, CluAll, current_directory, nameOutput,
                                         "ARCIMBOLDO-BORGES", "FTF", convNames, fixed_frags, makeEmpty=True,
                                         LIMIT_CLUSTER=i,coiled_coil=coiled_coil)
                arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)

                USE_PACKING = True
                USE_TRANSLA = False


            if USE_PACKING:
                if not os.path.exists(
                        os.path.join(current_directory, "./7.5_PACK_Library/" + str(i) + "/clustersRed.sum")):
                    SystemUtility.open_connection(DicGridConn, DicParameters, cm)
                    nqueue8 = SELSLIB2.startPACK(DicParameters=DicParameters, cm=cm, sym=sym,
                                                 nameJob="7.5_PACK_Library_" + str(i), ClusAll=CluAll,
                                                 ensembles=convNames, outputDire=os.path.join(current_directory,
                                                                                              "./7.5_PACK_Library/" + str(
                                                                                                  i) + "/"), mtz=mtz,
                                                 MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities, Aniso=Aniso,
                                                 normfactors=normfactors, tncsfactors=tncsfactors, nice=nice, RMSD=RMSD,
                                                 lowR=99, highR=1.0, cutoff=CLASHES, formfactors=formfactors,
                                                 spaceGroup=spaceGroup, frag_fixed=nfixfr,
                                                 tops=topPACK, LIMIT_CLUSTER=i, VRMS=VRMS, BFAC=BFAC, datacorr=readcorr)

                    SystemUtility.endCheckQueue()
                    
                    CluAll, convNames, nfixfr = SELSLIB2.evaluateFTF(DicParameters, cm, sym, DicGridConn,
                                                                     "7.5_PACK_Library_" + str(i),
                                                                     os.path.join(current_directory,
                                                                                  "./7.5_PACK_Library/" + str(i) + "/"),
                                                                     nqueue8, convNames, -10, nfixfr, quate, "PACK",
                                                                     laue, ncs, clusteringAlg, cell_dim,
                                                                     thresholdCompare, evaLLONG, LIMIT_CLUSTER=i,
                                                                     tops=topPACK,make_positive_llg=make_positive_llg)

                    SELSLIB2.writeSumClusters(CluAll,
                                              os.path.join(current_directory, "./7.5_PACK_Library/" + str(i) + "/"),
                                              "clustersRed", convNames, LIMIT_CLUSTER=i)
                    convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(
                                                                                                   current_directory,
                                                                                                   "./7.5_PACK_Library/" + str(
                                                                                                       i) + "/clustersRed.sum"),
                                                                                               "ROTSOL",
                                                                                               LIMIT_CLUSTER=i,
                                                                                               give_fixed_frags=True)

                    all_empty = True
                    for clu in CluAll:
                        if len(clu["heapSolutions"].asList()) > 0:
                            all_empty = False
                            break

                    if all_empty:
                        print("Packing has excluded everything...EXIT")
                        # TODO: Close the output row, to do so write <td></td> for the remaning columns and </tr>
                        continue
                else:
                    convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(
                                                                                                   current_directory,
                                                                                                   "./7.5_PACK_Library/" + str(
                                                                                                       i) + "/clustersRed.sum"),
                                                                                               "ROTSOL",
                                                                                               LIMIT_CLUSTER=i,
                                                                                               give_fixed_frags=True)
                    if len(convNames.keys()) == 0:
                        print("Packing has excluded everything...EXIT")
                        # TODO: Close the output row, to do so write <td></td> for the remaning columns and </tr>
                        continue

                SELSLIB2.writeOutputFile(lock, DicParameters, CluAll, current_directory, nameOutput,
                                         "ARCIMBOLDO-BORGES", "PACK", convNames, fixed_frags, LIMIT_CLUSTER=i,coiled_coil=coiled_coil)
                arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)
                sumPACK = os.path.join(current_directory, "./7.5_PACK_Library/" + str(i) + "/clustersRed.sum")
            else:
                SELSLIB2.writeOutputFile(lock, DicParameters, CluAll, current_directory, nameOutput,
                                         "ARCIMBOLDO-BORGES", "PACK", convNames, fixed_frags, makeEmpty=True,
                                         LIMIT_CLUSTER=i,coiled_coil=coiled_coil)
                arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)
                sumPACK = os.path.join(current_directory, "./6_FTF_Library/" + str(i) + "/clustersNoRedPSol.sum")

            if swap_model_after_translation != None:
                print('\n\n * Info * This is the moment in which we are going to swap the models *********')

                # Choose the name of the folder depending on the option
                # NOTE CM: mend after translation will also perform a smart packing check.
                # The only difference with the smart_packing mode is that we would continue with the full models
                if smart_packing and not mend_after_translation:
                    swap_tag = 'SMART'
                if mend_after_translation:
                    swap_tag = 'MEND'

                path_swap = os.path.join(current_directory, "./7_SWAP"+'_'+swap_tag +"/" + str(i) + "/")

                if not os.path.exists(os.path.join(path_swap,"swapped.sum")):  # check that the sum file exists
                    # if the sum is not there, the folder could still be but it is from an incomplete run
                    if os.path.exists(path_swap):
                        shutil.rmtree(path_swap)
                    # otherwise it is already created in the call to getTheTOPNOfEachCluster function below
                   
                    saveCluAll = copy.deepcopy(CluAll)  # we need to copy it because next function will empty the object

                    SELSLIB2.getTheTOPNOfEachCluster(DicParameters=DicParameters, frag_fixed=fixed_frags,
                                                     dirout=path_swap, mode="matrix", quate=quate, ClusAll=saveCluAll,
                                                     convNames=convNames,ntop=None, writePDB=True, performTranslation=True,
                                                     elongatingModel=None, createSimmetry=False, cell_dim=cell_dim,
                                                     laue=laue, ncs=ncs, modeTra="frac", LIMIT_CLUSTER=i,
                                                     renameWithConvNames=True, sufixSolPos=not applyNameFilter)

                    list_path_models_to_swap = [os.path.join(path_swap, ele) for ele in os.listdir(path_swap)]
                    list_swapped_models = []

                    # NOTE CM: CHECKING DIFFERENCES BETWEEN ALGORITHMS IN SUPERPOSITION
                    #file_check_rmsd = open(os.path.join(path_swap,'checking_rmsds.txt'), 'w')
                    #del file_check_rmsd
                    # NOTE CM: CHECKING DIFFERENCES BETWEEN ALGORITHMS IN SUPERPOSITION

                    # Now we superposed the swap_model to all translation solutions that survived the Phaser packing
                    strutemp = Bioinformatics.get_structure('toswap', swap_model_after_translation)
                    new_list_atoms = Selection.unfold_entities(strutemp, 'A')
                    new_list_atoms = sorted(new_list_atoms, key=lambda x:x.get_parent().get_full_id()[3][1:])
                    PDBTEMP = Bioinformatics.get_pdb_from_list_of_atoms(new_list_atoms)[0]

                    for file_to_swap in list_path_models_to_swap:
                        print('\n\nProcessing',file_to_swap)
                        struswap = Bioinformatics.get_structure('swapswap', file_to_swap)
                        old_list_atoms = Selection.unfold_entities(struswap, 'A')
                        old_list_atoms = sorted(old_list_atoms, key=lambda x:x.get_parent().get_full_id()[3][1:])
                        PDBTRANS = Bioinformatics.get_pdb_from_list_of_atoms(old_list_atoms)[0]                        
                        if mend_after_translation:
                            file_b=open(file_to_swap[:-4]+'_trans.pdb','w')
                            file_b.write(cryst_card_arci)
                            file_b.write(PDBTRANS)
                            file_b.close()
                        else:
                            al.add_cryst_card(cryst_card_arci, file_to_swap)
                        try:
                            (rmsT, nref, ncom,
                             allAtoms, compStru, pda) = Bioinformatics.getSuperimp(referenceFile=str(PDBTRANS),
                                                                                   compareFile=str(PDBTEMP),
                                                                                   mode="PDBSTRINGBM_RESIDUES_CONSERVED",
                                                                                   algorithm="nigels-core2",
                                                                                   backbone=True, superpose_exclude=1,
                                                                                   n_iter=None, onlyCA=True)
                            # TODO: Move to ALEPH superposition
                        except:
                            print("Error in superposition at the swapping, skipping this model",file_to_swap)
                            print(sys.exc_info())
                            traceback.print_exc(file=sys.stdout)
                            continue
                        print('************************************************')
                        print('rmsd between model_to_swap and target is',rmsT)
                        print('writing out swapped model')
                        print('file_to_swap',file_to_swap)
                        if rmsT==100:
                            print('The rmsd for this model could not be computed, skipping it')
                            continue
                        print('************************************************')
                        # Now this is writing the superposed full model
                        if mend_after_translation:
                            file_c = open(file_to_swap,'w')
                            file_c.write(cryst_card_arci)
                            file_c.write(pda[0])
                            file_c.close()
                        else:
                            file_c = open(file_to_swap[:-4]+'_full.pdb','w')
                            file_c.write(cryst_card_arci)
                            file_c.write(pda[0])
                            file_c.close()
                        # NOTE CM: CHECKING DIFFERENCES BETWEEN ALGORITHMS IN SUPERPOSITION
                        # file_check_rmsd = open(os.path.join(path_swap,'checking_rmsds.txt'),'a')
                        # file_check_rmsd.write(os.path.basename(file_to_swap)+'\t'+str(rmsT)+'\n')
                        # del file_check_rmsd
                        # NOTE CM: CHECKING DIFFERENCES BETWEEN ALGORITHMS IN SUPERPOSITION
                        list_swapped_models.append(os.path.basename(file_to_swap))

                    if smart_packing and not mend_after_translation:
                        # only smart packing and then continue with fragments
                        # the full models have extension full
                        filtered_models = SELSLIB2.start_smart_packing(input_dir=path_swap,
                                                                       path_spack=SELSLIB2.PATH_SPACK,
                                                                       smart_packing_clashes=smart_packing_clashes,
                                                                       ext_full=True, fragments=True)
                        filtered_sol_names = [ele[:-9]+'.pdb' for ele in filtered_models]
                        CluAll, convNames = SELSLIB2.filter_CluAll_by_smart_packing(CluAll=CluAll, convNames=convNames,
                                                                           filtered_models=filtered_sol_names, path_folder=path_swap)
                    else:
                        filtered_models = SELSLIB2.start_smart_packing(input_dir=path_swap,
                                                                       path_spack=SELSLIB2.PATH_SPACK,
                                                                       smart_packing_clashes=smart_packing_clashes,
                                                                       ext_full=False, fragments=True)

                        CluAll, convNames = SELSLIB2.filter_CluAll_by_smart_packing(CluAll=CluAll, convNames=convNames,
                                                                           filtered_models=filtered_models, path_folder=path_swap)


                    SELSLIB2.writeSumClusters(Clusters=CluAll, dirout=path_swap, filename='swapped',
                                              RotClu=RotClu, convNames=convNames, LIMIT_CLUSTER=i, euler_frac_zero=True)

                    convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(path_swap,
                                                                                                            "swapped.sum"),
                                                                                               'ROTSOL',
                                                                                               LIMIT_CLUSTER=i,
                                                                                               give_fixed_frags=True)
                else:
                    convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(path_swap,
                                                                                                            "swapped.sum"),
                                                                                               'ROTSOL',
                                                                                               LIMIT_CLUSTER=i,
                                                                                               give_fixed_frags=True)
            

            #convNames_writepdbs = copy.deepcopy(convNames)
            if not os.path.exists(os.path.join(current_directory, "./8.5_ROTTRA/" + str(i) + "/")):
                SELSLIB2.getTheTOPNOfEachCluster(DicParameters=DicParameters, frag_fixed=fixed_frags,
                                                 dirout=os.path.join(current_directory, "./8.5_ROTTRA/" + str(i) + "/"),
                                                 mode="matrix", quate=quate, ClusAll=CluAll, convNames=convNames,
                                                 ntop=None, writePDB=True, performTranslation=True,
                                                 elongatingModel=None, createSimmetry=False, cell_dim=cell_dim,
                                                 laue=laue, ncs=ncs, modeTra="frac", LIMIT_CLUSTER=i,
                                                 renameWithConvNames=True, sufixSolPos=not applyNameFilter)

            if not os.path.exists(os.path.join(current_directory, "9.5_EXP",str(i),"solCC.sum")):
                currentClusterDir= os.path.normpath(os.path.join(current_directory, "9.5_EXP",str(i)))

                # NS, delete the old cluster expansion folder if it is already present (meaning it had finished incorrectly in a previous run)
                if ANOMALOUS and os.path.exists(currentClusterDir):
                    try :
                        print("REMARK: It seems that the folder {} exists from a previous interrupted run, deleting it\n.".format(currentClusterDir))
                        shutil.rmtree(currentClusterDir)
                        shutil.rmtree(os.path.join(ANOMDIR, "EVALUATION",str(i)))

                        # Deleting subsequent folders
                        ANOMLIB.deleteSubsequentFiles(root=os.path.abspath(current_directory))  # deletes 10*, 11*, best*
                        dir9Exp=os.path.normpath(os.path.join(current_directory, "9_EXP",str(i)))
                        if os.path.exists(dir9Exp):    #delete also this one since it comes after (just in case)
                            shutil.rmtree(dir9Exp)
                            print("REMARK: It seems that the folder {} also exists from a previous interrupted run, deleting it, as well as subsequent directories 10* 11*\n.".format(dir9Exp))
                            

                    except Exception as e:
                        print("WARNING, cannot delete {}".format(currentClusterDir))
                        print(e)


                SystemUtility.open_connection(DicGridConn, DicParameters, cm)
                print("\n******START_EXPANSION 9_5EXP for cluster {} ******\n".format(i))
                (nqueue9, convNames_2) = SELSLIB2.startExpansion(cm, sym, "9.5_EXP_" + str(i),
                                                                 os.path.join(current_directory,"./9.5_EXP/"
                                                                              + str(i) + "/"), hkl, ent, nice,
                                                                 cell_dim, spaceGroup, shlxLinea0,
                                                                 os.path.join(current_directory,
                                                                              "./8.5_ROTTRA/" + str(i) + "/"),
                                                                 fragdomain=True, initCCAnom=initCCAnom,
                                                                 **startExpAnomDic)

                SystemUtility.endCheckQueue()
                if ANOMALOUS:
                    # if "9.5_EXP" not in solutions_filtered_out[str(i)] or os.path.exists(os.path.join(ANOMDIR,'filteredSol.json')):
                    #     #reinitialize the dictionnary of eliminated solutions for this cluster since it will be recomputed
                    #     print("REMARK: Erasing previous recorded filtered solutions from filteredSol.json for cluster {} and step {}".format(i,"9.5_EXP"))
                    #     solutions_filtered_out[str(i)]["9.5_EXP"] = []


                    if delEvalDir:
                        try:
                            shutil.rmtree(os.path.join(ANOMDIR, "EVALUATION"))
                            shutil.rmtree(os.path.join(ANOMDIR, "RESFILES"))
                            print("** REMARK: deleting the EVALUATION and RESFILES directories from ANOMFILES")

                        except:
                            print("WARNING, cannot delete {}".format(os.path.join(ANOMDIR, "EVALUATION")))

                        finally:
                            delEvalDir=False   #These will not be deleted for the next clusters


                    #convNamesAnom.update(convNames)
                    llgdic= ANOMLIB.llgdic(convNames, CluAll)

                    CC_Val2, eliminatedSol = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9.5_EXP_" + str(i),
                                                      outputDicr=os.path.join(current_directory, "./9.5_EXP/" + str(i) + "/"), nqueue=nqueue9,
                                                      convNames=convNames_2, savePHS=savePHS, archivingAsBigFile=archivingAsBigFile,
                                                      phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim, anomDic=startExpAnomDic, pattersonPeaks=pattersonPeaks, isBORGES=True, llgdic=llgdic, cleanAnom=True)

                    # CC_Val2 is already filtered when coming out of evaluateExp_CC
                    # But we have to filter out CluAll later because it gets re-read from 7.5_PACK at line 2049
                    # solutions_filtered_out[str(i)]["9.5_EXP"] +=  eliminatedSol                                    
                    # if len(solutions_filtered_out[str(i)]["9.5_EXP"])>0:
                    #     ANOMLIB.saveFilteredSol(os.path.join(ANOMDIR,'filteredSol.json'),solutions_filtered_out)
                
                else:
                    CC_Val2 = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9.5_EXP_" + str(i),
                                                      outputDicr=os.path.join(current_directory, "./9.5_EXP/" + str(i) + "/"), nqueue=nqueue9,
                                                      convNames=convNames_2, savePHS=savePHS, archivingAsBigFile=archivingAsBigFile,
                                                      phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim)

                # SystemUtility.close_connection(DicGridConn,DicParameters,cm)
            else:
                CC_Val2, con = SELSLIB2.readCCValFromSUM(
                    os.path.join(current_directory, "./9.5_EXP/" + str(i) + "/solCC.sum"))

            # NS: here it reads the solutions backwards, just after packing
            if not os.path.exists(os.path.join(current_directory, "./8_RBR/" + str(i) + "/clustersNoRed.sum")):
                if USE_PACKING:
                    if swap_model_after_translation==None:
                        convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(
                                                                                                   current_directory,
                                                                                                   "./7.5_PACK_Library/" + str(
                                                                                                       i) + "/clustersRed.sum"),
                                                                                               "ROTSOL",
                                                                                               LIMIT_CLUSTER=i,
                                                                                               give_fixed_frags=True)
                    else: # then it is either mend or smart_packing and we read again the correct sum for the swapped
                        print('The swap model option is ON, we need to get the files from the proper directory')
                        convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                                   os.path.join(
                                                                                                       path_swap,
                                                                                                       "swapped.sum"),
                                                                                                   'ROTSOL',
                                                                                                   LIMIT_CLUSTER=i,
                                                                                                   give_fixed_frags=True)
                elif USE_TRANSLA:
                    convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(
                                                                                                   current_directory,
                                                                                                   "./6_FTF_Library/" + str(
                                                                                                       i) + "/clustersNoRedPSol.sum"),
                                                                                               "ROTSOL",
                                                                                               LIMIT_CLUSTER=i,
                                                                                               give_fixed_frags=True)

                else:
                    if not USE_TNCS and not USE_RGR:
                        convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters, os.path.join(
                                                                                                   current_directory,
                                                                                                   "./1_FRF_Library/clustersNoRed.sum"),
                                                                                                   "ROTSOL",
                                                                                                    LIMIT_CLUSTER=i,
                                                                                                    give_fixed_frags=True)
                    elif not USE_TNCS and USE_RGR:
                        # If you reach this point, no translation and no packing has been performed, but gyre has
                        # In that case, it should be reading from 3_RGR not from 1_FRF!
                        last_gyre=cycles_gyre-1
                        convNames,CluAll,RotClu,encn,nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters=DicParameters, 
                                                                                        sumPath=os.path.join(current_directory,
                                                                                        "./3_RGR/"+str(i)+"/"+str(last_gyre)+"/clustersNoRed.sum"),
                                                                                        table="ROTSOL",LIMIT_CLUSTER=i,euler_to_zero=True,give_fixed_frags=True)

                SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                (nqueue10, convino) = SELSLIB2.startRNP(DicParameters=DicParameters, cm=cm, sym=sym,
                                                        nameJob="8_RBR_" + str(i), ClusAll=CluAll, ensembles=convNames,
                                                        outputDire=os.path.join(current_directory,
                                                                                "./8_RBR/" + str(i) + "/"), mtz=mtz,
                                                        MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities,
                                                        Aniso=Aniso, normfactors=normfactors, tncsfactors=tncsfactors,
                                                        nice=nice, RMSD=RMSD, lowR=99, highR=res_refin,
                                                        spaceGroup=spaceGroup, frag_fixed=nfixfr, LIMIT_CLUSTER=i,
                                                        VRMS=VRMS, USE_TNCS=USE_TNCS,
                                                        USE_RGR=USE_RGR, BFAC=BFAC, BULK_FSOL=BULK_FSOL,
                                                        BULK_BSOL=BULK_BSOL, RNP_GYRE=False, formfactors=formfactors,
                                                        datacorr=readcorr)

                SystemUtility.endCheckQueue()

                CluAll, convNames, tolose = SELSLIB2.evaluateFTF(DicParameters=DicParameters, cm=cm, sym=sym,
                                                                 DicGridConn=DicGridConn, nameJob="8_RBR_" + str(i),
                                                                 outputDicr=os.path.join(current_directory,"./8_RBR/"
                                                                                         + str(i) + "/"),
                                                                 nqueue=nqueue10,ensembles=convNames, excludeZscore=-10,
                                                                 fixed_frags=nfixfr, quate=quate, mode="RNP", laue=laue,
                                                                 listNCS=ncs, clusteringMode=clusteringAlg,
                                                                 cell_dim=cell_dim, thresholdCompare=thresholdCompare,
                                                                 evaLLONG=evaLLONG,LIMIT_CLUSTER=i,convNames=convino,
                                                                 tops=topRNP,make_positive_llg=make_positive_llg)
                if USE_PACKING:
                    CluAll, convNames = SELSLIB2.mergeZSCOREinRNP(DicParameters, sumPACK, CluAll, convNames,
                                                                  isARCIMBOLDO_LITE=False)



                # NOTE CM: this is being converted into a small function as it will have to be called another time
                def reset_euler_and_frac_to_zero_and_filter_fixed_frags_in_CluAll(CluAll):
                    filteredCluAll=[]
                    for clu in CluAll:
                        dicclu = {"heapSolutions": ADT.Heap()}
                        for prio, rotaz in clu["heapSolutions"].asList():
                            if 'euler' in rotaz:
                                rotaz['euler']=[0.0,0.0,0.0]
                            if 'frac' in rotaz:
                                rotaz['frac'] = [0.0, 0.0, 0.0]
                            if 'quaternion' in rotaz:
                                rotaz['quaternion'] = [0.0, 0.0, 0.0, 0.0]
                            if 'fixed_frags' in rotaz:
                                returnval=rotaz.pop('fixed_frags', None)
                            dicclu["heapSolutions"].push(prio, rotaz)
                        filteredCluAll.append(dicclu)
                    return filteredCluAll

                # Before writing the sum file we need to filter out the fixed fragments and reset the euler and frac
                # to zero
                CluAll = reset_euler_and_frac_to_zero_and_filter_fixed_frags_in_CluAll(CluAll)

                #NS Also, we need to filter eliminated solutions from the anomalous scoring process:
                #if ANOMALOUS and ANOM_HARD_FILTER and len(solutions_filtered_out[str(i)])>0:
                #    print("REMARK: filtering out %d solutions after evaluateExp_CC 9_5exp"%len(solutions_filtered_out[str(i)]))
                #    CluAll = ANOMLIB.filterCluAll(CluAll, set(solutions_filtered_out[str(i)]), LIMIT_CLUSTER=i , convNamesDic=convNamesAnom)
                # print '***********************************************'
                # for clu in filteredCluAll:
                #     for prio, rotaz in clu["heapSolutions"].asList():
                #         print 'prio, rotaz',prio,rotaz
                #
                # sys.exit(0)



                SELSLIB2.writeSumClusters(Clusters=CluAll,
                                          dirout=os.path.join(current_directory, "./8_RBR/" + str(i) + "/"),
                                          filename="clustersNoRed", convNames=convNames, LIMIT_CLUSTER=i, saveMAP=False,
                                          euler_frac_zero=False) # They will be already reset
            else:
                convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters, os.path.join(current_directory, "./8_RBR/" + str(i) + "/clustersNoRed.sum"), "ROTSOL", LIMIT_CLUSTER=i, give_fixed_frags=True)
                

            if RNP_GYRE:
                names_before_gimble, a, b, c, d = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                   os.path.join(current_directory,
                                                                                                "./8_RBR/" + str(i) +
                                                                                                "/clustersNoRed.sum"),
                                                                                   "ROTSOL", LIMIT_CLUSTER=i,
                                                                                           give_fixed_frags=True)


            if RNP_GYRE and not os.path.exists(
                    os.path.join(current_directory, "./8_GIMBLE/" + str(i) + "/clustersNoRed.sum")):
                convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters, os.path.join(
                    current_directory, "./8_RBR/" + str(i) + "/clustersNoRed.sum"), "ROTSOL", LIMIT_CLUSTER=i,
                                                                                           give_fixed_frags=True)

                SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                (nqueue10, convino) = SELSLIB2.startRNP(DicParameters=DicParameters, cm=cm, sym=sym,
                                                        nameJob="8_GIMBLE_" + str(i), ClusAll=CluAll,
                                                        ensembles=names_before_gimble, outputDire=os.path.join(current_directory,
                                                                                                     "./8_GIMBLE/" + str(
                                                                                                         i) + "/"),
                                                        mtz=mtz, MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities,
                                                        Aniso=Aniso, normfactors=normfactors, tncsfactors=tncsfactors,
                                                        nice=nice, RMSD=RMSD, lowR=99, highR=res_refin,
                                                        spaceGroup=spaceGroup, frag_fixed=nfixfr, LIMIT_CLUSTER=i,
                                                        VRMS=VRMS, USE_TNCS=USE_TNCS,
                                                        USE_RGR=USE_RGR, BFAC=BFAC, BULK_FSOL=BULK_FSOL,
                                                        BULK_BSOL=BULK_BSOL, RNP_GYRE=True, formfactors=formfactors,
                                                        datacorr=readcorr)

                SystemUtility.endCheckQueue()

                CluAll, convNames, tolose = SELSLIB2.evaluateFTF(DicParameters=DicParameters, cm=cm, sym=sym,
                                                                 DicGridConn=DicGridConn, nameJob="8_GIMBLE_" + str(i),
                                                                 outputDicr=os.path.join(current_directory,
                                                                                                    "./8_GIMBLE/" + str(
                                                                                                        i) + "/"),
                                                                 nqueue=nqueue10, ensembles=convNames,
                                                                 excludeZscore=-10, fixed_frags=nfixfr, quate=quate,
                                                                 mode="RNP_GIMBLE", laue=laue, listNCS=ncs,
                                                                 clusteringMode=clusteringAlg, cell_dim=cell_dim,
                                                                 thresholdCompare=thresholdCompare, evaLLONG=evaLLONG,
                                                                 tops=topRNP,LIMIT_CLUSTER=i, convNames=convino,
                                                                 applyNameFilter=False, renamePDBs=True, giveids=False,
                                                                 isArcimboldo=False, ent=ent,
                                                                 models_directory=model_directory, model_file=None,
                                                                 excludeZscoreRNP=0.0, cleanshsol=True,
                                                                 make_positive_llg=make_positive_llg,
                                                                 nDefinitiveSolFound=1000, is_verification=False,
                                                                 use_tNCS=True)
                if USE_TRANSLA:
                    CluAll, convNames = SELSLIB2.mergeZSCOREinRNP(DicParameters, sumPACK, CluAll, convNames,
                                                                  isARCIMBOLDO_LITE=False)

                # Before writing the sum file we need to filter out the fixed fragments and reset the euler and frac
                # to zero
                CluAll = reset_euler_and_frac_to_zero_and_filter_fixed_frags_in_CluAll(CluAll)
                SELSLIB2.writeSumClusters(CluAll, os.path.join(current_directory, "./8_GIMBLE/" + str(i) + "/"),
                                          "clustersNoRed", convNames, LIMIT_CLUSTER=i)
                clusters_8, conv_names_8 = SELSLIB2.readClustersFromSUM(os.path.join(current_directory, "./8_GIMBLE/" + str(i) + "/clustersNoRed.sum"))
            elif os.path.exists(os.path.join(current_directory, "./8_GIMBLE/" + str(i) + "/clustersNoRed.sum")):
                convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters, os.path.join(
                   current_directory, "./8_GIMBLE/" + str(i) + "/clustersNoRed.sum"), "ROTSOL", LIMIT_CLUSTER=i,
                                                                                          give_fixed_frags=True)
                clusters_8, conv_names_8 = SELSLIB2.readClustersFromSUM(os.path.join(current_directory, "./8_GIMBLE/" + str(i) + "/clustersNoRed.sum"))
            else:
                convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters, os.path.join(current_directory, "./8_RBR/" + str(i) + "/clustersNoRed.sum"), "ROTSOL", LIMIT_CLUSTER=i, give_fixed_frags=True)
                clusters_8, conv_names_8 = SELSLIB2.readClustersFromSUM(os.path.join(current_directory, "./8_RBR/" + str(i) + "/clustersNoRed.sum"))

            for clu in clusters_8:
                for item in clu["heapSolutions"].asList():
                    prio, solu = item
                    if solu['n_prev_cluster'] == i and float(solu['zscore']) > 10 and not coiled_coil:
                        unbias = True
                        print("There are at least one solution with a ZSCORE above 10, the free model bias algorithm will be activated")

            # Now write the output, either of RNP
            SELSLIB2.writeOutputFile(lock=lock, DicParameters=DicParameters, ClusAll=CluAll,
                                     outputDir=current_directory, filename=nameOutput, mode="ARCIMBOLDO-BORGES",
                                     step="RNP", ensembles=convNames, frag_fixed=fixed_frags, LIMIT_CLUSTER=i,
                                     path1=None, path2=None, useRefP1=False, useRGR=False, numberCyclesRef=1,
                                     usePacking=True, useTransla=True, makeEmpty=False, readSum=None,
                                     filterClusters=True,fromphis=False, fromdirexp="11.EXP",coiled_coil=coiled_coil)

            arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)

            if os.path.exists(os.path.join(current_directory, "./8_RBR/" + str(i) + "/clustersNoRed.sum")):
                SELSLIB2.writeGraphSumClusters(os.path.join(current_directory, "./8_RBR/" + str(i) + "/clustersNoRed.sum"))

            path_rnps = os.path.join(current_directory, "./8_RBR/" + str(i) + "/")
            if RNP_GYRE:
                path_rnps = os.path.join(current_directory, "./8_GIMBLE/" + str(i) + "/")

            #9_EXP
            if not os.path.exists(os.path.join(current_directory, "9_EXP", str(i), "solCC.sum")):

                currentClusterDir= os.path.normpath(os.path.join(current_directory, "9_EXP",str(i)))

                # NS, delete the old cluster expansion folder if it is already present
                # (meaning it had finished incorrectly in a previous run)
                if ANOMALOUS and os.path.exists(currentClusterDir):
                    ANOMLIB.deleteSubsequentFiles(root=os.path.abspath(current_directory))  # deletes 10*, 11*, best*
                    try:
                        shutil.rmtree(currentClusterDir)
                        print("REMARK: It seems that the folder {} exists from a previous interrupted run, deleting it.".format(currentClusterDir))
                    except:
                        print("WARNING, cannot delete {}".format(currentClusterDir))



                SystemUtility.open_connection(DicGridConn, DicParameters, cm)
                print("\n****** START_EXPANSION 9_EXP for cluster {} ******\n".format(i))
                (nqueue11, convNames_3) = SELSLIB2.startExpansion(cm, sym, "9_EXP_" + str(i),
                                                                  os.path.join(current_directory,
                                                                               "./9_EXP/" + str(i) + "/"), hkl, ent,
                                                                  nice, cell_dim, spaceGroup, shlxLinea0, path_rnps,
                                                                  fragdomain=True, initCCAnom=initCCAnom,**startExpAnomDic)

                SystemUtility.endCheckQueue()
                if ANOMALOUS:
                    #convNamesAnom.update(convNames)
                    #NS Get the llg and zscore for all solutions:
                    llgdic= ANOMLIB.llgdic(convNames, CluAll)

                    # if "9_EXP" not in solutions_filtered_out[str(i)] or os.path.exists(os.path.join(ANOMDIR,'filteredSol.json')):
                    #     #reinitialize the dictionnary of eliminated solutions for this cluster since it will be recomputed
                    #     print("REMARK: Erasing previous recorded filtered solutions from filteredSol.json for cluster {} and step {}".format(i,"9_EXP"))
                    #     solutions_filtered_out[str(i)]["9_EXP"]=[]

                    CC_Val1, eliminatedSol = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9_EXP_" + str(i), 
                                                      outputDicr=os.path.join(current_directory, "./9_EXP/" + str(i) + "/"), nqueue=nqueue11,
                                                      convNames=convNames_3, savePHS=savePHS, archivingAsBigFile=archivingAsBigFile,
                                                      phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim, anomDic=startExpAnomDic, pattersonPeaks=pattersonPeaks, isBORGES=True, llgdic=llgdic)


                    if ANOM_HARD_FILTER:
                        # Eliminate in the ends solutions which have been either discarded in 9.5EXP or 9.5 (fast since few models remain in the end)               
                        #solutions_filtered_out[str(i)]["9_EXP"] += eliminatedSol
                        CC_Val1,CC_Val2 = ANOMLIB.intersectCCVal([CC_Val1,CC_Val2])
                    #else:
                        # eliminate in the end only solutions which have been discarded in BOTH 9.5EXP and 9.5 (more models retained)
                        # solutions_filtered_out[str(i)]["9_EXP"] = ANOMLIB.intersectionFilteredSol([CC_Val1,CC_Val2], eliminatedSol)

                    # if len(solutions_filtered_out[str(i)]["9_EXP"])>0:
                    #     print("REMARK: filtering out %d solutions after evaluateExp_CC 9_exp"%len(solutions_filtered_out[str(i)]["9_EXP"]))                        
                    #     ANOMLIB.saveFilteredSol(os.path.join(ANOMDIR,'filteredSol.json'),solutions_filtered_out)

                        # The solutions eliminated here must be removed from the previous CCVal2 list:

                        

                else:
                    CC_Val1 = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym,
                                                      DicGridConn=DicGridConn, nameJob="9_EXP_" + str(i),
                                                      outputDicr=os.path.join(current_directory,
                                                                              "./9_EXP/" + str(i) + "/"),
                                                      nqueue=nqueue11, convNames=convNames_3, savePHS=savePHS,
                                                      archivingAsBigFile=archivingAsBigFile,
                                                      phs_fom_statistics=phs_fom_statistics, fragNumber=i,
                                                      spaceGroupNum=sg_number, cell_dim=cell_dim)

            else:
                CC_Val1, con1 = SELSLIB2.readCCValFromSUM(os.path.join(current_directory,
                                                                       "./9_EXP/" + str(i) + "/solCC.sum"))
                # The solutions eliminated here must be removed from the previous CCVal2 list:
                if ANOMALOUS:
                    if ANOM_HARD_FILTER:
                        CC_Val1,CC_Val2 = ANOMLIB.intersectCCVal([CC_Val1,CC_Val2])
                    #else:
                        # eliminate in the end only solutions which have been discarded in BOTH 9.5EXP and 9.5 (more models retained)
                        # Here this is just a way of keeping only the relevant solution names to filter cluall afterwards
                        # print("The number of eliminated solutions is so far: %d"%len(solutions_filtered_out[str(i)]["9_EXP"]))
                        # solutions_filtered_out[str(i)]["9_EXP"] = ANOMLIB.intersectionFilteredSol([CC_Val1,CC_Val2], solutions_filtered_out[str(i)])
                        # print("The number of eliminated solutions is now %d"%len(solutions_filtered_out[str(i)]["9_EXP"]))                       


            if os.path.exists(os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/")):
                for r, subF, fi in os.walk(os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/")):
                    for fileu in fi:
                        pdbf = os.path.join(r, fileu)
                        if pdbf.endswith(".pdb"):
                            os.remove(pdbf)

            # NS: if CC_Val1 is empty (nothing selected from 9_EXP), this will return an empty convNames14 dic
            convNames14 = SELSLIB2.startPREPARE(cm=cm, sym=sym, nameJob="10_PREPARED_" + str(i), CC_Val=CC_Val1,
                                                outputDirectory=os.path.join(current_directory,
                                                                             "./10_PREPARED/" + str(i) + "/"),
                                                cell_dim=cell_dim, spaceGroup=spaceGroup, nTop=topExp, topNext=None)

            if USE_NMA:
                if not os.path.exists(os.path.join(current_directory, "./8.6_NMA/" + str(i) + "/")):
                    SystemUtility.open_connection(DicGridConn, DicParameters, cm)
                    (nqueue15, c) = SELSLIB2.startNMA(DicParameters=DicParameters, cm=cm, sym=sym,
                                                      nameJob="8.6_NMA_" + str(i),
                                                      dir_o_liFile=os.path.join(current_directory,
                                                                                "./10_PREPARED/" + str(i) + "/"),
                                                      outputDire=os.path.join(current_directory,
                                                                              "./8.6_NMA/" + str(i) + "/"), mtz=mtz,
                                                      MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities,
                                                      Aniso=Aniso, normfactors=normfactors, tncsfactors=tncsfactors,
                                                      nice=nice, RMSD=RMSD, lowR=99, highR=res_refin, final_rot=peaks,
                                                      save_rot=peaks, frag_fixed=fixed_frags, spaceGroup=spaceGroup,
                                                      VRMS=VRMS, BFAC=BFAC, BULK_FSOL=BULK_FSOL,
                                                      BULK_BSOL=BULK_BSOL, formfactors=formfactors,datacorr=readcorr)

                    SystemUtility.endCheckQueue()
                    SELSLIB2.evaluateNMA(DicParameters, cm, sym, DicGridConn, "8.6_NMA_" + str(i),
                                         os.path.join(current_directory, "./8.6_NMA/" + str(i) + "/"), i, nqueue15, c)

                if not os.path.exists(os.path.join(current_directory, "./9.6_EXP/" + str(i) + "/solCC.sum")):
                    currentClusterDir= os.path.normpath(os.path.join(current_directory, "9.6_EXP",str(i)))

                    # NS, delete the old cluster expansion folder if it is already present (meaning it had finished incorrectly in a previous run)
                    if ANOMALOUS and os.path.exists(currentClusterDir):

                        try :
                            shutil.rmtree(currentClusterDir)
                            print("REMARK: It seems that the folder {} exists from a previous interrupted run, deleting it.".format(currentClusterDir))


                        except:
                            print("WARNING, cannot delete {}".format(currentClusterDir))

                    SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                    (nqueue14, convNames_4) = SELSLIB2.startExpansion(cm, sym, "9.6_EXP_" + str(i),
                                                                      os.path.join(current_directory,
                                                                                   "./9.6_EXP/" + str(i) + "/"), hkl,
                                                                      ent, nice, cell_dim, spaceGroup, shlxLinea0,
                                                                      os.path.join(current_directory,
                                                                                   "./8.6_NMA/" + str(i) + "/"),
                                                                      fragdomain=True, initCCAnom=initCCAnom,**startExpAnomDic)

                    SystemUtility.endCheckQueue()
                    if ANOMALOUS:

                        # if "9.6_EXP" not in solutions_filtered_out[str(i)] or os.path.exists(os.path.join(ANOMDIR,'filteredSol.json')):
                        #     #reinitialize the dictionnary of eliminated solutions for this cluster since it will be recomputed
                        #     #solutions_filtered_out={}
                        #     print("REMARK: Erasing previous recorded filtered solutions from filteredSol.json for cluster {} and step {}".format(i,"9_EXP"))
                        #     solutions_filtered_out[str(i)]["9.6_EXP"]=[]

                        #Get the llg and zscore for all solutions:
                        llgdic= ANOMLIB.llgdic(convNames, CluAll)
                        CC_Val3, eliminatedSol = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9.6_EXP_" + str(i),
                                                          outputDicr=os.path.join(current_directory, "./9.6_EXP/" + str(i) + "/"),
                                                          nqueue=nqueue14, convNames=convNames_4, savePHS=savePHS,
                                                          archivingAsBigFile=archivingAsBigFile,
                                                          phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim, anomDic=startExpAnomDic, pattersonPeaks=pattersonPeaks, isBORGES=True, llgdic=llgdic)
                       
                        if ANOM_HARD_FILTER:
                            # Eliminate in the ends solutions which have been either discarded in 9.5EXP or 9.5 (fast since few models remain in the end)               
                            #solutions_filtered_out[str(i)]["9.6_EXP"] += eliminatedSol
                            CC_Val1, CC_Val2, CC_Val3 = ANOMLIB.intersectCCVal([CC_Val1,CC_Val2,CC_Val3])
                        # else:
                        #     # eliminate in the end only solutions which have been discarded in BOTH 9.5EXP and 9.5 (more models retained)
                        #     solutions_filtered_out[str(i)]["9.6_EXP"] = ANOMLIB.intersectionFilteredSol([CC_Val1,CC_Val2,CC_Val3], eliminatedSol)

                        # if len(solutions_filtered_out[str(i)]["9.6_EXP"])>0:
                        #     print("REMARK: filtering out %d solutions after evaluateExp_CC 9.6_exp"%len(solutions_filtered_out[str(i)]["9.6_EXP"]))                        
                        #     ANOMLIB.saveFilteredSol(os.path.join(ANOMDIR,'filteredSol.json'),solutions_filtered_out)
                            
                            

                    else:
                        CC_Val3 = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9.6_EXP_" + str(i),
                                                          outputDicr=os.path.join(current_directory, "./9.6_EXP/" + str(i) + "/"),
                                                          nqueue=nqueue14, convNames=convNames_4, savePHS=savePHS,
                                                          archivingAsBigFile=archivingAsBigFile,
                                                          phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim)                        

                    # SystemUtility.close_connection(DicGridConn,DicParameters,cm)
                else:
                    CC_Val3, con4 = SELSLIB2.readCCValFromSUM(os.path.join(current_directory, "./9.6_EXP/" + str(i) + "/solCC.sum"))
                    if ANOMALOUS and ANOM_HARD_FILTER:
                        # The solutions eliminated here must be removed from the previous CCVal3 list:
                        CC_Val1, CC_Val2, CC_Val3 = ANOMLIB.intersectCCVal([CC_Val1,CC_Val2,CC_Val3])
            elif USE_OCC:
                if not os.path.exists(os.path.join(current_directory, "./8.6_OCC/" + str(i) + "/")):
                    SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                    (nqueue15, c) = SELSLIB2.startOCC(DicParameters=DicParameters, cm=cm, sym=sym,
                                                      nameJob="8.6_OCC_" + str(i), dir_o_liFile=path_rnps,
                                                      outputDire=os.path.join(current_directory,
                                                                              "./8.6_OCC/" + str(i) + "/"), mtz=mtz,
                                                      MW=MW, NC=NC, F=F, SIGF=SIGF, Intensities=Intensities,
                                                      Aniso=Aniso, normfactors=normfactors, tncsfactors=tncsfactors,
                                                      nice=nice, RMSD=RMSD, lowR=99, highR=res_refin, final_rot=peaks,
                                                      save_rot=peaks, frag_fixed=fixed_frags, spaceGroup=spaceGroup,
                                                      ellg=None, nres=None, rangeocc=None,
                                                      merge=None, occfrac=None, occoffset=None, ncycles=None, VRMS=VRMS,
                                                      BFAC=BFAC, BULK_FSOL=BULK_FSOL, BULK_BSOL=BULK_BSOL,
                                                      formfactors=formfactors,datacorr=readcorr)

                    SystemUtility.endCheckQueue()
                    SELSLIB2.evaluateOCC(DicParameters, cm, sym, DicGridConn, "8.6_OCC_" + str(i),
                                         os.path.join(current_directory, "./8.6_OCC/" + str(i) + "/"), nqueue15, c)

                # 9.6 EXP    
                if not os.path.exists(os.path.join(current_directory, "9.6_EXP", str(i), "solCC.sum")):
                    currentClusterDir= os.path.normpath(os.path.join(current_directory, "9.6_EXP",str(i)))

                    # NS, delete the old cluster expansion folder if it is already present (meaning it had finished incorrectly in a previous run)
                    if ANOMALOUS and os.path.exists(currentClusterDir):
                        
                        try :
                            shutil.rmtree(currentClusterDir)
                            print("REMARK: It seems that the folder {} exists from a previous interrupted run, deleting it.".format(currentClusterDir))

                        except:
                            print("WARNING, cannot delete {}".format(currentClusterDir))
                        SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                    (nqueue14, convNames_4) = SELSLIB2.startExpansion(cm, sym, "9.6_EXP_" + str(i),
                                                                      os.path.join(current_directory,
                                                                                   "./9.6_EXP/" + str(i) + "/"), hkl,
                                                                      ent, nice, cell_dim, spaceGroup, shlxLinea0,
                                                                      os.path.join(current_directory,
                                                                                   "./8.6_OCC/" + str(i) + "/"),
                                                                      fragdomain=True, initCCAnom=initCCAnom,**startExpAnomDic)

                    SystemUtility.endCheckQueue()
                    if ANOMALOUS:

                        # if "9.6_EXP" not in solutions_filtered_out[str(i)] or os.path.exists(os.path.join(ANOMDIR,'filteredSol.json')):
                        #     #reinitialize the dictionnary of eliminated solutions for this cluster since it will be recomputed
                        #     #solutions_filtered_out={}
                        #     print("REMARK: Erasing previous recorded filtered solutions from filteredSol.json for cluster {} and step {}".format(i,"9.6_EXP"))
                        #     solutions_filtered_out[str(i)]["9.6_EXP"]=[]


                        #Get the llg and zscore for all solutions:
                        llgdic= ANOMLIB.llgdic(convNames, CluAll)
                        CC_Val3, eliminatedSol = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9.6_EXP_" + str(i),
                                                          outputDicr=os.path.join(current_directory, "./9.6_EXP/" + str(i) + "/"),
                                                          nqueue=nqueue14, convNames=convNames_4, savePHS=savePHS,
                                                          archivingAsBigFile=archivingAsBigFile,
                                                          phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim, anomDic=startExpAnomDic, pattersonPeaks=pattersonPeaks, isBORGES=True, llgdic=llgdic)
                        
                        if ANOM_HARD_FILTER:
                            # Eliminate in the ends solutions which have been either discarded in 9.5EXP or 9.5 (fast since few models remain in the end)               
                            #solutions_filtered_out[str(i)]["9.6_EXP"] += eliminatedSol
                            CC_Val1, CC_Val2, CC_Val3 = ANOMLIB.intersectCCVal([CC_Val1,CC_Val2,CC_Val3])
                        # else:
                        #     # eliminate in the end only solutions which have been discarded in BOTH 9.5EXP and 9.5 (more models retained)
                        #     solutions_filtered_out[str(i)]["9.6_EXP"] = ANOMLIB.intersectionFilteredSol([CC_Val1,CC_Val2,CC_Val3], eliminatedSol)

                        # if len(solutions_filtered_out[str(i)]["9.6_EXP"])>0:                       
                        #     ANOMLIB.saveFilteredSol(os.path.join(ANOMDIR,'filteredSol.json'),solutions_filtered_out)                     
                        
                    else:
                        CC_Val3 = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9.6_EXP_" + str(i),
                                                          outputDicr=os.path.join(current_directory, "./9.6_EXP/" + str(i) + "/"),
                                                          nqueue=nqueue14, convNames=convNames_4, savePHS=savePHS,
                                                          archivingAsBigFile=archivingAsBigFile,
                                                          phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim)                        

                    # SystemUtility.close_connection(DicGridConn,DicParameters,cm)
                else:
                    CC_Val3, con4 = SELSLIB2.readCCValFromSUM(os.path.join(current_directory, "./9.6_EXP/" + str(i) + "/solCC.sum"))
                    if ANOMALOUS:
                        if ANOM_HARD_FILTER:
                            # The solutions eliminated here must be removed from the previous CCVal1 and CCval2 lists:
                            CC_Val1, CCVal2, CC_Val3 = ANOMLIB.intersectCCVal([CC_Val1,CC_Val2,CC_Val3])
                        # else:
                        #     solutions_filtered_out[str(i)]["9.6_EXP"] = ANOMLIB.intersectionFilteredSol([CC_Val1,CC_Val2,CC_Val3], eliminatedSol)

            else:
                CC_Val3 = []

            convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters, os.path.join(path_rnps,"clustersNoRed.sum"), "ROTSOL", LIMIT_CLUSTER=i,give_fixed_frags=True)
            
            #NS: here we have to refilter CluAll to what it was after 8_RBR and all subsequent steps, CC_Val1, CC_Val2, CC_Val3 are already filtered in their respective evaluateExp function
            if ANOMALOUS:

                # print("length CC_val1 %d"%len(CC_Val1))
                # print("length CC_val2 %d"%len(CC_Val2))
                # print("length CC_val3 %d"%len(CC_Val3))
                # sys.exit(1)

                if len(CC_Val1)==0 and len(CC_Val2)==0 and len(CC_Val3)==0:
                    print("SORRY: it seems that no solution survived the anomalous scoring process!")
                    print("Next Cluster!")
                    arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)
                    continue

                #Now we can filter CluAll    
               #CluAll = ANOMLIB.filterCluAll(CluAll, solutions_filtered_out[str(i)], LIMIT_CLUSTER=i , convNamesDic=convNamesAnom)
                #print("REMARK: Removing %d eliminated solutions from CluAll (from the anomalous scoring process)"%len(solutions_filtered_out[str(i)]))

            if not USE_OCC:
                CC_Val = SELSLIB2.unifyCC2(CC_Val1, CC_Val2, CC_Val3, convNames, CluAll, suffixA="_rnp",
                                           suffixB="_rottra", suffixC="_nma",
                                           solution_sorting_scheme=solution_sorting_scheme, mode="ARCIMBOLDO_BORGES")
                sufix = ['_rnp.pdb', '_rottra.pdb', '_nma.pdb']

            elif prioritize_occ:
                CC_Val = SELSLIB2.unifyCC2([], [], CC_Val3, convNames, CluAll, suffixA="_rnp", suffixB="_rottra",
                                           suffixC="_occ", solution_sorting_scheme=solution_sorting_scheme, mode="ARCIMBOLDO_BORGES")
                sufix = ['_rnp.pdb', '_rottra.pdb', '_occ.pdb']
            else:
                CC_Val = SELSLIB2.unifyCC2(CC_Val1, CC_Val2, CC_Val3, convNames, CluAll, suffixA="_rnp",
                                           suffixB="_rottra", suffixC="_occ",
                                           solution_sorting_scheme=solution_sorting_scheme, mode="ARCIMBOLDO_BORGES")
                sufix = ['_rnp.pdb', '_rottra.pdb', '_occ.pdb']

            if USE_NMA or USE_OCC:
                SELSLIB2.writeOutputFile(lock, DicParameters, CluAll, current_directory, nameOutput,
                                         "ARCIMBOLDO-BORGES", "INITCC", convNames, fixed_frags,
                                         path1=os.path.join(current_directory, "./9.5_EXP/" + str(i) + "/solCC.sum"),
                                         path2=os.path.join(current_directory, "./9.6_EXP/" + str(i) + "/solCC.sum"),
                                         LIMIT_CLUSTER=i,coiled_coil=coiled_coil)
            else:
                SELSLIB2.writeOutputFile(lock, DicParameters, CluAll, current_directory, nameOutput,
                                         "ARCIMBOLDO-BORGES", "INITCC", convNames, fixed_frags,
                                         path1=os.path.join(current_directory, "./9.5_EXP/" + str(i) + "/solCC.sum"),
                                         path2=os.path.join(current_directory, "./9_EXP/" + str(i) + "/solCC.sum"),
                                         LIMIT_CLUSTER=i,coiled_coil=coiled_coil)

            # NS: again, an empty dictionary will be returned here if CC_Val is []
            convNames14 = SELSLIB2.startPREPARE(cm, sym, "10_PREPARED_" + str(i), CC_Val,
                                                os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/"),
                                                cell_dim, spaceGroup, topExp)

            arci_output.generateHTML(lock, current_directory, nameOutput,coiled_coil=coiled_coil)

            if topExp_run is not None:
                if os.path.exists(os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/")):
                    for r, subF, fi in os.walk(os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/")):
                        for fileu in fi:
                            pdbf = os.path.join(r, fileu)
                            if pdbf.endswith(".pdb"):
                                os.remove(pdbf)

                # General multiprocessing case
                if distribute_computing == "multiprocessing":
                    topExp_run = sym.PROCESSES - 1

                # In the case that it is multiprocessing but with less than 8 cores
                if distribute_computing == "multiprocessing" and sym.PROCESSES - 1 < 8:
                    topExp_run = 2 * (sym.PROCESSES - 1)

                if force_exp:
                    # Take the topExp value and use it
                    topExp_run = topExp


                convNames14 = SELSLIB2.startPREPARE(cm, sym, "10_PREPARED_" + str(i), CC_Val,
                                                    os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/"),
                                                    cell_dim, spaceGroup, topExp_run)



                completernp = "RBR"
                if RNP_GYRE:
                    completernp = "GIMBLE"

                # NOTE: New method to extend solutions randomly
                if randomAtoms or SecStrElong:
                    convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters,
                                                                                               os.path.join(
                                                                                                   current_directory,
                                                                                                   "./8_" + completernp + "/" + str(
                                                                                                       i) + "/clustersNoRed.sum"),
                                                                                               "ROTSOL",
                                                                                               LIMIT_CLUSTER=i,
                                                                                               give_fixed_frags=True)
                    if not os.path.exists(os.path.join(current_directory, "./2015_EXPLOIT/" + str(i) + "/")):
                        if randomAtoms:
                            lisvalto = (Config.get(job_type, "parameters_elongation")).split()
                            vala = float(lisvalto[0])
                            valb = int(lisvalto[1])
                            valc = int(lisvalto[2])
                            SELSLIB2.startRandomlyExpand(
                                os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/"),
                                os.path.join(current_directory, "./2015_EXPLOIT/" + str(i) + "/"), vala, valb, valc)
                        elif SecStrElong:
                            lisvalto = (Config.get(job_type, "parameters_elongation")).split()
                            vala = int(lisvalto[0])
                            valb = int(lisvalto[1])
                            valc = int(lisvalto[2])
                            SELSLIB2.startPlaneElongation(
                                os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/"),
                                os.path.join(current_directory, "./2015_EXPLOIT/" + str(i) + "/"), vala, valb, valc)


                    if not os.path.exists(os.path.join(current_directory, "9.6_EXP_REXPL", str(i), "solCC.sum")):

                        currentClusterDir= os.path.normpath(os.path.join(current_directory, "9.6_EXP_REXPL",str(i)))

                        # NS, delete the old cluster expansion folder if it is already present (meaning it had finished incorrectly in a previous run)
                        if ANOMALOUS and os.path.exists(currentClusterDir):

                            try :
                                shutil.rmtree(currentClusterDir)
                                print("REMARK: It seems that the folder {} exists from a previous interrupted run, deleting it.".format(currentClusterDir))

                            except:
                                print("WARNING, cannot delete {}".format(currentClusterDir))


                        SystemUtility.open_connection(DicGridConn, DicParameters, cm)

                        (nqueue14, convNames_4) = SELSLIB2.startExpansion(cm, sym, "9.6_EXPREXPL_" + str(i),
                                                                          os.path.join(current_directory,"./9.6_EXP_REXPL/" + str(i) + "/"), hkl, ent, nice,
                                                                          cell_dim, spaceGroup, shlxLinea0 + " -o",
                                                                          os.path.join(current_directory,"./2015_EXPLOIT/" + str(i) + "/"), fragdomain=True, initCCAnom=initCCAnom,**startExpAnomDic)

                        SystemUtility.endCheckQueue()
                        if ANOMALOUS:

                            # if "9.6_EXP_REXPL" not in solutions_filtered_out[str(i)] or os.path.exists(os.path.join(ANOMDIR,'filteredSol.json')):
                            #     #reinitialize the dictionnary of eliminated solutions for this cluster since it will be recomputed
                            #     #solutions_filtered_out={}
                            #     print("REMARK: Erasing previous recorded filtered solutions from filteredSol.json for cluster {} and step {}".format(i,"9.6_EXP_REXPL"))
                            #     solutions_filtered_out[str(i)]["9.6_EXP_REXPL"]=[]


                            #Get the llg and zscore for all solutions:
                            llgdic= ANOMLIB.llgdic(convNames, CluAll)
                            CC_Val3, eliminatedSol = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9.6_EXPREXPL_" + str(i),
                                                              outputDicr=os.path.join(current_directory,
                                                                           "./9.6_EXP_REXPL/" + str(i) + "/"), nqueue=nqueue14,
                                                              convNames=convNames_4, initcc_global=True, savePHS=savePHS,
                                                              archivingAsBigFile=archivingAsBigFile,
                                                              phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim, anomDic=startExpAnomDic, pattersonPeaks=pattersonPeaks, isBORGES=True, llgdic=llgdic)
                            
                            #if ANOM_HARD_FILTER:
                                # Here we'll keep the HARD_FILTER mode by default to work only with what previously retained before               
                            #solutions_filtered_out[str(i)]["9.6_EXP_REXPL"] += eliminatedSol
                            if ANOM_HARD_FILTER:
                                CC_Val1, CC_Val2, CC_Val3 = ANOMLIB.intersectCCVal([CC_Val1,CC_Val2,CC_Val3])
                            #else:
                            #    solutions_filtered_out[str(i)] = ANOMLIB.intersectionFilteredSol(solutions_filtered_out[str(i)], eliminatedSol)

                            # if len(eliminatedSol)>0:
                            #     ANOMLIB.saveFilteredSol(os.path.join(ANOMDIR,'filteredSol.json'),solutions_filtered_out)
                                #CluAll = ANOMLIB.filterCluAll(CluAll, solutions_filtered_out[str(i)], LIMIT_CLUSTER=i , convNamesDic=convNamesAnom)
                                

                        else:
                            CC_Val3 = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="9.6_EXPREXPL_" + str(i),
                                                              outputDicr=os.path.join(current_directory,
                                                                           "./9.6_EXP_REXPL/" + str(i) + "/"), nqueue=nqueue14,
                                                              convNames=convNames_4, initcc_global=True, savePHS=savePHS,
                                                              archivingAsBigFile=archivingAsBigFile,
                                                              phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim)                            

                        # SystemUtility.close_connection(DicGridConn,DicParameters,cm)
                    else:
                        CC_Val3, con4 = SELSLIB2.readCCValFromSUM(os.path.join(current_directory, "./9.6_EXP_REXPL/" + str(i) + "/solCC.sum"))
                        if ANOMALOUS and ANOM_HARD_FILTER:
                            CC_Val1, CC_Val2, CC_Val3 = ANOMLIB.intersectCCVal([CC_Val1,CC_Val2,CC_Val3])

                        # CC_Val = SELSLIB2.selectCC(CC_Val3)
                    CC_Val = CC_Val3
                    shutil.rmtree(os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/"))
                    convNames14 = SELSLIB2.startPREPARE(cm, sym, "10_PREPARED_" + str(i), CC_Val,
                                                        os.path.join(current_directory,
                                                                     "./10_PREPARED/" + str(i) + "/"), cell_dim,
                                                        spaceGroup, topExp)

                ######################################################

                convNames, CluAll, RotClu, encn, nfixfr = SELSLIB2.readClustersFromSUMToDB(DicParameters, os.path.join(
                    current_directory, "./8_" + completernp + "/" + str(i) + "/clustersNoRed.sum"), "ROTSOL",
                                                                                           LIMIT_CLUSTER=i,give_fixed_frags=True)
                # NS re-filtering since CluAll has been called from before
                if ANOMALOUS: # and len(solutions_filtered_out[str(i)])>0:
                    #CluAll = ANOMLIB.filterCluAll(CluAll, solutions_filtered_out[str(i)], LIMIT_CLUSTER=i,convNamesDic=convNamesAnom)
                    #Get the llg and zscore for all solutions: # added 07Feb2019
                    #convNamesAnom.update(convNames)
                    llgdic= ANOMLIB.llgdic(convNames, CluAll)

                addo = ""
                if randomAtoms or SecStrElong:
                    addo += " -o"

                if unbias and not coiled_coil:
                    if not '-V' in shlxLineaUnbias and (float(shelxe_version)>float(2021.1)):
                        shlxLineaUnbias += ' -V'

                    if '-O3' in shlxLineaUnbias:
                        shlxLineaUnbias = shlxLineaUnbias.replace('-O3', '')

                    print("The shelxe line used for the unbias will be: ", shlxLineaUnbias)
            
                    if skip_predicted:
                        shutil.rmtree(os.path.join(current_directory, "./10_PREPARED/" + str(i) + "/"))
                        convNames = SELSLIB2.start_prepare_unbias(model_directory, os.path.join(current_directory,"./10_PREPARED/" + str(i) + "/"), cell_dim, spaceGroup)

                    failure_all = SELSLIB2.shelxe_cycle_BORGES(lock=lock, DicParameters=DicParameters, ClusAll=CluAll, cm=cm, sym=sym,
                                                               DicGridConn=DicGridConn, i=i,current_directory=current_directory,
                                                               nameOutput=nameOutput, dirPathPart=os.path.join(current_directory,
                                                                                                               "./temp_transfer/" + str(i) + "/"),
                                                               fromNcycles=1, toNcycles=2, spaceGroup=spaceGroup,
                                                               hkl=hkl, ent=ent, seq=seq, cell_dim=cell_dim, shlxLineaB='',
                                                               shlxLineaLast= shlxLineaUnbias, traceShelxe=True, fixed_frags=fixed_frags,
                                                               USE_PACKING=USE_PACKING, USE_TRANSLA=USE_TRANSLA, USE_REFINEMENT=PERFORM_REFINEMENT_P1,
                                                               nice=nice, NUMBER_REF_CYCLES=cycle_ref, USE_RGR=USE_RGR,
                                                               isSHREDDER=isShredder, is_unbias_exp=True, startExpAnomDic=startExpAnomDic,
                                                               pattersonPeaks=pattersonPeaks, llgdic=llgdic, nBunchAutoTracCyc=nBunchAutoTracCyc)

                    if failure_all:
                        print('WARNING: In rotation cluster ', i, ' all shelxe jobs failed to trace')
                    else:
                        for r1, subF1, fi1 in os.walk(os.path.join(current_directory,"./12_EXP_UNBIAS/" + str(i) + "/")):
                            for fileu1 in fi1:
                                pdbf1 = os.path.join(r1, fileu1)
                                if pdbf1[-7:-4]=="rnp":
                                    os.rename(pdbf1, pdbf1[:-8] + pdbf1[-4:])
                        alixe = True
                        alixe_mode = 'monomer'

                    if not os.path.exists(os.path.join(current_directory, "12.5_PREPARED_UNBIAS", str(i), "solCC.sum")):
                        currentClusterDir = os.path.normpath(os.path.join(current_directory, "12.5_PREPARED_UNBIAS", str(i)))

                        if os.path.exists(currentClusterDir):
                            try:
                                shutil.rmtree(currentClusterDir)
                                print(
                                    "REMARK: It seems that the folder {} exists from a previous interrupted run, deleting it.".format(
                                        currentClusterDir))
                            except:
                                print("WARNING, cannot delete {}".format(currentClusterDir))

                        SystemUtility.open_connection(DicGridConn, DicParameters, cm)
                        print("\n****** Calculate phs from model-free-bias traces for cluster {} ******\n".format(i))

                        (nqueue12, convNames_12) = SELSLIB2.startExpansion(cm, sym, "12.5_PREPARED_UNBIAS_" + str(i),
                                                                         os.path.join(current_directory, "./12.5_PREPARED_UNBIAS/"
                                                                                      + str(i) + "/"), hkl, ent, nice,
                                                                         cell_dim, spaceGroup, shlxLinea0,
                                                                         os.path.join(current_directory,
                                                                                      "./12_EXP_UNBIAS/" + str(i) + "/"),
                                                                         fragdomain=True, initCCAnom=initCCAnom,
                                                                         **startExpAnomDic)
                        SystemUtility.endCheckQueue()


                        CC_Val4 = SELSLIB2.evaluateExp_CC(DicParameters=DicParameters, cm=cm, sym=sym, DicGridConn=DicGridConn, nameJob="12.5_PREPARED_UNBIAS_" + str(i),
                                                          outputDicr=os.path.join(current_directory, "./12.5_PREPARED_UNBIAS/" + str(i) + "/"), nqueue=nqueue12,
                                                          convNames=convNames_12, savePHS=True, archivingAsBigFile=archivingAsBigFile,
                                                          phs_fom_statistics=phs_fom_statistics, fragNumber=i, spaceGroupNum=sg_number, cell_dim=cell_dim)
                    else:
                        print("se ha saltado el crear el solCC")
                        CC_Val4, con4 = SELSLIB2.readCCValFromSUM(os.path.join(current_directory,
                                                                               "./12.5_PREPARED_UNBIAS/" + str(i) + "/solCC.sum"))


                
                if alixe:
                    skip_cluster_alixe=False
                    runstring = ""
                    tuple_phi = ()
                    not_expanded = True
                    if isShredder:
                        runstring = "SHREDDER"
                    else:
                        runstring = "BORGES"
                    # NS: check that the directory in which alixe will work contains at least one phs file
                    # For this we can check the size of sumCC.sol in 9, 9.5 and 9.6 folders
                    input_mode=0

                    if not unbias:
                        for folder in (9,9.5,9.6):
                            fileToCheck=os.path.join(current_directory, str(folder)+'_EXP', str(i), 'solCC.sum')
                            if os.path.exists(fileToCheck) and os.path.getsize(fileToCheck)>0:
                                input_mode = folder
                                break
                    else: #NOTE AMB: if unbias, the .phs generated out of the new trace are in the folder 12.5_PREPARED_UNBIAS
                        fileToCheck=os.path.join(current_directory, str(12.5)+'_PREPARED_UNBIAS', str(i), 'solCC.sum')
                        if os.path.exists(fileToCheck) and os.path.getsize(fileToCheck)>0:
                            input_mode = 12.5

                        try:
                            print("The path for chescat is ", ali_confdict['path_chescat'])
                        except:
                            SELSLIB2.PATH_CHESCAT = Config.get("LOCAL", "path_local_chescat")
                            if SELSLIB2.PATH_CHESCAT == '':
                                if sys.platform == "darwin":
                                    SELSLIB2.PATH_CHESCAT = os.path.join(os.path.dirname(__file__),
                                                                         "executables/chescat_mac")
                                else:
                                    SELSLIB2.PATH_CHESCAT = os.path.join(os.path.dirname(__file__),
                                                                         "executables/chescat_linux")
                            if not al.check_path_chescat(SELSLIB2.PATH_CHESCAT):
                                print(colored("FATAL:", "red"),
                                      "The path given for chescat: " + str(os.path.abspath(SELSLIB2.PATH_CHESCAT)) + \
                                      " does not exist or it is not accessible to the user")
                                sys.exit(0)
                            else:
                                ali_confdict = {}
                                ali_confdict['path_chescat'] = SELSLIB2.PATH_CHESCAT

                    # NOTE CM: add a check to avoid calling start alixe function with a cluster with a single solution
                    values = SELSLIB2.readCCValFromSUM(fileToCheck)
                    if len(values[0]) == 1:
                        print('Only a single solution present in this rotation cluster, no ALIXE will be performed')
                        skip_cluster_alixe=True
                    if input_mode == 0: # This would only happen if Nico's MR-SAD has filtered every solution
                        print("No folder with solCC.sum could be found for ALIXE, SKIPPING TO NEXT CLUSTER")
                        continue
                        
                    if not skip_cluster_alixe:
                        # General config no matter whether one or two steps
                        ali_confdict['number_cores_parallel'] = sym.PROCESSES
                        if ent:
                            ali_confdict['ent_file'] = ent
                            ali_confdict['postmortem'] = True
                            ali_confdict['ccfromphi'] = True
                        else:
                            ali_confdict['postmortem'] = False
                        # NOTE CM: in principle these three are only need if either postmortem or fused are being checked
                        ali_confdict['hkl_file'] = hkl
                        ali_confdict['shelxe_line_alixe'] = shlxLinea0
                        ali_confdict['shelxe_path'] = SELSLIB2.PATH_NEW_SHELXE
                        # NOTE CM: adding fusedcoord to True while I program the usage of an external alixe config file.
                        ali_confdict['fusedcoord'] = True
                        # Prepare output folders
                        clust_fold_root = os.path.join(current_directory, "./11.5_CLUSTERING/")

                        ali_confdict = al.fill_ali_confdict_with_defaults(ali_confdict,current_directory,program=runstring)

                        if unbias and not coiled_coil:
                            ali_confdict['tolerance_first_round'] = 80.0
                            clust_fold_root = os.path.join(current_directory, "./13.5_CLUSTERING/")
                        al.check_dir_or_make_it(clust_fold_root, remove=False)
                        clust_fold_rotclu = os.path.abspath(os.path.join(clust_fold_root, str(i)))

                        if alixe_mode == 'monomer':
                            tuple_phi, ali_confdict = al.startALIXEforARCIMBOLDO_OneStep(ali_confdict=ali_confdict,
                                                                                         input_mode=input_mode,
                                                                                         wd=current_directory,
                                                                                         path_rotclu=clust_fold_rotclu,
                                                                                         type_run=runstring,
                                                                                         limit_references=topExp_run)
                            # Format tuple_phi = (name.ins, list_files_to_expand)
                            if tuple_phi[1] != []:  # If any phi, call SELSLIB2.shelxe_cycle_BORGES
                                print('\n * Info * ALIXE found phase sets combining in monomer mode in rotation cluster '+str(i))
                                print('            sending them to SHELXE expansion\n')

                                failure_all = SELSLIB2.shelxe_cycle_BORGES(lock=lock, DicParameters=DicParameters,
                                                                           ClusAll=CluAll, cm=cm,sym=sym,
                                                                           DicGridConn=DicGridConn, i=i,
                                                                           current_directory=current_directory,
                                                                           nameOutput=nameOutput,
                                                                           dirPathPart=os.path.join(current_directory,
                                                                                                    "./temp_transfer/" +
                                                                                                    str(i) + "/"),
                                                                           fromNcycles=1, toNcycles=nautocyc,
                                                                           spaceGroup=spaceGroup, hkl=hkl, ent=ent, seq=seq,
                                                                           cell_dim=cell_dim, nice=nice,
                                                                           shlxLineaB=shlxLinea1 + addo,
                                                                           shlxLineaLast=shlxLineaLast, traceShelxe=True,
                                                                           fixed_frags=fixed_frags, USE_PACKING=USE_PACKING,
                                                                           USE_TRANSLA=USE_TRANSLA,
                                                                           USE_REFINEMENT=PERFORM_REFINEMENT_P1,
                                                                           NUMBER_REF_CYCLES=cycle_ref, USE_RGR=USE_RGR,
                                                                           isSHREDDER=isShredder, tuple_phi=tuple_phi,
                                                                           is_alixe_exp=True, is_unbias_exp=unbias,
                                                                           startExpAnomDic=startExpAnomDic,
                                                                           pattersonPeaks=pattersonPeaks,llgdic=llgdic,
                                                                           nBunchAutoTracCyc=nBunchAutoTracCyc)
                        elif alixe_mode == 'multimer':
                            for clu in evaluated_clusters:
                                clust_fold_rotclu = os.path.abspath(os.path.join(clust_fold_root, str(clu)))
                                path_pickle = os.path.join(clust_fold_rotclu, str(clu) + '_dictio_clustering_alixe.pkl')
                                if not os.path.exists(path_pickle):
                                    # ali_confdict, input_mode, wd, path_rotclu, type_run, limit_references):
                                    tuple_phi, ali_confdict = al.startALIXEforARCIMBOLDO_OneStep(ali_confdict=ali_confdict,
                                                                                                 input_mode=input_mode,
                                                                                                 wd=current_directory,
                                                                                                 path_rotclu=clust_fold_rotclu,
                                                                                                 type_run=runstring,
                                                                                                 limit_references=topExp_run)
                                else:
                                    print('\n * Info * The monomer step of ALIXE was already completed for rotation cluster ',clu)

                            # Now we can go to the second step
                            # Note, if we could, passing a list instead of a single cluster id
                            tuple_phi_second, ali_confdict = al.startALIXEforARCIMBOLDO_TwoSteps(ali_confdict, clust_fold_root)

                            # If any phi,
                            # and if this was not yet performed
                            # call SELSLIB2.shelxe_cycle_BORGES
                            if os.path.exists(os.path.join(current_directory,'11_EXP_alixe')):
                                not_expanded = False
                            if tuple_phi_second[1] != {} and not_expanded: #and not os.path.exists(os.path.ijoin(current_directory,'11_EXP_alixe')): # we should check this internally in shelxe_cycles
                                print('\n * Info * ALIXE found phase sets combining in multimer mode')
                                print('sending them to SHELXE expansion\n')
                                failure_all = SELSLIB2.shelxe_cycle_BORGES(lock=lock, DicParameters=DicParameters,
                                                                           ClusAll=CluAll, cm=cm,
                                                                           sym=sym, DicGridConn=DicGridConn, i=i,
                                                             current_directory=current_directory, nameOutput=nameOutput,
                                                             dirPathPart=os.path.join(current_directory,
                                                                                      "./temp_transfer/" + str(i) + "/"),
                                                             fromNcycles=1, toNcycles=nautocyc, spaceGroup=spaceGroup, hkl=hkl,
                                                             ent=ent, seq=seq, cell_dim=cell_dim, nice=nice,
                                                             shlxLineaB=shlxLinea1 + addo, shlxLineaLast=shlxLineaLast,
                                                             traceShelxe=True,fixed_frags=fixed_frags,
                                                             USE_PACKING=USE_PACKING,USE_TRANSLA=USE_TRANSLA,
                                                             USE_REFINEMENT=PERFORM_REFINEMENT_P1,NUMBER_REF_CYCLES=cycle_ref,
                                                             USE_RGR=USE_RGR,isSHREDDER=isShredder,
                                                             tuple_phi=tuple_phi_second, is_alixe_exp=True,
                                                             startExpAnomDic=startExpAnomDic, pattersonPeaks=pattersonPeaks,
                                                             llgdic=llgdic, nBunchAutoTracCyc=nBunchAutoTracCyc)

                if coiled_coil:
                    clu_all_merged.append(copy.deepcopy(CluAll))
                    conv_names_merged.append(copy.deepcopy(convNames))

                # NS: Here the pdb files to be extended will be looked for in the directory temp_transfer (from the previous startPREPARE funcions)
                # If no phase cluster has solved keep going with normal expansions

                if (Config.getboolean("ARCIMBOLDO-BORGES", "multicopy") == True and Config.getboolean("ARCIMBOLDO-BORGES", "skip_expansion") == True) or unbias:
                    print("Shelxe expansions will be skipped")
                else:
                    failure_all = SELSLIB2.shelxe_cycle_BORGES(lock=lock, DicParameters=DicParameters, ClusAll=CluAll, cm=cm, sym=sym,
                                                 DicGridConn=DicGridConn, i=i, current_directory=current_directory,
                                                 nameOutput=nameOutput, dirPathPart=os.path.join(current_directory,
                                                                                                 "./temp_transfer/" + str(
                                                                                                     i) + "/"),
                                                 fromNcycles=1, toNcycles=nautocyc, spaceGroup=spaceGroup, hkl=hkl, ent=ent, seq=seq,
                                                 cell_dim=cell_dim,shlxLineaB=shlxLinea1 + addo,shlxLineaLast=shlxLineaLast,
                                                 traceShelxe=True, fixed_frags=fixed_frags, USE_PACKING=USE_PACKING,
                                                 USE_TRANSLA=USE_TRANSLA,USE_REFINEMENT=PERFORM_REFINEMENT_P1, nice=nice,
                                                 NUMBER_REF_CYCLES=cycle_ref,USE_RGR=USE_RGR, isSHREDDER=isShredder,
                                                 startExpAnomDic=startExpAnomDic, pattersonPeaks=pattersonPeaks,
                                                               llgdic=llgdic, nBunchAutoTracCyc=nBunchAutoTracCyc)

                    if failure_all:
                        print('WARNING: In rotation cluster ',i,' all shelxe jobs failed to trace')

    if coiled_coil:
        try:
            SELSLIB2.verification_coil_predicted(lock=lock, cm=cm, sym=sym, DicGridConn=DicGridConn, DicParameters=DicParameters,
                                                nice=nice, current_dir=current_directory, output_name=nameOutput, job_name="14_VERIFICATION", 
                                                hkl=hkl, seq=seq, clu_all_merged=clu_all_merged, conv_names_merged=conv_names_merged, cell_dim=cell_dim, space_group=spaceGroup, 
                                                shlxLineaB=shlxLinea1, shlxLineaLast=shlxLineaLast, toNcycles=nautocyc, fixed_frags=fixed_frags,
                                                i=i, USE_PACKING=USE_PACKING, USE_TRANSLA=USE_TRANSLA, USE_REFINEMENT=PERFORM_REFINEMENT_P1, 
                                                isSHREDDER=isShredder, startExpAnomDic=startExpAnomDic, llgdic=llgdic, nBunchAutoTracCyc=nBunchAutoTracCyc,
                                                pattersonPeaks=pattersonPeaks,NUMBER_REF_CYCLES=cycle_ref, USE_RGR=USE_RGR)
        except Exception as e:
            print(e)
            print('Coiled-coil verification could not be performed')

    #RUNNING LITE MULTICOPY
    if Config.getboolean("ARCIMBOLDO-BORGES", "multicopy") == True:
        print("\nStarting muticopy step")
        #Reading FOMS for the prioritisation of the 1st fragment
        print('Evaluating the first fragment')
        if os.path.exists(os.path.join(current_directory, '10_PREPARED')):
            list_pdbs = []
            dict_wMPE = {}
            for cluster in evaluated_clusters:
                cluster = str(cluster)
                if cluster not in os.listdir(os.path.join(current_directory, '10_PREPARED')):
                    continue
                try:
                    CC__Val1, con1 = SELSLIB2.readCCValFromSUM(os.path.join(current_directory, "./9_EXP/" + cluster + "/solCC.sum"))
                except:
                    print("There was a problem reading solCC.sum file")
                    CC__Val1 = []
                try:
                    CC__Val2, con2 = SELSLIB2.readCCValFromSUM(os.path.join(current_directory, "./9.5_EXP/" + cluster + "/solCC.sum"))
                except:
                    print("There was a problem reading solCC.sum file")
                    CC__Val2 = []
                try:
                    CC__Val3, con3 = SELSLIB2.readCCValFromSUM(os.path.join(current_directory, "./9.6_EXP/" + cluster + "/solCC.sum"))
                except:
                    print("There was a problem reading solCC.sum file")
                    CC__Val3 = []

                list_CC__Val = [CC__Val1, CC__Val2, CC__Val3]

                for i, CC__Val in enumerate(list_CC__Val):
                    for dict_sol in CC__Val:
                        model = os.path.basename(dict_sol['corresp'])[:-4] + sufix[i]
                        if model in os.listdir(os.path.join(current_directory, '10_PREPARED/') + cluster):
                            list_pdbs.append([cluster, model])
                            if ent:
                                dict_wMPE[cluster + '_'+ model[:-4]] = float(dict_sol['wMPE_end'][0])


        #Writing sum file for the prioritisation of the 1st fragment
        multicopy_prio = os.path.join(current_directory, 'multicopy_prioritisation')
        if not os.path.exists(multicopy_prio):
            os.makedirs(multicopy_prio)

        g1 = open(multicopy_prio + '/prioritisation_1stfrag.sum', 'w')
        if not dict_wMPE:
            g1.write("priorisation\tpdb\tLLG\tZSCORE\n")
        else:
            g1.write("priorisation\tpdb\tLLG\tZSCORE\twMPE_1st_fragment\n")


        for i, pdb in enumerate(list_pdbs):
            f1 = open(os.path.join(current_directory, '10_PREPARED', str(pdb[0]), str(pdb[1])), 'r')
            lines_files = f1.readlines()
            f1.close()
            for line_file in lines_files:
                if line_file.startswith('REMARK  LLG'):
                    llg = line_file.split()[1].split('=')[1]
                    zscore = line_file.split()[2].split('==')[1]
                    break

            if not dict_wMPE:
                g1.write(str(i + 1) + '\t' + str(pdb[0]) + '_' + str(pdb[1]) + '\t' + llg + '\t' + zscore + '\n')
            else:
                g1.write(str(i + 1) + '\t' + str(pdb[0]) + '_' + str(pdb[1]) + '\t' + llg + '\t' + zscore + '\t' + str(dict_wMPE[str(pdb[0]) + '_' + str(pdb[1])[:-4]]) + '\n')

        g1.close()

        #Running individuals ARCIMBOLDO_LITE for each probe. Stopping after the packing for evaluation and prioritisation
        if not os.path.exists(os.path.join(current_directory, 'ARCIMBOLDO_LITE')):
            os.makedirs(os.path.join(current_directory, 'ARCIMBOLDO_LITE'))

        list_FOMS_rotation = []
        list_FOMS_translation = []

        for i, elem in enumerate(list_pdbs):
            cluster_pdb = elem[0] + '_' + elem[1]
            lite_dir = os.path.join(current_directory, 'ARCIMBOLDO_LITE', cluster_pdb[:-4])
            
            if not os.path.exists(lite_dir):
                os.makedirs(lite_dir)
            else:
                print("The directory exists", lite_dir)

            if not os.path.exists(os.path.join(lite_dir,'fixed')):
                os.makedirs(os.path.join(lite_dir,'fixed'))

            shutil.copyfile(os.path.join(current_directory, '10_PREPARED', elem[0], elem[1]), os.path.join(lite_dir, cluster_pdb))
            shutil.copyfile(os.path.join(current_directory, '10_PREPARED', elem[0], elem[1]), os.path.join(lite_dir,'fixed',cluster_pdb))

            inpconf = inputConfig()
            print("Running multicopy", cluster_pdb, lite_dir)
            bordata = __prepareAnewARCIMBOLDOmulticopy(cluster_pdb, lite_dir, cluster_pdb[:-4], Config, inpconf, last_rmsd)
            html_path = os.path.join(bordata.get("GENERAL", "working_directory"), bordata.get("ARCIMBOLDO", "name_job") + ".html")
            SELSLIB2.writeMultiCopyFile(lock, current_directory, nameOutput, bordata.get("ARCIMBOLDO", "name_job"), html_path)
            
            if isShredder:
                aniout = out_phaser_given
            SELSLIB2.LAST_AVAILABLE_ROTID = 0
            SELSLIB2.MAP_OF_ROT_COMB = {}


            #TODO: try exist in case the LITE fails
            ARCIMBOLDO_LITE.startARCIMBOLDO(bordata, "borfile", DicParameters=DicParameters, DicGridConn=DicGridConn,
                                             cm=cm, sym=sym, doTest=False, mtz_given=mtz, F_given=F, SIGF_given=SIGF,
                                             normfactors=normfactors, tncsfactors=tncsfactors, Intensities=Intensities,
                                             Aniso=Aniso, nice=nice, out_phaser_given=aniout, fneed=fneed, isShredder=True,
                                             isMulticopy=True)

            print('Evaluating rotation of the second fragment')
            sum_file_rotation = os.path.join(lite_dir, 'ens1_frag2', '1_FRF_LIBRARY', 'clusters.sum')
            if os.path.exists(sum_file_rotation):
                list_FOMS_rotation.append([cluster_pdb[:-4], SELSLIB2.BestFOMSFromSUM(sum_file_rotation)[0],SELSLIB2.BestFOMSFromSUM(sum_file_rotation)[1]]) #e.g. [''3_frag185_0_0_rnp', 77.5, 6.04]


            print('Evaluating translation of the second fragment')
            sum_file_translation = os.path.join(lite_dir, 'ens1_frag2', '4_PACK_LIBRARY', 'clusters.sum')
            if os.path.exists(sum_file_translation):
                list_FOMS_translation.append([cluster_pdb[:-4], SELSLIB2.BestFOMSFromSUM(sum_file_translation)[0], SELSLIB2.BestFOMSFromSUM(sum_file_translation)[1]]) #e.g ['3_frag67_0_0_rnp', 56.5, 6.17]

        # Writing sum file for the prioritisation of the rotation of the 2nd fragment
        g1 = open(multicopy_prio + '/prioritisation_2ndfrag_rot.sum', 'w')
        if not dict_wMPE:
            g1.write("priorisation\tpdb\tLLG\tZSCORE\n")
        else:
            g1.write("priorisation\tpdb\tLLG\tZSCORE\twMPE_1st_fragment\n")
        sorted_list_FOMS_rotation = sorted(list_FOMS_rotation, key=lambda x: x[1], reverse=True)
        for i, pdb_FOM in enumerate(sorted_list_FOMS_rotation):
            if not dict_wMPE:
                g1.write(str(i+1) + '\t' + str(pdb_FOM[0]) + '\t' + str(pdb_FOM[1]) + '\t' + str(pdb_FOM[2]) + '\n')
            else:
                g1.write(str(i+1) + '\t' + str(pdb_FOM[0]) + '\t' + str(pdb_FOM[1]) + '\t' + str(pdb_FOM[2]) + '\t' + str(dict_wMPE[str(pdb_FOM[0])]) + '\n')
        g1.close()

        # Writing sum file for the prioritisation of the translation of the 2nd fragment
        g1 = open(multicopy_prio + '/prioritisation_2ndfrag_tra.sum', 'w')
        if not dict_wMPE:
            g1.write("priorisation\tpdb\tLLG\tZSCORE\n")
        else:
            g1.write("priorisation\tpdb\tLLG\tZSCORE\twMPE_1st_fragment\n")
        sorted_list_FOMS_translation = sorted(list_FOMS_translation, key=lambda x: x[1], reverse=True)

        for i, pdb_FOM in enumerate(sorted_list_FOMS_translation):
            if not dict_wMPE:
                g1.write(str(i+1) + '\t' + str(pdb_FOM[0]) + '\t' + str(pdb_FOM[1]) + '\t' + str(pdb_FOM[2]) + '\n')
            else:
                g1.write(str(i + 1) + '\t' + str(pdb_FOM[0]) + '\t' + str(pdb_FOM[1]) + '\t' + str(pdb_FOM[2]) + '\t' + str(dict_wMPE[str(pdb_FOM[0])]) + '\n')
        g1.close()

        #Generating plots
        SELSLIB2.plots_multicopy(multicopy_prio + '/prioritisation_1stfrag.sum', ent=ent)
        SELSLIB2.plots_multicopy(multicopy_prio + '/prioritisation_2ndfrag_rot.sum', ent=ent)
        SELSLIB2.plots_multicopy(multicopy_prio + '/prioritisation_2ndfrag_tra.sum', ent=ent)

        #Re-running the top5 best partial models according to the LLG of the translation of the 2nd fragment
        g1 = open(multicopy_prio + '/prioritisation_2ndfrag_tra.sum', 'r')
        lines = g1.readlines()
        g1.close()

        for i, line in enumerate(lines):
            if i != 0 and i <= 5:
                line_sep = line.split()
                cluster_pdb = line_sep[1] + '.pdb'
                lite_dir = os.path.join(current_directory, 'ARCIMBOLDO_LITE', cluster_pdb[:-4])

                inpconf = inputConfig()
                print("Re-running multicopy", cluster_pdb, lite_dir)
                bordata = __prepareAnewARCIMBOLDOmulticopy(cluster_pdb, lite_dir, cluster_pdb[:-4], Config, inpconf,
                                                           last_rmsd)
                html_path = os.path.join(bordata.get("GENERAL", "working_directory"),
                                         bordata.get("ARCIMBOLDO", "name_job") + ".html")
                SELSLIB2.writeMultiCopyFile(lock, current_directory, nameOutput, bordata.get("ARCIMBOLDO", "name_job"),
                                            html_path)

                if isShredder:
                    aniout = out_phaser_given
                SELSLIB2.LAST_AVAILABLE_ROTID = 0
                SELSLIB2.MAP_OF_ROT_COMB = {}

                ARCIMBOLDO_LITE.startARCIMBOLDO(bordata, "borfile", DicParameters=DicParameters, DicGridConn=DicGridConn,
                                                cm=cm, sym=sym, doTest=False, mtz_given=mtz, F_given=F, SIGF_given=SIGF,
                                                normfactors=normfactors, tncsfactors=tncsfactors, Intensities=Intensities,
                                                Aniso=Aniso, nice=nice, out_phaser_given=aniout, fneed=fneed, isShredder=True)
                print("Finish re-run ARCIMBOLDO LITE")
    try:
        if hasattr(cm, "channel"): #If True, remote grid. Elif None, multiprocessing. Else, local_grid
            # REMOVE THE FULL LIBRARY IN THE REMOTE SERVER
            actualdi = cm.get_remote_pwd()
            print(cm.change_remote_dir(".."))
            print(cm.remove_remote_dir(model_directory, model_directory))
            print(cm.change_remote_dir(actualdi))

        SystemUtility.close_connection(DicGridConn, DicParameters, cm)
    except:
        pass
    # new_t.stop()
    sym.couldIClose = True

def __prepareAnewARCIMBOLDOmulticopy(pdbf, direc, namep, Config, inpconf, last_rmsd):
    bordata = configparser.ConfigParser()
    bordata.read_file(io.StringIO(str(Data.defaults_bor)))
    listpro = ["CONNECTION", "GENERAL", "LOCAL", "ANOMALOUS"]
    for elem in listpro:
        if Config.has_section(elem):
            bordata.remove_section(elem)
            bordata.add_section(elem)
            for pair in Config.items(elem):
                bordata.set(elem, pair[0], pair[1])
        bordata.set("GENERAL", "working_directory", direc)

    for pair in bordata.items("ARCIMBOLDO"):
        if Config.has_option("ARCIMBOLDO-BORGES", pair[0]):
            bordata.set("ARCIMBOLDO", pair[0], Config.get("ARCIMBOLDO-BORGES", pair[0]))

    #bordata.set("ARCIMBOLDO", "shelxe_line", Config.get("ARCIMBOLDO-BORGES", "shelxe_line"))
    #bordata.set("ARCIMBOLDO", "shelxe_line_last", Config.get("ARCIMBOLDO-BORGES", "shelxe_line_last"))
    #bordata.set("ARCIMBOLDO", "molecular_weight", str(inpconf.MW))
    #bordata.set("ARCIMBOLDO", "number_of_component", str(inpconf.NC))


    #try:
        #bordata.set("ARCIMBOLDO", "f_label", Config.get("ARCIMBOLDO-SHREDDER", "f_label"))
        #bordata.set("ARCIMBOLDO", "sigf_label", Config.get("ARCIMBOLDO-SHREDDER", "sigf_label"))
    #except:
        #bordata.set("ARCIMBOLDO", "i_label", Config.get("ARCIMBOLDO-SHREDDER", "i_label"))
        #bordata.set("ARCIMBOLDO", "sigi_label", Config.get("ARCIMBOLDO-SHREDDER", "sigi_label"))

    #bordata.set("ARCIMBOLDO", "rmsd", str(inpconf.RMSD_ARC))
    bordata.set("ARCIMBOLDO", "name_job", pdbf[:-4])
    bordata.set("ARCIMBOLDO", "model_file", os.path.join(direc, pdbf))
    if bordata.getint("ARCIMBOLDO", "fragment_to_search") <= 1:
        bordata.set("ARCIMBOLDO", "fragment_to_search", "2")
    bordata.set("ARCIMBOLDO", "rmsd", str(last_rmsd))
    bordata.set("ARCIMBOLDO", "fixed_models_directory", os.path.join(direc,'fixed'))
    bordata.set("ARCIMBOLDO", "pack_tra", "True")
    bordata.set("ARCIMBOLDO", "alixe", "False")
    bordata.set("ARCIMBOLDO", "pack_clashes", "10")

    bordata.remove_section("ARCIMBOLDO-SHREDDER")
    bordata.remove_section("ARCIMBOLDO-BORGES")

    #bordata.set("ARCIMBOLDO", "fragment_to_search", str(Config.getint("ARCIMBOLDO-BORGES", "number_of_component")))
    #bordata.set("ARCIMBOLDO", "name_job", namep)
    #bordata.set("ARCIMBOLDO", "resolution_rotation", str(inpconf.resolution_rotation_arcimboldo))
    #bordata.set("ARCIMBOLDO", "sampling_rotation", str(inpconf.sampling_rotation_arcimboldo))

    # NS, I need to keep track of the original shredder model for anomalous checkings
    #original_shredder_model = Config.get("ARCIMBOLDO-SHREDDER", "model_file")
    #original_shredder_model = os.path.abspath(os.path.normpath(original_shredder_model))
    #bordata.set("ARCIMBOLDO", "model_shredder", original_shredder_model)

    # NS autotracing cycle number
    # NOTE CM this is not defined
    # bordata.set("ARCIMBOLDO", "nAutoTracCyc", nAutoTracCyc)
    # bordata.set("ARCIMBOLDO",'unitCellcontentAnalysis',unitCellcontentAnalysis)
    # NS ANOM pass the parameters to Shredder
    #anomParameters = ANOMLIB.anomParameters()  # returns a list of the current anomParameters
    #for anomP in anomParameters:
        #bordata.set("ANOMALOUS", anomP, Config.get("ANOMALOUS", anomP))

    #try:
        #bordata.set("ARCIMBOLDO", "SKIP_RES_LIMIT", Config.get("ARCIMBOLDO-SHREDDER", "SKIP_RES_LIMIT"))
    #except:
        #pass

    #try:
        #stop_if_solved = Config.getboolean("ARCIMBOLDO-SHREDDER", "STOP_IF_SOLVED")
        #SELSLIB2.STOP_IF_SOLVED = stop_if_solved
    #except:
        #pass

    #if inpconf.mend_after_translation:
        #bordata.set("ARCIMBOLDO", "swap_model_after_translation", model_file)

    # Write an explicit bor file in the ARCIMBOLDO run
    path_explicit_bor = os.path.join(direc, namep)
    file_object_bor = open(path_explicit_bor + '.bor', 'w')
    bordata.write(file_object_bor)
    del file_object_bor
    return bordata

#######################################################################################################
#                                               MAIN                                                  #
#######################################################################################################

def main():
    warnings.simplefilter("ignore", DeprecationWarning)
    # Put the signal retrieval for the killing
    if hasattr(sys, '_MEIPASS'):
        try:
            signal.signal(signal.SIGTERM,SystemUtility.signal_term_handler)
        except:
            pass
        try:
            signal.signal(signal.SIGKILL,SystemUtility.signal_term_handler)
        except:
            pass
        try:
            signal.signal(signal.SIGINT,SystemUtility.signal_term_handler)
        except:
            pass

    head1 = """
.-----------------------------------------------------------------------------------------------------------------------.
|          _____   _____ _____ __  __ ____   ____  _      _____   ____        ____   ____  _____   _____ ______  _____  |
|    /\   |  __ \ / ____|_   _|  \/  |  _ \ / __ \| |    |  __ \ / __ \      |  _ \ / __ \|  __ \ / ____|  ____|/ ____| |
|   /  \  | |__) | |      | | | \  / | |_) | |  | | |    | |  | | |  | |_____| |_) | |  | | |__) | |  __| |__  | (___   |
|  / /\ \ |  _  /| |      | | | |\/| |  _ <| |  | | |    | |  | | |  | |_____|  _ <| |  | |  _  /| | |_ |  __|  \___ \  |
| / ____ \| | \ \| |____ _| |_| |  | | |_) | |__| | |____| |__| | |__| |     | |_) | |__| | | \ \| |__| | |____ ____) | |
|/_/    \_\_|  \_\\\\_____|_____|_|  |_|____/ \____/|______|_____/ \____/      |____/ \____/|_|  \_\\\\_____|______|_____/  |
#-----------------------------------------------------------------------------------------------------------------------#
                                        Requires Phaser >= 2.8.x and Shelxe 2018
    """

    print(colored(head1, 'cyan'))
    print("""
       Institut de Biologia Molecular de Barcelona --- Consejo Superior de Investigaciones Cientificas
                         I.B.M.B.                                            C.S.I.C.

                                             Department of Structural Biology
                                             Crystallographic Methods Group
                              http://www.sbu.csic.es/research-groups/crystallographic-methods/

    In case this result is helpful, please, cite:

    Exploiting tertiary structure through local folds for ab initio phasing
    Sammito, M., Millan, C., Rodriguez, D. D., M. de Ilarduya, I., Meindl, K.,
    De Marino, I., Petrillo, G., Buey, R. M., de Pereda, J. M., Zeth, K., Sheldrick, G. M. & Uson, I.
    (2013) Nat Methods. 10, 1099-1101.
    
    Phaser crystallographic software
    McCoy, A. J., Grosse-Kunstleve, R. W., Adams, P. D., Winn, M. D., Storoni, L. C. & Read, R. J.
    (2007) J Appl Cryst. 40, 658-674.

    An introduction to experimental phasing of macromolecules illustrated by SHELX; new autotracing features. 
    Uson, I. and Sheldrick, G. M.
    (2018) Acta Cryst. D74, 106-116.
    """)
    print("Email support: ", colored("bugs-borges@ibmb.csic.es", 'blue'))
    print("\nARCIMBOLDO_BORGES website: ", colored("http://chango.ibmb.csic.es", 'blue'))
    print("\n")
    usage = """usage: %prog [options] example.bor"""

    parser = OptionParser(usage=usage)
    # parser.add_option("-x", "--XGUI", action="store_true", dest="gui", help="Will automatically launch the GUI Option Viewer to read the output", default=False)


    parser.add_option("-b", "--userconf", dest="userconf",
                      help="Create a template .bor file and print customizable parameters for users", default=False, metavar="FILE")
    parser.add_option("-v", "--devconf", dest="devconf",
                      help="Create a template .bor file and print customizable parameters for developers", default=False, metavar="FILE")
    parser.add_option("-r", "--rottest", dest="rottest", help=SUPPRESS_HELP)

    (options, args) = parser.parse_args()

    if options.userconf != False:
        SELSLIB2.GenerateBorFile(arcimboldo_software='ARCIMBOLDO-BORGES', developers=False, bor_name=options.userconf)
        with open(options.userconf, 'r') as bor_file:
            print(bor_file.read())

    if options.devconf != False:
        print ("The selected option is only available for the developers team. Please insert the password:")
        command = input("<> ")
        if hashlib.sha224(command).hexdigest() == "d286f6ad6324a21cf46c7e3c955d8badfdbb4a14d630e8350ea3149e":
            SELSLIB2.GenerateBorFile(arcimboldo_software='ARCIMBOLDO-BORGES', developers=True, bor_name=options.devconf)
            with open(options.devconf, 'r') as bor_file:
                print(bor_file.read())
        else:
            print("Sorry. You have not the permissions.")
            sys.exit(0)

    if options.rottest is not None and options.rottest != "" and os.path.exists(options.rottest):
        startROT_NODE(options.rottest)
    else:
        if len(args) < 1:
            parser.print_help()
            sys.exit(0)

    model_directory = ""
    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    input_bor = os.path.abspath(args[0])
    print('\n Reading the bor configuration file for ARCIMBOLDO_BORGES at ', input_bor)
    if not os.path.exists(input_bor):
        print('Sorry, the given path for the bor file either does not exist or you do not have the permissions to read it')
        sys.exit(1)
    path_module = os.path.dirname(__file__)

    Config = configparser.ConfigParser()
    #Config.readfp(cStringIO.StringIO(Data.defaults_bor))
    Config.read(input_bor)

    try:
        startARCIMBOLDO_BORGES(Config, False, input_bor, startCheckQueue=True)
    except SystemExit:
        pass
    except:
        print(traceback.print_exc(file=sys.stdout))
        if hasattr(sys, '_MEIPASS'):
            print("Exited with errors, temp file was ", sys._MEIPASS, " and was removed before exiting")


if __name__ == "__main__":
    main()

