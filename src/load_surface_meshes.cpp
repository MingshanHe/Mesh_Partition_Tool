#include "pipeline.hpp"

#include <cstdlib>
#include <boost/regex.hpp>
#include <string>
#include <boost/filesystem.hpp>
#include <yaml-cpp/yaml.h>

#include <CGAL/Polygon_mesh_processing/remesh.h>

// To avoid verbose function and named parameters call
using namespace boost::filesystem;
using namespace CGAL::parameters;
using namespace std;

const double target_edge_length = 4.0;   // arbitrary remesh edge length // move to inout commands

int load_surface_meshes(string in_dir, vector<Tissue> &tissues){
  path p (in_dir.c_str());
  try
  {
    if (!is_directory(p)){cout <<"[USER ERROR]: Input directory is not a directory\n";}
    else {
        cout <<"[PROGRAM INFORMATION]: Input is a directory containing:\n";
        // Store and Sort Paths
        typedef vector<path> vec;                                                                   
        vec v;
        copy(directory_iterator(p), directory_iterator(), back_inserter(v));
        sort(v.begin(), v.end());

        for (vec::const_iterator it (v.begin()); it != v.end(); ++it)                               // loop through input dir
        {
            cout << "[FILE INFORMATION]: " << it->filename().c_str() << "\n";                          // list files
            if(it->filename()=="tissues.yaml" ){                                                    // read "tissues.yaml" file
                std::ifstream input(it->c_str());
                // cout << "\n Reading a yaml file \n\n";
                YAML::Node config = YAML::LoadFile(it->c_str());
                for (size_t i=0 ;i<config.size();i++){
                    cout << "[YAML FILE INFORMATION]: Adding - ";
                    cout << config[i][0] << "\t";
                    cout << config[i][1] << "\n";
                    Tissue new_tissue;
                    new_tissue.name = config[i][0].as<string>();
                    new_tissue.YoungsModulus = config[i][1].as<int>();
                    std::vector<Mesh> temp_vec;
                    new_tissue.mesh_vec = temp_vec;
                    tissues.push_back(new_tissue);                                                  // push_back tissues
                    
                }
                cout << "[YAML FILE INFORMATION]: tissues.size() : "<< tissues.size() << "\n";
            }
        }                                          
        // Read *.off Files 
        for (vec::const_iterator file_it (v.begin()); file_it != v.end(); ++file_it)
        {                                                    
            if(file_it->extension()==".off"){     
                cout<<"[FILE INFORMATION]: Detected MESH File - "<<*file_it<<"\n";                                                  // if  *.off  load mesh
                std::ifstream input(file_it->c_str());
                Mesh  tmp_poly;
                input >> tmp_poly;
                // Find the propriate tissue name in Tissues vector and push back the mesh file in mesh_vec
                for(std::vector<Tissue>::iterator tissue_it = tissues.begin(); tissue_it != tissues.end(); ++tissue_it) {
                    std::string s = file_it->filename().c_str();
                    std::string e = ".*"+ tissue_it->name +".*";
                    cout << "[FILE INFORMATION]: s = " << s << "\t e = " << e << "\n";
                    if(substring_match(e,s)){                                                       // if regex tissue[].name  match  filename  
                        tissue_it->mesh_vec.push_back(tmp_poly);                                    // then copy mesh to this tissue
                        cout << tissue_it->name << "->mesh_vec.size() = " << tissue_it->mesh_vec.size() << "\n";
                    }
                }
            }else{
                cout << "[FILE INFORMATION]: Not Detected a .off file \t" << *file_it << "\n"; 
            }
        }
        cout << "[PROGRAM INFORMATION]: Finished Reading Mesh Files\n ";
    }
  }
    catch (const filesystem_error& ex)
  {
    cout << ex.what() << '\n';
  }
  
  cout << "[TISSUE INFORMATION]: tissues.size() = " << tissues.size() << "\n";
  cout << "[TISSUE INFORMATION]: tissues.begin()->name = " << tissues.begin()->name << "\n";
  cout << "[TISSUE INFORMATION]: tissues.begin()->mesh_vec.size() = " << tissues.begin()->mesh_vec.size() << "\n";

  return 0;
}
