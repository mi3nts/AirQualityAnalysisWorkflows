"""
Volumetric soil water layer 2
=============================

The metadata used to detect the styles are :  

.. list-table::  
     :widths: 25 25 

     * - **paramId**
       - 40  
     * - **shortName**
       - swvl2  


 

Default style: 
--------------
**Contour shade (Level list : (0./0.1/0.2/0.3/0.4/0.5/0.6/0.7/0.8/0.9/1)** \[sh_all_f0t1lst]  

.. image:: /_static/styles/swvl2-sh_all_f0t1lst.png  
    :width: 400

Other available styles:
-----------------------

**Contour shade (Level list : (0./0.1/0.2/0.3/0.4/0.5/0.6/0.7/0.8/0.9/1)** \[sh_all_f0t1lst]

.. image:: /_static/styles/swvl2-sh_all_f0t1lst.png  
    :width: 400
    
 

"""


from Magics import macro as magics

output = magics.output(output_formats = ['png'],
                output_name_first_page_number = "off",
                output_name = "swvl2")

 

data =  magics.mgrib(grib_input_file_name = "swvl2.grib")
        
contour = magics.mcont(contour_automatic_setting="style_name",
                        contour_style_name= "sh_all_f0t1lst",)
        
coastlines = magics.mcoast(map_grid = "off" )
        
magics.plot(output, data, contour, coastlines)

# sphinx_gallery_thumbnail_path = '_static/styles/swvl2-sh_all_f0t1lst.png'

