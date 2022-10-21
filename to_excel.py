def dicom2excel(self, name_file, name_struct):
        """
        It creates DICOM contour in excelable form.
        The Contour Data for each organ is set on different sheets.
        The file is created in the same directory with the name name.xlsx
        INPUT:
        name_file -> str, with the name of the file.
        name_struct -> str, name of the structure for which the user want the excel file.
        OUTPUT:
        Excel file of the desired structure.
        """
        
        extension = '.xlsx'
        if name_file.endswith(extension):
            pass
        else:
            name_file = ''.join([name_file, extension])
        names = self.get_names()
        workbook = xlsxwriter.Workbook(name_file)
        merge_format = workbook.add_format({'align': 'center'})
        dicom_contour = self.dicom_struct.ROIContourSequence
        names = self.get_names()
        ind = -1 #int number, Index of the list names where the string name_struct is present
        n = "" #name_struct 
       
        for i in range(len(names)):
            if names[i]==name_struct:
                ind = i    
               
        worksheet = workbook.add_worksheet(name_struct)   
        dicom_contour = self.dicom_struct.ROIContourSequence[ind]   
        #print(len(dicom_contour.ContourSequence)) 11195
        
        for num in range(len(dicom_contour.ContourSequence)):
            contour = dicom_contour.ContourSequence[num].ContourData
            worksheet.merge_range(0, 3*num, 0, 3*num + 2,
                                      f'Contour {num + 1}', merge_format)
            worksheet.write_row(1, 3*num, ['x [mm]', 'y [mm]', 'z [mm]'])
           
            
            for count in range(int(len(contour)/3)):
                x = float(contour[3*count])
                y = float(contour[3*count+1])
                z = float(contour[3*count+2])
                worksheet.write_row(2+count, 3*num, [x, y, z])
                
                
        workbook.close()
