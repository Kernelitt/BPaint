# TODO: Add PNG Import Functionality

- [x] Add PIL import for image processing
- [x] Create hex_to_rgb() helper function
- [x] Create find_closest_color() helper function
- [x] Add "Import PNG" option to File menu
- [x] Implement import_png() function:
  - [x] Open file dialog for PNG files
  - [x] Load and validate image (max 256x256)
  - [x] Set grid size to max(image dimensions)
  - [x] Convert each pixel to closest matching color
  - [x] Handle RGBA images with alpha transparency
  - [x] Update grid and redraw canvas
