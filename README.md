# Practical-Example-of-Flow-in-a-Porous-Medium
Practical Example of Flow in a Porous Medium Using the Finite Element Method

The example demonstrates a practical example of flow in a porous medium using a computational code in Python, the programming structure followed the same steps as in the book LOGAN (2015) using the numerical formulations of the Finite Element Method.
The validation of the practical example was through modeling developed by ABAQUS using the heat transfer solver.
The developed code is structured in steps as follows: (i) Initial parameters and input data, (ii) Loop for constructing the element matrix and global matrix, (iii) Application of the Boundary conditions, (iv) Solution of the System of Equations and (v) Saving the results and carrying out Post-Processing in the GID.
The practical example consists of a rectangular concrete dam 7.0m wide and 10.0m high, and the base is a granite rock 10.0m thick and 27.0m wide, the dam is on the rock supported on the midpoint, both materials were considered with equal permeability K_x=K_y=1x10^(-10) m/s.
The example used 469 nodes and 838 constant strain triangle (CST) triangular elements. The boundary conditions were the upstream water buoyancy acting in a triangular manner on the concrete dam, with zero value at the top and maximum at the base of the dam, and constantly in the granite rock.
The results obtained in the script are nodal values ​​of the flow in porous media. The GID software was used for post-processing and comparison with the ABAQUS result.
