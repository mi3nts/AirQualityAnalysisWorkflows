#!/bin/bash
echo "Copying files..."
grib_copy -w count=585/586 /data/test.grb2 /data/output_u_v_combined.grb2
echo "All done!"