
# Breadth-First Search Maze Solver

This project is a visualization of the **Breadth-First Search (BFS)** algorithm applied to a grid maze. The user can interact with the grid to place obstacles, set a start point, and an end point. The BFS algorithm will then find the shortest path from the start to the end, avoiding obstacles. This project is built using **Pygame**.

## Features

- **Interactive Grid**: Users can place obstacles, set start and end points on the grid.
- **Breadth-First Search Algorithm**: The BFS algorithm is visualized as it explores the grid, finding the shortest path between the start and end points.
- **Optimized Rendering**: The grid rendering and obstacle management have been optimized for smooth user interactions.
- **Real-Time Pathfinding Visualization**: Watch as the BFS algorithm dynamically explores the grid and marks the shortest path in real time.
- **Customizable Grid Size**: Adjust the grid size according to your needs, perfect for exploring different maze complexities.

## Installation

1. Make sure you have Python 3.x installed.
2. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the code and run the main file:
   ```bash
   python main.py
   ```

## How to Use

1. **Start Point**: Click on the "Start Point" button and then click on a cell in the grid to set the starting point.
2. **End Point**: Click on the "End Point" button and then click on a cell in the grid to set the end point.
3. **Obstacles**: Click on the "Obstacles" button and then click on grid cells to place obstacles.
4. **Run BFS**: Click on the "Start" button to run the BFS algorithm and find the shortest path.
5. **Restart Grid**: Click on the "Restart grid" button to clear the grid and reset all settings.

## Optimization Notes

The code for managing and rendering the grid with obstacles has been optimized for better performance. Below are the key optimizations implemented:

### Efficient Grid Rendering:

- **Grid Background Optimization**: The grid background is drawn only once and cached as a surface (`grid_surface`). This background is then reused in subsequent frames without redrawing the entire grid, which reduces computational overhead.

- **Obstacle Management**: Instead of redrawing the entire grid every frame, only the obstacles that are added or removed are updated. This ensures that only the relevant portions of the grid are updated, which increases rendering performance.

### Efficient Obstacle Handling:

- **Set for Obstacles**: Obstacles are stored in a set, which allows for constant-time lookups and efficient removal operations. This ensures that adding, checking, or removing obstacles is fast, even with a large number of obstacles.

- **Direct Grid Modification**: The grid is directly modified (i.e., setting cells to 0 or 1) when obstacles are added or removed, reducing the need to recreate or redraw the entire grid.

### Event Handling:

- **Optimized Mouse Input**: Mouse position updates and mouse button state changes are tracked only when necessary. This avoids unnecessary checks and ensures that only valid grid positions are updated based on mouse interactions.

- **Efficient Drawing**: The screen is cleared and redrawn only when changes occur (i.e., when obstacles are added or removed). This minimizes the number of redraws and improves the frame rate.

## Performance Impact

These optimizations reduce the time spent on recalculating and redrawing the grid, especially when interacting with large grids. By handling only the parts of the grid that change (i.e., obstacles), the application becomes more responsive and can handle more complex grids without significant performance degradation.


## License

This project is licensed under the MIT License

