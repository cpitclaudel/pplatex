"""
SCons.Tool.cuda
CUDA Tool for SCons

Copied from http://www.scons.org/wiki/CudaTool
Modified by Stefan Hepp for gracious failing if SDK not found.
"""
import os
import platform
import sys
import SCons.Tool
import SCons.Scanner.C
import SCons.Defaults
CUDAScanner = SCons.Scanner.C.CScanner()
# this object emitters add '.linkinfo' suffixed files as extra targets
# these files are generated by nvcc. The reason to do this is to remove
# the extra .linkinfo files when calling scons -c
def CUDANVCCStaticObjectEmitter(target, source, env):
        tgt, src = SCons.Defaults.StaticObjectEmitter(target, source, env)
        for file in src:
                lifile = os.path.splitext(src[0].rstr())[0] + '.linkinfo'
                #tgt.append(lifile)
        return tgt, src
def CUDANVCCSharedObjectEmitter(target, source, env):
        tgt, src = SCons.Defaults.SharedObjectEmitter(target, source, env)
        for file in src:
                lifile = os.path.splitext(src[0].rstr())[0] + '.linkinfo'
                #tgt.append(lifile)
        return tgt, src

def generate(env):
        staticObjBuilder, sharedObjBuilder = SCons.Tool.createObjBuilders(env);
        staticObjBuilder.add_action('.cu', '$STATICNVCCCMD')
        staticObjBuilder.add_emitter('.cu', CUDANVCCStaticObjectEmitter)
        sharedObjBuilder.add_action('.cu', '$SHAREDNVCCCMD')
        sharedObjBuilder.add_emitter('.cu', CUDANVCCSharedObjectEmitter)
        SCons.Tool.SourceFileScanner.add_scanner('.cu', CUDAScanner)
        # default compiler
        env.SetDefault(NVCC = 'nvcc')
        # default flags for the NVCC compiler
        env.SetDefault(
	    NVCCFLAGS = [],
	    STATICNVCCFLAGS = [],
	    SHAREDNVCCFLAGS = [],
	    ENABLESHAREDNVCCFLAG = ['-shared'],
	    NVCCLIBPATH = '$LIBPATH',
	    NVCCINCPATH = '$CPPPATH',
	    NVCCLIBS    = '$LIBS',
	    NVCCDEFINES = '$CPPDEFINES'
	)
        # default NVCC commands
        env['STATICNVCCCMD'] = '$NVCC -o $TARGET -c $_NVCCFLAGS $STATICNVCCFLAGS $SOURCES'
        env['SHAREDNVCCCMD'] = '$NVCC -o $TARGET -c $_NVCCFLAGS $SHAREDNVCCFLAGS $ENABLESHAREDNVCCFLAG $SOURCES'
	
	env['_NVCCFLAGS'] = '$NVCCFLAGS $_NVCCINCFLAGS $_NVCCDEFFLAGS'

	env['NVCCLIBLINKPREFIX'] = '-l'
	env['NVCCLIBLINKSUFFIX'] = ''
	env['NVCCLIBDIRPREFIX'] = '-L'
	env['NVCCLIBDIRSUFFIX'] = ''
	env['NVCCINCPREFIX'] = '-I'
	env['NVCCINCSUFFIX'] = ''
	env['NVCCDEFPREFIX'] = '-D'
	env['NVCCDEFSUFFIX'] = ''

	env['_NVCCLIBFLAGS']    = '${_concat(NVCCLIBLINKPREFIX, NVCCLIBS, NVCCLIBLINKSUFFIX, __env__)}'
	env['_NVCCLIBDIRFLAGS'] = '$( ${_concat(NVCCLIBDIRPREFIX, NVCCLIBPATH, NVCCLIBDIRSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
	env['_NVCCINCFLAGS']    = '$( ${_concat(NVCCINCPREFIX, NVCCINCPATH, NVCCINCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
	env['_NVCCDEFFLAGS']    = '${_defines(NVCCDEFPREFIX, CPPDEFINES, NVCCDEFSUFFIX, __env__)}'

def exists(env):
        return env.Detect('nvcc')
