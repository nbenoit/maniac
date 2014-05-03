#!/usr/bin/python


#
# Maniac : Validates and compares various variants of a program
#
# Copyright (c) 2011 Nicolas BENOIT
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#


import subprocess
import sys
import getopt
import os
import copy
import random
import datetime
import threading

from xml.dom.minidom import parse
from xml.parsers.expat import ExpatError



# USAGE
def version ( ):
    return '1.0.1'

def copyright ( ):
    return 'Copyright (c) 2011 Nicolas BENOIT\n' + \
           'This is free software; see the source for copying conditions.  There is NO\n' + \
           'warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.'

def print_usage ( ):
    print ( '' )
    print ( 'maniac version %s' % version() )
    print ( 'validates and compares multiple variants of a program' )
    print ( '' )
    print ( 'usage: maniac.py [OPTIONS] <dir|plan> ...' )
    print ( '' )
    print ( 'options:' )
    print ( '\t-G\t--nogen\t\tdisable generation of variants' )
    print ( '\t-m M\t--mania=M\tlook in file M for mania definition' )
    print ( '\t-n N\t--numrpt=N\trepeat each plan N times' )
    print ( '\t-o O\t--output=O\toutput HTML report to file named O' )
    print ( '\t-h\t--help\t\tshow this help message and exit' )
    print ( '\t-v\t--version\toutput version information and exit' )
    print ( '' )
    return



# GLOBAL CONSTANTS
COMP = 'gcc'
COMPFLAGS = '-O2 -lpthread -lm -g'
LOADERFLAGS='-g -O2 -fPIC -ldl -lpthread'
LOADERTIMEOUT=10


# UTILS

# indent
def indent ( f, idt ):
    for i in range(idt):
        f.write ( ' ' )
    return

# str2bool
def str2bool ( s ):
    if ( s.lower() == 'true' ):
        return True
    return False


# subproc_call
def subproc_call ( path, cmd, timeout=0 ):
    out = ''
    err = ''
    retcode = 0
    oldpath = os.getcwd ( )
    killed = False
    try:
        ks = None
        os.chdir ( path )
        sp = subprocess.Popen ( 'exec '+cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        if ( timeout > 0 ):
            ks = threading.Timer ( timeout, lambda x:x.kill(), [sp] )
            ks.start ( )
        comm = sp.communicate ( )
        if ( timeout > 0 ):
            if ( ks.is_alive() ):
                ks.cancel ( )
                kill = False
            else:
                killed = True
        retcode = sp.returncode
        out = comm[0] # stdout
        err = comm[1] # stderr
        if ( killed ):
            err += str(os.path.basename(cmd)+': Killed')
    except OSError as e:
        err = str ( e )
        retcode = 1
    os.chdir ( oldpath )
    return (retcode,out,err)



# CORE

# data
class data:
    xml_node = 'data'
    xml_attr = [ 'type', 'name', 'ini', 'chk' ]
    uid = 1
    
    def __init__ ( self, type=None, name=None, varname=None, ini='true', chk='true' ):
        if ( type == None ):
            print ( 'maniac: data.__init__(): error: \'type\' should not be None.\n' )
            sys.exit ( 1 )
        
        if ( name == None ):
            print ( 'maniac: data.__init__(): error: \'name\' should not be None.\n' )
            sys.exit ( 1 )

        self.uid = data.uid
        data.uid = data.uid + 1
        
        self.type = type
        self.name = name

        if ( varname == None ):
            self.varname = '_' + self.name
        else:
            self.varname = varname

        self.ini = str2bool ( ini )
        self.chk = str2bool ( chk )
        self.extern = False
        return

    def produce_decl ( self, f, idt=0 ):
        indent ( f, idt )
        return

    def produce_decl_chk ( self, f, idt=0 ):
        indent ( f, idt )
        return


# data scalar
class scalar ( data ):
    xml_node = 'scalar'
    xml_attr = data.xml_attr + [ 'value' ]

    def __init__ ( self, type=None, name=None, varname=None, ini='true', chk='true', value='0' ):
        data.__init__ ( self, type, name, varname, ini, chk )
        value = value.strip ( )
        if ( 'rand' in value ):
            self.value = value.replace('rand','%d'%random.randint(0,10000) )
        else:
            self.value = value
        return

    def produce_decl ( self, f, idt=0 ):
        data.produce_decl ( self, f, idt )
        if ( self.extern ):
            f.write ( '%s *%s' % ( self.type, self.varname ) )
        else:
            f.write ( '%s %s' % ( self.type, self.varname ) )
        return
    
    def produce_decl_chk ( self, prefix, f, idt=0 ):
        data.produce_decl_chk ( self, f, idt )
        f.write ( '%s %s%s' % (self.type,prefix,self.name) )
        return
    
    def produce_cast ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( '(%s' % self.type )
        if ( self.extern ):
            f.write ( '*' )
        f.write ( ') ' )
        return
    
    def produce_arg ( self, f, idt=0 ):
        f.write ( self.varname )
        return

    def produce_init ( self, f, idt=0 ):
        indent ( f, idt )
        if ( self.extern ):
            f.write ( '*(' )
        f.write ( '%s' % self.varname )
        if ( self.extern ):
            f.write ( ')' )
        f.write ( ' = %s;\n' % self.value )
        return

    def produce_copy ( self, prefix, f, idt=0 ):
        indent ( f, idt )
        f.write ( '%s%s = ' % (prefix,self.name) )
        if ( self.extern ):
            f.write ( '*(' )
        f.write ( '%s' % self.varname )
        if ( self.extern ):
            f.write ( ')' )
        f.write ( ';\n' )
        return

    def produce_check ( self, variantname, prefix, f, idt=0 ):
        indent ( f, idt )
        f.write ( 'if ( ' )
        if ( self.extern ):
            f.write ( '*(' )
        f.write ( '%s' % self.varname )
        if ( self.extern ):
            f.write ( ')' )
        f.write ( ' != %s%s )\n' % (prefix,self.name) )
        indent ( f, idt+2 )
        f.write ( '{\n' )
        indent ( f, idt+4 )
        f.write ( 'fprintf ( stderr, "%s Invalid value in data \\\'%s\\\'\\n" );\n' % (variantname, self.name ) )
        indent ( f, idt+4 )
        f.write ( 'fflush ( stderr );\n' )
        indent ( f, idt+4 )
        f.write ( 'error = 1;\n\n' )
        indent ( f, idt+2 )
        f.write ( '}\n' )
        return


# data array
class array ( data ):
    xml_node = 'array'
    xml_attr = data.xml_attr + [ 'dims', 'value' ]

    def __init__ ( self, type=None, name=None, varname=None, ini='true', chk='true', dims=None, value='index' ):
        data.__init__ ( self, type, name, varname, ini, chk )

        if ( dims == None ):
            print ( 'maniac: array.__init__(): error: \'dims\' should not be None.\n' )
            sys.exit ( 1 )

        self.dims = eval ( dims )
        self.itername = lambda d:chr(ord('i')+d) # will return 'i', 'j', 'k', ...

        self.seed = random.randint ( 0, 10000 )
        if ( (self.type == 'double') or (self.type == 'float') ):
            self.randfunc = 'drand48'
            self.seedfunc = 'srand48'
        else:
            self.randfunc = 'rand'
            self.seedfunc = 'srand'

        self.value = value.strip()
        self.value = self.value.replace ( 'index', '('+self.offset()+')' )
        self.value = self.value.replace ( 'rand', self.randfunc+'()' )

        self.lid = 0
        return

    def produce_decl ( self, f, idt=0 ):
        data.produce_decl ( self, f, idt )
        if ( self.extern ):
            f.write ( '%s *' % self.type )
            f.write ( '%s' % self.varname )
        else:
            f.write ( '%s %s' % ( self.type, self.varname ) )
            for d in self.dims:
                f.write ( '[%d]' % d )
        return

    def produce_cast ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( '(%s *' % self.type )
        f.write ( ') ' )
        return

    def produce_decl_chk ( self, prefix, f, idt=0 ):
        data.produce_decl_chk ( self, f, idt )
        f.write ( '%s %s%s' % (self.type,prefix,self.name) )
        if ( self.extern ):
            f.write ( '[%s]' % '*'.join([str(sd) for sd in self.dims]) )
        else:
            for d in self.dims:
                f.write ( '[%d]' % d )
        return

    def produce_arg ( self, f, idt=0 ):
        f.write ( self.varname )
        return

    def produce_loop_in ( self, f, idt=0 ):
        self.lid = self.lid + 1
        for d in range(len(self.dims)):
            indent ( f, idt+2*d )
            f.write ( 'for ( %s=0; %s<%s; ++%s )\n' % ( self.itername(d), self.itername(d), self.dims[d], self.itername(d) ) )
            indent ( f, idt+2*d )
            f.write ( '  {\n' )
        return

    def produce_loop_out ( self, f, idt=0, withlabel=False ):
        for d in range(len(self.dims)):
            indent ( f, idt+2*(len(self.dims)-d) )
            f.write ( '}\n' )
        if ( withlabel ):
            f.write ( ' exit_%d_%d:\n' % (self.uid,self.lid) )
        return

    def offset ( self ):
        off = ''
        for d in range(len(self.dims)):
            off = off + ( '*'.join(['%s'%self.itername(d)]+[str(sd) for sd in self.dims[d+1:]]) )
            if ( d < len(self.dims)-1 ):
                off = off + '+'
        return off

    def produce_indexing ( self, f ):
        if ( self.extern ):
            f.write ( '[%s]' % self.offset() )
        else:
            for d in range(len(self.dims)):
                f.write ( '[%s]' % chr(ord('i')+d) )
        return

    def produce_init ( self, f, idt=0 ):
        if ( 'rand' in self.value ):
            indent ( f, idt )
            f.write ( '%s ( %d );\n' % (self.seedfunc,self.seed) )
        self.produce_loop_in ( f, idt )
        indent ( f, idt+4*len(self.dims) )
        f.write ( '%s' % self.varname )
        self.produce_indexing ( f )
        f.write ( ' = (%s) (%s);\n' % (self.type,self.value) );
        self.produce_loop_out ( f, idt )
        return

    def produce_copy ( self, prefix, f, idt=0 ):
        self.produce_loop_in ( f, idt )
        indent ( f, idt+4*len(self.dims) )
        f.write ( '%s%s' % (prefix,self.name) )
        self.produce_indexing ( f )
        f.write ( ' = ' )
        f.write ( '%s' % self.varname )
        self.produce_indexing ( f )
        f.write ( ';\n' )
        self.produce_loop_out ( f, idt )
        return

    def produce_check ( self, variantname, prefix, f, idt=0 ):
        self.produce_loop_in ( f, idt )
        indent ( f, idt+4*len(self.dims) )
        f.write ( 'if ( ' )
        f.write ( '%s' % self.varname )
        self.produce_indexing ( f )
        f.write ( ' != %s%s' % (prefix,self.name) )
        self.produce_indexing ( f )
        f.write ( ' )\n' )
        indent ( f, idt+4*len(self.dims)+2 )
        f.write ( '{\n' )
        indent ( f, idt+4*len(self.dims)+4 )
        f.write ( 'fprintf ( stderr, "%s Invalid value in data \\\'%s\\\'' % (variantname,self.name) )
        for d in range(len(self.dims)):
            f.write ( ' %s=%%d' % self.itername(d) )
        f.write ( '\\n"' )
        for d in range(len(self.dims)):
            f.write ( ', %s' % self.itername(d) )
        f.write ( ' );\n' )
        indent ( f, idt+4*len(self.dims)+4 )
        f.write ( 'fflush ( stderr );\n' )
        indent ( f, idt+4*len(self.dims)+4 )
        f.write ( 'error = 1;\n' )
        indent ( f, idt+4*len(self.dims)+4 )
        f.write ( 'goto exit_%d_%d;\n' % (self.uid,self.lid) )
        indent ( f, idt+4*len(self.dims)+2 )
        f.write ( '}\n' )
        self.produce_loop_out ( f, idt, True )
        return


# data struct
class struct ( data ):
    xml_node = 'struct'
    xml_attr= data.xml_attr

    def __init__ ( self, type=None, name=None, varname=None, ini='true', chk='true', fields=None ):
        data.__init__ ( self, 'struct '+type, name, varname, ini, chk )
        
        if ( fields == None ):
            print ( 'maniac: struct.__init__(): error: \'fields\' should not be None.\n' )
            sys.exit ( 1 )
        
        self.fields = fields
        return

    def produce_decl ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( '%s\n' % self.type )
        indent ( f, idt )
        f.write ( '{\n' )
        for fld in self.fields:
            fld.produce_decl ( f, idt+2 )
            f.write ( ';\n' )
        indent ( f, idt )
        f.write ( '};\n' )
        
        if ( self.extern ):
            f.write ( '%s *%s' % ( self.type, self.varname ) )
            for fld in self.fields:
                fld.access = '%s->%s' % (self.varname,fld.varname)
                fld.chkaccess = '%s->%s' % (self.name,fld.varname)
        else:
            f.write ( '%s %s' % ( self.type, self.varname ) )
            for fld in self.fields:
                fld.access = '%s.%s' % (self.varname,fld.varname)
                fld.chkaccess = '%s.%s' % (self.name,fld.varname)
        return
    
    def produce_decl_chk ( self, prefix, f, idt=0 ):
        data.produce_decl_chk ( self, f, idt )
        if ( self.extern ):
            f.write ( '%s _%s%s;\n' % (self.type,prefix,self.name) )
            f.write ( '%s *%s%s = &_%s%s' % (self.type,prefix,self.name,prefix,self.name) )
        else:
            f.write ( '%s %s%s' % (self.type,prefix,self.name) )
        return
    
    def produce_cast ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( '(%s' % self.type )
        if ( self.extern ):
            f.write ( '*' )
        f.write ( ') ' )
        return
    
    def produce_arg ( self, f, idt=0 ):
        f.write ( self.varname )
        return

    def produce_init ( self, f, idt=0 ):
        for fld in self.fields:
            n = fld.varname
            fld.varname = fld.access
            chkn = fld.name
            fld.name = fld.chkaccess
            fld.produce_init ( f, idt )
            fld.name = chkn
            fld.varname = n
        return

    def produce_copy ( self, prefix, f, idt=0 ):
        for fld in self.fields:
            n = fld.varname
            fld.varname = fld.access
            chkn = fld.name
            fld.name = fld.chkaccess
            fld.produce_copy ( prefix, f, idt )
            fld.name = chkn
            fld.varname = n
        return

    def produce_check ( self, variantname, prefix, f, idt=0 ):
        for fld in self.fields:
            n = fld.varname
            fld.varname = fld.access
            chkn = fld.name
            fld.name = fld.chkaccess
            fld.produce_check ( variantname, prefix, f, idt )
            fld.name = chkn
            fld.varname = n
        return


# data union
class union ( data ):
    xml_node = 'union'
    xml_attr= data.xml_attr

    def __init__ ( self, type=None, name=None, varname=None, ini='true', chk='true', fields=None ):
        data.__init__ ( self, 'union '+type, name, varname, ini, chk )
        
        if ( fields == None ):
            print ( 'maniac: union.__init__(): error: \'fields\' should not be None.\n' )
            sys.exit ( 1 )
        
        self.fields = fields
        return

    def produce_decl ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( '%s\n' % self.type )
        indent ( f, idt )
        f.write ( '{\n' )
        for fld in self.fields:
            fld.produce_decl ( f, idt+2 )
            f.write ( ';\n' )
        indent ( f, idt )
        f.write ( '};\n' )
        
        if ( self.extern ):
            f.write ( '%s *%s' % ( self.type, self.varname ) )
            for fld in self.fields:
                fld.access = '%s->%s' % (self.varname,fld.varname)
                fld.chkaccess = '%s->%s' % (self.name,fld.varname)
        else:
            f.write ( '%s %s' % ( self.type, self.varname ) )
            for fld in self.fields:
                fld.access = '%s.%s' % (self.varname,fld.varname)
                fld.chkaccess = '%s.%s' % (self.name,fld.varname)
        return
    
    def produce_decl_chk ( self, prefix, f, idt=0 ):
        data.produce_decl_chk ( self, f, idt )
        if ( self.extern ):
            f.write ( '%s _%s%s;\n' % (self.type,prefix,self.name) )
            f.write ( '%s *%s%s = &_%s%s' % (self.type,prefix,self.name,prefix,self.name) )
        else:
            f.write ( '%s %s%s' % (self.type,prefix,self.name) )
        return
    
    def produce_cast ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( '(%s' % self.type )
        if ( self.extern ):
            f.write ( '*' )
        f.write ( ') ' )
        return
    
    def produce_arg ( self, f, idt=0 ):
        f.write ( self.varname )
        return

    def produce_init ( self, f, idt=0 ):
        for fld in self.fields:
            n = fld.varname
            fld.varname = fld.access
            chkn = fld.name
            fld.name = fld.chkaccess
            fld.produce_init ( f, idt )
            fld.name = chkn
            fld.varname = n
        return

    def produce_copy ( self, prefix, f, idt=0 ):
        for fld in self.fields:
            n = fld.varname
            fld.varname = fld.access
            chkn = fld.name
            fld.name = fld.chkaccess
            fld.produce_copy ( prefix, f, idt )
            fld.name = chkn
            fld.varname = n
        return

    def produce_check ( self, variantname, prefix, f, idt=0 ):
        for fld in self.fields:
            n = fld.varname
            fld.varname = fld.access
            chkn = fld.name
            fld.name = fld.chkaccess
            fld.produce_check ( variantname, prefix, f, idt )
            fld.name = chkn
            fld.varname = n
        return


# entry
class entry:
    xml_node = 'entry'
    xml_attr = [ 'name' ]

    def __init__ ( self, name='entry', data=[] ):
        self.name = name
        self.varname = '_' + self.name
        self.data = data
        return

    def produce_decl ( self, f, idt=0 ):
        for d in self.data:
            d.produce_decl ( f, 0 )
            f.write ( ';\n' )
            if ( d.chk ):
                d.produce_decl_chk ( 'chk_', f, idt )
                f.write ( ';\n' )
        
        f.write ( 'void (*%s) ( ' % self.varname )
        if ( len(self.data) >= 1 ):
            for idx in range(len(self.data)-1):
                self.data[idx].produce_decl ( f, 0 )
                f.write ( ', ' )
            self.data[len(self.data)-1].produce_decl ( f )
            f.write ( ' ' )
        f.write ( ');\n' )
        return

    def produce_cast ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( '' )
        return

    def produce_call ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( '%s ( ' % self.varname )
        if ( len(self.data) >= 1 ):
            for idx in range(len(self.data)-1):
                self.data[idx].produce_arg ( f )
                f.write ( ', ' )
            self.data[len(self.data)-1].produce_arg ( f )
            f.write ( ' ' )
        f.write ( ');\n' )
        return



# program
class program:
    xml_node = 'program'
    xml_attr = [ 'name', 'ext' ]

    def __init__ ( self, name='unnamed', ext='c', extrafiles=[], data=[], entry=entry() ):
        self.name = name
        self.ext = ext
        self.extrafiles = extrafiles
        self.data = data
        self.entry = entry
        
        self.data_ini = [ ]
        self.data_chk = [ ]
        self.data_iter = [ ]
        
        self.init_dataset ( self.data, True )
        self.init_dataset ( self.entry.data, False )
        return

    def init_dataset ( self, data, extern ):
        for d in data:
            d.extern = extern
            if ( d.ini ):
                self.data_ini.append ( d )
            if ( d.chk ):
                self.data_chk.append ( d )
            if ( d.__class__ == array ):
                if ( len(d.dims) > len(self.data_iter) ):
                    for i in range ( len(self.data_iter), len(d.dims), 1 ):
                        self.data_iter.append ( scalar(type='int',name=chr(ord('i')+i),varname=chr(ord('i')+i),ini='false',chk='false') )
        return

    def produce_data_decl ( self, f, idt=0 ):
        for d in self.data:
            d.produce_decl ( f, idt )
            f.write ( ';\n' )
            if ( d.chk ):
                d.produce_decl_chk ( 'chk_', f, idt )
                f.write ( ';\n' )
        for d in self.data_iter:
            d.produce_decl ( f, idt )
            f.write ( ';\n' )
        return

    def produce_init ( self, f, idt=0 ):
        for d in self.data_ini:
            d.produce_init ( f, idt )
        return

    def produce_time_in ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( 'gettimeofday ( &start, NULL );\n' )
        return

    def produce_time_out ( self, vname, f, idt=0 ):
        indent ( f, idt )
        f.write ( 'gettimeofday ( &end, NULL );\n' )
        indent ( f, idt )
        f.write ( 'printf ( \"%s time %%.2f\\n\", ((end.tv_sec-start.tv_sec)*1000000+(end.tv_usec-start.tv_usec))/1000.0 );\n' % vname )
        return

    def produce_copy ( self, f, idt=0 ):
        for d in self.data_chk:
            d.produce_copy ( 'chk_', f, idt )
        return
    
    def produce_check ( self, vname, f, idt=0 ):
        indent ( f, idt )
        f.write ( 'error = 0;\n' )

        for d in self.data_chk:
            d.produce_check ( vname, 'chk_', f, idt )

        f.write ( '\n' )
        indent ( f, idt )
        f.write ( 'printf ( \"%s check %%d\\n\", error );\n' % vname )
        indent ( f, idt )
        f.write ( 'fflush ( stdout );\n' )
        return



# check
class check:
    xml_node = 'check'
    xml_attr = [ 'name', 'file' ]

    def __init__ ( self, name=None, file=None ):
        if ( name == None ):
            print ( 'maniac: check.__init__(): error: name should not be None.\n' )
            sys.exit ( 1 )

        if ( file == None ):
            print ( 'maniac: check.__init__(): error: file should not be None.\n' )
            sys.exit ( 1 )

        self.name = name
        self.file = file
        return

    def get_files ( self ):
        return self.file
    
    def get_filename ( self, prog ):
        f = self.file.replace ( '%prog%', prog.name )
        return f
    
    def copy ( self, dir=os.curdir, prog=None, log=None ):
        fname = self.get_filename ( prog )
        status = event.STATUS_SUCCESS
        t = subproc_call ( dir, 'cp %s %s-ref > /dev/null'%(fname,fname) )
        if ( t[0] != 0 ):
            status = event.STATUS_FAILURE
        log.add_event ( event.CREATE_REF, self.name, status, t[2] )
        return t[0]
    
    def perform ( self, dir=os.curdir, prog=None, log=None ):
        fname = self.get_filename ( prog )
        status = event.STATUS_SUCCESS
        text = ''
        if ( os.path.exists(os.path.join(dir,'%s-ref'%fname)) ):
            t = subproc_call ( dir, 'diff -u %s-ref %s'%(fname,fname) )
            if ( t[0] != 0 ):
                status = event.STATUS_FAILURE
            text = t[2]+t[1]
        else:
            status = event.STATUS_WARNING
            text = str ( '%s-ref'%fname + ': Reference file not found\n' )
        log.add_event ( event.CHECK_GENERATE, self.name, status, text )
        return status


# clean
class clean:
    xml_node = 'clean'
    xml_attr = [ 'files' ]

    def __init__ ( self, files=None ):
        if ( files == None ):
            print ( 'maniac: clean.__init__(): error: files should not be None.\n' )
            sys.exit ( 1 )
            
        self.files = files
        return
    
    def perform ( self, already_cleaned, dir=os.curdir, prog=None, variants=None, log=None ):
        f = self.files.replace ( '%prog%', prog.name )

        flist = ''
        if ( '%variant%' in self.files ):
             for v in variants:
                 flist = flist + f.replace('%variant%',v.name) + ' '
        else:
            flist = f

        status = event.STATUS_SUCCESS
        if ( flist not in already_cleaned ):
            t = subproc_call ( dir, 'rm -f %s > /dev/null'%(flist) )
            if ( t[0] != 0 ):
                status = event.STATUS_FAILURE
            log.add_event ( event.CLEAN, self.files, status, t[2] )
            already_cleaned.append ( flist )
        return status



# generator
class generator:
    xml_node = 'generator'
    xml_attr = [ 'name', 'bin', 'flags' ]

    def __init__ ( self, name=None, bin=None, flags='', checks=None, cleans=None ):
        if ( name == None ):
            print ( 'maniac: generator.__init__(): error: name should not be None.\n' )
            sys.exit ( 1 )
        
        self.name = name
        self.bin = bin
        self.flags = flags

        if ( checks == None ):
            self.checks = [ ]
        else:
            self.checks = checks
        
        if ( cleans == None ):
            self.cleans = [ ]
        else:
            self.cleans = cleans
        
        return

    def build_binpath ( self, dir ):
        binpath = self.bin.split ( os.sep ) # adjust binary path according to dir
        for d in dir.split(os.sep):
            if ( d == os.curdir ):
                pass
            elif ( d == os.pardir ):
                binpath = binpath[1:]
            elif ( len(d) > 0 ):
                binpath = [os.pardir] + binpath
        bin = os.sep.join ( binpath )
        # check that the binary path built is valid from provided dir
        oldpath = os.getcwd ( )
        found = False
        try:
            os.chdir ( dir )
            found = os.path.exists(bin)
        except:
            pass
        os.chdir ( oldpath )
        # if binary found, return new path
        if ( found ):
            return bin
        # else, consider the binary to be in $PATH
        return os.path.basename ( self.bin )

    def generate ( self, dir=os.curdir, prog=None, log=None ):
        bin = self.build_binpath ( dir )
        status = event.STATUS_SUCCESS
        flags = self.flags.replace ( '%prog%', prog.name )
        t = subproc_call ( dir, '%s %s %s.%s > /dev/null'%(bin,flags,prog.name,prog.ext) )
        if ( t[0] != 0 ):
            status = event.STATUS_FAILURE
        log.add_event ( event.GENERATE, self.name, status, t[2] )
        return status

    def create_refs ( self, dir=os.curdir, prog=None, log=None ):
        retcode = 0
        for c in self.checks:
            retcode = retcode + c.copy ( dir, prog, log )
        return retcode

    def check ( self, dir=os.curdir, prog=None, log=None ):
        retcode = 0
        for c in self.checks:
            retcode = retcode + c.perform ( dir, prog, log )
        return retcode

    def clean ( self, already_cleaned, dir=os.curdir, prog=None, variants=None, log=None ):
        retcode = 0
        for c in self.cleans:
            retcode = retcode + c.perform ( already_cleaned, dir, prog, variants, log )
        for c in self.checks:
            cl = clean ( c.get_files() )
            cl.perform ( already_cleaned, dir, prog, variants, log )
        for v in variants:
            if ( v.gen == self.name ):
                cl = clean ( v.get_files(prog) )
                cl.perform ( already_cleaned, dir, prog, None, log )
        cl = clean ( loader.get_files() )
        cl.perform ( already_cleaned, dir, prog, None, log )
        return retcode


# generator_none (special no-op generator)
class generator_none ( generator ):
    def __init__ ( self, variants ):
        generator.__init__ ( self, 'none', 'echo', '', None, None )
        return

    def generate ( self, dir=os.curdir, prog=None, log=None ):
        return event.STATUS_SUCCESS

    def clean ( self, already_cleaned, dir=os.curdir, prog=None, variants=None, log=None ):
        for v in variants:
            if ( v.gen == self.name ):
                cl = clean ( v.get_object_files(prog) )
                cl.perform ( already_cleaned, dir, prog, None, log )
        cl = clean ( loader.get_files() )
        cl.perform ( already_cleaned, dir, prog, None, log )
        return 0


# generator_copy (special copy generator)
class generator_copy ( generator ):
    def __init__ ( self, variants ):
        generator.__init__ ( self, 'copy', 'ln', '', None, None )

        # create list of variants to 'copy'
        self.tocreate = [ ]
        for v in variants:
            if ( variants[v].gen == 'copy' ):
                self.tocreate.append ( v )
        return

    def generate ( self, dir=os.curdir, prog=None, log=None ):
        status = event.STATUS_SUCCESS
        msg = ''
        for vname in self.tocreate:
            t = subproc_call ( dir, 'rm -f %s-%s.%s'%(prog.name,vname,prog.ext) )
            if ( t[0] != 0 ):
                status = event.STATUS_FAILURE
                msg += t[2]
            t = subproc_call ( dir, 'ln -s %s.%s %s-%s.%s'%(prog.name,prog.ext,prog.name,vname,prog.ext) )
            if ( t[0] != 0 ):
                status = event.STATUS_FAILURE
                msg += t[2]
        if ( status != event.STATUS_SUCCESS ):
            log.add_event ( event.GENERATE, self.name, status, msg )
        return status



# variant
class variant:
    xml_node = 'variant'
    xml_attr = [ 'name', 'gen', 'comp', 'compflags', 'chk', 'time' ]

    def __init__ ( self, name=None, gen=None, comp=COMP, compflags=COMPFLAGS, chk='true', time='false' ):
        if ( name == None ):
            print ( 'maniac: variant.__init__(): error: name should not be None.\n' )
            sys.exit ( 1 )

        self.name = name
        self.gen = gen
        self.comp = comp
        self.compflags = compflags
        self.chk = str2bool ( chk )
        self.time = str2bool ( time )

        self.tag = '-'+self.name
        self.ref = False

        if ( self.name == 'ref' ):
            self.chk = False
            self.tag = ''
            self.ref = True
        
        return

    def reload_attributes ( self, gen=None, comp=None, compflags=None, chk=None, time=None ):
        if ( gen != None ):
            self.gen = gen

        if ( comp != None ):
            self.comp = comp

        if ( compflags != None ):
            self.compflags = compflags

        if ( chk != None ):
            self.chk = str2bool ( chk )

        if ( time != None ):
            self.time = str2bool ( time )
        return

    def get_source_files ( self, prog ):
        if ( not self.ref ):
            return '%%prog%%%s.%s' % (self.tag,prog.ext)
        return ''

    def get_object_files ( self, prog ):
        return '%%prog%%%s.so' % self.tag

    def get_files ( self, prog ):
        return ' '.join ( [ self.get_object_files(prog), self.get_source_files(prog) ] )
    
    def compile ( self, dir='', prog=None, log=None ):
        fname = prog.name+self.tag
        subproc_call ( dir, 'rm -f %s.so > /dev/null'%fname )
        status = event.STATUS_SUCCESS
        extrafiles = ' '.join ( prog.extrafiles )
        t = subproc_call ( dir, '%s -fPIC -DMANIAC -shared %s -o %s.so %s.%s %s > /dev/null' % (self.comp,self.compflags,fname,fname,prog.ext,extrafiles) )
        if ( t[0] != 0 ):
            status = event.STATUS_FAILURE
        log.add_event ( event.COMPILE_VARIANT, self.name, status, t[2] )
        return t[0]

    def produce_load_symbol ( self, symb, phaseid, next_phaseid, f, idt=0 ):
        indent ( f, idt )
        #f.write ( '*(void **) (&' )
        f.write ( '%s' % symb.varname )
        f.write ( ' = ' )
        #symb.produce_cast ( f )
        f.write ( 'dlsym ( dlhandle, \"%s\" );\n' % symb.name )
        indent ( f, idt )
        f.write ( 'dlerr = dlerror ( );\n' )
        indent ( f, idt )
        f.write ( 'if ( dlerr != NULL )\n' )
        indent ( f, idt+2 )
        f.write ( '{\n' )
        indent ( f, idt+4 )
        f.write ( 'fprintf ( stderr, "%s %%s\\n", dlerr );\n' % self.name )
        indent ( f, idt+4 )
        f.write ( 'fflush ( stderr );\n' )
        indent ( f, idt+4 )
        f.write ( 'printf ( \"%s check 1\\n\" );\n' % self.name )
        indent ( f, idt+4 )
        f.write ( 'fflush ( stdout );\n' )
        indent ( f, idt+4 )
        f.write ( 'dlclose ( dlhandle );\n' )
        indent ( f, idt+4 )
        f.write ( 'goto phase%d;\n' % next_phaseid )
        indent ( f, idt+2 )
        f.write ( '}\n\n' )
        return

    def produce_load ( self, prog, phaseid, next_phaseid, f, idt=0 ):
        shortname = prog.name+self.tag
        indent ( f, idt )
        f.write ( '/* dealing with variant %s */\n' % self.name )
        f.write ( ' phase%d:\n' % phaseid )
        indent ( f, idt )
        f.write ( 'dlhandle = dlopen ( \"./%s.so\", RTLD_LAZY );\n' % shortname )
        indent ( f, idt )
        f.write ( 'if ( !dlhandle )\n' )
        indent ( f, idt+2 )
        f.write ( '{\n' )
        indent ( f, idt+4 )
        f.write ( 'fprintf ( stderr, "%s %%s\\n", dlerror() );\n' % self.name )
        indent ( f, idt+4 )
        f.write ( 'fflush ( stderr );\n' )
        indent ( f, idt+4 )
        f.write ( 'printf ( \"%s check 1\\n\" );\n' % self.name )
        indent ( f, idt+4 )
        f.write ( 'fflush ( stdout );\n' )
        indent ( f, idt+4 )
        f.write ( 'goto phase%d;\n' % next_phaseid )
        indent ( f, idt+2 )
        f.write ( '}\n\n' )

        self.produce_load_symbol ( prog.entry, phaseid, next_phaseid, f, idt )

        for d in prog.data:
            if ( d.extern ):
                self.produce_load_symbol ( d, phaseid, next_phaseid, f, idt )
        return
    
    def produce_unload ( self, f, idt=0 ):
        indent ( f, idt )
        f.write ( 'dlclose ( dlhandle );\n' )
        return
    
    def produce_exec ( self, prog, phaseid, next_phaseid, f, idt=0 ):
        self.produce_load ( prog, phaseid, next_phaseid, f, idt )
        prog.produce_init ( f, 2 )

        if ( self.time ):
            prog.produce_time_in ( f, idt )
            f.write ( '\n' )

        prog.entry.produce_call ( f, idt )

        if ( self.time ):
            f.write ( '\n' )
            prog.produce_time_out ( self.name, f, idt )

        if ( self.ref ):
            f.write ( '\n' )
            prog.produce_copy ( f, idt )
            f.write ( '\n' )

        if ( self.chk ):
            f.write ( '\n' )
            prog.produce_check ( self.name, f, idt )
            f.write ( '\n' )
            
        self.produce_unload ( f, idt )
        f.write ( '\n' )
        return



# command
class command:
    xml_node = 'command'
    xml_attr = [ 'id', 'cmd' ]

    def __init__ ( self, id=None, cmd=None ):
        if ( id == None ):
            print ( 'maniac: command.__init__(): error: type should not be None.\n' )
            sys.exit ( 1 )

        if ( cmd == None ):
            print ( 'maniac: command.__init__(): error: cmd should not be None.\n' )
            sys.exit ( 1 )

        try:
            self.id = event.types_str.index ( id.upper() )
        except:
            print ( 'maniac: command.__init__(): error: invalid command type \'%s\'.\n' % id )
            sys.exit ( 1 )

        self.cmd = cmd
        return

    def execute ( self, dir='', prog=None, log=None, timeout=0 ):
        t = subproc_call ( dir, self.cmd, timeout )
        if ( log != None ):
            if ( t[0] != 0 ):
                status = event.STATUS_FAILURE
                text = t[2]+t[1]
            elif ( t[2] == '' ):
                status = event.STATUS_SUCCESS
                text = ''
            else:
                status = event.STATUS_WARNING
                text = t[2]
            log.add_event ( self.id, self.cmd, status, text )
        return t


# plan
class plan:
    xml_node = 'plan'
    xml_attr = [ 'name', 'default', 'nogen' ]

    def __init__ ( self, name=None, default='false', nogen='false', variants=None, commands=None ):
        if ( name == None ):
            print ( 'maniac: plan.__init__(): error: name should not be None.\n' )
            sys.exit ( 1 )

        if ( variants == None ):
            print ( 'maniac: plan.__init__(): error: variants should not be None.\n' )
            sys.exit ( 1 )
        
        self.name = name
        self.default = str2bool ( default )
        self.nogen = str2bool ( nogen )
        self.variants = variants
        self.commands = [ None for i in range(event.NB_IDENTS) ]
        if ( commands != None ):
            for c in commands:
                self.commands[c.id] = c
        self.loader_built = False
        return

    def get_needed_generators ( self, generators ):
        #  prune similar generation
        gen = { }
        if ( self.nogen ):
            return gen
        for v in self.variants:
            if ( v.gen == None ):
                continue
            if ( v.gen not in gen ):
                gen[v.gen] = generators[v.gen]
        return gen
    
    def follow ( self, dir='', prog=None, generators=None, last_plan=None ):
        j = journal ( self, prog )

        if ( last_plan != (self.name,dir) ):
            gen = self.get_needed_generators ( generators )

            # generate variants
            for g in gen:
                rc = gen[g].generate ( dir, prog, j )
                if ( rc != 0 ):
                    return j
                gen[g].check ( dir, prog, j )
        
            # compile variants
            if ( self.commands[event.COMPILE_VARIANT] != None ):
                self.commands[event.COMPILE_VARIANT].execute ( dir, prog, j ) # variants are grouped :/
            else:
                for v in self.variants:
                    v.compile ( dir, prog, j )

        # compile loader
        l = loader ( dir, prog, self )
        l.produce ( )

        if ( last_plan != (self.name,dir) ):
            if ( self.commands[event.COMPILE_LOADER] != None ):
                self.commands[event.COMPILE_LOADER].execute ( dir, prog, j )
            else:
                rc = l.compile ( j )
            self.loader_built = True
        elif ( self.loader_built ):
            rc = 0

        # run loader
        if ( rc == 0 ):
            l.run ( self.commands[event.RUN_LOADER], j )

        return j


# plan_ref
class plan_ref ( plan ):
    def __init__ ( self, nogen='false', variants=None ):
        plan.__init__ ( self, 'ref', 'false', nogen, variants )
        return
    
    def follow ( self, dir='', prog=None, generators=None, last_plan=None ):
        j = journal ( self, prog )
        gen = self.get_needed_generators ( generators )

        for g in gen:
            gen[g].generate ( dir, prog, j )
            gen[g].create_refs ( dir, prog, j )
        
        return j


# plan_clean
class plan_clean ( plan ):
    def __init__ ( self, variants=None ):
        plan.__init__ ( self, 'clean', 'false', 'false', variants )
        return
    
    def follow ( self, dir='', prog=None, generators=None, last_plan=None ):
        j = journal ( self, prog )
        already_cleaned = [ ]

        for g in generators:
            generators[g].clean ( already_cleaned, dir, prog, self.variants, j )
        
        return j



# loader
class loader:
    xml_node = 'loader'
    xml_attr = [ ]

    def __init__ ( self, dir='', prog=None, plan=None ):
        self.dir = dir
        self.prog = prog
        self.plan = plan
        self.cflags = LOADERFLAGS
        return

    def produce_header ( self, f, fname ):
        f.write ( '/*\n * %s\n * produced by maniac test generator\n */\n\n' % fname )
        f.write ( '#include <stdlib.h>\n' )
        f.write ( '#include <stdio.h>\n' )
        f.write ( '#include <dlfcn.h>\n' )
        f.write ( '#include <sys/time.h>\n' )
        return

    def get_files ( cls ):
        return '%prog%-loader %prog%-loader.c'
    get_files = classmethod(get_files)
    
    def produce ( self ):
        fname = self.prog.name+'-loader.c'
        dirfname = os.path.join ( self.dir, fname )
        f = file ( dirfname, 'w' )

        self.produce_header ( f, fname )
        f.write ( '\n' )

        self.prog.produce_data_decl ( f, 0 )
        f.write ( '\n' )

        self.prog.entry.produce_decl ( f, 0 )
        f.write ( '\n' )

        f.write ( 'int\nmain ( )\n{\n' )

        f.write ( '  int error = 0;\n' )
        f.write ( '  void *dlhandle;\n' )
        f.write ( '  char *dlerr;\n' )
        for v in self.plan.variants:
            if ( v.time ):
                f.write ( '  struct timeval start, end;' )
                break
        f.write ( '\n\n' )

        phaseid = 0
        for v in self.plan.variants:
            if ( v.ref ):
                next_phaseid = len(self.plan.variants)
            else:
                next_phaseid = phaseid + 1
            v.produce_exec ( self.prog, phaseid, next_phaseid, f, 2 )
            phaseid = phaseid + 1

        f.write ( ' phase%d:\n' % phaseid )
        f.write ( '  return 0;\n' )
        f.write ( '}\n' )
        f.close ( )
        return

    def compile ( self, log=None ):
        shortname = self.prog.name+'-loader'
        status = event.STATUS_SUCCESS
        t = subproc_call ( self.dir, '%s -ldl %s -o %s %s.c > /dev/null' % (COMP,self.cflags,shortname,shortname) )
        if ( t[0] != 0 ):
            status = event.STATUS_FAILURE
        log.add_event ( event.COMPILE_LOADER, self.prog.name, status, t[2] )
        return t[0]

    def run ( self, cmd=None, log=None ):
        variants_out = ''
        loader_msg = ''
        
        if ( self.dir == '' ):
            d = os.curdir
        else:
            d = self.dir

        status = event.STATUS_SUCCESS
        if ( cmd == None ):
            t = subproc_call ( d, './%s' % (self.prog.name+'-loader'), LOADERTIMEOUT )
        else:
            t = cmd.execute ( self.dir, self.prog, None, LOADERTIMEOUT )
        retcode = t[0]
        variants_out = t[1]
        loader_msg = t[2]
        
        if ( retcode == 0 ):
            lines = variants_out.split ( '\n' )
            for l in lines:
                if ( l == '' ):
                    continue
                vstatus = l.split ( ' ', 2 )
                vestatus = event.STATUS_SUCCESS
                if ( vstatus[1] == 'check' ):
                    check_lines = loader_msg.split ( '\n' )
                    check_msg = ''
                    for cl in check_lines:
                        if ( cl.startswith(vstatus[0]+' ') ):
                            check_msg = check_msg + cl.replace(vstatus[0]+' ','') + '\n'
                    if ( int(vstatus[2]) != 0 ):
                        vestatus = event.STATUS_FAILURE
                    log.add_event ( event.CHECK_VARIANT, vstatus[0], vestatus, check_msg )
                elif ( vstatus[1] == 'time' ):
                    log.add_event ( event.TIME_VARIANT, vstatus[0], vestatus, vstatus[2] )
        else:
            status = event.STATUS_FAILURE
        log.add_event ( event.RUN_LOADER, self.prog.name, status, loader_msg )
        return retcode



# event
class event:
    GENERATE = 0
    CHECK_GENERATE = 1
    CREATE_REF = 2
    COMPILE_VARIANT = 3
    COMPILE_LOADER = 4
    RUN_LOADER = 5
    CHECK_VARIANT = 6
    TIME_VARIANT = 7
    CLEAN = 8
    NB_IDENTS = 9
    types = [ GENERATE, CHECK_GENERATE, CREATE_REF, COMPILE_VARIANT, COMPILE_LOADER, RUN_LOADER, CHECK_VARIANT, TIME_VARIANT, CLEAN ]
    types_str = [ 'GENERATE', 'CHECK_GENERATE', 'CREATE_REF', 'COMPILE_VARIANT', 'COMPILE_LOADER', 'RUN_LOADER', 'CHECK_VARIANT', 'TIME_VARIANT', 'CLEAN' ]

    STATUS_SUCCESS = 0
    STATUS_WARNING = 1
    STATUS_FAILURE = 2

    def __init__ ( self, ident, tag, status, msg='' ):
        self.ident = ident
        self.tag = tag
        self.status = status
        self.msg = msg
        return

    def get_status ( self ):
        if ( self.status == event.STATUS_FAILURE ):
            return '\033[41m\033[30m \033[0m'
        elif ( self.status == event.STATUS_WARNING ):
            return '\033[43m\033[30m \033[0m'
        
        if ( self.ident == event.TIME_VARIANT ):
            return self.msg
        elif ( self.ident == event.CREATE_REF ):
            return '\033[37mready\033[0m'
        elif ( self.ident == event.CLEAN ):
            return '\033[37mclean\033[0m'
        
        return '\033[42m\033[30m \033[0m'

    def get_html_status ( self ):
        if ( self.status == event.STATUS_FAILURE ):
            return 'failure'
        elif ( self.status == event.STATUS_WARNING ):
            return 'warning'
        
        if ( self.ident == event.TIME_VARIANT ):
            return self.msg
        elif ( self.ident == event.CREATE_REF ):
            return 'ready'
        elif ( self.ident == event.CLEAN ):
            return 'clean'
        
        return 'success'

    def get_html_message ( self ):
        msg = self.msg.replace ( '&', '&amp;' )
        msg = msg.replace ( '<', '&lt;' )
        msg = msg.replace ( '<', '&gt;' )
        return msg
    
    def produce_html ( self, f, j, n ):
        msg = ''
        if ( ( self.status != 0 ) and ( len(self.msg) > 0 ) ):
            msg = unicode ( self.msg, errors='ignore' )
            msg = msg.replace ( '\'', '\\\'' )
            msg = msg.replace ( '\"', '\\\"' )
            msg = msg.replace ( '\n', '\\n' )
        if ( self.status == event.STATUS_SUCCESS ):
            cl = 'succrow'
            idchar = 'p'
        elif ( self.status == event.STATUS_WARNING ):
            cl = 'warnrow'
            idchar = 'w'
        else:
            cl = 'failrow'
            idchar = 'f'
        f.write ( '<tr id=\'%st%d.%d.%d\' class=\'hiddenRow\'>\n' % (idchar,j.uid,self.ident,n) )
        f.write ( '    <td class=\'none\'><div class=\'eventcell\'><i>%s</i></div></td>\n' % self.tag )
        if ( len(msg) > 0 ):
            f.write ( '    <td colspan=\'5\' align=\'center\' class=\'%s\'><div class=\'statuscell\'>' % cl )
            f.write ( '<a class=\'link\' href="javascript:showMessage(\'mt%d.%d.%d\')">%s</a></div>' % (j.uid,self.ident,n,self.get_html_status()) )
            f.write ( '</tr>\n' )
            f.write ( '<tr id=\'mt%d.%d.%d\' class=\'hiddenRow\'>\n' % (j.uid,self.ident,n) )
            f.write ( '    <td colspan=\'6\' align=\'left\' class=\'msgrow\'><div class=\'msgcell\'><pre>%s</pre></div></td>\n' % (self.get_html_message()) )
        else:
            f.write ( '    <td colspan=\'5\' align=\'center\' class=\'%s\'><div class=\'statuscell\'>%s</div></td>\n' % (cl,self.get_html_status()) )
        f.write ( '</tr>\n' )
        return

    def __str__ ( self ):
        msg = ''
        nl = ''
        if ( ( self.status != event.STATUS_SUCCESS ) and ( len(self.msg) > 0 ) ):
            msg = '\n%s' % unicode(self.msg,errors='ignore')
            if ( msg[len(msg)-1] == '\n' ):
                msg = msg[0:len(msg)-1]
                nl = '\n'
            msg = msg.replace ( '\n', '\n        ' )
        if ( self.ident == event.CLEAN ):
            nl = '\n'
        return '\033[37m%s\033[0m %s%s%s' % (self.tag,self.get_status(),msg,nl)


# journal
class journal:
    EVENT_TYPES = [ 'GENERATE', 'CHECK GENERATE', 'CREATE REF', 'COMPILE VARIANTS', 'COMPILE LOADER', 'RUN LOADER', 'CHECK VARIANTS', 'TIME VARIANTS', 'CLEAN' ]
    uid = 1
    
    def __init__ ( self, plan, prog ):
        self.plan = plan
        self.prog = prog
        self.events = { }
        
        self.uid = journal.uid
        journal.uid = journal.uid + 1
        
        for i in range(len(journal.EVENT_TYPES)):
            self.events[i] = [ ]
        
        return

    def add_event ( self, ident, tag, status, msg='' ):
        self.events[ident].append ( event(ident,tag,status,msg) )
        return

    def has_events ( self, ident ):
        return ( len(self.events[ident]) > 0 )

    def generation_failed ( self ):
        if ( journal.EVENT_TYPES[event.GENERATE] in self.events ):
            for e in self.events[journal.EVENT_TYPES[event.GENERATE]]:
                if ( e.status == event.STATUS_FAILURE ):
                    return True
        return False

    def has_failed ( self ):
        for ident in event.types:
            for e in self.events[ident]:
                if ( e.status == event.STATUS_FAILURE ):
                    return True
        return False

    def has_warned ( self ):
        for ident in event.types:
            for e in self.events[ident]:
                if ( e.status == event.STATUS_WARNING ):
                    return True
        return False

    def produce_html_events ( self, f, ident ):
        if ( not self.has_events(ident) ):
            return

        cl = 'succjob'
        npass = 0
        nwarn = 0
        nfail = 0
        for e in self.events[ident]:
            if ( e.status == event.STATUS_SUCCESS ):
                npass += 1
            elif ( e.status == event.STATUS_WARNING ):
                if ( cl == 'succjob' ):
                    cl = 'warnjob'
                nwarn += 1
            else:
                cl = 'failjob'
                nfail += 1
                
        f.write ( '<tr class=\'%s\'>\n' % cl )
        f.write ( '    <td><div class=\'jobcell\'>%s</div></td>\n' % journal.EVENT_TYPES[ident] )
        f.write ( '    <td align=\'center\'>%d</td>\n' % len(self.events[ident]) )
        f.write ( '    <td align=\'center\'>%d</td>\n' % npass )
        f.write ( '    <td align=\'center\'>%d</td>\n' % nwarn )
        f.write ( '    <td align=\'center\'>%d</td>\n' % nfail)
        f.write ( '    <td align=\'center\'><a class=\'link\' href="javascript:showJobDetail(\'c%d.%d\',%d)">details</a></td>\n' % (self.uid,ident,len(self.events[ident])) )
        f.write ( '</tr>\n' )
        n = 1
        for e in self.events[ident]:
            e.produce_html ( f, self, n )
            n = n +1
        return

    def produce_html ( self, f ):
        f.write ( '<div class=\'journal\'>\n' )
        f.write ( '<a name=\'%d\'>\n' % self.uid )
        f.write ( '<p class=\'section\'><strong>Program:</strong> %s<br/><strong>Plan:</strong> %s</p>\n' % (self.prog.name,self.plan.name) )
        f.write ( '<p id=\'table_cmd\'>show ' )
        f.write ( '<a class=\'showlink\' href=\'javascript:showCase(%d,0)\'>summary</a> ' % self.uid )
        f.write ( '<a class=\'showlink\' href=\'javascript:showCase(%d,1)\'>warnings</a> ' % self.uid )
        f.write ( '<a class=\'showlink\' href=\'javascript:showCase(%d,2)\'>failures</a> ' % self.uid )
        f.write ( '<a class=\'showlink\' href=\'javascript:showCase(%d,3)\'>all</a> ' % self.uid )
        f.write ( '</p>\n' )
        f.write ( '<table id=\'result_table\'>\n' )
        f.write ( '<colgroup><col/><col/><col/><col/><col/><col/></colgroup>\n' )
        f.write ( '<tr id=\'header_row\'>\n' )
        f.write ( '    <td align=\'center\'><div class=\'headcell\'>Job Category</div></td>\n' )
        f.write ( '    <td align=\'center\'><div class=\'headcell\'>Count</div></td>\n' )
        f.write ( '    <td align=\'center\'><div class=\'headcell\'>Successes</div></td>\n' )
        f.write ( '    <td align=\'center\'><div class=\'headcell\'>Warnings</div></td>\n' )
        f.write ( '    <td align=\'center\'><div class=\'headcell\'>Failures</div></td>\n' )
        f.write ( '    <td align=\'center\'><div class=\'headcell\'>View</div></td>\n' )
        f.write ( '</tr>\n' )
        for ident in event.types:
            self.produce_html_events ( f, ident )
        f.write ( '</table>\n' )
        f.write ( '<p><a class=\'toplink\' href=\'#top\'>top</a></p>\n' )
        f.write ( '</div>\n' )
        return

    def produce_events ( self, f, ident ):
        if ( not self.has_events(ident) ):
            return
        
        f.write ( '    %s:\n' % journal.EVENT_TYPES[ident] )
        s = '      '
        for e in self.events[ident]:
            s = s + str(e)
            if ( e != self.events[ident][len(self.events[ident])-1] ):
                if ( s[len(s)-1] != '\n' ):
                    s = s + '  '     # concatenate successful event sequence
                else:
                    s = s + '      ' # add indentation for an event message which ends with a new line
        if ( s[len(s)-1] != '\n' ):
            s = s + '\n'
        f.write ( s )
        return

    def produce_csv_timings ( self, f ):
        if ( not self.has_events(event.TIME_VARIANT) ):
            return
        for e in self.events[event.TIME_VARIANT]:
            f.write ( '%s ' % e.msg )
        f.write ( '\n' )
        return

    def produce ( self, f ):
        f.write ( '\033[1m%s\033[0m\n' % self.prog.name )
        f.write ( '  %s\n' % self.plan.name )
        self.produce_events ( f, event.GENERATE )
        self.produce_events ( f, event.CHECK_GENERATE )
        self.produce_events ( f, event.CREATE_REF )
        self.produce_events ( f, event.COMPILE_VARIANT )
        self.produce_events ( f, event.COMPILE_LOADER )
        self.produce_events ( f, event.RUN_LOADER )
        self.produce_events ( f, event.CHECK_VARIANT )
        self.produce_events ( f, event.TIME_VARIANT )
        self.produce_events ( f, event.CLEAN )
        return



# xml_open
def xml_open ( fname, rootTag, can_fail=False ):
    try:
        doc = parse ( fname )
    except IOError as e:
        if ( not can_fail ):
            print ( 'maniac: xml_open(): error: %s.\n' % str(e) )
            sys.exit ( 1 )
        else:
            return None
    except ExpatError as e:
        print ( 'maniac: xml_open(): error: %s.\n' % str(e) )
        sys.exit ( 1 )

    rootNode = doc.childNodes.item ( 0 )

    if ( rootNode == None ):
        print ( 'maniac: xml_open(): error: file is empty.\n' )
        sys.exit ( 1 )
    if ( rootNode.nodeType != rootNode.ELEMENT_NODE ):
        print ( 'maniac: xml_open(): error: root node is invalid.\n' )
        sys.exit ( 1 )
    if ( rootNode.tagName != rootTag ):
        if ( not can_fail ):
            print ( 'maniac: xml_open(): error: root node must be of type \'%s\'.\n' % rootTag )
            sys.exit ( 1 )
        else:
            return None
    
    return rootNode


# xml_read_attributes
def xml_read_attributes ( node, attrlist ):
    attr = { }
    for a in attrlist:
        if ( node.hasAttribute(a) ):
            attr[a] = node.getAttribute ( a )
    return attr


# xml_extrafile_import
extrafile_xml_node = 'extrafile'
extrafile_xml_attr = ['name']

def xml_extrafiles_import ( node ):
    extrafiles_list = [ ]
    for subNode in node.childNodes:
        if ( subNode.nodeType != subNode.ELEMENT_NODE ):
            continue
        if ( subNode.tagName == extrafile_xml_node ):
            attr = xml_read_attributes ( subNode, extrafile_xml_attr )
            extrafiles_list.append ( attr['name'] )
    return extrafiles_list


# xml_data_import
def xml_data_import ( node ):
    data_list = [ ]
    for subNode in node.childNodes:
        if ( subNode.nodeType != subNode.ELEMENT_NODE ):
            continue
        if ( subNode.tagName == data.xml_node ):
            for subsubNode in subNode.childNodes:
                if ( subsubNode.nodeType != subsubNode.ELEMENT_NODE ):
                    continue
                if ( subsubNode.tagName == scalar.xml_node ):
                    attr = xml_read_attributes ( subsubNode, scalar.xml_attr )
                    data_list.append ( scalar(**attr) )
                elif ( subsubNode.tagName == array.xml_node ):
                    attr = xml_read_attributes ( subsubNode, array.xml_attr )
                    data_list.append ( array(**attr) )
                elif ( subsubNode.tagName == struct.xml_node ):
                    attr = xml_read_attributes ( subsubNode, struct.xml_attr )
                    attr['fields'] = xml_data_import ( subsubNode )
                    data_list.append ( struct(**attr) )
                elif ( subsubNode.tagName == union.xml_node ):
                    attr = xml_read_attributes ( subsubNode, union.xml_attr )
                    attr['fields'] = xml_data_import ( subsubNode )
                    data_list.append ( union(**attr) )
    return data_list


# xml_entry_import
def xml_entry_import ( node ):
    e = None
    for subNode in ( node.getElementsByTagName ( entry.xml_node ) ):
        attr = xml_read_attributes ( subNode, entry.xml_attr )
        attr['data'] =  xml_data_import ( subNode )
        e = entry ( **attr )
    return e


# xml_program_import
def xml_program_import ( fname ):
    rootNode = xml_open ( fname, program.xml_node, True )
    if ( rootNode == None ):
        maniaNode = xml_open ( fname, mania_xml_node )
        for subNode in maniaNode.childNodes:
            if ( subNode.nodeType != subNode.ELEMENT_NODE ):
                continue
            if ( subNode.tagName == program.xml_node ):
                rootNode = subNode
                break
        if ( rootNode == None ):
            print ( 'maniac: xml_program_import(): error: no \'%s\' node found.\n' % program.xml_node )
            sys.exit ( 1 )
    attr = xml_read_attributes ( rootNode, program.xml_attr )
    attr['extrafiles'] = xml_extrafiles_import ( rootNode )
    attr['data'] = xml_data_import ( rootNode )
    attr['entry'] = xml_entry_import ( rootNode )
    prog = program ( **attr )
    return prog


# xml_checks_import
checks_xml_node = 'checks' 

def xml_checks_import ( node ):
    checks = [ ]
    for subNode in node.childNodes:
        if ( subNode.nodeType != subNode.ELEMENT_NODE ):
            continue
        if ( subNode.tagName == checks_xml_node ):            
            for subsubNode in subNode.childNodes:
                if ( subsubNode.nodeType != subsubNode.ELEMENT_NODE ):
                    continue
                if ( subsubNode.tagName == check.xml_node ):
                    attr = xml_read_attributes ( subsubNode, check.xml_attr )
                    checks.append ( check ( **attr ) )
    return checks


# xml_cleans_import
cleans_xml_node = 'cleans'

def xml_cleans_import ( node ):
    cleans = [ ]
    for subNode in node.childNodes:
        if ( subNode.nodeType != subNode.ELEMENT_NODE ):
            continue
        if ( subNode.tagName == cleans_xml_node ):            
            for subsubNode in subNode.childNodes:
                if ( subsubNode.nodeType != subsubNode.ELEMENT_NODE ):
                    continue
                if ( subsubNode.tagName == clean.xml_node ):
                    attr = xml_read_attributes ( subsubNode, clean.xml_attr )
                    cleans.append ( clean ( **attr ) )
    return cleans


# xml_generators_import
generators_xml_node = 'generators'

def xml_generators_import ( node, path ):
    generators = { }
    for subNode in node.childNodes:
        if ( subNode.nodeType != subNode.ELEMENT_NODE ):
            continue
        if ( subNode.tagName == generators_xml_node ):            
            for subsubNode in subNode.childNodes:
                if ( subsubNode.nodeType != subsubNode.ELEMENT_NODE ):
                    continue
                if ( subsubNode.tagName == generator.xml_node ):
                    attr = xml_read_attributes ( subsubNode, generator.xml_attr )
                    attr['checks'] = xml_checks_import ( subsubNode )
                    attr['cleans'] = xml_cleans_import ( subsubNode )
                    attr['bin'] = os.path.join ( path, attr['bin'] )
                    generators[attr['name']] = generator ( **attr )
    return generators


# xml_variants_import
variants_xml_node = 'variants'

def xml_variants_import ( node, db_variants=None ):
    variants = [ ]

    if ( db_variants == None ):
        db_variants = { }

    for subNode in node.childNodes:
        if ( subNode.nodeType != subNode.ELEMENT_NODE ):
            continue
        if ( subNode.tagName == variants_xml_node ):            
            for subsubNode in subNode.childNodes:
                if ( subsubNode.nodeType != subsubNode.ELEMENT_NODE ):
                    continue
                if ( subsubNode.tagName == variant.xml_node ):
                    attr = xml_read_attributes ( subsubNode, variant.xml_attr )
                    if ( attr['name'] in db_variants ):
                        v = copy.deepcopy ( db_variants[attr['name']] )
                        del attr['name']
                        v.reload_attributes ( **attr )
                        variants.append ( v )
                    else:
                        variants.append ( variant ( **attr ) )
    return variants


# xml_commands_import
commands_xml_node = 'commands'

def xml_commands_import ( node ):
    commands = [ ]

    for subNode in node.childNodes:
        if ( subNode.nodeType != subNode.ELEMENT_NODE ):
            continue
        if ( subNode.tagName == commands_xml_node ):            
            for subsubNode in subNode.childNodes:
                if ( subsubNode.nodeType != subsubNode.ELEMENT_NODE ):
                    continue
                if ( subsubNode.tagName == command.xml_node ):
                    attr = xml_read_attributes ( subsubNode, command.xml_attr )
                    commands.append ( command(**attr) )
    return commands


# xml_plans_import
plans_xml_node = 'plans'

def xml_plans_import ( node, db_variants ):
    plans = { }

    for subNode in node.childNodes:
        if ( subNode.nodeType != subNode.ELEMENT_NODE ):
            continue
        if ( subNode.tagName == plans_xml_node ):            
            for subsubNode in subNode.childNodes:
                if ( subsubNode.nodeType != subsubNode.ELEMENT_NODE ):
                    continue
                if ( subsubNode.tagName == plan.xml_node ):
                    attr = xml_read_attributes ( subsubNode, plan.xml_attr )
                    attr['variants'] = xml_variants_import ( subsubNode, db_variants )
                    attr['commands'] = xml_commands_import ( subsubNode )
                    if ( 'nogen' not in attr ):
                        attr['nogen'] = nogen # nogen refers to the default defined prior to command line parsing
                    if ( attr['name'] == 'ref' ):
                        plans['ref'] = plan_ref ( attr['variants'] )
                    elif ( attr['name'] == 'clean' ):
                        plans['clean'] = plan_clean ( attr['variants'] )
                    else:
                        plans[attr['name']] = plan ( **attr )
    return plans


# xml_mania_import
mania_xml_node = 'mania'
mania_xml_file = 'mania.xml'

def xml_locate_and_open_mania ( fname, nb ):
    if ( nb == 0 ):
        print ( 'maniac: xml_locate_and_open_mania(): error: no mania definition found.\n' )
        sys.exit ( 1 )

    rootNode = xml_open ( fname, mania_xml_node, True )

    if ( rootNode == None ):
        ret = xml_locate_and_open_mania ( os.path.join(os.pardir,fname), nb-1 )
    else:
        ret = (os.path.dirname(fname),rootNode)

    return ret

def xml_mania_read ( rootDir, rootNode ):
    generators = xml_generators_import ( rootNode, rootDir )

    db_variants = { }
    variants = xml_variants_import ( rootNode )
    for v in variants:
        db_variants[v.name] = v

    plans = xml_plans_import ( rootNode, db_variants )
    return (generators,db_variants,plans)
    
def xml_mania_import ( fname=None, dirs=None ):
    manias = { }

    if ( ( dirs != None ) and ( fname == None ) ):
        for d in dirs:
            rootDir = os.path.abspath ( d )
            rootNode = xml_open ( os.path.join(d,mania_xml_file), mania_xml_node, True )
            if ( rootNode != None ):
                manias[d] = xml_mania_read ( rootDir, rootNode )

    if ( rootNode == None ):
        if ( fname == None ):
            t = xml_locate_and_open_mania ( mania_xml_file, os.getcwd().count(os.sep) )
            manias['.'] = xml_mania_read ( t[0], t[1] )
        else:
            manias['.'] = xml_mania_read ( os.curdir, xml_open(fname,mania_xml_node) )
    return manias



# html_header_export
def html_header_export ( f ):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write ( '<?xml version="1.0" encoding="UTF-8"?>\n' )
    f.write ( '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n' )
    f.write ( '<html xmlns="http://www.w3.org/1999/xhtml">\n' )
    f.write ( '<head><title>Maniac Report - %s</title>\n' % timestamp )
    f.write ( '<meta name="generator" content="Maniac %s"/>\n' % version() )
    f.write ( '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>\n' )
    f.write ( '<style type="text/css" media="screen">\n' )
    f.write ( 'body        { font-family: sans-serif; font-size: small; }\n' )
    f.write ( 'table       { font-size: 100%; }\n' )
    f.write ( 'pre         { }\n' )
    f.write ( '/* header */\n' )
    f.write ( 'h1 { }\n' )
    f.write ( '.header { margin-top: 0ex; margin-bottom: 1ex; }\n' )
    f.write ( '.header .section { }\n' )
    f.write ( '/* summary */\n' )
    f.write ( '.info { margin-top: 0ex; margin-bottom: 1ex; }\n' )
    f.write ( '.summary { margin-top: 0ex; margin-bottom: 1ex; margin-left: 5%; }\n' )
    f.write ( '#summary_table { margin-left:10%; border-collapse: collapse; border: medium solid #777; }\n' )
    f.write ( '#summary_table td { border: thin solid #777; padding: 0.3em; }\n' )
    f.write ( '.progcell   { margin-left: 0em; margin-right: 2em; }\n' )
    f.write ( '.plancell   { margin-left: 0em; margin-right: 2em; }\n' )
    f.write ( '.succplan  { background-color: #88dd88; padding: 8em; }\n' )
    f.write ( '.warnplan  { background-color: #d5df78; padding: 8em; }\n' )
    f.write ( '.failplan  { background-color: #df8878; }\n' )
    f.write ( '/* journal */\n' )
    f.write ( '.journal { margin-top: 0ex; margin-bottom: -2ex; margin-left: 5%; }\n' )
    f.write ( '#table_cmd { margin-left:10%; font-size: x-small; }\n' )
    f.write ( '#result_table { margin-left:10%; border-collapse: collapse; border: medium solid #777; }\n' )
    f.write ( '#header_row { }\n' )
    f.write ( '#result_table td { border: thin solid #777; padding: 0.3em; }\n' )
    f.write ( '.succjob  { background-color: #88dd88; }\n' )
    f.write ( '.succrow   { background-color: #b0fab0; }\n' )
    f.write ( '.warnjob  { background-color: #d5df78; }\n' )
    f.write ( '.warnrow   { background-color: #faf9a0; }\n' )
    f.write ( '.failjob  { background-color: #df8878; }\n' )
    f.write ( '.failrow   { background-color: #fab0a0; }\n' )
    f.write ( '.hiddenRow  { display: none; }\n' )
    f.write ( '.headcell   { margin-left: 1em; margin-right: 1em; }\n' )
    f.write ( '.jobcell   { margin-left: 0em; margin-right: 2em; }\n' )
    f.write ( '.statuscell   { margin-left: 0.3em; margin-right: 0.3em; }\n' )
    f.write ( '.eventcell   { margin-left: 2em; margin-right: 3em; }\n' )
    f.write ( '.msgrow   { background-color: #f3f3f3; }\n' )
    f.write ( '.msgcell   { margin-left: 3em; margin-right: 1em; }\n' )
    f.write ( '.link { color: #000; }\n' )
    f.write ( '.showlink { color: #2030cc; }\n' )
    f.write ( '.toplink { font-size: x-small; color: #2030cc; }\n' )
    f.write ( '.separator { width: 55%; margin-left: 2%; }\n' )
    f.write ( '/* footer */\n' )
    f.write ( '#footer { }\n' )
    f.write ( '</style>\n' )
    f.write ( '</head>\n' )
    f.write ( '<body>\n' )
    f.write ( '<script language="javascript" type="text/javascript"><!--\n' )
    f.write ( '/* level - 0:summary; 1:warnings; 2:failures; 3:all; */\n' )
    f.write ( 'function showCase(jid,level) {\n' )
    f.write ( '    trs = document.getElementsByTagName("tr");\n' )
    f.write ( '    for (var i = 0; i < trs.length; i++) {\n' )
    f.write ( '        tr = trs[i];\n' )
    f.write ( '        id = tr.id;\n' )
    f.write ( '        idx = id.indexOf ( "." );\n' )
    f.write ( '        tjid = id.substr(2,idx-2);\n' )
    f.write ( '        if ( tjid != jid ) continue;\n' )
    f.write ( '        if (id.substr(0,2) == \'ft\') {\n' )
    f.write ( '            if (level >= 2) {\n' )
    f.write ( '                tr.className = \'\';\n' )
    f.write ( '            }\n' )
    f.write ( '            else {\n' )
    f.write ( '                tr.className = \'hiddenRow\';\n' )
    f.write ( '            }\n' )
    f.write ( '        }\n' )
    f.write ( '        if (id.substr(0,2) == \'wt\') {\n' )
    f.write ( '            if ((level == 1) || (level==3)){\n' )
    f.write ( '                tr.className = \'\';\n' )
    f.write ( '            }\n' )
    f.write ( '            else {\n' )
    f.write ( '                tr.className = \'hiddenRow\';\n' )
    f.write ( '            }\n' )
    f.write ( '        }\n' )
    f.write ( '        if (id.substr(0,2) == \'pt\') {\n' )
    f.write ( '            if (level == 3) {\n' )
    f.write ( '                tr.className = \'\';\n' )
    f.write ( '            }\n' )
    f.write ( '            else {\n' )
    f.write ( '                tr.className = \'hiddenRow\';\n' )
    f.write ( '            }\n' )
    f.write ( '        }\n' )
    f.write ( '        if (id.substr(0,2) == \'mt\') {\n' )
    f.write ( '            if (level == 3) {\n' )
    f.write ( '                tr.className = \'\';\n' )
    f.write ( '            }\n' )
    f.write ( '            else {\n' )
    f.write ( '                tr.className = \'hiddenRow\';\n' )
    f.write ( '            }\n' )
    f.write ( '        }\n' )
    f.write ( '    }\n' )
    f.write ( '}\n' )
    f.write ( 'function showJobDetail(cid, count) {\n' )
    f.write ( '    var id_list = Array(count);\n' )
    f.write ( '    var toHide = 1;\n' )
    f.write ( '    for (var i = 0; i < count; i++) {\n' )
    f.write ( '        tid0 = \'t\' + cid.substr(1) + \'.\' + (i+1);\n' )
    f.write ( '        tid = \'f\' + tid0;\n' )
    f.write ( '        tr = document.getElementById(tid);\n' )
    f.write ( '        if (!tr) {\n' )
    f.write ( '            tid = \'p\' + tid0;\n' )
    f.write ( '            tr = document.getElementById(tid);\n' )
    f.write ( '        }\n' )
    f.write ( '        if (!tr) {\n' )
    f.write ( '            tid = \'w\' + tid0;\n' )
    f.write ( '            tr = document.getElementById(tid);\n' )
    f.write ( '        }\n' )
    f.write ( '        id_list[i] = tid;\n' )
    f.write ( '        if (tr.className) {\n' )
    f.write ( '            toHide = 0;\n' )
    f.write ( '        }\n' )
    f.write ( '    }\n' )
    f.write ( '    for (var i = 0; i < count; i++) {\n' )
    f.write ( '        tid = id_list[i];\n' )
    f.write ( '        if (toHide) {\n' )
    f.write ( '            document.getElementById(tid).className = \'hiddenRow\';\n' )
    f.write ( '            mid = \'m\' + tid.substr(1);\n' )
    f.write ( '            mtr = document.getElementById(mid);\n' )
    f.write ( '            if (mtr) {\n' )
    f.write ( '                mtr.className = \'hiddenRow\';\n' )
    f.write ( '            }\n' )
    f.write ( '        }\n' )
    f.write ( '        else {\n' )
    f.write ( '            document.getElementById(tid).className = \'\';\n' )
    f.write ( '        }\n' )
    f.write ( '    }\n' )
    f.write ( '}\n' )
    f.write ( 'function showMessage(tid) {\n' )
    f.write ( '    var toHide = 1;\n' )
    f.write ( '    tr = document.getElementById(tid);\n' )
    f.write ( '    if (tr.className) {\n' )
    f.write ( '        toHide = 0;\n' )
    f.write ( '    }\n' )
    f.write ( '    if (toHide) {\n' )
    f.write ( '       tr.className = \'hiddenRow\';\n' )
    f.write ( '    }\n' )
    f.write ( '    else {\n' )
    f.write ( '        tr.className = \'\';\n' )
    f.write ( '    }\n' )
    f.write ( '}\n' )
    f.write ( '--></script>\n' )
    f.write ( '<a name=\'top\'>\n' )
    f.write ( '<div class=\'header\'><h1>Maniac Report - %s</h1>\n</div>\n' % timestamp )
    return


# html_summary_export
def html_summary_export ( journals, f ):
    jprogs = [ ] # a list is used to conserve order
    plans = [ ]
    idx = { }
    n = 0

    for j in journals:
        if ( j.prog not in idx ):
            idx[j.prog] = n
            jprogs.append ( [ j ] )
            n = n + 1
        else:
            jprogs[idx[j.prog]].append ( j )

    for j in jprogs[0]:
        plans.append ( j.plan )

    f.write ( '<div class=\'info\'>\n' )
    f.write ( '<pre>' )
    l = 'maniac '
    for i in range ( 1, len(sys.argv) ):
        l = l + sys.argv[i] + ' '
        if ( len(l) > 40 ):
            if ( i == len(sys.argv)-1 ):
                f.write ( l )
            else:
                f.write ( l+'\\\n' )
            l = '       '
    if ( l != '       ' ):
        f.write ( l )
    f.write ( '</pre><br/></div>\n' )
    f.write ( '<div class=\'summary\'>\n' )
    f.write ( '<p class=\'section\'><strong>Summary:</strong></p>\n' )
    f.write ( '<table id=\'summary_table\'>\n' )
    f.write ( '<colgroup><col/>' )
    for j in jprogs[0]:
        f.write ( '<col/>' )
    f.write ( '</colgroup>\n' )
    f.write ( '<tr id=\'header_row\'>\n' )
    f.write ( '    <td align=\'center\'><div class=\'headcell\'></div></td>\n' )
    n = 0
    for j in jprogs[0]:
        f.write ( '    <td align=\'center\'><div class=\'headcell\'>%s</div></td>\n' % j.plan.name )
        n = n + 1
    f.write ( '</tr>\n' )
    for jp in jprogs:
        f.write ( '<tr>\n' )
        f.write ( '    <td align=\'center\'><div class=\'progcell\'>%s</div></td>\n' % jp[0].prog.name )
        for j in jp:
            cl = 'succplan'
            txt = 'success'
            if ( j.has_failed() ):
                cl = 'failplan'
                txt = 'failure'
            elif ( j.has_warned() ):
                cl = 'warnplan'
                txt= 'warning'
            f.write ( '    <td align=\'center\' class=\'%s\'><div><a class=\'link\' href="#%d">%s</a></div></td>\n' % (cl,j.uid,txt) )
        f.write ( '</tr>\n' )
    f.write ( '</table>\n' )
    f.write ( '</div>\n' )
    return


# html_footer_export
def html_footer_export ( f ):
    f.write ( '<div id=\'footer\'>&nbsp;</div>\n' )
    f.write ( '</body>\n</html>\n' )
    return


# html_journals_export
def html_journals_export ( fname, journals ):
    f = file ( fname, 'w' )
    html_header_export ( f )
    html_summary_export ( journals, f )
    for j in journals:
        f.write ( '<br/>&nbsp;<br/><hr class=\'separator\'><br/>\n' )
        j.produce_html ( f )
    f.write ( '<br/>&nbsp;<br/><hr class=\'separator\'><br/>\n' )
    html_footer_export ( f )
    f.close ( )
    return



# csv_timings_export
def csv_timings_export ( f, prog, journals ):
    timing_journals = [ ]
    for j in journals:
        if ( j.prog != prog ):
            continue
        if ( j.has_events(event.TIME_VARIANT) ):
            timing_journals.append ( j )
    if ( len(timing_journals) == 0 ):
        return
    f.write ( '\033[1m%s\033[0m TIMINGS SUMMARY\n' % prog.name )
    for v in timing_journals[0].plan.variants:
        f.write ( '%s ' % v.name )
    f.write ( '\n' )
    for j in timing_journals:
        j.produce_csv_timings ( f )
    f.write ( '\n' )
    return



# maniac
def maniac ( mania_fname=None, dirs=None, plannames_list=None, nogen='false', numrpt=1, output=None ):
    if ( ( dirs == None ) or ( len(dirs) == 0 ) ):
        dirs = [ os.curdir ]
    
    manias = xml_mania_import ( mania_fname, dirs )
    journals = [ ]

    sys.stdout.write ( '\n' )
    sys.stdout.flush ( )

    for m in manias:
        generators = manias[m][0]
        db_variants = manias[m][1]
        plans = manias[m][2]

        # create builtin generators
        if ( 'none' not in generators ):
            generators['none'] = generator_none ( db_variants )

        if ( 'copy' not in generators ):
            generators['copy'] = generator_copy ( db_variants )

        # create builtin variants
        if ( 'ref' not in db_variants ):
            db_variants['ref'] = variant ( 'ref', 'none' )

        # create builtin plans
        if ( 'ref' not in plans ):
            plans['ref'] = plan_ref ( nogen, [db_variants[v] for v in db_variants] )
        elif ( len(plans['ref'].variants) == 0 ):
            plans['ref'].variants = [db_variants[v] for v in db_variants]
    
        if ( 'clean' not in plans ):
            plans['clean'] = plan_clean ( [db_variants[v] for v in db_variants] )
        elif ( len(plans['clean'].variants) == 0 ):
            plans['clean'].variants = [db_variants[v] for v in db_variants]
    
        # make list of plans to-be-followed
        if ( plannames_list == None ):
            plannames_list = [ ]

        plans_list = [ ]
        if ( len(plannames_list) == 0 ):
            for p in plans:
                if ( plans[p].default ):
                    plans_list.append ( plans[p] )
        else:
            for p in plannames_list:
                try:
                    plans_list.append ( plans[p] )
                except:
                    print ( 'maniac: error: no such plan as \'%s\'.' % p )
    
            if ( len(plans_list) == 0 ):
                print ( 'maniac: error: empty plan list.\n' )
                sys.exit ( -1 )

        # follow specified plans
        progs = [ ]
        local_journals = [ ]
        last_plan = None

        for d in dirs:
            if ( ( '.' not in manias ) and ( d != m ) ): # if no default mania and not current one, skip d
                continue
            name = os.path.basename ( os.path.normpath(d) )
            if ( not os.path.isdir(d) ):
                print ( 'maniac: skipping invalid program directory \'%s\'.\n'%d )
                continue
            prog = xml_program_import ( os.path.join(d,mania_xml_file) )
            progs.append ( prog )

            for p in plans_list:
                for n in range ( numrpt ):
                    j = p.follow ( d, prog, generators, last_plan )
                    j.produce ( sys.stdout )
                    journals.append ( j )
                    local_journals.append ( j )
                    if ( not j.generation_failed() ):
                        last_plan = (p.name,d)

            sys.stdout.write ( '\n' )

        for prog in progs:
            csv_timings_export ( sys.stdout, prog, local_journals )

    if ( output != None ):
        html_journals_export ( output, journals )

    sys.exit ( 0 )


# MAIN
if ( __name__ == '__main__' ):
    # parse command line
    options = 'hGm:n:o:v'
    long_options = [ 'help', 'nogen', 'numrpt', 'mania', 'output', 'version' ]
    
    try:
        opts, args = getopt.gnu_getopt ( sys.argv[1:], options, long_options )
    except getopt.GetoptError as e:
        print ( str(e) )
        print_usage ( )
        sys.exit ( 2 )

    # defaults
    nogen = 'false'
    numrpt = 1
    mania_fname = None
    output = None
    plannames_list = [ ]
    dirnames_list = [ ]

    # process options
    for opt, val in opts:
        if opt in ('-h','--help'):
            print_usage ( )
            sys.exit ( 0 )
        elif opt in ('-G', '--nogen'):
            nogen = 'true'
        elif opt in ('-n', '--num'):
            numrpt = int(val)
            numrpt = max ( 1, numrpt )
        elif opt in ('-m', '--mania'):
            mania_fname = val
        elif opt in ('-o','--output'):
            output = val
        elif opt in ('-v','--version'):
            print ( '\nmaniac version %s\n\n%s\n' % (version(),copyright()) )
            sys.exit ( 0 )
        else:
            assert False, 'unhandled option'
            print_usage ( )
            sys.exit ( -1 )

    # distinguish plan and directory names
    for a in args:
        if ( os.path.exists(a) ):
            dirnames_list.append ( a )
        else:
            plannames_list.append ( a )

    # call maniac
    maniac ( mania_fname, dirnames_list, plannames_list, nogen, numrpt, output )
