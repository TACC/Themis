#!/usr/bin/env python
# -*- python -*-
from __future__ import print_function
import os, sys, re, json

def main():

    testresults = {
        'Hermes_Version' : "2.1",
        'HumanData'      : """
*******************************************************************************************************
*** Test Results                                                                                    ***
*******************************************************************************************************
 
Date:             Fri Dec 27 09:17:34 2013
TARGET:           x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12
Tag:              2013_12_27
TM Version:       1.6.6
Hermes Version:   2.1
Lua Version:      Lua 5.2
Total Test Time:  00:00:36.79
 
*******************************************************************************************************
*** Test Summary                                                                                    ***
*******************************************************************************************************
 
Total:   9
passed:  9

*******  *  ****   *********                                ***************
Results  R  Time   Test Name                                version/message
*******  *  ****   *********                                ***************
passed   R  1.3    mgf/rt/Petsc/p/2x3y4z-2/2x3y4z-2/t1      
passed   R  8.71   mgf/rt/Petsc/p/2x3y4z-8/2x3y4z-8/t1      
passed   R  10.2   mgf/rt/Petsc/p/coupled0-8/coupled0-8/t1  
passed   R  3.75   mgf/rt/Petsc/p/flow0-2/flow0-2/t1        
passed   R  12.3   mgf/rt/Petsc/p/tfu0-8/tfu0-8/t1          
passed   R  0.163  mgf/rt/Petsc/s/coupled0/coupled0/t1      
passed   R  0.136  mgf/rt/Petsc/s/flow0/flow0/t1            
passed   R  0.115  mgf/rt/Petsc/s/tfu0/tfu0/t1              
passed   R  0.095  mgf/rt/Petsc/s/thermal0/thermal0/t1      

""",
        'date' : "Fri Dec 27 09:17:34 2013",
        'tests' :  [ {
      "ProgVersion" : "",
      "UUid": "x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64",
      "active": 1,
      "cmdResultFn": "mgf/rt/Petsc/p/2x3y4z-2/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-2x3y4z-2/results.lua",
      "hostName": "vmijo",
      "id": "mgf/rt/Petsc/p/2x3y4z-2/2x3y4z-2/t1",
      "idTag": "t1",
      "machName": "x86_64",
      "message": "",
      "osName": "Linux",
      "outputDir": "mgf/rt/Petsc/p/2x3y4z-2/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-2x3y4z-2",
      "report": False,
      "result": "passed",
      "resultFn": "mgf/rt/Petsc/p/2x3y4z-2/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-2x3y4z-2/t1.result",
      "runtime": 1.3025999069214,
      "runtimeFn": "mgf/rt/Petsc/p/2x3y4z-2/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-2x3y4z-2/t1.runtime",
      "start_epoch": 1388157454.3306,
      "strRuntime": "1.3",
      "tag": "2013_12_27",
      "target": "x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12",
      "testName": "2x3y4z-2",
      "versionFn": "mgf/rt/Petsc/p/2x3y4z-2/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-2x3y4z-2/version.lua",
    },
    {
      "ProgVersion": "",
      "UUid": "x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64",
      "active": 1,
      "cmdResultFn": "mgf/rt/Petsc/s/tfu0/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-tfu0/results.lua",
      "hostName": "vmijo",
      "id": "mgf/rt/Petsc/s/tfu0/tfu0/t1",
      "idTag": "t1",
      "machName": "x86_64",
      "message": "",
      "osName": "Linux",
      "outputDir": "mgf/rt/Petsc/s/tfu0/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-tfu0",
      "report": False,
      "result": "passed",
      "resultFn": "mgf/rt/Petsc/s/tfu0/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-tfu0/t1.result",
      "runtime": 0.11479997634888,
      "runtimeFn": "mgf/rt/Petsc/s/tfu0/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-tfu0/t1.runtime",
      "start_epoch": 1388157455.6366,
      "strRuntime": "0.115",
      "tag": "2013_12_27",
      "target": "x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12",
      "testName": "tfu0",
      "versionFn": "mgf/rt/Petsc/s/tfu0/t1/x86_64_06_3a_intel-14.0.1_mpich-3.0.4_petsc-3.2_phdf5-1.8.12-2013_12_27_09_17_34-Linux-x86_64-tfu0/version.lua",
    },
    ]
        }
    print("testresults['Hermes_version']: ", testresults['Hermes_Version'])

    print(json.dumps(testresults, sort_keys=True,
                     indent=2, separators=(',', ': ')))
if ( __name__ == '__main__'): main()
