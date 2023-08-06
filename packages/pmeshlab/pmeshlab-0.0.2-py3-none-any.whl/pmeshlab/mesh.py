import pymeshlab
from pymeshlab import Mesh as _Mesh
import numpy as np


class Mesh:
    def __init__(self, input):
        self._model = pymeshlab.MeshSet()
        if type(input) == str:
            self._model.load_new_mesh(input)
        elif type(input) == _Mesh:
            self._model.add_mesh(input)

    def connected_components(self):
        self._model.split_in_connected_components(delete_source_mesh=True)
        cmpts = []
        N = len(self._model)
        for k in range(N):
            try:
                cmpts.append(PyMeshLab(self._model[k]))
            except:
                pass
        return cmpts

    def show(self):
        return self.to_nmesh().show()

    def to_NMesh(self):
        from nmesh import NMesh
        from trimesh import Trimesh

        return NMesh(
            Trimesh(
                vertices=self.vertices(),
                faces=self.faces(),
                face_colors=self.face_colors(),
                vertex_colors=self.vertex_colors(),
            )
        )

    def vertices(self):
        return self._model[0].vertex_matrix()

    def faces(self):
        return self._model[0].face_matrix()

    def face_colors(self):
        return self._model[0].face_color_matrix()

    def vertex_colors(self):
        return self._model[0].vertex_color_matrix()

    def face_color(self):
        return self._model[0].face_color_matrix()[0]

    def discrete_curvatures(self):
        output = self._model.apply_filter(
            "compute_scalar_by_discrete_curvature_per_vertex"
        )
        return self, output

    def split_binary(self):
        self.discrete_curvatures()
        c0, c1, border = self.to_nmesh().split_binary()
        return c0.to_PyMeshLab(), c1.to_PyMeshLab(), border.to_PyMeshLab()

    @staticmethod
    def get_vertex_wn(file):
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(file)
        ms.apply_filter("compute_normals_for_point_sets")
        ms.normalize_vertex_normals()
        vertex_wn = np.concatenate(
            (ms[0].vertex_matrix(), ms[0].vertex_normal_matrix()), axis=1
        )
        return vertex_wn

    def export(self, *args, **kwargs):
        self.to_nmesh().export(*args, **kwargs)
