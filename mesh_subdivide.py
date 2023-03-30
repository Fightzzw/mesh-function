def bat_mesh_subdivide():
    parser = argparse.ArgumentParser(description='mesh subdivide help document，同时执行loop和midpoint')
    parser.add_argument('-i', '--input_mesh_dir', type=str, help='输入mesh的目录，里面的mesh全部会subdivide')
    parser.add_argument('-o', '--output_dir', type=str, help='输出目录的路径')
    parser.add_argument('-r', '--iter', type=int, help='划分次数', default=3)

    args = parser.parse_args()

    if os.path.isdir(args.output_dir):
        # print('文件夹已存在')
        pass
    else:
        os.makedirs(args.output_dir)

    # list to store files
    mesh_file_list = ['elephant_overfit_f1000.obj']
    # # Iterate directory
    # for path in os.listdir(args.input_mesh_dir):
    #     # check if current path is a obj file
    #     if os.path.splitext(path)[-1] == ".obj":
    #         mesh_file_list.append(path)
    print('The following mesh will be subdivided.')
    print(mesh_file_list)
    for filename in mesh_file_list:
        file_path = os.path.join(args.input_mesh_dir, filename)
        base_mesh = o3d.io.read_triangle_mesh(file_path)
        base_mesh_filename = filename[:-4]
        print('Base mesh ' + filename + ' has [vertices: %d], [faces: %d]' % (
        len(base_mesh.vertices), len(base_mesh.triangles)))
        for i in range(args.iter):
            print('\t subdivide iteration process:', i)
            loop_mesh = base_mesh.subdivide_loop(i + 1)
            midpoint_mesh = base_mesh.subdivide_midpoint(i + 1)
            loop_mesh_out_path = args.output_dir + '/' + base_mesh_filename + '_loop' + str(i) + '.obj'
            midpoint_mesh_out_path = args.output_dir + '/' + base_mesh_filename + '_midpoint' + str(i) + '.obj'
            o3d.io.write_triangle_mesh(loop_mesh_out_path, loop_mesh)
            o3d.io.write_triangle_mesh(midpoint_mesh_out_path, midpoint_mesh)

def mesh_subdivide(input_path, output_path, iters = 2, subdivide_method = 'midpoint'):
    base_mesh = o3d.io.read_triangle_mesh(input_path)
    filename = os.path.basename(input_path)
    original_faces_num = len(base_mesh.triangles)
    print('Base mesh: ' + filename + ' has [vertices: %d], [faces: %d]' % (
        len(base_mesh.vertices), original_faces_num))

    output_mesh_path = ''

    if subdivide_method == 'midpoint':
        subdiv_mesh = base_mesh.subdivide_midpoint(iters)
        output_mesh_name  = filename[:-4] + '_mid' + str(iters)+'.obj'
        output_mesh_path = os.path.join(output_path, output_mesh_name)
        o3d.io.write_triangle_mesh(output_mesh_path, subdiv_mesh)
    elif subdivide_method == 'loop':
        subdiv_mesh = base_mesh.subdivide_loop(iters)
        output_mesh_name  = filename[:-4] + '_loop' + str(iters)+'.obj'
        output_mesh_path = os.path.join(output_path, output_mesh_name)
        o3d.io.write_triangle_mesh(output_mesh_path, subdiv_mesh)
    elif subdivide_method == 'butterfly':
        output_mesh_name = filename[:-4] + '_btf' + str(iters) + '.obj'
        output_mesh_path = os.path.join(output_path, output_mesh_name)
        btf_cmd = '/work/Users/zhuzhiwei/SubdivisionSurfaces-master/subdivide ' +\
                   input_path + ' ' + output_mesh_path + ' butterfly ' + str(iters)
        os.system(btf_cmd)
    elif subdivide_method == 'modified_butterfly':
        output_mesh_name = filename[:-4] + '_mbtf' + str(iters) + '.obj'
        output_mesh_path = os.path.join(output_path, output_mesh_name)
        mbtf_cmd = '/work/Users/zhuzhiwei/SubdivisionSurfaces-master/subdivide ' + \
                   input_path + ' ' + output_mesh_path + ' modified_butterfly ' + str(iters)
        os.system(mbtf_cmd)
    elif subdivide_method == 'neural_subdiv':
        output_mesh_name = filename[:-4] + '_nrsd' + str(iters) + '.obj'
        output_mesh_path = os.path.join(output_path, output_mesh_name)
        nrsd_cmd = '/work/Users/zhuzhiwei/anaconda3/envs/mesh_subdiv/bin/python ' \
                   '/work/Users/zhuzhiwei/neuralSubdiv-master/zzwtest.py ' \
                   '/work/Users/zhuzhiwei/neuralSubdiv-master/jobs/net_cartoon_elephant/ ' + \
                   input_path + ' ' + output_mesh_path + ' ' + str(iters)
        os.system(nrsd_cmd)
        mesh_scale(input_path, output_mesh_path)
    return output_mesh_path
