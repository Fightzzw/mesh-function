from scipy.spatial import cKDTree as KDTree
import numpy as np
import trimesh


def mesh_metric(gt_mesh_path, pred_mesh_path, vertex_num=500000):
    # gt_points, gt_indices = gt_mesh.sample(200000, return_index=True)
    gt_mesh = trimesh.load(gt_mesh_path)
    gt_points, gt_indices = trimesh.sample.sample_surface_even(gt_mesh, vertex_num)
    gt_points = gt_points.astype(np.float32)
    gt_normals = gt_mesh.face_normals[gt_indices]

    pred_mesh = trimesh.load(pred_mesh_path)
    pred_points, pred_indices = trimesh.sample.sample_surface_even(pred_mesh, vertex_num)
    pred_points = pred_points.astype(np.float32)
    pred_normals = pred_mesh.face_normals[pred_indices]

    gt_kdtree = KDTree(gt_points)
    dist_p2g, indices_p2g = gt_kdtree.query(pred_points)

    pred_kdtree = KDTree(pred_points)
    dist_g2p, indices_g2p = pred_kdtree.query(gt_points)

    # point to point distance
    D1 = max(np.mean(dist_p2g ** 2), np.mean(dist_g2p ** 2))

    # point to point average displacement
    absD = max(np.mean(np.abs(dist_p2g)), np.mean(np.abs(dist_g2p)))

    # Hausdorff distance
    H = max(np.max(dist_p2g), np.max(dist_g2p))

    # point to plane distance
    gt_points = np.array(gt_points)
    pred_points = np.array(pred_points)
    vector_p2g = pred_points - gt_points[indices_p2g]
    normals_p2g = gt_normals[indices_p2g]
    n_dist_p2g = np.abs(np.sum(vector_p2g * normals_p2g, axis=1)) / np.linalg.norm(normals_p2g, axis=1)

    vector_g2p = gt_points - pred_points[indices_g2p]
    normals_g2p = pred_normals[indices_g2p]
    n_dist_g2p = np.abs(np.sum(vector_g2p * normals_g2p, axis=1)) / np.linalg.norm(normals_g2p, axis=1)
    D2 = max(np.mean(n_dist_p2g ** 2), np.mean(n_dist_g2p ** 2))

    # return {'D1': D1, 'D2': D2, 'H': H, 'absD': absD}
    return [D1, D2, H, absD]
    
