# Mesh Partition Tool
## Briefly Introduction
  This repository is used to mesh parts with different stiffness coefficient and properties. And the output file could be simulated in SOFA fraework, you could also think of it as the plugin.
## Build
1. git clone it
2. `mkdir build` and `cd build`
3. `cmake ..` to configure
4. `make -j` with your processor
5. `./mesh_partition_tool -i /home/brl/Mesh_Partition_Tool/input_files_dir/input_files_demo/  -o /home/brl/Mesh_Partition_Tool/output_files_dir/output_files_demo`
