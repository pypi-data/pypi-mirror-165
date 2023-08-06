import re
import numpy as np

from itertools import product, combinations


def cosine(u, v):
    '''Pure NumPy analog of scipy.spatial.distance.cosine'''
    return 1 - np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


class RubiksSnake:
    POINTS_PER_UNIT = 6
    TRIANGLES_PER_UNIT = 4
    DEFAULT_COLORS = [
        [0, 'blue'],
        [1, 'white'],
    ]
    
    def __init__(self, n_segments=24, color_scale=DEFAULT_COLORS, segment_colors=None, initial_state=None):
        '''
        Class for modeling, visualizing and studying the Rubik's Snake        
        '''
        self.n_segments = n_segments
        self.state = np.zeros(n_segments - 1, dtype=np.uint8)
        self.conformation = np.zeros((n_segments, 6, 3), dtype=np.int16)
        self.color_scale = color_scale
        
        if segment_colors is None:
            self.colors = np.tile([0,1], n_segments // 2)[:n_segments]
        else:
            self.colors = np.array(segment_colors)
        
        if initial_state is None:
            self.compute_conformation()
        else:
            self.assemble_by_formula(initial_state)
            
        
    def interference_check(self):
        cells = self.conformation.min(axis=1)
        lower_bounds = cells.min(axis=0)
        grid_shape = cells.max(axis=0) - lower_bounds + 1
        grid = -np.ones(grid_shape, dtype=np.int16)
        interference_candidates = {}
        for i in range(cells.shape[0]):
            x, y, z = cells[i] - lower_bounds
            if grid[x, y, z] >= 0:
                interference_candidates[(x, y, z)] = interference_candidates.get((x, y, z), [grid[x, y, z]]) + [i]
            else:
                grid[x, y, z] = i

        interferences = []
        for points in interference_candidates.values():
            if len(points) > 2:
                interferences.append(points)
                continue

            a, b = points
            p2a, p3a = self.conformation[a, [2,3]]
            p2b, p3b = self.conformation[b, [2,3]]

            ridge_a, ridge_b = p3a - p2a, p3b - p2b

            is_collinear = (ridge_a == ridge_b).all()
            is_anticollinear = (ridge_a == -ridge_b).all()
            if not (is_collinear or is_anticollinear):
                interferences.append(points)
                continue

            if ((is_collinear and np.abs(p2a - p2b).sum() < 2)
                or (is_anticollinear and np.abs(p2a - p3b).sum() < 2)):
                interferences.append(points)

        self.interferences = interferences
        return bool(interferences)
    
        
    def assemble_by_formula(self, formula):
        formula_unit = re.compile(r'(\d+)([RL])(\d)')
        formula_parsed = [formula_unit.match(unit).groups() for unit in formula.split('-')]
        for segment, side, rotation in formula_parsed:
            segment, rotation = map(int, (segment, rotation))
            i = (segment - 1) * 2
            if side == 'R':
                self.state[i] = rotation
            elif side == 'L':
                self.state[i-1] = -rotation % 4
                
        self.compute_conformation()
        
        
    def compute_conformation(self):
        self.conformation[0] = [
            [0, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 0],
        ]

        for i in range(self.n_segments - 1):
            
            p0, p1, p2, p3, p4, p5 = self.conformation[i] # prev state
            offset = p2 - p4
            
            if self.state[i] == 0:
                self.conformation[i+1] = [
                    p1 + offset,
                    p0 + offset,
                    p1,
                    p0,
                    p3,
                    p2,
                ]
            elif self.state[i] == 1:
                self.conformation[i+1] = [
                    p3 + offset,
                    p1 + offset,
                    p3,
                    p1,
                    p2,
                    p0,
                ]
            elif self.state[i] == 2:
                self.conformation[i+1] = [
                    p2 + offset,
                    p3 + offset,
                    p2,
                    p3,
                    p0,
                    p1,
                ]
            elif self.state[i] == 3:
                self.conformation[i+1] = [
                    p0 + offset,
                    p2 + offset,
                    p0,
                    p2,
                    p1,
                    p3,
                ]
            else:
                raise Exception
                
        if self.interference_check():
            print(f'WARNING! Self-intersection detected between segments {self.interferences}')
        
        
    def get_triangulation(self):
        triangles_per_unit = self.TRIANGLES_PER_UNIT
        points_per_unit = self.POINTS_PER_UNIT
        
        unit_triangles = np.array([
            [0, 2, 4],
            [1, 3, 5],
            [0, 1, 4],
            [1, 4, 5],
        ], dtype=np.uint16)
        unit_cap_start = np.array([
            [2, 3, 4],
            [3, 4, 5],
        ], dtype=np.uint16)
        unit_cap_end = np.array([
            [0, 1, 2],
            [1, 2, 3],
        ], dtype=np.uint16)
        assert unit_triangles.shape[0] == triangles_per_unit
        
        triangles = []
        for i in range(self.n_segments):
            triangles.append(unit_triangles + i*points_per_unit)
            
        triangles.append(unit_cap_start)
        triangles.append(unit_cap_end + i*points_per_unit)
            
        return self.conformation.reshape(-1,3), np.vstack(triangles)
    
    
    def get_intersecting_volume(self, i, j):
        
        def get_plane_norm(unit):
            p0, p1, p2, p3, p4, p5 = unit.astype(np.float64)
            ridge = p3 - p2
            visor = p4 - p0
            plane_norm = np.cross(ridge, visor)
            return plane_norm

        def get_horns(unit):
            p0, p1, p2, p3, p4, p5 = unit.astype(np.float64)
            ridge = p3 - p2
            slope_1, slope_2 = p0 - p2, p2 - p4
            return np.cross(ridge, slope_1), np.cross(ridge, slope_2)
        
        norm_i, norm_j = get_plane_norm(self.conformation[i]), get_plane_norm(self.conformation[j])
        interference_type = cosine(norm_i, norm_j)
        
        if np.isclose(interference_type, 0.0):    # full match cos_nn = 0
            intersection = self.conformation[i]

            unit_triangles = np.array([
                [0, 2, 4],
                [1, 3, 5],
                [0, 1, 4],
                [1, 4, 5],
                [0, 1, 2],
                [1, 2, 3],
                [2, 3, 4],
                [3, 4, 5],
            ], dtype=np.uint16)
            
            edge_bypass = [0, 1, 3, 2, 0, 4, 5, 1, 3, 5, 4, 2]
            edges = intersection[edge_bypass]
        
        elif np.isclose(interference_type, 0.5):    # big prism cos_nn = 0.5
            horns_i = get_horns(self.conformation[i])
            horns_j = get_horns(self.conformation[j])
            for n, m in product((0, 1), (0, 1)):
                if np.isclose(cosine(horns_i[n], horns_j[m]), 0):
                    break

            if n == 0:
                bottom = self.conformation[i, :4]
                p4i, p5i = self.conformation[i, 4:]
                if m == 0:
                    p4j, p5j = self.conformation[j, 4:]
                    vertex = p4i if np.isclose(p4i, p5j).all() else p5i
                else:
                    p0j, p1j = self.conformation[j, :2]
                    vertex = p4i if np.isclose(p4i, p0j).all() else p5i
            else:
                bottom = self.conformation[i, 2:]
                p0i, p1i = self.conformation[i, :2]
                if m == 0:
                    p4j, p5j = self.conformation[j, 4:]
                    vertex = p0i if np.isclose(p0i, p5j).all() else p1i
                else:
                    p0j, p1j = self.conformation[j, :2]
                    vertex = p0i if np.isclose(p0i, p1j).all() else p1i

            (p0, p1, p2, p3), p4 = bottom, vertex
            intersection = np.vstack((p0, p1, p2, p3, p4))

            unit_triangles = np.array([
                [0, 1, 2],
                [1, 2, 3],
                [0, 1, 4],
                [1, 3, 4],
                [2, 3, 4],
                [0, 2, 4],
            ], dtype=np.uint16)
            
            edge_bypass = [0, 1, 3, 2, 0, 4, 2, 3, 4, 1]
            edges = intersection[edge_bypass]
            
        elif np.isclose(interference_type, 1.0):    # "roof" (extra points required) cos_nn = 1
            vert_1 = self.conformation[i, 2] + norm_i/2
            vert_2 = self.conformation[i, 3] + norm_i/2
            
            horns_i = get_horns(self.conformation[i])
            horns_j = get_horns(self.conformation[j])
            for n, m in product((0, 1), (0, 1)):
                if np.isclose(cosine(horns_i[n], horns_j[m]), 0):
                    break
                    
            if n == 0:
                bottom = self.conformation[i, :4]
            else:
                bottom = self.conformation[i, 2:]
                
            (p0, p1, p2, p3), p4, p5 = bottom, vert_1, vert_2
            intersection = np.vstack((p0, p1, p2, p3, p4, p5))
            
            unit_triangles = np.array([
                [0, 2, 4],
                [1, 3, 5],
                [0, 1, 4],
                [1, 4, 5],
                [0, 1, 2],
                [1, 2, 3],
                [2, 3, 4],
                [3, 4, 5],
            ], dtype=np.uint16)
            
            edge_bypass = [0, 1, 3, 2, 0, 4, 5, 1, 3, 5, 4, 2]
            edges = intersection[edge_bypass]
        
        elif np.isclose(interference_type, 1.5):    # small prism cos_nn = 1.5
            p0i, p1i, p2i, p3i, p4i, p5i = self.conformation[i]
            ridge_i = p3i - p2i, p2i - p3i
            vert_ax_i = p3i - p5i
            horns_j = get_horns(self.conformation[j])
            for n, m in product((0, 1), (0, 1)):
                if np.isclose(cosine(ridge_i[n], horns_j[m]), 0):
                    break
                    
            m = (m + 1) % 2
            cos_dist = cosine(vert_ax_i, horns_j[m])
            if n == 0:
                if np.isclose(cos_dist, 1):
                    p0, p1, p2, p3 = p1i, p3i, p5i, p0i
                elif np.isclose(cos_dist, 2):
                    p0, p1, p2, p3 = p1i, p3i, p5i, p4i
                else:
                    raise Exception
            else:
                if np.isclose(cos_dist, 1):
                    p0, p1, p2, p3 = p0i, p2i, p4i, p1i
                elif np.isclose(cos_dist, 2):
                    p0, p1, p2, p3 = p0i, p2i, p4i, p5i
                else:
                    raise Exception
                
            intersection = np.vstack((p0, p1, p2, p3))
            
            unit_triangles = np.array([
                [0, 1, 2],
                [0, 1, 3],
                [1, 2, 3],
                [0, 2, 3],
            ], dtype=np.uint16)
            
            edge_bypass = [0, 1, 2, 0, 3, 1, 2, 3]
            edges = intersection[edge_bypass]
        
        elif np.isclose(interference_type, 2.0):    # no intersection cos_nn = 2
            return None, None, None
            
        else:
            raise Exception

        return intersection, unit_triangles, edges
    
    
    def get_edges(self):
        edge_bypass = [0, 1, 3, 2, 0, 4, 5, 1, 3, 5, 4, 2]
        edges = [unit[edge_bypass].T for unit in self.conformation]
        return edges
    
    
    def get_triangle_colors(self):
        colors = np.tile(self.colors, (self.TRIANGLES_PER_UNIT,1)).T.flatten()
        cap_colors = [self.colors[0]]*2 + [self.colors[-1]]*2
        return np.hstack((colors, cap_colors))
    
    
    def get_plot_ranges(self):
        DELTA = 0.2
        
        coords = self.conformation.reshape(-1,3)
        min_c = coords.min(axis=0)
        max_c = coords.max(axis=0)
        mean_c = (max_c + min_c) / 2
        max_range = (max_c - min_c).max() + DELTA
        lower_bounds = mean_c - max_range/2
        upper_bounds = mean_c + max_range/2
        return np.vstack((lower_bounds, upper_bounds)).T
        
    
    def plot_3d(self, figsize=(800, 800), 
                allow_self_intersection=True, 
                visualize_interferences=True, 
                background_color='LightSteelBlue'):
        
        if not allow_self_intersection and self.interferences:
            return
        
        import plotly.graph_objects as go
        
        coordinates, triangles = self.get_triangulation()
        x, y, z = coordinates.T
        i, j, k = triangles.T
        mesh3d = go.Mesh3d(
            x=x, y=y, z=z,
            i=i, j=j, k=k,
            colorscale=self.color_scale,
            intensity=self.get_triangle_colors(),
            intensitymode='cell',
            opacity=1 if not self.interferences else 0.5,
            showscale=False,
        )
        
        mesh3d_intersections = []
        if visualize_interferences:
            
            for units in self.interferences:
                for i, j in combinations(units, 2):
                    coordinates, triangles, edges = self.get_intersecting_volume(i, j)
                    if coordinates is None:
                        continue

                    x, y, z = coordinates.T
                    i, j, k = triangles.T
                    mesh3d_intersections.append(go.Mesh3d(
                        x=x, y=y, z=z,
                        i=i, j=j, k=k,
                        color='lightpink',
                        opacity=0.9,
                    ))
                    x, y, z = edges.T
                    mesh3d_intersections.append(go.Scatter3d(
                        x=x, y=y, z=z,
                        mode='lines',
                        name='',
                        line=dict(color='red', width=8),
                    ))
        
        lines = [go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            name='',
            line=dict(color='black', width=8),
        ) for x, y, z in self.get_edges()]
        
        fig = go.Figure(data=[mesh3d] + lines + mesh3d_intersections)
        
        x_range, y_range, z_range = self.get_plot_ranges()
        width, height = figsize
        fig.update_layout(
            autosize=False,
            width=width,
            height=height,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
            ),
            scene = dict(
                xaxis = dict(visible=False, range=x_range),
                yaxis = dict(visible=False, range=y_range),
                zaxis = dict(visible=False, range=z_range),
            ),
            showlegend=False,
            scene_aspectmode='cube',
            paper_bgcolor=background_color,
        )
        
        fig.show(config={'displaylogo': False})
