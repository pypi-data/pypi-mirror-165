
winW, winH = gh_window.getsize(0)

gx_camera.update_perspective(camera, camera_fov, 1, 0, 0, winW, winH, camera_znear, camera_zfar)

gh_camera.update_ortho(camera_ortho, -winW/2, winW/2, -winH/2, winH/2, 1.0, 10.0)
gh_camera.set_viewport(camera_ortho, 0, 0, winW, winH)

gh_mesh.update_quad_size(fullscreen_quad, winW, winH)

