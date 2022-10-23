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
    std::cout << "\nprog_opts() done\n" << std::endl;

    //// Imports
    load_surface_meshes(in_dir, tissues);
    std::cout << "\nload_surface_meshes() done" << std::endl;

    //// Polygon mesh processing ////
    // Generate subdomain meshes & patches
    generate_subdomain_meshes(tissues, subdomain_meshes, patch_vec, pair_vec, out_dir);  
    std::cout << "\ngenerate_subdomain_meshes() done" << std::endl;
   
    // Split disconnected patches into separate files. & update pair_vec
    //split_patches(patch_vec, pair_vec);
    mkvec_cc(patch_vec, pair_vec);
    std::cout << "\nmkvec_cc() done" << std::endl;


    // // 7 make partioned tetrahedral mesh
    make_partitioned_tet_mesh(patch_vec, pair_vec, edge_size, tet_mesh, out_dir);
    std::cout << "\nmake_partitioned_tet_mesh() done" << std::endl;


    return 0;
}
