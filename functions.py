from PyQt4 import QtCore, QtGui
from subprocess import Popen, PIPE

import sys
import os
import string
import shutil
import glint
glint.load_plugin('core-gui')


class Commands():
    def send(self, program):

        if program == "maya":

            jobtitle = self.le_jobtitle_maya.text()
            currentfile = self.le_mayafile.text()
            cpu = self.te_cpus_maya.toPlainText()
            sframe = self.sb_sframe_maya.value()
            eframe = self.sb_eframe_maya.value()
            enablebatch = self.cb_enablebatch_maya.isChecked()
            ebvalue = self.sb_enablebatch_maya.value()

            outdir = self.le_outdir_maya.text()

            if self.cb_renderengine_maya.currentText() == "Mental Ray":
                engine = "mr"
            if self.cb_renderengine_maya.currentText() == "Software":
                engine = "sw"
            if self.cb_renderengine_maya.currentText() == "Hardware":
                engine = "hw"

            if not (jobtitle and currentfile and cpu and outdir):
                QtGui.QMessageBox.about(self, "Maya Incomplete Information",
                                        "Please complete job information.")
            else:
                if enablebatch:
                    command_options = "%s %s %s %s %s" % (program, engine,
                                                          outdir, "-batch",
                                                          ebvalue)
                else:
                    command_options = "%s %s %s" % (program, engine, outdir)

        if program == "blender":
            jobtitle = self.le_jobtitle_blender.text()
            currentfile = self.le_blenderfile.text()
            cpu = self.te_cpus_blender.toPlainText()
            sframe = self.sb_sframe_blender.value()
            eframe = self.sb_eframe_blender.value()
            enablebatch = self.cb_enablebatch_blender.isChecked()
            ebvalue = self.sb_enablebatch_blender.value()
            engine = self.cb_renderengine_blender.currentText()

            if not (jobtitle and currentfile and cpu):
                QtGui.QMessageBox.about(self, "Blender Incomplete Information",
                                        "Please complete job information.")
            else:
                if enablebatch:
                    command_options = "%s %s %s %s" % (program, engine,
                                                       "-batch", ebvalue)
                else:
                    command_options = "%s %s" % (program, engine)

        if program == "max":
            jobtitle = self.le_jobtitle_max.text()
            currentfile = self.le_maxfile.text()
            cpu = self.te_cpus_max.toPlainText()
            sframe = self.sb_sframe_max.value()
            eframe = self.sb_eframe_max.value()
            enablebatch = self.cb_enablebatch_max.isChecked()
            ebvalue = self.sb_enablebatch_max.value()
            outname = self.le_outname_max.text()

            if not (jobtitle and currentfile and cpu and maxtime and outdir):
                QtGui.QMessageBox.about(self, "3ds Max Incomplete Information",
                                        "Please complete job information.")
            else:
                if enablebatch:
                    command_options = "%s %s %s %s" % (program, outname,
                                                       "-batch", ebvalue)
                else:
                    command_options = "%s %s" % (program, outname)

        if program == "ae":
            jobtitle = self.le_jobtitle_ae.text()
            currentfile = self.le_aefile.text()
            cpu = self.te_cpus_ae.toPlainText()
            sframe = self.sb_sframe_ae.value()
            eframe = self.sb_eframe_ae.value()
            enablebatch = self.cb_enablebatch_ae.isChecked()
            ebvalue = self.sb_enablebatch_ae.value()
            outname = self.le_outdir_ae.text()
            compname = self.le_compname_ae.text()

            if not (jobtitle and currentfile and cpu and maxtime and outdir):
                QtGui.QMessageBox.about(self, "AE Incomplete Information",
                                        "Please complete job information.")
            else:
                if enablebatch:
                    command_options = "%s %s %s %s %s" % (program, compname,
                                                          outname, "-batch",
                                                          ebvalue)
                else:
                    command_options = "%s %s %s" % (program, compname, outname)
        # --create job dir--
        jobdir = '%s%s' % ('//viz_fx_server/renderfarm/jobs/', jobtitle)
        joblog = '%s%s' % (jobdir, '/log')
        os.mkdir(jobdir)
        os.mkdir(joblog)

        # --copy/duplicate to job dir
        print currentfile
        print jobdir

        shutil.copy("%s" % (currentfile), "%s" % (jobdir))
        # --copied file directory
        basename = os.path.basename("%s" % (currentfile))
        copiedfile = '%s/%s' % (jobdir, basename)
        copiedrenamed = copiedfile.replace('/', '\\\\')

        in_frame = str('%d-%d' % (sframe, eframe))
        in_engine = str('%s' % (engine))
        in_cpu = str('%s' % (cpu))
        in_title = str('%s' % (jobtitle))
        in_comm = 'echo command //viz_fx_server/Tools/deploy/scripts/standalone_render.bat'
        cmdline = '%s %s %s' % (in_comm, command_options, copiedrenamed)

        submit = Popen('rush -submit gollum'.split(), stdin=PIPE, stdout=PIPE)
        submit.stdin.write('ram 100\n')
        submit.stdin.write('title %s\n' % in_title)
        submit.stdin.write('logdir %s\n' % joblog)
        submit.stdin.write('cpus %s\n' % in_cpu)
        submit.stdin.write('command %s\n' % cmdline)

        # if batch render is on, then: else single render
        if enablebatch:
            submit.stdin.write('frames %s,%s\n' % (in_frame, ebvalue))

        else:
            submit.stdin.write('frames %s\n' % in_frame)
        out, err = submit.communicate()
        self.SendComplete()

    def SendComplete(self):
        QtGui.QMessageBox.about(self, "File Sent", "Job Sent to Farm!")

    def DirDialog(self, filetype):
        select = "%s%s %s" % ("Select ", filetype, "file")

        if filetype == "maya":
            dialog_type_query = "Maya File (*.ma *.mb)"
            filename = QtGui.QFileDialog.getOpenFileName(self, select,
                                                         "c:\\",
                                                         dialog_type_query)
            self.le_mayafile.setText(filename)

        if filetype == "blender":
            dialog_type_query = "Blend File (*.blend)"
            filename = QtGui.QFileDialog.getOpenFileName(self, select,
                                                         "c:\\",
                                                         dialog_type_query)
            self.le_blenderfile.setText(filename)

        if filetype == "max":
            dialog_type_query = "Max File (*.max)"
            filename = QtGui.QFileDialog.getOpenFileName(self, select,
                                                         "c:\\",
                                                         dialog_type_query)
            self.le_maxfile.setText(filename)

        if filetype == "ae":
            dialog_type_query = "AE File (*.aep)"
            filename = QtGui.QFileDialog.getOpenFileName(self, select,
                                                         "c:\\",
                                                         dialog_type_query)
            self.le_aefile.setText(filename)

    def OutDialog(self, filetype):
        if filetype == "max":
            cmd_txt = "Save Output Name"
            output_format = "Images (*.png *.tif *iff *.jpg)"
            filename = QtGui.QFileDialog.getSaveFileName(self, cmd_txt,
                                                         "c:\\",
                                                         output_format)
            self.le_outname_max.setText(filename)

        if filetype == "maya":

            cmd_txt = "Select Output Folder Directory"
            filename = QtGui.QFileDialog.getExistingDirectory(self, cmd_txt)
            self.le_outdir_maya.setText(filename)

        if filetype == "ae":

            cmd_txt = "Save Output Name"
            video_format = "Video Format (*.avi *.mp4 *.mov *tif *.jpg *.png)"
            filename = QtGui.QFileDialog.getSaveFileName(self, cmd_txt,
                                                         "c:\\", video_format)
