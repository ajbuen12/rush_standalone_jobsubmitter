import sys
import os
import string
import shutil

from subprocess import Popen, PIPE

from PyQt4 import QtCore, QtGui

class Commands():

    def send(self, program):

        #----SAME COMPONENTS----#
        jobtitle = "%s%s%s" % ("self.le_jobtitle_", program, ".text()")
        file = "%s%s%s" % ("self.le_", program, "file.text()")
        cpu = "%s%s%s" % ("self.te_cpus_", program, ".toPlainText()")
        sframe = "%s%s%s" % ("self.sb_sframe_", program, ".value()")
        eframe = "%s%s%s" % ("self.sb_eframe_", program, ".value()")
        enablebatch = "%s%s%s" % ("self.cb_enablebatch_", program, ".isChecked()")
        ebvalue = "%s%s%s" % ("self.sb_enablebatch_", program, ".value()")


        if program=="maya":



            if self.cb_renderengine_maya.currentText()=="Mental Ray":
                engine = "mr"
            if self.cb_renderengine_maya.currentText()=="Software":
                engine = "sw"
            if self.cb_renderengine_maya.currentText()=="Hardware":
                engine = "hw"

            if not (jobtitle and file and cpu and outdir):
                QtGui.QMessageBox.about(self, "Maya Incomplete Information", "Please complete job information.")
            else:
                if enablebatch:
                    command_options = "%s %s %s %s %s" % (program, engine, outdir, "-batch", ebvalue)
                else:
                    command_options = "%s %s %s" % (program, engine, outdir)



        if program=="blender":
            engine = self.cb_renderengine_blender.currentText()

            if not (jobtitle and file and cpu):
                QtGui.QMessageBox.about(self, "Blender Incomplete Information", "Please complete job information.")
            else:
                if enablebatch:
                    command_options = "%s %s %s %s" % (program, engine, "-batch", ebvalue)
                else:
                    command_options = "%s %s" % (program, engine)


        if program=="max":
            outname = self.le_outname_max.text()

            if not (jobtitle and file and cpu and maxtime and outdir):
                QtGui.QMessageBox.about(self, "3ds Max Incomplete Information", "Please complete job information.")
            else:
                if enablebatch:
                    command_options = "%s %s %s %s" % (program, outname, "-batch", ebvalue)
                else:
                    command_options = "%s %s" % (program, outname)



        if program=="ae":
            outname = self.le_outdir_ae.text()
            compname = self.le_compname_ae.text()

            if not (jobtitle and file and cpu and maxtime and outdir):
                QtGui.QMessageBox.about(self, "After Effects Incomplete Information", "Please complete job information.")
            else:
                if enablebatch:
                    command_options = "%s %s %s %s %s" % (program, compname, outname, "-batch", ebvalue)
                else:
                    command_options = "%s %s %s" % (program, compname, outname)

        #--create job dir--
        jobdir = '%s%s' % ('//viz_fx_server/renderfarm/jobs/', jobtitle)
        joblog = '%s%s' % (jobdir, '/log')
        os.mkdir(jobdir)
        os.mkdir(joblog)
        #--copy/duplicate to job dir
        currentfile = file
        shutil.copy(currentfile, jobdir)
        #--variables--
            #--copied file directory
        basename = os.path.basename(currentfile)
        copiedfile = '%s/%s' % (jobdir, basename)
        copiedrenamed = copiedfile.replace('/', '\\\\')
            #--frames
        in_frame = str('%d-%d' % (sframe, eframe))
        in_engine = str('%s' % (engine))
        in_cpu = str('%s' % (cpu))
        in_title = str('%s' % (jobtitle))
        cmdline = '%s %s %s' % ('echo command //viz_fx_server/Tools/deploy/scripts/blender_submit_cmd.bat', command_options, copiedrenamed)
        #--render submit --
        submit = Popen('rush -submit gollum'.split(), stdin=PIPE, stdout=PIPE)
        Popen('echo ram 100'.split(), stdout=submit.stdin)
        Popen('%s%s' % ('echo title ', in_title), stdout=submit.stdin)
        Popen('%s%s' % ('echo logdir ', joblog), stdout=submit.stdin)
        Popen('%s%s' % ('echo cpus ', in_cpu), stdout=submit.stdin)
        Popen(cmdline, stdout=submit.stdin)
        #if batch render is on, then: else single render
        if enablebatch:
            Popen('%s %s,%s' % ('echo frames', in_frame, ebvalue), stdout=submit.stdin)
        else:
            Popen('%s %s' % ('echo frames', in_frame), stdout=submit.stdin)
        self.SendComplete()


    def SendComplete(self):
        QtGui.QMessageBox.about(self, "File Sent", "Job Sent to Farm!")

    def DirDialog(self, filetype):
        select = "%s%s%s" %  ("Select ", filetype, " file")

        if filetype=="maya":
            dialog_type_query = "Maya File (*.ma *.mb)"
            filename = QtGui.QFileDialog.getOpenFileName(self, select, "c:\\", dialog_type_query)
            self.le_mayafile.setText(filename)

        if filetype=="blender":
            dialog_type_query = "Blend File (*.blend)"
            filename = QtGui.QFileDialog.getOpenFileName(self, select, "c:\\", dialog_type_query)
            self.le_blenderfile.setText(filename)

        if filetype=="max":
            dialog_type_query = "Max File (*.max)"
            filename = QtGui.QFileDialog.getOpenFileName(self, select, "c:\\", dialog_type_query)
            self.le_maxfile.setText(filename)

        if filetype=="ae":
            dialog_type_query = "AE File (*.aep)"
            filename = QtGui.QFileDialog.getOpenFileName(self, select, "c:\\", dialog_type_query)
            self.le_aefile.setText(filename)

    def OutDialog(self, filetype):

        if filetype=="max":

            filename  = QtGui.QFileDialog.getSaveFileName(self, "Save Output Name", "c:\\", "Images (*.png *.tif *iff *.jpg)")
            self.le_outname_max.setText(filename)

        if filetype=="maya":

            filename = QtGui.QFileDialog.getExistingDirectory(self, "Select Output Folder Directory")
            self.le_outdir_maya.setText(filename)

        if filetype=="ae":

            filename = QtGui.QFileDialog.getSaveFileName(self, "Save Output Name", "c:\\", "Video Format (*.avi *.mp4 *.mov *tif *.jpg *.png)")