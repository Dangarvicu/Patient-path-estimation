# Patient-path-estimation
Patient-path-estimation folder contains folders: config, data, functions and scripts.

1. config: The folder contains the Python file where the constants are defined.

2. data: The folder contains the files with the data generated for the study. In total there are 101 simulated pandemics, of which 100 are used for parameter estimation and the last one for the simulation study.

3. functions: The folder contains the Python file where different functions that are needed are defined.

3. results: The folder contains the daily estimates of the 100 simulated scenarios and the results of the ICU occupancy simulations.

4. scripts: The folder contains four Python files used in the study of patient path estimation:
    - Estimation: The file generates different pandemic scenarios and calculates daily estimates for each scenario with each method.
    - Estimation_report: The file calculates the percentiles of the estimates for all scenarios.
    - Simulation: The file, starting from a simulated pandemic, reproduces the scenario up to a selected day and simulates into the future based on the estimated distributions at that time.
    - Simulation_report: The file calculates the estimation errors between the predictions when simulating with each estimation method and with actual values.

