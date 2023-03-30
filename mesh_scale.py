import open3d as o3d
import argparse
import os

def mesh_normalize():
    parser = argparse.ArgumentParser(description='mesh normalize help document')
    parser.add_argument('-i', '--input_mesh_dir', type=str, help='输入mesh的目录，里面的mesh全部会normalize')
    parser.add_argument('-o', '--output_dir', type=str, help='输出目录的路径')

    args = parser.parse_args()

    if os.path.isdir(args.output_dir):
        print('文件夹已存在')
        pass
    else:
        os.makedirs(args.output_dir)

    # list to store files
    mesh_file_list = []
    # Iterate directory
    for path in os.listdir(args.input_mesh_dir):
        # check if current path is a obj file
        if os.path.splitext(path)[-1] == ".obj":
            mesh_file_list.append(path)
    print('The following mesh will be downsampled.')
    print(mesh_file_list)
    for filename in mesh_file_list:
        file_path = os.path.join(args.input_mesh_dir, filename)
        base_mesh = o3d.io.read_triangle_mesh(file_path)
        base_mesh_filename = filename[:-4]
        print('Base mesh ' + filename + ' has [vertices: %d], [faces: %d]' % (
        len(base_mesh.vertices), len(base_mesh.triangles)))
        min_bound = base_mesh.get_min_bound()
        max_bound = base_mesh.get_max_bound()
        scale_len = (max_bound - min_bound).max()

        vertices = base_mesh.vertices
        for v in range(len(vertices)):
            vertices[v] -= min_bound
            vertices[v] /= scale_len
        base_mesh.vertices = vertices

        normalize_mesh_out_path = args.output_dir + '/' + base_mesh_filename + '_normalize' + '.obj'
        o3d.io.write_triangle_mesh(normalize_mesh_out_path, base_mesh)

def bat_mesh_scale():

    parser = argparse.ArgumentParser(description='mesh scale help document')
    parser.add_argument('-i1', '--input_mesh_dir', type=str, help='输入mesh的目录，里面的mesh全部会scale')
    parser.add_argument('-i2', '--input_reference_mesh_dir', type=str, help='输入mesh的目录，里面的mesh全部会scale')
    parser.add_argument('-o', '--output_dir', type=str, help='输出目录的路径')

    args = parser.parse_args()

    if os.path.isdir(args.output_dir):
        print('文件夹已存在')
        pass
    else:
        os.makedirs(args.output_dir)

    # list to store files
    mesh_file_list = []
    # Iterate directory
    for path in os.listdir(args.input_mesh_dir):
        # check if current path is a obj file
        if os.path.splitext(path)[-1] == ".obj":
            mesh_file_list.append(path)
    print('The following mesh will be scaled.')
    print(mesh_file_list)
    for filename in mesh_file_list:
        # refer_file_name = filename.split("_")[0] + '_f1000.obj'
        refer_file_name = 'elephant_overfit_f1000.obj'
        refer_file_path = os.path.join(args.input_reference_mesh_dir, refer_file_name)
        refer_mesh = o3d.io.read_triangle_mesh(refer_file_path)

        file_path = os.path.join(args.input_mesh_dir, filename)
        base_mesh = o3d.io.read_triangle_mesh(file_path)
        # base_mesh_filename = filename[:-4]

        min_bound = refer_mesh.get_min_bound()
        max_bound = refer_mesh.get_max_bound()
        scale_len = (max_bound - min_bound).max()

        vertices = base_mesh.vertices
        for v in range(len(vertices)):

            vertices[v] *= scale_len
            vertices[v] += min_bound
        base_mesh.vertices = vertices

        scale_mesh_out_path = args.output_dir + '/' + filename
        o3d.io.write_triangle_mesh(scale_mesh_out_path, base_mesh)

def mesh_scale(refer_file_path, file_path):

    refer_mesh = o3d.io.read_triangle_mesh(refer_file_path)

    base_mesh = o3d.io.read_triangle_mesh(file_path)
    # base_mesh_filename = filename[:-4]

    min_bound = refer_mesh.get_min_bound()
    max_bound = refer_mesh.get_max_bound()
    scale_len = (max_bound - min_bound).max()

    vertices = base_mesh.vertices
    for v in range(len(vertices)):
        vertices[v] *= scale_len
        vertices[v] += min_bound
    base_mesh.vertices = vertices

    scale_mesh_out_path = file_path
    o3d.io.write_triangle_mesh(scale_mesh_out_path, base_mesh)
