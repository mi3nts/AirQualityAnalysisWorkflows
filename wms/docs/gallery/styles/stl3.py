"""
Soil temperature level 3
=============================

The metadata used to detect the styles are :  

.. list-table::  
     :widths: 25 25 

     * - **paramId**
       - 183  
     * - **shortName**
       - stl3  


 

Default style: 
--------------
**Contour shade (Range: -72 / 72)** \[sh_all_fM72t72i4]  

.. image:: /_static/styles/stl3-sh_all_fM72t72i4.png  
    :width: 400

Other available styles:
-----------------------

**Contour shade (Range: -72 / 72)** \[sh_all_fM72t72i4]

.. image:: /_static/styles/stl3-sh_all_fM72t72i4.png  
    :width: 400
    
 

"""


from Magics import macro as magics

output = magics.output(output_formats = ['png'],
                output_name_first_page_number = "off",
                output_name = "stl3")

 

data =  magics.mgrib(grib_input_file_name = "stl3.grib")
        
contour = magics.mcont(contour_automatic_setting="style_name",
                        contour_style_name= "sh_all_fM72t72i4",)
        
coastlines = magics.mcoast(map_grid = "off" )
        
magics.plot(output, data, contour, coastlines)

# sphinx_gallery_thumbnail_path = '_static/styles/stl3-sh_all_fM72t72i4.png'

