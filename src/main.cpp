#include "pipeline.hpp"


int main(int argc, char* argv[])
{

    string in_dir, out_dir;
    //Mesh_criteria mesh_criteria;
    float edge_size;
    std::vector<Tissue> tissues;
    std::vector<Tissue> subdomain_meshes;                     // nb these are all surface meshes
    vector<Mesh> patch_vec;
    vector<std::pair<int, int> >  pair_vec;
    C3t3 tet_mesh;
    
    //// Program options 
    prog_opts(argc, argv, &in_dir, &out_dir, &edge_size);
    std::cout << "\n[PROGRAM INFORMATION]: Program Options Done -prog_opts()\n" << std::endl;

    //// Imports
    load_surface_meshes(in_dir, tissues);
    std::cout << "\n[PROGRAM INFORMATION]: Load Mesh File Done -load_surface_meshes()\n" << std::endl;

    //// Polygon mesh processing ////
    // Generate subdomain meshes & patches
    generate_subdomain_meshes(tissues, subdomain_meshes, patch_vec, pair_vec, out_dir);  
    std::cout << "\n[PROGRAM INFORMATION]: Generate Subdomain Meshes Done -generate_subdomain_meshes()\n" << std::endl;
   
    // Split disconnected patches into separate files. & update pair_vec
    //split_patches(patch_vec, pair_vec);
    mkvec_cc(patch_vec, pair_vec);
    std::cout << "\n[PROGRAM INFORMATION]: Split Disconnected Patches into Separate Files -mkvec_cc()\n" << std::endl;


    // // 7 make partioned tetrahedral mesh
    make_partitioned_tet_mesh(patch_vec, pair_vec, edge_size, tet_mesh, out_dir);
    std::cout << "\n[PROGRAM INFORMATION]: Make Partioned Tetrahedral Mesh Done -make_partitioned_tet_mesh()" << std::endl;


    return 0;
}
