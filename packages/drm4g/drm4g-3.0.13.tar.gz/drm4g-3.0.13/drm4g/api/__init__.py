#
# Copyright 2021 Santander Meteorology Group (UC-CSIC)
#
# Licensed under the EUPL, Version 1.1 only (the
# "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# http://ec.europa.eu/idabc/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
#

import logging
from os.path             import join, exists
from drm4g               import DRM4G_DIR_VAR
from drm4g.utils.command import exec_cmd

class Job( object ):
    """
    DRM4G job
    """
    args          = dict()
    template_file = None

    def set_name(self, job_name ):
        """
        A name for the job.

        @param job_name: Name of job
        @type  job_name: string
        """
        if isinstance( job_name, str ) :
            self.args[ 'NAME' ] = job_name
        else:
            raise Exception( 'Expected a string for job name' )


    def get_name(self):
        """
        Get job name
        """
        return self.args.get( 'NAME' )

    def set_executable(self, executable ):
        """
        The executable file

        @param executable: Executable
        @type  executable: string
        """
        if isinstance(executable, str ):
            self.args[ 'EXECUTABLE' ] =  executable
        else:
            raise Exception( 'Expected a string for executable' )


    def get_executable(self):
        """
        Get executable file
        """
        return self.args.get( 'EXECUTABLE' )

    def set_arguments(self, arguments ):
        """
        Arguments to the executable

        @param arguments: Executable arguments
        @type  arguments: string
        """
        if isinstance( arguments, str ):
            self.args[ 'ARGUMENTS' ] = arguments
        else:
            raise Exception( 'Expected a string for arguments' )

    def get_arguments(self):
        """
        Get executable arguments.
        """
        return self.args.get( 'ARGUMENTS' )

    def set_environment(self, environment):
        """
        User defined environment variables.

        @param environment: Executable arguments
        @type  environment: dictionary
        """
        if isinstance( environment, dict):
            self.args[ 'ENVIRONMENT' ] = environment
        else:
            raise Exception( 'Expected a dictionary for environment' )

    def get_environment(self):
        """
        Get environment variables.
        """
        return self.args.get( 'ENVIRONMENT' )

    def set_input_files(self, files):
        """
        Pair of "local remote" filenames. If the remote filename is missing,
        the local filename will be preserved in the execution host.

        @param files: Input sandbox files
        @type  files: String or list of strings
        """
        if isinstance( files, list):
            self.args[ 'INPUT_FILES' ] = files
        elif isinstance( files, str):
            self.args[ 'INPUT_FILES' ] = [files]
        else:
            raise Exception( 'Expected a string or a list for input files' )

    def get_input_files(self):
        """
        Get input files.
        """
        return self.args.get( 'INPUT_FILES' )

    def set_output_files(self, files):
        """
        Pair of remote filename local filename. If the local filename is missing,
        the remote filename will be preserved in the client host.

        @param files: Output sandbox files
        @type  files: String or list of strings
        """
        if isinstance( files, list):
            self.args[ 'OUTPUT_FILES' ] = files
        elif isinstance( files, str) :
            self.args[ 'OUTPUT_FILES' ] = [files]
        else:
            raise Exception( 'Expected a string or a list for input files' )

    def get_output_files(self):
        """
        Get output files.
        """
        return self.args.get( 'OUTPUT_FILES' )

    def set_stdin_file(self, stdin_file ):
        """
        Standard input file.

        @param stdin_file: input file
        @type  stdin_file: string
        """
        if isinstance( stdin_file, str):
            self.args[ 'STDIN_FILE' ] = stdin_file
        else:
            raise Exception( 'Expected a string for stdin file' )

    def get_stdin_file(self):
        """
        Get standard input file.
        """
        return self.args.get( 'STDIN_FILE' )

    def set_stdout_file(self, stdout_file ):
        """
        Standard output file.

        @param stdout_file: output file
        @type  stdout_file: string
        """
        if isinstance( stdout_file, str) :
            self.args[ 'STDOUT_FILE' ] = stdout_file
        else:
            raise Exception( 'Expected a string for stdout file' )

    def get_stdout_file(self):
        """
        Get standard output file.
        """
        return self.args.get( 'STDOUT_FILE' )

    def set_stderr_file(self, stderr_file ):
        """
        Standard error file.

        @param stderr_file: error file
        @type  stderr_file: string
        """
        if isinstance( stderr_file, str):
            self.args[ 'STDERR_FILE' ] = stderr_file
        else:
            raise Exception( 'Expected a string for error file' )

    def get_stderr_file(self):
        """
        Get standard error file.
        """
        return self.args.get( 'STDERR_FILE' )

    def set_requirements(self, requirements ):
        """
        A boolean expression evaluated for each host, if it
        is true the host will be considered to submit the job. Check the user or
        reference guide to know which variables and operators can be used.

        @param requirements: requirement expression
        @type  requirements: string
        """
        if isinstance( requirements, str):
            self.args[ 'REQUIREMENTS' ] = requirements
        else:
            raise Exception( 'Expected a string for requirements' )

    def get_requirements(self):
        """
        Get requirement expression.
        """
        return self.args.get( 'REQUIREMENTS' )

    def set_np(self, np ):
        """
        Number of process.

        @param np: number of process
        @type  np: string or integer
        """
        if isinstance( np, int):
            self.args[ 'NP' ] = str(np)
        elif isinstance( np, str):
            self.args[ 'NP' ] = np
        else:
            raise Exception( 'Expected a string or a ingeter for np' )

    def get_np(self):
        """
        Get number of process.
        """
        return self.args.get( 'NP' )

    def set_template_file(self, file ):
        """
        Set template file name.

        @param file: filename
        @type  file: string
        """
        if isinstance( file, str):
            self.template_file = file
        else :
            raise Exception( 'Expected a string for fime template' )

    def get_template_file(self):
        """
        Get template file.
        """
        if self.template_file :
            return self.template_file
        else :
            return './template.job'

    def create_template(self):
        """
        Create string template.
        """
        tmpstr = ''
        for key, val in list(self.args.items()) :
            if key == 'ENVIRONMENT':
                tmpstr = tmpstr + '%s = %s\n' % ( key, ','.join( "%s %s" % (k,v) for k,v in list(key.items()) ) )
            elif key in ( 'INPUT_FILES', 'OUTPUT_FILES' ):
                tmpstr = tmpstr + '%s = %s\n' % ( key, ','.join( val ) )
            else :
                tmpstr = tmpstr + "%s = %s\n" % ( key, val )
        return tmpstr

    def create_file(self, string_template ):
        """
        Create file template.
        """
        try :
            f = open( self.get_template_file() , 'w' )
        except :
            raise Exception( "Error creating file template %s" % self.get_template_file() )
        else :
            f.write( string_template )
            f.close()

class DRM4G( object ):
    """
    Class to intact with DRM4G
    """

    def submit(self, job, dep = [] , priority = 0, type_dep = "afterok" ):
        """
        Submit jobs.

        @param job_id: DRM4G job
        @type  job: object
        @param dep: job dependencies
        @type  dep: list
        @param priority: fixed priority
        @type  priority: integer
        @param type_dep: type of dependency : afterok, afterany and afternotok
        @type  type_dep: string
        """
        str_template  = job.create_template()
        job.create_file( str_template )
        depend = "-d %s -r %s" % ( ' '.join( dep ), type_dep ) if dep else ''
        cmd = "gwsubmit -p %d -v %s -t %s" % ( priority,
                                               depend,
                                               job.get_template_file() )
        code, out = exec_cmd( cmd )
        logging.debug( out )
        if code:
            raise Exception( out )
        job_id = int( out[ 8: ] )
        return job_id

    def get_log(self, job_id ):
        """
        Get log of a job.

        @param job_id: job identifier
        @type  job_id: integer
        """
        job_log = join(DRM4G_DIR_VAR , '%d00-%d99' % ( job_id/100, job_id/100 ), str( job_id ) , 'job.log' )
        if not exists( job_log ) :
            raise Exception( 'There is not a log available for this job.' )
        try :
            f = open( job_log, 'r' )
            return f.readlines()
        finally :
            f.close()

    def status(self, job_id):
        """
        Get job status

        @param job_id: job identifier
        @type  job_id: integer

        JID DM   EM   START    END      EXEC    XFER    EXIT HOST
        33  fail ---- 09:53:18 09:56:57 0:00:00 0:01:00 --   localmachine/fork
        """
        cmd = 'gwps -n -o setxh %d'  % ( job_id )
        code, out = exec_cmd( cmd )
        if code : raise Exception( "Error getting status for job %d" % job_id )
        header = [ 'DM', 'EM', 'START', 'END', 'EXEC', 'XFER', 'EXIT', 'HOST' ]
        return dict( ( key, val ) for key, val in zip( header, out.split() ) )

    def cancel(self, job_id, hard = False):
        """
        Cancel a job.

        @param job_id: job identifier
        @type  job_id: integer
        @param hard: asynchronous cancel option
        @type  hard: boolean
        """
        cmd = "gwkill %s %d" % ( '-9' if hard else '', job_id )
        code, out = exec_cmd( cmd )
        if code :
            raise Exception( "Error canceling job %d" % job_id )

    def set_priority(self, job_id, priority = 0):
        """
        Set fixed priority to a job.

        @param job_id: job identifier
        @type  job_id: integer
        @param priority: fixed priority
        @type  priority: integer
        """
        cmd = "gwkill -9 -p %d %d" % ( priority, job_id )
        code, out = exec_cmd( cmd )
        if code:
            raise Exception( "Error updating priority for job %d" % job_id )
