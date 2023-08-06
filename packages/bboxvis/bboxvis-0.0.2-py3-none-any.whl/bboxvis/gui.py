import numpy as np
import vispy
import vispy.io
vispy.use("PyQt5")
import vispy.scene as scene
from vispy import app
import threading
from queue import Queue
import os.path as osp
import zmq
import sys
sys.path.append('..')
sys.path.append('.')
from bboxvis.tools import get_corners, pc_in_box
import threading
from loguru import logger
from queue import Queue
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt


PARAMETERS = [('点尺寸', 0.0, 20.0, 'double', 3.0),
              ('字体大小', 0.0, 100.0, 'double', 10.0),
              ('帧号', 0, 4000, 'int', 0),
              ('物体ID', -10, 10000, 'int', -1),
              ('检测框标签', 0, 40, 'int', 5),
              ('FPS帧率', 1.0, 25.0, 'double', 20.0),
              ('图像框字体大小', 0, 100, 'double', 10.0)]


CONVERSION_DICT = {'帧号': 'frame_num',
                   '物体ID': 'tracklet_id',
                   '字体大小': 'pc_font_size',
                   '点尺寸': 'pc_size',
                   '检测框标签': 'label_font_size',
                   'FPS帧率': 'fps',
                   '图像框字体大小': 'font_size'
                   }

COLORS = plt.get_cmap('Paired').colors

def get_color(i):
    return COLORS[i % len(COLORS)] + (1,)


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon=True
        # logger.debug(f'{fn} start a thread')
        thread.start()
    return wrapper

class VisMessenger:
    def __init__(self, port='19999'):
        self.socket = zmq.Context().socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")

    def array_to_msg(self, array):
        _shape = np.array(array.shape, dtype=np.int32)
        return [array.dtype.name.encode(),
                _shape.tostring(),
                array.tostring()]

    def send_numpy(self, array, nptype='pc', name=''):
        '''
        type: "pc" or "bbox"
        '''
        assert isinstance(array, np.ndarray)
        # _msg = self.array_to_msg(array)
        head_msg = str(nptype) + '/' + str(name)
        self.socket.send_string(head_msg, zmq.SNDMORE)
        self.socket.send_pyobj(array)

class PViz:
    def __init__(self) -> None:
        self.appQt = QtWidgets.QApplication(sys.argv)
        self.window = VisWindow()
        self.window.show()
        self.appQt.exec_()

class VisWindow(QtWidgets.QMainWindow):
    def __init__(self, param=None):
        QtWidgets.QMainWindow.__init__(self)

        # self.showMaximized()
        screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        self.resize(int(screen_size.width() * .75),
                    int(screen_size.height() / 2))
        self.setWindowTitle('PViz')
        visualization = VisCanvas()
        self.view_box = visualization
        self.view_box.create_native()
        self.view_box.native.setParent(self)
        self.parameter_object = SetupWidget(self, visualization)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.view_box.native)
        self.setCentralWidget(splitter)



class VisCanvas(scene.SceneCanvas):

    PTS_OPT = dict(alpha=0.8, spherical=True)



    def __init__(self, pc_size=5.0, pc_font_size=10.0, label_font_size=5, server=False):
        super().__init__(keys=None, size=(1000, 800), title='PointCloud Canvas', show=True)
        self.unfreeze()

        self.view = self.central_widget.add_view()
        self.axis = scene.visuals.XYZAxis(parent=self.view.scene)

        self.view.camera = 'turntable'
        self.view.camera.center = [0, 0, 0]
        self.view.camera.distance = 10
        self.view.camera.elevation = 30
        self.view.camera.azimuth = -90
        # Press Shift to translate camera view
        self.view.camera.translate_speed = 25
        # GUI
        self.pc_points_size = pc_size
        self.pc_font_size = pc_font_size
        self.label_text_size = label_font_size * 100
        # Visual Elements
        self._pc = dict()
        self._bbox = dict()
        self._bbox_color = list()
        self.numpy_queue = Queue()
        if server == True:
            self._init_server_mode()


    def _init_server_mode(self):
        self.data_thread = threading.Thread(target=self.recv_data, daemon=True)
        self.data_thread.start()
        pass

    def recv_data(self):
        print('thread start')
        socket = zmq.Context().socket(zmq.SUB)  
        socket.setsockopt_string(zmq.SUBSCRIBE, '')  
        port = '19999'
        socket.connect("tcp://localhost:%s" % port)
        while True:
            topic = socket.recv_string()
            msg = socket.recv_pyobj()
            print(topic)
            self.numpy_queue.put([topic, msg])
            event = app.KeyEvent(type='key_press', text='*')
            self.events.key_press(event)

    def _init_bbox(self):
        self.bbox_all_points = np.empty((0,3))
        self.bbox_all_connect = np.empty((0,2))
        self.bbox_all_colors = np.empty((0,4))
        self.connect_template = np.array([
            [0, 1], [1, 2], [2, 3], [3, 0],  # front
            [4, 5], [5, 6], [6, 7], [7, 4],  # back
            [0, 4], [1, 5], [2, 6], [3, 7],  # side
            [0, 2], [1, 3], # front cross
        ])
        self.all_labels_text = []
        self.all_labels_pos = []
    
    @threaded
    def add_pc(self, pc, color=None, name='pointcloud', size=None):
        '''
        Add Point Cloud to canvas
        Args:
        ------
            pc : numpy.ndarray
            color: numpy.ndarray
        '''
        if color is None:
            color = 'w'
        if size is None:
            size = self.pc_points_size
        if name == '':
            name = 'pointcloud'
        if hasattr(self, name):
            self.__dict__[name].set_data(pos=pc, face_color=color, edge_color=None, size=self.pc_points_size)
        else:
            setattr(self, name , scene.visuals.Markers(pos=pc, face_color=color, edge_color=None, size=self.pc_points_size, parent=self.view.scene, **self.PTS_OPT ))

        # Add visual element to dict for further modification
        self._pc[name] = self.__dict__[name]
        return self.__dict__[name]

    @threaded
    def add_bbox(self, bbox, color=(1,1,1,1), name='bbox', width=None):
        '''
        Add Bbox to canvas
        -------
        bbox: (n, 9) numpy ndarray
        color: (n, 4) numpy ndarray
        name: bbox name in canvas
        width: bounding box line width
        '''
        self._init_bbox()
        self._bbox_color.append(color)
        if width is None:
            width = 4
        if name == '':
            name = 'bbox'
        try:
            assert len(color) == 4
        except Exception as e:
            print(e)
            return
        pts, center = get_corners(bbox, ret_center=True)
        self._bbox[name] = [pts, center, bbox]

        curr_idx = 0
        for bbox_name in self._bbox:
            self.bbox_all_points = np.append(self.bbox_all_points, self._bbox[bbox_name][0], axis=0)
            self.bbox_all_connect = np.append(self.bbox_all_connect, self.connect_template + curr_idx * 8, axis=0)
            color = np.asanyarray(self._bbox_color[curr_idx]).reshape(1, 4)
            curr_color = np.repeat(color, 8, axis=0)
            self.bbox_all_colors = np.append(self.bbox_all_colors, curr_color, axis=0)
            self.all_labels_text.append(bbox_name)
            self.all_labels_pos.append(self._bbox[bbox_name][1].tolist())
            curr_idx += 1


        if hasattr(self, 'bbox'):
            self.bbox.set_data(pos=self.bbox_all_points, color=self.bbox_all_colors, connect=self.bbox_all_connect, width=width)
        else:
            self.bbox = scene.visuals.Line(pos=self.bbox_all_points, connect=self.bbox_all_connect,
                                           color=self.bbox_all_colors, width=width, parent=self.view.scene)


    def color_pc_in_bbox(self):
        for bbox_name in self._bbox:
            bbox = self._bbox[bbox_name][2]
            pc_in_bbox_indices = pc_in_box(bbox, self.points, mask=True)
            self.points_color[pc_in_bbox_indices] = np.array([1, 1, 0, 1])
        self.world_points.set_data(
            pos=self.points, edge_color=self.points_color, face_color=self.points_color, 
            size=self.pc_points_size)
        self.update()

    def run(self):
        vispy.app.run()

    def render_img(self, dir='/home/nio/workspace/sot_new/bboxvis/example.png',
                   cam_center=(0,0,0), cam_distance=10):
        self.view.camera.center = cam_center
        self.view.camera.distance = cam_distance
        img = self.render()
        vispy.io.write_png(dir, img)
    
    def on_key_press(self, event):
        self.view_center = list(self.view.camera.center)
        if (event.text == '*'):
            this_data = self.numpy_queue.get()
            head_msg = this_data[0]
            nptype, name = head_msg.split('/')
            if nptype == 'pc':
                self.add_pc(this_data[1], name=name)
                logger.info('Received a Point Cloud')
            elif nptype == 'bbox':
                self.add_bbox(this_data[1])
                logger.info('Received a Bbox')
        if(event.text == 'w' or event.text == 'W'):
            dx, dy = self.get_cam_delta()
            self.view_center[0] += dx
            self.view_center[1] += dy
            self.view.camera.center = self.view_center

        if(event.text == 's' or event.text == 'S'):
            dx, dy = self.get_cam_delta()
            self.view_center[0] -= dx
            self.view_center[1] -= dy
            self.view.camera.center = self.view_center

        if(event.text == 'a' or event.text == 'A'):
            dx, dy = self.get_cam_delta()
            self.view_center[0] -= dy
            self.view_center[1] += dx
            self.view.camera.center = self.view_center

        if(event.text == 'd' or event.text == 'D'):
            dx, dy = self.get_cam_delta()
            self.view_center[0] += dy
            self.view_center[1] -= dx
            self.view.camera.center = self.view_center

        if(event.key == 'up'):
            self.view_center[2] += 1
            self.view.camera.center = self.view_center

        if(event.key == 'down'):
            self.view_center[2] -= 1
            self.view.camera.center = self.view_center

        if(event.text == 'c' or event.text == 'C'):
            # Centered
            self.view_center[0] = 0
            self.view_center[1] = 0
            self.view_center[2] = 0
            self.view.camera.center = self.view_center
    
    def get_cam_delta(self):
        theta = self.view.camera.azimuth
        dx = -np.sin(theta * np.pi / 180)
        dy = np.cos(theta * np.pi / 180)
        return dx, dy

class Paramlist(object):

    def __init__(self, parameters):
        """Container for object parameters.
        Based on methods from ../gloo/primitive_mesh_viewer_qt.
        """
        self.parameters = parameters
        self.props = dict()
        self.props['add_annotation'] = False
        self.props['draw_trace'] = False
        self.props['lidar_seg'] = False
        self.props['subtype'] = False
        self.props['show_score'] = False
        self.props['ext_bbox'] = False
        self.props['obj_velo'] = False
        self.props['raw_dets'] = False
        for nameV, minV, maxV, typeV, iniV in parameters:
            nameV = CONVERSION_DICT[nameV]
            self.props[nameV] = iniV

class SetupWidget(QtWidgets.QWidget):
    """Widget for holding all the parameter options in neat lists.
    Based on methods from ../gloo/primitive_mesh_viewer_qt.
    """
    def __init__(self, visualization, parent=None):
        super(SetupWidget, self).__init__()
        self.visualization = visualization
        # Create the parameter list from the default parameters given here
        self.param = Paramlist(PARAMETERS)

        self.show_score = QtWidgets.QCheckBox("显示dets score")
        self.show_score.setChecked(self.param.props['show_score'])
        # self.show_score.toggled.connect(self.update_parameters)

        self.show_ext_bbox = QtWidgets.QCheckBox("External bboxes")
        self.show_ext_bbox.setChecked(self.param.props['ext_bbox'])
        # self.show_ext_bbox.toggled.connect(self.update_parameters)

        # Separate the different parameters into groupboxes,
        # so there's a clean visual appearance
        self.parameter_groupbox = QtWidgets.QGroupBox(u"可视化选项")
        self.display_groupbox = QtWidgets.QGroupBox(u"显示参数")
        self.conditions_groupbox = QtWidgets.QGroupBox(u"Clip参数")

        self.show_points_button = QtWidgets.QPushButton(u'Points in BBox')
        self.show_points_button.clicked.connect(self.show_bbox_points)

        self.load_sot_button = QtWidgets.QPushButton(u'load bbox json file')
        # self.load_sot_button.clicked.connect(self.load_sot_file)

        self.groupbox_list = [self.display_groupbox,
                              self.conditions_groupbox,
                              self.parameter_groupbox]

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        # Get ready to create all the spinboxes with appropriate labels
        plist = []
        self.psets = []
        # important_positions is used to separate the
        # parameters into their appropriate groupboxes
        important_positions = [0, ]
        # Layout, three vertical grid layout
        param_boxes_layout = [QtWidgets.QGridLayout(),
                              QtWidgets.QGridLayout(),
                              QtWidgets.QGridLayout()]
        for nameV, minV, maxV, typeV, iniV in self.param.parameters:
            # Create Labels for each element
            plist.append(QtWidgets.QLabel(nameV))
            if CONVERSION_DICT[nameV] == 'frame_num':
                important_positions.append(len(plist) - 1)

            # Create Spinboxes based on type - doubles get a DoubleSpinBox,
            # ints get regular SpinBox.
            # Step sizes are the same for every parameter except font size.
            if typeV == 'double':
                self.psets.append(QtWidgets.QDoubleSpinBox())
                self.psets[-1].setDecimals(1)
                if nameV == 'font size':
                    self.psets[-1].setSingleStep(1.0)
                else:
                    self.psets[-1].setSingleStep(0.1)
            elif typeV == 'int':
                self.psets.append(QtWidgets.QSpinBox())
            self.psets[-1].setValue(iniV)
            self.psets[-1].setMaximum(maxV)
            self.psets[-1].setMinimum(minV)

        pidx = -1
        # update_function = [self.setPoint, self.setFont_size, self.setFrame_num,
        #                    self.setTrack_id, self.setLabel_size, self.setFps, self.setImg_font]
        idx = 0
        for pos in range(len(plist)):
            if pos in important_positions:
                pidx += 1
            param_boxes_layout[pidx].addWidget(plist[pos], pos + pidx, 0)
            param_boxes_layout[pidx].addWidget(self.psets[pos], pos + pidx, 1)
            # self.psets[pos].valueChanged.connect(update_function[idx])
            idx += 1

        # param_boxes_layout[0].addWidget(QtWidgets.QLabel('Method: '), 8, 0)
        param_boxes_layout[-2].addWidget(self.show_score)
        param_boxes_layout[-2].addWidget(self.show_ext_bbox)
        param_boxes_layout[-1].addWidget(self.show_points_button)
        param_boxes_layout[-1].addWidget(self.load_sot_button)

        for groupbox, layout in zip(self.groupbox_list, param_boxes_layout):
            groupbox.setLayout(layout)

        for groupbox in self.groupbox_list:
            self.splitter.addWidget(groupbox)

        vbox = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        scrollarea = QtWidgets.QScrollArea()
        scrollarea.setWidgetResizable(True)
        scrollarea.setWidget(self.splitter)

        hbox.addWidget(scrollarea)
        vbox.addWidget(scrollarea)
        self.setLayout(vbox)
    
    def show_bbox_points(self):
        '''
        Change color of points in bbox
        '''
        self.visualization.color_pc_in_bbox()