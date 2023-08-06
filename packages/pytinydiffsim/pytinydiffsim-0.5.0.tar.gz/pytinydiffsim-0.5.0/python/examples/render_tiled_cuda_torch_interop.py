#pycuda cuda interop inspired by
#https://gist.github.com/victor-shepardson/5b3d3087dc2b4817b9bffdb8e87a57c4
#and https://discuss.pytorch.org/t/create-edit-pytorch-tensor-using-opengl/42111/5
#pip install pytinydiffsim, pycuda, numpy, matplotlib, PyQt5
#visit https://pytorch.org/get-started/locally to install cuda-enabled pytorch
#git clone https://github.com/erwincoumans/tiny-differentiable-simulator.git
#cd tiny-differentiable-simulator/python/examples


import pytinydiffsim as tds
import time
import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)
import numpy as np

use_matplotlib = True

if use_matplotlib:
  import matplotlib.pyplot as plt
  plt.ion()
  img = np.random.rand(400, 400)
  image = plt.imshow(img, interpolation='none')#, cmap='gray', vmin=0.8, vmax=1)
  ax = plt.gca()

import pycuda.gl
from pycuda.gl import graphics_map_flags
import pycuda.driver as cuda
cuda.init()
device = cuda.Device(0)  # enter your Gpu id here
ctx = device.make_context()
    
import torch

tile_width = 120
tile_height = 80

nx=10
ny=10

width = nx*tile_width
height = ny*tile_height


from contextlib import contextmanager

@contextmanager
def cuda_activate(img):
    """Context manager simplifying use of pycuda.gl.RegisteredImage"""
    mapping = img.map()
    yield mapping.array(0,0)
    mapping.unmap()


if 1:
    num_actors = 2 #1024#4096
    auto_reset_when_done = True
    tds_robot = tds.VectorizedLaikagoEnv(num_actors, auto_reset_when_done)
    tds_robot.reset()
    actions = [[0] * tds_robot.action_dim()]*num_actors
    res = tds_robot.step(actions)


    import pytinyopengl3 as g
    viz = g.OpenGLUrdfVisualizer(width=width, height=height, window_type=0, render_device=-1)
    viz.opengl_app.set_background_color(1,0,0)

    viz.opengl_app.swap_buffer()
    viz.opengl_app.swap_buffer()
    
    img_width = width
    img_height = height
    
    tex_id = viz.opengl_app.enable_render_to_texture(img_width,img_height)#width, height)
    print("opengl tex_id = ", tex_id)


    map_flags = graphics_map_flags.NONE
    tex_target = g.GL_TEXTURE_2D
    print("tex_target=",tex_target)
    cuda_buffer = pycuda.gl.RegisteredImage(int(tex_id), tex_target, map_flags)
    
    
    mytensor = torch.ones((img_width, img_height, 4), dtype=torch.float32, device="cuda")
    print("mytensor.is_cuda=",mytensor.is_cuda)
    print("mytensor.shape=", mytensor.shape)
    
    urdf = g.OpenGLUrdfStructures()
    parser = g.UrdfParser()
    file_name = tds_robot.urdf_filename()
    urdf = parser.load_urdf(file_name)
    print("urdf=",urdf)
    texture_path = "laikago_tex.jpg"
    viz.path_prefix = g.extract_path(file_name)
    print("viz.path_prefix=",viz.path_prefix)
    viz.convert_visuals(urdf, texture_path)
    print("create_instances")

    all_instances_prev = viz.create_instances(urdf, texture_path, num_actors)
    all_instances = viz.create_instances(urdf, texture_path, num_actors)

    #print("all_instances=",all_instances)
    #print("all_instances[0]=",all_instances[0])

    for i in all_instances[1]:
      print(i.visual_instance)
      
    #sync transforms
    #for pairs in all_instances:
    #  for pair in pairs:
    #    print("pair.link=", pair.link_index, " pair.visual_instance=", pair.visual_instance)
    sim_spacing = 0


    

    print("len(all_instances)=",len(all_instances))
    print("\nhold CTRL and right/left/middle mouse button to rotate/zoom/move camera")
    
    
    st = time.time()
    
    if 1:
      width = viz.opengl_app.renderer.get_screen_width()
      print("screen_width=",width)
      height = viz.opengl_app.renderer.get_screen_height()
      print("screen_height=",height)
      

      
      tiles=[]
      
      
      for x in range (nx):
        for y in range (ny):
          tile = g.TinyViewportTile()
          tile.visual_instances = [35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67]
          #tile.visual_instances = [35,37,39,41]^M
          cam = viz.opengl_app.renderer.get_active_camera()
          tile.projection_matrix = cam.get_camera_projection_matrix()
          tile.view_matrix = cam.get_camera_view_matrix()
          tile.viewport_dims=[x*tile_width,y*tile_height,tile_width, tile_height]
          tiles.append(tile)  


    cam = g.TinyCamera()
    cam.set_camera_up_axis(2)
    cam.set_camera_distance(1)
    cam.set_camera_pitch(-30)
    cam.set_camera_target_position(0.,0.,0.)
    viz.opengl_app.renderer.set_camera(cam)


            
    frame = 0
    #for frame in range (100):
    while not viz.opengl_app.window.requested_exit():
      frame=frame+1
    
      viz.opengl_app.enable_render_to_texture(img_width,img_height)
      width = viz.opengl_app.renderer.get_screen_width()
      height = viz.opengl_app.renderer.get_screen_height()
      
      tile_width = int(width/nx)
      tile_height = int(height/ny)
    
      ct = time.time()
      
      cam = viz.opengl_app.renderer.get_active_camera()
      tile_index = 0
      for x in range (nx):
        for y in range (ny):
          tile = tiles[tile_index]
          tile_index+=1
          tile.view_matrix = cam.get_camera_view_matrix()
          tile.viewport_dims=[x*tile_width,y*tile_height,tile_width, tile_height]


      et = time.time()
      print("update viewports dt=",et-ct)
      
          
      ct = time.time()
      res = tds_robot.step(actions)
      et = time.time()
      print("tds_robot.step dt=",et-ct)
      
      viz.sync_visual_transforms(all_instances, res.visual_world_transforms, tds_robot.obs_dim(), sim_spacing)
    
      #viz.render(do_swap_buffer=False, render_segmentation_mask=True)
      #name = "test_"+str(frame)+".png"
      #viz.opengl_app.dump_next_frame_to_png(filename=name, render_to_texture=False, width=19200, height=10800)
      ct = time.time()
      viz.render_tiled(tiles, do_swap_buffer = False, render_segmentation_mask=False)
      et = time.time()
      print("render dt=",et-ct)
      
      #viz.render()

      
      if 1:
        with cuda_activate(cuda_buffer) as ary:
            cpy = pycuda.driver.Memcpy2D()
            cpy.set_src_array(ary)
            cpy.set_dst_device(mytensor.data_ptr())
            cpy.width_in_bytes = cpy.src_pitch = cpy.dst_pitch = img_width*16 # 4 times 32bit float 
            cpy.height = img_height
            cpy(aligned=False)
            torch.cuda.synchronize()
          
      #print("mytensor=",mytensor)
      
      if use_matplotlib:
        ct = time.time()
        #pixels2 = g.ReadPixelBuffer(viz.opengl_app)
        #print("pixels2.rgba.shape=", pixels2.rgba.shape)
        #print("pixels2.rgba=", pixels2.rgba)
        #pixels_rgba = pixels2.rgba
        pixels_rgba = mytensor.cpu().numpy()
        print("pixels_rgba.shape=",pixels_rgba.shape)
        et = time.time()
        print("ReadPixelBuffer dt=",et-ct)
        #print('pixels.rgba=', pixels.rgba)
        #print('pixels.rgba.shape=', pixels.rgba.shape)

        #np_img_arr = pixels_rgba
        np_img_arr = np.reshape(pixels_rgba, (img_height, img_width, 4))
        
        #print('np_img_arr.shape=', np_img_arr.shape)
        #np_img_arr = np_img_arr * (1. / 255.)
        #print('np_img_arr.shape=', np_img_arr.shape)
        np_img_arr = np.flipud(np_img_arr)
      
        #image.set_data(np_img_arr)
        
        #np_depth_arr = np.flipud(np.reshape(pixels.depth, (height, width, 1)))
        #image.set_data(np_depth_arr)
        ct = time.time()
        #viz.swap_buffer()
        et = time.time()
        print("swap_buffer dt=",et-ct)
        et = time.time()
        dt = et-st
        st = et
        
        image.set_data(np_img_arr)
        ax.plot([0])
        #plt.draw()
        #plt.show()
        plt.pause(0.0001)
          
        print(dt)
        print("fps = ", len(tiles)*(1./dt))
      

      viz.swap_buffer()
      #cam = viz.opengl_app.renderer.get_active_camera()
      #print("cam=",cam)
      #print("cam.get_camera_projection_matrix=",cam.get_camera_projection_matrix())
      #print("cam.get_camera_view_matrix=",cam.get_camera_view_matrix())

print("cuda_buffer.unregister()")
cuda_buffer.unregister()
print("ctx.pop()")
ctx.pop()       
print("end")              
          
