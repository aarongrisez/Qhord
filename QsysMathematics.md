# Evolution
This is the process that begins when the simulation's run_continuous() method is called. When there is no user input, the quantum system needs to evolve according to a differential equation (the Schrodinger Equation). Evolution will occur at every clock cycle. This can be achieved one of two ways:

1. Computationally expensive: Runge-Kutta

We numerically solve the differential equation every clock cycle of the simulation using the Runge-Kutta algorithm. This is computationally expensive during the simulation, but easily handles any time-dependency in the generator. This method will take at least 4 matrix multiplications and additional constant multiplications and additions per clock cycle

2. Storage expensive: Approximate propogator

We approximately solve the differential equation by first making a discrete time mesh and then solving analytically for each time window. This will require much more computation during the setup (exponentiating a matrix N times where N is the number of time-mesh points), but would require popping an array from a stack and a single matrix operation at each clock cycle.

# Measurements
When there is user input, the simulation stops:

1. Based on the input, the first probability distribution is sampled
2. Based on the input and the result of the first sampling, the second probability distribution is sampled
3. Based on the input, result of the first sampling, and result of the second sampling, a matrix is selected
4. 3 matrix multiplications and an inner product of two vectors is performed
5. The "Play" method is triggered
6. Evolution resumes
