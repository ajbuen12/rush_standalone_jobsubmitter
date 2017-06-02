class DialogBox():

    def SendComplete(self):
        QtGui.QMessageBox.about(self, "File Sent", "Job Sent to Farm!")

    def DirDialog(self, filetype):
        select = "%s%s%s" % ("Select ", filetype, " file")

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
            output_format = "Video Format (*.avi *.mp4 *.mov *tif *.jpg *.png)"
            filename = QtGui.QFileDialog.getSaveFileName(self, cmd_txt,
                                                         "c:\\",
                                                         output_format)
