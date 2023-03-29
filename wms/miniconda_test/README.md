Build the container via 
```bash
docker compose up --build -d 
```

To run the command, copy the test grib file from `/test-data` into the `/data` directory. 

To execute the `grib_copy` command, run 
```bash
docker compose run miniconda grib_copy -w count=585/586 /data/test.grb2 /data/output_u_v_combined.grb2
```
